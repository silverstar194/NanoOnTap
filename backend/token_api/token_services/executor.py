from collections.abc import Iterable
import logging
import time
from datetime import datetime
import copy

from ..nano_services.transaction_service import InsufficientNanoException
from ..nano_services.transaction_service import NegativeNanoException
from ..nano_services.transaction_service import RCPException
from ..nano_services.transaction_service import InvalidPOWException
from .validation.action_set_validation import ValidateActionSet
from ..nano_services.transaction_service import TransactionService
from ..models.token_models.action_history import ActionHistory


logger = logging.getLogger(__name__)


class Executor:

    def __init__(self, device, token, application, debug=False):
        self.device = device
        self.token = token
        self.application = application
        self.debug = debug
        self.transactions = []

        self.action_history = ActionHistory.objects.create()
        self.action_history.application = application
        self.action_history.device = device
        self.action_history.token = token
        self.action_history.save()

    def run_action_set_async(self):
        self.generate_transactions()
        object_before_async = copy.deepcopy(self.action_history)

        logger.info("Starting async thread...")
        self.send_transactions()
        #thread = threading.Thread(target=self.send_transactions)
        #thread.start()

        return object_before_async

    def run_action_set(self):
        if self.debug:
            return
        self.generate_transactions()
        return self.send_transactions()

    def generate_transactions(self):
        action_sets = self.device.action_sets.all()
        logger.info(action_sets)
        action_policies = self.token.action_polices.all()
        logger.info(action_policies)

        selected_one = False
        for action_set in action_sets:
            action_set_validator = ValidateActionSet(action_set, self.device, action_policies)
            valid_policy, valid_to_account, valid_from_account = action_set_validator.validate_action_set()
            if valid_policy and not selected_one:
                logger.info("Running action set '{0}'".format(action_set.action_set_name, valid_policy))
                logger.info("Using action policy '{0}' \n {1}".format(valid_policy.policy_name, valid_policy))

                selected_one = True

                self.action_history.action_set = action_set
                self.action_history.policy = valid_policy
                self.action_history.save()

                transaction_service = TransactionService()
                actions = action_set.actions.all() if isinstance(action_set.actions.all(), Iterable) else [action_set.actions]
                for action in actions:
                    transaction = transaction_service.new_transaction(self.application, action.from_account, action.to_account, action.amount)
                    logger.info("Generating transaction from {0} to {1} amount {2}".format(action.from_account, action.to_account, action.amount))

                    self.transactions.append(transaction)
                    self.action_history.transactions.add(transaction)

                    transaction.save()
                    self.action_history.save()

    def send_transactions(self):
        logger.info(self.transactions)
        transaction_service = TransactionService()
        for transaction in self.transactions:

            try:
                transaction_service.send_transaction(transaction)
                transaction.complete = True
                transaction.timestamp = int(time.time())
                transaction.save()

            except InsufficientNanoException:
                transaction.complete = False
                transaction.error = "Action failed. Insufficient Nano."
                logger.error(transaction.error)
                transaction.save()

            except NegativeNanoException:
                transaction.complete = False
                transaction.error = "Action failed. Nano send amount must be positive."
                logger.error(transaction.error)
                transaction.save()

            except InvalidPOWException:
                transaction.complete = False
                transaction.error = "Action failed. Total PoW failure."
                logger.error(transaction.error)
                transaction.save()

            except RCPException:
                transaction.complete = False
                transaction.error = "Action failed. Cannot connect to node."
                logger.error(transaction.error)
                transaction.save()

            except Exception as e:
                transaction.complete = False
                transaction.error = "Action failed. Unknown error. {0}".format(str(e))
                transaction.save()
                logger.error(transaction.error)
                raise e

        self.action_history.executed = True
        self.action_history.executed_time = datetime.now()
        self.action_history.save()

        return self.action_history

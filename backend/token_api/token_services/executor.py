from collections.abc import Iterable
import logging


from .validation.action_set_validation import ValidateActionSet
from ..nano_services.transaction_service import TransactionService

logger = logging.getLogger(__name__)


class Executor:

    def __init__(self, device, token, application, debug=False):
        self.device = device
        self.token = token
        self.application = application
        self.debug = debug

    def run_action_set(self):
        action_sets = self.device.action_sets.all()
        action_policies = self.token.action_polices.all()

        for action_set in action_sets:
            action_set_validator = ValidateActionSet(action_set, self.device, action_policies)
            valid_policy, valid_to_account, valid_from_account = action_set_validator.validate_action_set()
            if valid_policy:
                logger.info("Running action set '{0}'".format(action_set.action_set_name, valid_policy))
                logger.info("Using action policy '{0}' \n {1}".format(valid_policy.policy_name, valid_policy))

                transaction_service = TransactionService()
                actions = action_set.actions.all() if isinstance(action_set.actions.all(), Iterable) else [action_set.actions]
                for action in actions:
                    transaction = transaction_service.new_transaction(self.application, action.from_account, action.to_account, action.amount)
                    logger.info("Running transaction from {0} to {1} amount {2}".format(action.from_account, action.to_account, action.amount))

                    if not self.debug:
                        transaction_service.send_transaction(transaction)

                return action_set, valid_policy

        return None, None


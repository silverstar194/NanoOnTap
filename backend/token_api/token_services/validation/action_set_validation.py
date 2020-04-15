from .account_policies_validation import ValidateAccountsWithAccountPolices
from .action_polices_validation import ValidateActionWithActionPolicies
from .account_validation import AccountValidation

from collections.abc import Iterable

import logging
logger = logging.getLogger(__name__)


class ValidateActionSet:

    def __init__(self, action_set, device, action_polices):
        self.action_set = action_set
        self.actions = action_set.actions if isinstance(action_set.actions, Iterable) else [action_set.actions]
        self.device = device
        self.action_polices = action_polices
        self.action_set_action_count = len(self.actions)
        self.action_set_send_amount = sum(action.amount for action in self.actions)

    def validate_action_set(self):
        valid_action_set = False
        for action in self.actions:
            logger.info("Validating action '{0}'".format(action.action_name))
            valid_policy, valid_to_account, valid_from_account = self.validate_action(action)

            if valid_policy and valid_to_account and valid_from_account:
                valid_action_set = True
                break

        if not valid_policy and valid_to_account and valid_from_account:
            return None, None, None

        # validate accounts
        valid_to_policy = False
        for action in self.actions:
            for policy in action.to_account.account_policies.all():
                if not valid_to_policy:
                    valid_to_account = self.validate_account_limits(action.to_account, policy)
                    valid_to_policy = valid_to_account or valid_to_policy
                    logger.info("Validating action '{0}' against to_account '{1}' policy as {2}".format(action.action_name, policy.policy_name, valid_to_policy))


        valid_from_policy = False
        for action in self.actions:
            for policy in action.from_account.account_policies.all():
                if not valid_from_policy:
                    valid_from_account = self.validate_account_limits(action.from_account, policy)
                    valid_from_policy = valid_from_account or valid_from_policy
                    logger.info("Validating action '{0}' against from_account '{1}' policy as {2}".format(action.action_name, policy.policy_name, valid_to_policy))


        if not valid_from_policy or not valid_to_policy:
            valid_action_set = False

        within_action_policy_action_limit = self.validate_action_policy_action_limit(valid_policy)
        within_action_policy_send_limit = self.validate_action_policy_send_limit(valid_policy)

        if not within_action_policy_action_limit or not within_action_policy_send_limit:
            valid_action_set = False

        if not valid_action_set:
            return None, None, None

        return valid_policy, valid_to_account, valid_from_account

    def validate_action(self, action):
        valid_policy = self.validate_action_inner(action)

        valid_to_account = self.valid_to_account(action)
        logger.info("Validating action '{0}' to_account account policies isvalid={1}".format(action.action_name, valid_to_account != None))

        valid_from_account = self.valid_from_account(action)
        logger.info("Validating action '{0}' from_account account policies isvalid={1}".format(action.action_name, valid_from_account != None))

        return (valid_policy, valid_to_account, valid_from_account)

    def validate_action_inner(self, action):
        action_validator = ValidateActionWithActionPolicies(action, self.device, self.action_polices)
        valid_policy = action_validator.validate_action_against_policies()
        return valid_policy

    def valid_to_account(self, action):
        to_account_validator = ValidateAccountsWithAccountPolices(action, action.to_account)
        valid_to_account = to_account_validator.validate_accounts_against_account_polices()
        return valid_to_account

    def valid_from_account(self, action):
        from_account_validator = ValidateAccountsWithAccountPolices(action, action.from_account)
        valid_from_account = from_account_validator.validate_accounts_against_account_polices()
        return valid_from_account

    # action set limits
    def validate_action_policy_action_limit(self, action_policy):
        logger.info("Validating action policy action limit: {0} <= {1} isvalid={2}".format(self.action_set_action_count, action_policy.action_limit,  self.action_set_action_count <= action_policy.action_limit or action_policy.action_limit == -1))
        return self.action_set_action_count <= action_policy.action_limit or action_policy.action_limit == -1

    def validate_action_policy_send_limit(self, action_policy):
        logger.info("Validating action policy send limit: {0} <= {1} isvalid={2}".format(self.action_set_send_amount, action_policy.send_limit, self.action_set_send_amount <= action_policy.send_limit or action_policy.send_limit == -1))
        return self.action_set_send_amount <= action_policy.send_limit or action_policy.send_limit == -1

    def validate_account_limits(self, account, policy):
        send_amount = sum(x.amount for x in filter(lambda action: action.from_account == account, self.actions))
        send_count = len(list(filter(lambda action: action.from_account == account, self.actions)))

        receive_amount = sum(x.amount for x in filter(lambda action: action.to_account == account, self.actions))
        receive_count = len(list(filter(lambda action: action.from_account == account,  self.actions)))

        validator_to_account = AccountValidation(account, account_policy=policy, send_amount=send_amount, send_count=send_count, receive_amount=receive_amount, receive_count=receive_count)
        return validator_to_account.validate_account_against_action_set_limits()



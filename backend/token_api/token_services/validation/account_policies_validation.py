from .account_validation import AccountValidation

import logging

logger = logging.getLogger(__name__)


class ValidateAccountsWithAccountPolices:

    def __init__(self, action, device):
        self.action = action
        self.device = device

    def validate_accounts_against_account_polices(self):
        valid_to_account_policy = self.validate_to_account_against_policy()
        valid_from_account_policy = self.validate_from_account_against_policy()
        return valid_to_account_policy, valid_from_account_policy

    def validate_to_account_against_policy(self):
        to_account_validator = AccountValidation(self.action.to_account, action=self.action)
        valid_to_account_policy = to_account_validator.validate_account_against_account_policies()
        return valid_to_account_policy

    def validate_from_account_against_policy(self):
        from_account_validator = AccountValidation(self.action.from_account, action=self.action)
        valid_from_account_policy = from_account_validator.validate_account_against_account_policies()
        return valid_from_account_policy

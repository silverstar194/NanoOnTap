import logging
logger = logging.getLogger(__name__)

from collections.abc import Iterable

class AccountValidation:

    def __init__(self, account, action=None, account_policy=None, send_amount=None, send_count=None, receive_amount=None, receive_count=None):
        self.action = action
        self.account = account
        self.account_policy = account_policy
        self.account_policies = account.account_policies.all()[0]
        self.account_policies = self.account_policies if isinstance(self.account_policies, Iterable) else [self.account_policies]
        self.send_amount = send_amount
        self.send_count = send_count
        self.receive_amount = receive_amount
        self.receive_count = receive_count

    """
    Return the valid account policy for action or no policy
    """
    def validate_account_against_account_policies(self):
        for account_policy in self.account_policies:
            if self.validate_account_against_account_policy(account_policy):
                return account_policy

        return None

    """
        Validate account limits against all action set limits
    """
    def validate_account_against_account_policy(self, account_policy):
        return account_policy.allow_account_usage()

    def validate_account_against_action_set_limits(self):
        valid_address =self.validate_account_send_action_limit() and self.validate_account_send_amount_limit() and self.validate_account_receive_action_limit() and self.validate_account_receive_amount_limit()
        logger.info("AccountValidation: Policy {0} account {2}".format(self.account_policy.policy_name,  self.account.address, valid_address))
        return valid_address

    def validate_account_send_action_limit(self):
        logger.info("AccountValidation: Policy {0} self.send_count  {1} self.account_policy.send_action_limit  {2}".format(self.account_policy.policy_name,  self.send_count ,self.account_policy.send_action_limit ))
        return self.send_count <= self.account_policy.send_action_limit or self.account_policy.send_action_limit == -1

    def validate_account_send_amount_limit(self):
        logger.info("AccountValidation: Policy {0} self.send_amount {1} self.account_policy.send_amount_limit  {2}".format(self.account_policy.policy_name, self.send_amount, self.account_policy.send_amount_limit))

        return self.send_amount <= self.account_policy.send_amount_limit or self.account_policy.send_amount_limit == -1

    def validate_account_receive_action_limit(self):
        logger.info("AccountValidation: Policy {0} receive_count {1} receive_action_limit {2}".format(self.account_policy.policy_name, self.receive_count, self.account_policy.receive_action_limit))
        return self.receive_count <= self.account_policy.receive_action_limit or self.account_policy.receive_action_limit  == -1

    def validate_account_receive_amount_limit(self):
        logger.info("AccountValidation: Policy {0} receive_amount {1} receive_amount_limit {2}".format(self.account_policy.policy_name, self.receive_amount, self.account_policy.receive_amount_limit))
        return self.receive_amount <= self.account_policy.receive_amount_limit or self.account_policy.receive_amount_limit == -1


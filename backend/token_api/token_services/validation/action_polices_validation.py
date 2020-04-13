
import logging
logger = logging.getLogger(__name__)
from collections.abc import Iterable

class ValidateActionWithActionPolicies:

    def __init__(self, action, device, action_polices):
        self.action = action
        self.device = device
        self.action_polices = action_polices if isinstance(action_polices, Iterable) else [action_polices]

    def validate_action_against_policies(self):
        for action_policy in self.action_polices:
            valid_device = self.validate_device_against_policy(action_policy)
            valid_to_account = self.validate_allowed_to_account_against_policy(action_policy)
            valid_from_account = self.validate_allowed_from_account_against_policy(action_policy)

            if valid_device and valid_to_account and valid_from_account:
                return action_policy

        return None

    def validate_device_against_policy(self, policy):

        allowed_devices = policy.allowed_devices.all()
        denied_devices = policy.denied_devices.all()
        allowed_devices = allowed_devices if isinstance(allowed_devices, Iterable) else [allowed_devices]
        denied_devices = denied_devices if isinstance(denied_devices, Iterable) else [denied_devices]

        allowed = (self.device in allowed_devices or not policy.allowed_devices)
        not_allowed = (self.device in denied_devices)

        logger.info("{0} isvalid={1} for action '{2}'".format(self.device, allowed and not not_allowed, self.action.action_name))

        return allowed and not not_allowed

    def validate_allowed_to_account_against_policy(self, policy):
        allowed_accounts = policy.allowed_to_accounts .all()
        denied_accounts = policy.denied_to_accounts.all()
        allowed_accounts = allowed_accounts if isinstance(allowed_accounts, Iterable) else [allowed_accounts]
        denied_accounts = denied_accounts if isinstance(denied_accounts, Iterable) else [denied_accounts]

        allowed = (self.action.to_account in allowed_accounts or not policy.allowed_to_accounts)
        not_allowed = (self.action.to_account in denied_accounts)

        logger.info("to_account '{0}' isvalid={1} for action '{2}'".format(self.action.to_account, allowed and not not_allowed, self.action.action_name))

        return allowed and not not_allowed

    def validate_allowed_from_account_against_policy(self, policy):
        allowed_accounts = policy.allowed_from_accounts.all()
        denied_accounts = policy.denied_from_accounts.all()
        allowed_accounts = allowed_accounts if isinstance(allowed_accounts, Iterable) else [allowed_accounts]
        denied_accounts = denied_accounts if isinstance(denied_accounts, Iterable) else [denied_accounts]

        allowed = (self.action.from_account in allowed_accounts or not policy.allowed_from_accounts)
        not_allowed = (self.action.from_account in denied_accounts)

        logger.info("from_account '{0}' isvalid={1} for action '{2}'".format(self.action.to_account, allowed and not not_allowed, self.action.action_name))

        return allowed and not not_allowed

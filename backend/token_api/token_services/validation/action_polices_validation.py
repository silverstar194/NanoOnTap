
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
            logger.info("Starting action validation for action {0}".format(self.action.action_name))

            valid_device = self.validate_device_against_policy(action_policy)
            valid_to_account = self.validate_allowed_to_account_against_policy(action_policy)
            valid_from_account = self.validate_allowed_from_account_against_policy(action_policy)

            if valid_device and valid_to_account and valid_from_account:
                return action_policy

        return None

    def validate_device_against_policy(self, policy):

        allowed_devices = policy.allowed_devices if isinstance(policy.allowed_devices, Iterable) else [policy.allowed_devices]
        denied_devices = policy.denied_devices if isinstance(policy.denied_devices, Iterable) else [policy.denied_devices]

        allowed = (self.device in allowed_devices or not policy.allowed_devices)
        not_allowed = (self.device, denied_devices)

        logger.info("Action {0} on device {0} is allowed {0}".format(self.action.action_name, self.device, str(allowed and not not_allowed)))

        return allowed and not not_allowed

    def validate_allowed_to_account_against_policy(self, policy):
        allowed_accounts = policy.allowed_to_accounts if isinstance(policy.allowed_to_accounts, Iterable) else [policy.allowed_to_accounts]
        denied_accounts = policy.allowed_to_accounts if isinstance(policy.denied_to_accounts, Iterable) else [policy.denied_to_accounts]

        allowed = (self.action.to_account in allowed_accounts or not policy.allowed_to_accounts)
        not_allowed = (self.action.to_account in denied_accounts)

        logger.info("Action {0} to_account {0} is allowed {0}".format(self.action.action_name, self.action.to_account, str(allowed and not not_allowed)))

        return allowed and not not_allowed

    def validate_allowed_from_account_against_policy(self, policy):
        allowed_accounts = policy.allowed_to_accounts if isinstance(policy.allowed_from_accounts, Iterable) else [policy.allowed_from_accounts]
        denied_accounts = policy.allowed_to_accounts if isinstance(policy.denied_from_accounts, Iterable) else [policy.denied_from_accounts]

        allowed = (self.action.from_account in allowed_accounts or not policy.allowed_from_accounts)
        not_allowed = (self.action.from_account in denied_accounts)

        logger.info("Action {0} from_account {0} is allowed {0}".format(self.action.action_name, self.action.from_account, str(allowed and not not_allowed)))

        return allowed and not not_allowed

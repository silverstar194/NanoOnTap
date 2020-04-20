import random

from ..token_models.custom_action_policy_base import CustomActionPolicyBase


class CustomActionPolicy(CustomActionPolicyBase):
    """
    Implement any custom logic for policies

    """
    # allow device action 50% of time at random
    def policy_passed(self):
        return random.random() < .5

    def __str__(self):
        return self.custom_policy_name


from .validation.action_set_validation import ValidateActionSet

import logging
logger = logging.getLogger(__name__)

class Executor:

    def __init__(self, device, token):
        self.device = device
        self.token = token


    def run_action_set(self):

        action_sets = self.device.action_sets.select_related().all()
        action_policies = self.token.action_polices.select_related().all()

        for action_set in action_sets:
            action_set_validator = ValidateActionSet(action_set, self.device, action_policies)
            valid_action_set = action_set_validator.validate_action_set()
            if valid_action_set:
                logger.info("Running action set {0}".format(valid_action_set.action_set_name))

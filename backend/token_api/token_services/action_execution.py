from ..token_services.device import *
from ..token_services.token import *
from ..token_services.action_history import *

def action_execution(device_id, token_id):
    device = get_device(device_id)
    device_actions = get_device_actions(device)

    token = get_token(token_id)

    action_policies = get_token_action_policies(token)

    for device_action in device_actions:
        policy = valid_action_against_polices(device, device_action, action_policies)
        if policy:
            execute(device_action)
            audit_execution(device_action, policy)
            return

    print("No valid policy found")


def valid_action_against_polices(device, device_action, action_policies):

    if not action_policies:
        print("No policy present on token")
        raise Exception("No policy present on token")

    for policy in action_policies:

        # validate device
        if not policy.device_allowed(device):
            continue

        # validate from account in policy
        if not policy.from_account_allowed(device_action.from_account):
            continue

        # validate to account in policy
        if not policy.to_account_allowed(device_action.to_account):
            continue

        # validate from account
        all_from_account_polices = device_action.from_account.account_policies
        if all_from_account_polices:
            for from_account_policy in all_from_account_polices:
                if not from_account_policy.allow_account_usage():
                    continue

        # validate to account
        all_to_account_polices = device_action.from_account.account_policies
        if all_to_account_polices:
            for to_account_policy in all_to_account_polices:
                if not to_account_policy.allow_account_usage():
                    continue

        return policy

    return None


def execute(vaild_action):
    pass

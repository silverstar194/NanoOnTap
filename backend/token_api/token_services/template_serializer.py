from django.core import serializers

import re
import json
import datetime
from decimal import Decimal


from ..models.token_models.device import Device
from ..models.token_models.token import Token
from ..models.token_models.action_policy import ActionPolicy
from ..models.nano_models.account import Account
from ..models.token_models.account_policy import AccountPolicy
from ..models.token_models.action import Action
from ..models.nano_models.wallet import Wallet
from ..models.nano_models.node import Node
from ..models.token_models.application import Application
from ..models.token_models.action_set import ActionSet
from ..models.token_models.transaction import Transaction


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def export_template(application):
    application_output = Application.objects.select_related().filter(application_name=application)
    devices = Device.objects.select_related().filter(application__application_name=application)
    tokens = Token.objects.select_related().filter(application__application_name=application)
    action_set = ActionSet.objects.select_related().filter(application__application_name=application)
    actions = Action.objects.select_related().filter(application__application_name=application)
    action_policies = ActionPolicy.objects.select_related().filter(application__application_name=application)
    accounts = Account.objects.select_related().filter(application__application_name=application)
    account_policies = AccountPolicy.objects.select_related().filter(application__application_name=application)
    wallets = Wallet.objects.select_related().filter(application__application_name=application)
    nodes = Node.objects.select_related().filter(application__application_name=application)

    template = {}
    template["application"] = serialize_applications(application_output)
    template["devices"] = serialize_devices(devices)
    template["tokens"] = serialize_tokens(tokens)
    template["action_set"] = serialize_action_set(action_set)
    template["actions"] = serialize_actions(actions)
    template["action_policies"] = serialize_action_policies(action_policies)
    template["accounts"] = serialize_accounts(accounts)
    template["account_policies"] = serialize_account_policies(account_policies)
    template["wallets"] = serialize_wallets(wallets)
    template["nodes"] = serialize_nodes(nodes)

    return template


def serialize_applications(applications):
    return serialize_general(applications)


def serialize_devices(devices):
    return serialize_general(devices)


def serialize_tokens(tokens):
    return serialize_general(tokens)


def serialize_action_policies(action_policies):
    return serialize_general(action_policies)


def serialize_action_set(action_set):
    return serialize_general(action_set)


def serialize_account_policies(account_policies):
    return serialize_general(account_policies)


def serialize_account_policies(account_policies):
    return serialize_general(account_policies)


def serialize_nodes(nodes):
    return serialize_general(nodes)


def serialize_action_set_history(action_set_history):
    if not len(action_set_history) == 1:
        raise Exception("Only can serialize single action_set_history")
    actions = serializers.serialize('python', action_set_history, use_natural_foreign_keys=True, use_natural_primary_keys=True, cls=DecimalEncoder)
    transactions = action_set_history[0].transactions.all()

    if len(actions[0]['fields']['transactions']) > 0:
        actions[0]['fields']['transactions'] = serializers.serialize('python', transactions, use_natural_foreign_keys=True, use_natural_primary_keys=True, cls=DecimalEncoder)

    return strip_text(actions, "token_api.")


def serialize_actions(actions):
    actions = serializers.serialize('python', actions, use_natural_foreign_keys=True, use_natural_primary_keys=True, cls=DecimalEncoder)
    return strip_text(actions, "token_api.")


def serialize_accounts(accounts):
    accounts = serializers.serialize('python', accounts, use_natural_foreign_keys=True, use_natural_primary_keys=True, fields=('account_name', 'wallet', 'application', 'account_policies'),  cls=DecimalEncoder)
    return strip_text(accounts, "token_api.")


def serialize_wallets(wallets):
    wallets = serializers.serialize('python', wallets, use_natural_foreign_keys=True, use_natural_primary_keys=True, fields=('node', 'wallet_name', 'application'))
    return strip_text(wallets, "token_api.")


def serialize_general(objects):
    object_temp = serializers.serialize('python', objects, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return strip_text(object_temp, "token_api.")


def strip_text(before, value):
    obj_str = json.dumps(before,  cls=DecimalEncoder).replace(value, "") # remove token_api
    re.sub(r', \s +]', "]", obj_str) # remove trailing comma
    re.sub(r', \s +}', "}", obj_str)  # remove trailing comma
    obj = json.loads(obj_str)
    return obj

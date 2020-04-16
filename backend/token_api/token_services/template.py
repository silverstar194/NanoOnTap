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


import json
import re

from django.core import serializers


def export_template(application):
    application_ouput = Application.objects.select_related().filter(application_id=application)
    devices = Device.objects.select_related().filter(application__application_id=application)
    tokens = Token.objects.select_related().filter(application__application_id=application)
    action_set = ActionSet.objects.select_related().filter(application__application_id=application)
    actions = Action.objects.select_related().filter(application__application_id=application)
    action_policies = ActionPolicy.objects.select_related().filter(application__application_id=application)
    accounts = Account.objects.select_related().filter(application__application_id=application)
    account_policies = AccountPolicy.objects.select_related().filter(application__application_id=application)
    wallets = Wallet.objects.select_related().filter(application__application_id=application)
    nodes = Node.objects.select_related().filter(application__application_id=application)

    template = {}
    application_output_text = serializers.serialize('python', application_ouput, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    devices_output = serializers.serialize('python', devices, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    tokens_output = serializers.serialize('python', tokens, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    action_policies_output = serializers.serialize('python', action_policies, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    action_set_output = serializers.serialize('python', action_set, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    action_output = serializers.serialize('python', actions, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    account_output = serializers.serialize('python', accounts, use_natural_foreign_keys=True, use_natural_primary_keys=True, fields=('account_id', 'wallet', 'application', 'account_policies'))
    account_policies_output = serializers.serialize('python', account_policies, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    wallet_output = serializers.serialize('python', wallets, use_natural_foreign_keys=True, use_natural_primary_keys=True, fields=('node', 'wallet_name', 'application'))
    node_output = serializers.serialize('python', nodes, use_natural_foreign_keys=True, use_natural_primary_keys=True)

    template["application"] = strip_text(application_output_text, "token_api.")
    template["devices"] = strip_text(devices_output, "token_api.")
    template["tokens"] = strip_text(tokens_output, "token_api.")
    template["action_set"] = strip_text(action_set_output, "token_api.")
    template["actions"] = strip_text(action_output, "token_api.")
    template["action_policies"] = strip_text(action_policies_output, "token_api.")
    template["accounts"] = strip_text(account_output, "token_api.")
    template["account_policies"] = strip_text(account_policies_output, "token_api.")
    template["wallets"] = strip_text(wallet_output, "token_api.")
    template["nodes"] = strip_text(node_output, "token_api.")

    return template


def import_template(json_data):
    application_setup = json.loads(json_data)

    if "application" in application_setup:
        application_setup["application"] = add_text(application_setup["application"], r'"model": "application"', r'"model": "token_api.application"')
        for obj in serializers.deserialize('python',  application_setup["application"], use_natural_foreign_keys=True, use_natural_primary_keys=True):
            obj.save()

    if "nodes" in application_setup:
        application_setup["nodes"] = add_text(application_setup["nodes"], r'"model": "node"', r'"model": "token_api.node"')
        for obj in serializers.deserialize('python', application_setup["nodes"],  use_natural_foreign_keys=True, use_natural_primary_keys=True):
            obj.save()

    if "wallets" in application_setup:
        application_setup["wallets"] = add_text(application_setup["wallets"], r'"model": "wallet"', r'"model": "token_api.wallet"')
        for obj in serializers.deserialize('python', application_setup["wallets"],  use_natural_foreign_keys=True, use_natural_primary_keys=True):
            # merge with current model data
            current_wallet = Wallet.objects.get(wallet_name=obj.__dict__['object'].wallet_name)
            if current_wallet.wallet_id:
                obj.__dict__['object'].wallet_id = current_wallet.wallet_id

            obj.save()

    if "account_policies" in application_setup:
        application_setup["account_policies"] = add_text(application_setup["account_policies"], r'"model": "accountpolicy"', r'"model": "token_api.accountpolicy"')
        for obj in serializers.deserialize('python', application_setup["account_policies"],  use_natural_foreign_keys=True, use_natural_primary_keys=True):
            obj.save()

    if "accounts" in application_setup:
        application_setup["accounts"] = add_text(application_setup["accounts"], r'"model": "account"', r'"model": "token_api.account"')
        for obj in serializers.deserialize('python', application_setup["accounts"],  use_natural_foreign_keys=True, use_natural_primary_keys=True):
            # merge with current model data
            current_account = Account.objects.get(account_id=obj.__dict__['object'].account_id)
            if current_account.address:
                obj.__dict__['object'].address = current_account.address

            obj.save()

    if "actions" in application_setup:
        application_setup["actions"] = add_text(application_setup["actions"], r'"model": "action"', r'"model": "token_api.action"')
        for obj in serializers.deserialize('python', application_setup["actions"],  use_natural_foreign_keys=True, use_natural_primary_keys=True):
            obj.save()

    if "action_set" in application_setup:
        application_setup["action_set"] = add_text(application_setup["action_set"], r'"model": "actionset"', r'"model": "token_api.actionset"')
        for obj in serializers.deserialize('python', application_setup["action_set"],  use_natural_foreign_keys=True, use_natural_primary_keys=True):
            obj.save()

    if "devices" in application_setup:
        application_setup["devices"] = add_text(application_setup["devices"], r'"model": "device"', r'"model": "token_api.device"')
        for obj in serializers.deserialize('python',  application_setup["devices"], use_natural_foreign_keys=True, use_natural_primary_keys=True):
            obj.save()

    if "action_policies" in application_setup:
        application_setup["action_policies"] = add_text(application_setup["action_policies"], r'"model": "actionpolicy"', r'"model": "token_api.actionpolicy"')
        for obj in serializers.deserialize('python', application_setup["action_policies"],  use_natural_foreign_keys=True, use_natural_primary_keys=True):
            obj.save()

    if "tokens" in application_setup:
        application_setup["tokens"] = add_text(application_setup["tokens"], r'"model": "token"', r'"model": "token_api.token"')
        for obj in serializers.deserialize('python', application_setup["tokens"], use_natural_foreign_keys=True, use_natural_primary_keys=True):
            obj.save()

    return True


def strip_text(before, value):
    obj_str = json.dumps(before).replace(value, "") # remove token_api
    re.sub(r', \s +]', "]", obj_str) # remove trailing comma
    re.sub(r', \s +}', "}", obj_str)  # remove trailing comma
    obj = json.loads(obj_str)
    return obj


def add_text(input, before, after):
    input_str = json.dumps(input)
    input_proccssed = input_str.replace(before, after)
    return json.loads(input_proccssed)

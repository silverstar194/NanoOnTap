from ..models.nano_models.account import Account
from ..models.nano_models.wallet import Wallet

from django.core import serializers
from ..common.constants import *

import json


def import_template(json_data):
    application_setup = json.loads(json_data)

    if "application" in application_setup:
        deserializer_applications(application_setup["application"])

    if "nodes" in application_setup:
        deserializer_nodes(application_setup["nodes"])

    if "wallets" in application_setup:
        deserializer_wallets(application_setup["wallets"])

    if "account_policies" in application_setup:
        deserializer_account_policies(application_setup["account_policies"])

    if "accounts" in application_setup:
        deserializer_accounts(application_setup["accounts"])

    if "actions" in application_setup:
        deserializer_actions(application_setup["actions"])

    if "action_set" in application_setup:
        deserializer_action_set(application_setup["action_set"])

    if "devices" in application_setup:
        deserializer_devices(application_setup["devices"])

    if "action_policies" in application_setup:
        deserializer_action_polices(application_setup["action_policies"])

    if "tokens" in application_setup:
        deserializer_tokens(application_setup["tokens"])

    return True


def deserializer_tokens(tokens):
    tokens = add_text(tokens, token_serialize_pre_string, token_serialize_post_string)
    deserializer_general(tokens)


def deserializer_devices(devices):
    devices = add_text(devices, device_serialize_pre_string, device_serialize_post_string)
    deserializer_general(devices)


def deserializer_applications(applications):
    applications = add_text(applications, application_set_serialize_pre_string, application_set_serialize_post_string)
    deserializer_general(applications)


def deserializer_action_set(action_set):
    action_set = add_text(action_set, action_set_serialize_pre_string, action_set_serialize_post_string)
    deserializer_general(action_set)


def deserializer_action_polices(action_polices):
    action_polices = add_text(action_polices, action_policy_serialize_pre_string, action_policy_serialize_post_string)
    deserializer_general(action_polices)


def deserializer_actions(actions):
    actions = add_text(actions, action_serialize_pre_string, action_serialize_post_string)
    deserializer_general(actions)


def deserializer_account_policies(account_polices):
    account_polices = add_text(account_polices, account_policy_serialize_pre_string, account_policy_serialize_post_string)
    deserializer_general(account_polices)


def deserializer_nodes(nodes):
    nodes = add_text(nodes, r'"model": "node"', r'"model": "token_api.node"')
    deserializer_general(nodes)


def deserializer_wallets(wallets):
    wallets = add_text(wallets, wallet_serialize_pre_string, wallet_serialize_post_string)
    for obj in serializers.deserialize('python', wallets, use_natural_foreign_keys=True, use_natural_primary_keys=True):
        # merge with current model data
        try:
            current_wallet = Wallet.objects.get(wallet_name=obj.__dict__['object'].wallet_name)
            if current_wallet.wallet_id:
                obj.__dict__['object'].wallet_id = current_wallet.wallet_id
        except Exception:
            pass
        obj.save()


def deserializer_accounts(accounts):
    accounts = add_text(accounts, account_serialize_pre_string, account_serialize_post_string)
    for obj in serializers.deserialize('python', accounts, use_natural_foreign_keys=True, use_natural_primary_keys=True):
        # merge with current model data
        try:
            current_account = Account.objects.get(account_name=obj.__dict__['object'].account_name)
            if current_account.address:
                obj.__dict__['object'].address = current_account.address

            if current_account.current_balance:
                obj.__dict__['object'].current_balance = current_account.current_balance

            if current_account.POW:
                obj.__dict__['object'].POW = current_account.POW
        except Exception:
            pass
        obj.save()


def deserializer_general(objects):
    for obj in serializers.deserialize('python', objects, use_natural_foreign_keys=True, use_natural_primary_keys=True):
        obj.save()


def add_text(input, before, after):
    input_str = json.dumps(input)
    input_proccssed = input_str.replace(before, after)
    return json.loads(input_proccssed)

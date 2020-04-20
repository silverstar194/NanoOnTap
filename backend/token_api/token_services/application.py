from ..models.token_models.device import Device
from ..models.token_models.token import Token
from ..models.token_models.action_policy import ActionPolicy
from ..models.nano_models.account import Account
from ..models.token_models.account_policy import AccountPolicy
from ..models.token_models.action import Action
from ..models.nano_models.wallet import Wallet
from ..models.nano_models.node import Node
from ..models.token_models.application import Application

def application_exists(application):
    return Application.objects.filter(application_name=application).count() > 0 or Token.objects.filter(application__application_id=application).count() > 0 or Device.objects.filter(application__application_id=application).count() > 0

def clean_up_failed_template(application):
    Token.objects.filter(application__application_name=application).delete()
    Device.objects.filter(application__application_name=application).delete()
    ActionPolicy.objects.filter(application__application_name=application).delete()
    Account.objects.filter(application__application_name=application).delete()
    AccountPolicy.objects.filter(application__application_name=application).delete()
    Action.objects.filter(application__application_name=application).delete()
    Wallet.objects.filter(application__application_name=application).delete()
    Node.objects.filter(application__application_name=application).delete()

def get_application(application):
    return Application.objects.get(application_name=application)



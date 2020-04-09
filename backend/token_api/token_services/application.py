from ..models.device import Device
from ..models.token import Token
from ..models.action_policy import ActionPolicy
from ..models.account import Account
from ..models.account import AccountPolicy
from ..models.action import Action
from ..models.wallet import Wallet
from ..models.node import Node
from ..models.application import Application

def application_exists(application):
    return Application.objects.filter(application_id=Application).count() > 0 or Token.objects.filter(application__application_id=application).count() > 0 or Device.objects.filter(application__application_id=application).count() > 0

def clean_up_failed_template(application):
    Token.objects.filter(application__application_id=application).delete()
    Device.objects.filter(application__application_id=application).delete()
    ActionPolicy.objects.filter(application__application_id=application).delete()
    Account.objects.filter(application__application_id=application).delete()
    AccountPolicy.objects.filter(application__application_id=application).delete()
    Action.objects.filter(application__application_id=application).delete()
    Wallet.objects.filter(application__application_id=application).delete()
    Node.objects.filter(application__application_id=application).delete()



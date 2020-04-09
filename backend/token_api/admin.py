# Register your token_models here.
from django.contrib import admin

from .models.nano_models.account import Account
from .models.nano_models.node import Node
from .models.nano_models.transaction import Transaction
from .models.nano_models.wallet import Wallet
from .models.token_models.action import Action
from .models.token_models.action_policy import ActionPolicy
from .models.token_models.account_policy import AccountPolicy
from .models.token_models.device import Device
from .models.token_models.token import Token
from .models.token_models.application import Application
from .models.custom_action_policies.example_custom_action_policy import CustomActionPolicy


class AccountAdmin(admin.ModelAdmin):
    exclude = ('POW', 'in_use', )

admin.site.register(Account, AccountAdmin)

class ExampleCustomActionPolicyAdmin(admin.ModelAdmin):
    pass
admin.site.register(CustomActionPolicy, ExampleCustomActionPolicyAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Application, ApplicationAdmin)

class NodeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Node, NodeAdmin)

class TransactionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Transaction, TransactionAdmin)

class WalletAdmin(admin.ModelAdmin):
    pass
admin.site.register(Wallet, WalletAdmin)

class ActionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Action, ActionAdmin)

class AllowedActionPolicyAdmin(admin.ModelAdmin):
    pass
admin.site.register(ActionPolicy, AllowedActionPolicyAdmin)

class AllowedAccountPolicyAdmin(admin.ModelAdmin):
    pass
admin.site.register(AccountPolicy, AllowedAccountPolicyAdmin)

class DeviceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Device, DeviceAdmin)

class TokenAdmin(admin.ModelAdmin):
    pass
admin.site.register(Token, TokenAdmin)


admin.site.site_header = "NanoToken API"
admin.site.index_title = "NanoToken API"
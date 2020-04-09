# Register your token_models here.
from django.contrib import admin

from .models.account import Account
from .models.node import Node
from .models.transaction import Transaction
from .models.wallet import Wallet
from .models.action import Action
from .models.action_policy import ActionPolicy
from .models.account_policy import AccountPolicy
from .models.device import Device
from .models.token import Token
from .models.application import Application



class AccountAdmin(admin.ModelAdmin):
    exclude = ('POW', 'in_use', )

admin.site.register(Account, AccountAdmin)

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
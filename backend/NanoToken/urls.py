"""NanoToken URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import token_api.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('action/template/import', views.import_template_view),
    path('action/template/export', views.export_template_view),
    path('action/execute', views.attempt_action),
    path('action/bootstrap', views.bootstrap_all),
    path('action/sync', views.sync),
    path('action/ping', views.ping),

    path('action/account/get', views.get_account, name='action/account/get'),
    path('action/account/get/balance', views.get_account_balance, name='action/account/get/balance'),
    path('action/account/get/address', views.get_account_address, name='action/account/get/address'),
    path('action/account/get/all', views.get_accounts, name='action/account/get/all'),
    path('action/account/update', views.update_account, name='action/account/update'),
    path('action/account/remove', views.remove_account, name='action/account/remove'),

    path('action/node/get', views.get_node, name='action/node/get'),
    path('action/node/get/all', views.get_nodes, name='action/node/get/all'),
    path('action/node/update', views.update_node, name='action/node/update'),
    path('action/node/remove', views.remove_node, name='action/node/remove'),

    path('action/transaction/get/all', views.get_transactions, name='action/transaction/get/all'),

    path('action/actionhistory/get', views.get_action_history, name='action/actionhistory/get'),

    path('action/wallet/get', views.get_wallet, name='action/wallet/get'),
    path('action/wallet/get/all', views.get_wallets, name='action/wallet/get/all'),
    path('action/wallet/update', views.update_wallet, name='action/wallet/update'),
    path('action/wallet/remove', views.remove_wallet, name='action/wallet/remove'),

    path('action/accountpolicy/get', views.get_account_policy, name='action/accountpolicy/get'),
    path('action/accountpolicy/get/all', views.get_account_policies, name='action/accountpolicy/get/all'),
    path('action/accountpolicy/update', views.update_account_policy, name='action/accountpolicy/update'),
    path('action/accountpolicy/remove', views.remove_account_policy, name='action/accountpolicy/remove'),

    path('action/action/get', views.get_action, name='action/action/get'),
    path('action/action/get/all', views.get_actions, name='action/action/get/all'),
    path('action/action/update', views.update_action, name='action/action/update'),
    path('action/action/remove', views.remove_action, name='action/action/remove'),

    path('action/actionpolicy/get', views.get_action_policy, name='action/actionpolicy/get'),
    path('action/actionpolicy/get/all', views.get_action_policies, name='action/actionpolicy/get/all'),
    path('action/actionpolicy/update', views.update_action_policy, name='action/actionpolicy/update'),
    path('action/actionpolicy/remove', views.remove_action_policy, name='action/actionpolicy/remove'),

    path('action/actionset/get', views.get_action_set, name='action/actionset/get'),
    path('action/actionset/get/all', views.get_action_sets, name='action/actionset/get/all'),
    path('action/actionset/update', views.update_action_set, name='action/actionset/update'),
    path('action/actionset/remove', views.remove_action_set, name='action/actionset/remove'),

    path('action/application/get', views.get_application, name='action/application/get'),
    path('action/application/get/all', views.get_applications, name='action/application/get/all'),
    path('action/application/update', views.update_application, name='action/application/update'),
    path('action/application/remove', views.remove_application, name='action/application/remove'),

    path('action/device/get', views.get_device, name='action/device/get'),
    path('action/device/get/all', views.get_devices, name='action/device/get/all'),
    path('action/device/update', views.update_device, name='action/device/update'),
    path('action/device/remove', views.remove_device, name='action/device/remove'),

    path('action/token/get', views.get_token, name='action/token/get'),
    path('action/token/get/all', views.get_tokens, name='action/token/get/all'),
    path('action/token/update', views.update_token, name='action/token/update'),
    path('action/token/remove', views.remove_token, name='action/token/remove'),
]

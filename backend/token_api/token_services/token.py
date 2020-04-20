from .. import models as models


def get_token(token_name, application_name):
    """
    Get token by id

    """
    return models.Token.objects.get(token_name = token_name, application__application_name=application_name)

def get_token_action_policies(token):
    return models.ActionPolicy.objects.filter(token=token)

def get_token_custom_action_policies(token):
    return models.CustomActionPolicy.objects.filter(token=token)


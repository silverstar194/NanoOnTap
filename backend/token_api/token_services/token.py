from .. import models as models


def get_token(token_id, application_id):
    """
    Get token by id

    """
    return models.Token.objects.get(token_id = token_id, application__application_id=application_id)

def get_token_action_policies(token):
    return models.ActionPolicy.objects.filter(token=token)

def get_token_custom_action_policies(token):
    return models.CustomActionPolicy.objects.filter(token=token)


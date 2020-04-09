from .. import models as models


def get_token(token_id):
    """
    Get token by id

    """
    return models.Token.objects.get(token_id = token_id)

def get_token_action_policies(token):
    return models.ActionPolicy.objects.filter(token=token).order_by("priority")

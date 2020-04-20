from django.utils import timezone

from backend.token_api.models.token_models.action_history import ActionHistory


def audit_execution(action, policy):
    action_history = ActionHistory.objects.create(action=action, policy=policy)
    action_history.executed_time = timezone.now()
    action_history.executed = True
    action_history.save()

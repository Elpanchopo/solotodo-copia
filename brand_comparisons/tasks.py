from celery import shared_task

from .models import BrandComparisonAlert


@shared_task(queue='reports', ignore_result=True)
def alert_check_for_changes(alert_id):
    BrandComparisonAlert.objects.get(pk=alert_id).check_for_changes()

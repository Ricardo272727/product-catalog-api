from celery import shared_task
from django.contrib.auth.models import User
from .models import ProductViewMetric 


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 2, "countdown": 10})
def notify_product_change(self, id, changes, updated_by):
    print(f"Product {id} changed: {changes} by {updated_by}")
    print("Notifying other admins...")
    admins = User.objects.all()

    for admin in admins:
        print(f"Notifying admin {admin.username} / {admin.email}") 


@shared_task
def save_visualization_metrics(products, ip=None, user_agent=None):
    print(f"Saving visualization metrics for customer: {ip} {user_agent}")
    for product in products:
        metric = ProductViewMetric()
        metric.product_id = product
        metric.ip_address = ip
        metric.user_agent = user_agent
        metric.save()
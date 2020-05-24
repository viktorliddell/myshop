from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    # Задача отправки email-уведомлений при успешном оформлении заказа
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name}! You have successfully placed an order. Your order is {order.id}'
    mail_sent = send_mail(subject, message, 'info@lidlab.ru', [order.email])
    return mail_sent

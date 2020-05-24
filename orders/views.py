from django.shortcuts import render
from django.core.mail import send_mail

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item['product'], price=item['price'], quantity=item['quantity'])

            # Очищаем корзину
            cart.clear()

            # Отправка письма на почту
            subject = f'Новый заказ №{order.id}'
            message = f'Дорогой {order.first_name}! Ваш заказ поступил к нам в обработку. Мы скоро Вам перезвоним!'
            send_mail(subject, message, 'info@lidlab.ru', [order.email])

            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

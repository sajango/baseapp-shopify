from django.conf.urls import url
from django.urls import path


from . import views

app_name = 'home'
urlpatterns = [
    path('orders', views.orders, name='orders'),
    url(r'order/(?P<order_id>[0-9]+)', views.order_detail, name='order_detail'),
    path('order-payment-wk', views.order_payment_wk, name='order_payment_wk'),
    path('api/update-status', views.line_item_update_status, name='line_item_update_status'),
    path('api/check-try-on', views.check_try_on, name='check_try_on'),
    path('api/line-items', views.LineItems.as_view(), name='line-items'),
]

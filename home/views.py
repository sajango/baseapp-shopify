import json

import shopify
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from home.models import LineItem
from shopify_app.decorators import shop_login_required
from shopify_app.shopify_utils import get_orders


@shop_login_required
def index(request):
    result = get_orders(limit=10)
    orders = shopify.Order.find()
    print(orders)
    return render(request, 'home/index.html', {'products': [], 'orders': []})


@csrf_exempt
def your_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            line_items = data['line_items']
            for item in line_items:
                line_item = {'line_item_id': item['id'], 'order_id': data['id'], 'customer_id': data['customer']['id'],
                             'variant_id': item['variant_id'], 'product_id': item['product_id'], 'title': item['title'],
                             'name': item['name'], 'quantity': item['quantity'],
                             'properties': '&'.join(item['properties']), 'price': item['price']}
                LineItem.objects.get_or_create(order_id=data['id'], line_item_id=item['id'],
                                               customer_id=data['customer']['id'],
                                               product_id=item['product_id'], defaults=line_item)
        except Exception as e:
            print(e)
    return HttpResponse("Your response")

import json

import shopify
from django.apps import apps
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response

from home.models import LineItem, Order
from home.serializers import OrderSerializer
from shopify_app.decorators import shop_login_required
from shopify_app.models import ShopifyStore

api_version = apps.get_app_config('shopify_app').SHOPIFY_API_VERSION


@shop_login_required
def orders(request):
    m_orders = Order.objects.prefetch_related('line_items').filter().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(m_orders, 50)
    try:
        m_orders = paginator.page(page)
    except PageNotAnInteger:
        m_orders = paginator.page(1)
    except EmptyPage:
        m_orders = paginator.page(paginator.num_pages)

    return render(request, 'home/index.html', {'orders': m_orders, 'shop_url': request.session.get('shop_url')}, )


@shop_login_required
def order_detail(request, order_id):
    line_items = LineItem.objects.filter(order_id=order_id)
    order = Order.objects.get(id=order_id)
    s_order = shopify.Order.find(id_=order.order_id)

    return render(request, 'home/detail.html',
                  {'line_items': line_items, 'order': s_order, 'shop_url': request.session.get('shop_url')})


def get_image(product, variant_id):
    images = product.images
    for img in images:
        if variant_id in img.variant_ids:
            return img.src


@csrf_exempt
@shop_login_required
def order_payment_wk(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_data = {'order_id': data['id'], 'order_number': data['order_number'],
                          'customer_id': data['customer']['id'], 'customer_first_name': data['customer']['first_name'],
                          'customer_last_name': data['customer']['last_name'], 'created': data['created_at']}
            order, _ = Order.objects.get_or_create(order_id=data['id'], defaults=order_data)

            line_items = data['line_items']
            product = None
            for item in line_items:
                if product is None:
                    product = shopify.Product.find(id_=item['product_id'])
                img = get_image(product, item['variant_id'])

                properties = item['properties']
                p_value = ''
                for p in properties:
                    p_name = p.get('name', None)
                    p_value = p.get('value', None)
                    if p_name == 'status' and p_value in ['try-on', 'purchased']:
                        break
                line_item = {'order_id': order.id, 'line_item_id': item['id'], 'variant_id': item['variant_id'],
                             'product_id': item['product_id'], 'title': item['title'],
                             'name': item['name'], 'quantity': item['quantity'],
                             'status': p_value, 'price': item['price'], 'variant_title': item['variant_title'],
                             'images': img}
                LineItem.objects.get_or_create(order_id=data['id'], line_item_id=item['id'], defaults=line_item)
        except Exception as e:
            print(e)
    return HttpResponse("Your response")


@csrf_exempt
def line_item_update_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for line_item_id, status in data.items():
            line_item = LineItem.objects.get(line_item_id=line_item_id);
            line_item.status = status
            line_item.save()
    return HttpResponse("Your response")


@csrf_exempt
def check_try_on(request):
    if request.method == 'GET':
        customer = request.GET.get('customer')
        m_orders = Order.objects.prefetch_related('line_items').filter(customer_id=customer)

        for order in m_orders:
            line_items = order.line_items.all()
            result = {'is_try_on': False}
            for item in line_items:
                if item.status in ['try-on', 'try-on-shiped', 'will-be-returned']:
                    result = {'is_try_on': True}
                    break
            return JsonResponse(result)
    return JsonResponse({'is_try_on': False})


class LineItems(generics.ListAPIView):
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        shop = request.GET.get('shop')
        shopify_store = ShopifyStore.objects.get(shop_url=shop)
        session = shopify.Session(shop, api_version, shopify_store.access_token)
        m_shopify = shopify.ShopifyResource.activate_session(session)
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True, context={shopify: m_shopify})
        return Response(serializer.data)

    def get_queryset(self):
        customer_id = self.request.GET.get('customer')
        queryset = Order.objects.prefetch_related('line_items').filter(customer_id=customer_id)
        return queryset

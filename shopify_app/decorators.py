import json

import shopify
from django.apps import apps
from django.shortcuts import redirect
from django.urls import reverse

from . import views
from .models import ShopifyStore

api_version = apps.get_app_config('shopify_app').SHOPIFY_API_VERSION


def shop_login_required(fn):
    def wrapper(request, *args, **kwargs):
        if request.method == "GET":
            shop_url = request.GET.get('shop')
        elif request.method == "POST":
            shop_url = request.headers.get('X-Shopify-Shop-Domain')

        if shop_url is None or shop_url == '':
            shop_url = request.GET.get('shop')
        request.session['shop_url'] = shop_url
        try:
            shopify_store = ShopifyStore.objects.get(shop_url=shop_url)
            if shopify_store is None:
                request.session['return_to'] = request.get_full_path()
                return redirect(reverse(views.login))
            else:
                session = shopify.Session(shop_url, api_version, shopify_store.access_token)
                shopify.ShopifyResource.activate_session(session)
            return fn(request, *args, **kwargs)
        except Exception as e:
            print(e)
            request.session['return_to'] = request.get_full_path()
            return redirect(reverse(views.login))

    wrapper.__name__ = fn.__name__
    return wrapper

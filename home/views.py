from django.shortcuts import render

from shopify_app.decorators import shop_login_required

from shopify_app.shopify_utils import get_all_products, get_product_by_id, create_shop_metafields


@shop_login_required
def index(request):
    result = create_shop_metafields()
    print(result)
    return render(request, 'home/index.html', {'products': [], 'orders': []})

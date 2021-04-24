from django.shortcuts import render

from shopify_app.decorators import shop_login_required
from shopify_app.shopify_utils import get_all_products, get_product_by_id


@shop_login_required
def index(request):
    result = get_all_products(limit=5)
    product = get_product_by_id(node_id="gid://shopify/Product/6051806576799")
    return render(request, 'home/index.html', {'products': [], 'orders': []})

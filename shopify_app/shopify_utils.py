import json

import shopify


# Reference to https://shopify.dev/tools/graphiql-admin-api
def get_all_products(limit, after=None):
    if after:
        query = '{products(first: %LIMIT%, after: %AFTER%) { edges { cursor node { id } } }}'
    else:
        query = '{products(first: %LIMIT%) { edges { cursor node { id } } }}'
    query = query.replace('%LIMIT%', str(limit))
    if after:
        query = query.replace('%AFTER%', after)

    result = shopify.GraphQL().execute(query)
    return json.loads(result)


def get_product_by_id(node_id):
    query = '{ product ( id: "%NODE_ID%" ) { bodyHtml createdAt status } }'
    query = query.replace('%NODE_ID%', str(node_id))
    result = shopify.GraphQL().execute(query)
    return json.loads(result)


def get_orders(limit, after, status):
    pass


def get_order_by_id(order_id):
    pass


def create_shop_metafields():
    r = shopify.Metafield.find(
    )
    return r

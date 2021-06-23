# from api.models import Product
from shopify_app.models import ShopifyStore
import json
import logging
import shopify

logger = logging.getLogger(__name__)


# Reference to https://shopify.dev/tools/graphiql-admin-api
def get_all_webhooks():
    query = """
    {
        webhookSubscriptions(first:5) {
            edges {
                node {
                    id
                }
            }
        }
    }
    """
    # result = shopify.GraphQL().execute(query)
    result = shopify.Webhook
    return json.loads(result)


def get_products():
    query = '''{
        products(first: 10) {
            edges {
                node {
                    createdAt
                    collections(first: 5) {
                        edges {
                            node {
                                id
                                handle
                                title 
                            }
                        }
                    }
                    description
                    featuredImage {
                        id
                        originalSrc
                        transformedSrc
                    }
                    id
                    isGiftCard
                    onlineStorePreviewUrl
                    onlineStoreUrl
                    productType
                    publishedAt
                    tags
                    title
                    totalInventory
                    updatedAt
                    vendor
                }
            }
        }
    }'''

    result = shopify.GraphQL().execute(query)
    data = json.loads(result)

    return data


def get_all_resources(resource, **kwargs):
    resource_count = resource.count(**kwargs)
    resources = []
    if resource_count > 0:
        for page in range(1, ((resource_count - 1) // 250) + 2):
            kwargs.update({"limit": 250, "page": page})
            resources.extend(resource.find(**kwargs))
    return resources


def get_all_products(limit, after=None):
    if after:
        query = '''
        {products(first: %LIMIT%, after: %AFTER%) { edges { node { id title
            status
            featuredImage {
                originalSrc
                transformedSrc(maxWidth:160, crop: CENTER)
            } } } }}
        '''
    else:
        query = '''{products(first: %LIMIT%) { edges { node { id title status
            featuredImage {
                originalSrc
                transformedSrc(maxWidth:160, crop: CENTER)
            }} } }}'''

    query = query.replace('%LIMIT%', str(limit))

    if after:
        query = query.replace('%AFTER%', after)

    result = shopify.GraphQL().execute(query)
    return json.loads(result)


def get_all_collections(first, after='', search=''):
    query = """{
        collections(%s) {
            pageInfo {
                hasNextPage
                hasPreviousPage
            }
            edges {
                cursor
                node {
                    id
                    title
                    productsCount
                    image {
                        originalSrc
                        transformedSrc(maxWidth:80, crop: CENTER)
                    }
                }
            }
        }
    }
    """

    pagination = f'first: {first}' if after == '' else f'first: {first}, after: "{after}"'
    query_params = f'query: ""' if search == '' else f'query: "title:{search}*"'

    result = shopify.GraphQL().execute(query % f'{pagination}, {query_params}')
    data = json.loads(result)
    pagination = None
    collections = []

    if 'data' in data and 'collections' in data['data']:
        if 'pageInfo' in data['data']['collections']:
            pagination = data['data']['collections']['pageInfo']

        if 'edges' in data['data']['collections'] and len(data['data']['collections']['edges']):
            for item in data['data']['collections']['edges']:
                if 'node' in item:
                    collections.append({
                        "cursor": item['cursor'],
                        "id": item['node']['id'],
                        "title": item['node']['title'],
                        "productsCount": item['node']['productsCount'],
                        "featured_image": item['node']['image']['originalSrc'] \
                            if item['node']['image'] is not None and 'originalSrc' in item['node']['image'] else None,
                        "thumbnail": item['node']['image']['transformedSrc'] \
                            if item['node']['image'] is not None and 'transformedSrc' in item['node'][
                            'image'] else None,
                    })

    return {
        'pagination': pagination,
        'collections': collections
    }


def get_all_tags(limit, after=None):
    if after:
        query = '''
        {
            shop{
                productTags(first: %LIMIT%, after: %AFTER%){
                    edges{
                        node
                    }
                }
            }
        }
        '''
    else:
        query = '''
        {
            shop{
                productTags(first: %LIMIT%){
                    edges{
                        node
                    }
                }
            }
        }
        '''

    query = query.replace('%LIMIT%', str(limit))

    if after:
        query = query.replace('%AFTER%', after)

    result = shopify.GraphQL().execute(query)
    data = json.loads(result)

    tags = []
    if 'data' in data and 'shop' in data['data'] and 'productTags' in data['data']['shop'] and 'edges' in \
            data['data']['shop']['productTags'] \
            and len(data['data']['shop']['productTags']['edges']):
        for item in data['data']['shop']['productTags']['edges']:
            if 'node' in item:
                tags.append(item['node'])

    return tags


def get_collections_by_product_id(product_id):
    query = '''{
        product(id: "%s") {
            collections(first: 50) {
                edges { 
                    node { 
                        id 
                        title 
                    }
                }
            }
        }
    }
    '''

    result = shopify.GraphQL().execute(query % product_id)
    data = json.loads(result)

    collections = []
    if 'data' in data and 'product' in data['data'] and data['data']['product'] is not None and 'collections' in \
            data['data']['product'] \
            and 'edges' in data['data']['product']['collections'] and len(
        data['data']['product']['collections']['edges']):
        for item in data['data']['product']['collections']['edges']:
            if 'node' in item:
                collections.append({
                    "id": item['node']['id'],
                    "title": item['node']['title'],
                })

    return collections


def get_collection_info_by_id(collection_id):
    query = '''{
        collection(id: "%s") {
            id 
            title 
        }        
    }
    '''

    result = shopify.GraphQL().execute(query % collection_id)
    data = json.loads(result)

    collection = None
    if 'data' in data and 'collection' in data['data'] and data['data']['collection'] is not None:
        collection = {
            "id": data['data']['collection']['id'],
            "title": data['data']['collection']['title'],
        }

    return collection


def get_product_by_id(product_id):
    query = '''{
        product(id: "%s") {
            id
            title
            status
            featuredImage {
                originalSrc
                transformedSrc(maxWidth:160, crop: CENTER)
            }
        }
    }
    '''

    result = shopify.GraphQL().execute(query % product_id)
    data = json.loads(result)

    product = None
    if 'data' in data and 'product' in data['data'] and data['data']['product'] is not None:
        product = {
            "id": data['data']['product']['id'],
            "title": data['data']['product']['title'],
            "featured_image": data['data']['product']['featuredImage']['originalSrc'] \
                if data['data']['product']['featuredImage'] is not None and 'originalSrc' in data['data']['product'][
                'featuredImage'] else None,
            "thumbnail": data['data']['product']['featuredImage']['transformedSrc'] \
                if data['data']['product']['featuredImage'] is not None and 'transformedSrc' in data['data']['product'][
                'featuredImage'] else None,
        }

    return product


def get_products_by_id_list(product_id_list):
    product_id_set = set(product_id_list)

    query = '{'
    for idx, product_id in enumerate(product_id_set):
        query += '''
        product%s: product(id: "%s") {
            id
            title
            status
        }
        ''' % (idx, product_id)
    query += '}'

    result = shopify.GraphQL().execute(query)
    data = json.loads(result)
    products = []

    if 'data' in data:
        for i in range(0, len(product_id_set)):
            if 'product' + str(i) in data['data'] and data['data']['product' + str(i)] is not None:
                item = data['data']['product' + str(i)]

                if item:
                    products.append({
                        "id": item['id'],
                        "title": item['title'],
                    })

    return products


def get_collections_by_id_list(set_collection_ids):
    set_collection_ids = set(set_collection_ids)

    query = '{'
    for idx, collection_id in enumerate(set_collection_ids):
        query += '''
        collection%s: collection(id: "%s") {
            id
            title
        }
        ''' % (idx, collection_id)
    query += '}'

    result = shopify.GraphQL().execute(query)
    data = json.loads(result)
    collections = {}

    if 'data' in data:
        for i in range(0, len(set_collection_ids)):
            if 'collection' + str(i) in data['data'] and data['data']['collection' + str(i)] is not None:
                item = data['data']['collection' + str(i)]

                if item:
                    collections[item['id']] = {
                        "id": item['id'],
                        "title": item['title'],
                    }

    return collections


def get_products_by_collection(collection):
    query = """{
        collection(id: "%s") {
            handle
            products(first: 100) {
                edges { 
                    node { 
                        id
                        title
                        status
                        featuredImage {
                            originalSrc
                            transformedSrc(maxWidth:160, crop: CENTER)
                        }
                    } 
                }
            }
        }
    }
    """

    result = shopify.GraphQL().execute(query % collection)
    data = json.loads(result)

    products = []

    if 'data' in data and 'collection' in data['data'] and data['data']['collection'] is not None and 'products' in \
            data['data']['collection'] \
            and 'edges' in data['data']['collection']['products'] \
            and len(data['data']['collection']['products']['edges']):
        for item in data['data']['collection']['products']['edges']:
            if 'node' in item and item['node']['status'] == 'ACTIVE':
                products.append({
                    "id": item['node']['id'],
                    "title": item['node']['title'],
                    "featured_image": item['node']['featuredImage']['originalSrc'] if item['node'][
                                                                                          'featuredImage'] is not None and 'originalSrc' in
                                                                                      item['node'][
                                                                                          'featuredImage'] else None,
                    "thumbnail": item['node']['featuredImage']['transformedSrc'] if item['node'][
                                                                                        'featuredImage'] is not None and 'transformedSrc' in
                                                                                    item['node'][
                                                                                        'featuredImage'] else None,
                })

    return products


def get_products_by_tag(tag):
    query = """{
        products(first: 100, query: "tag:%s") {
            edges {
                node {
                    id
                    title
                    featuredImage {
                        originalSrc
                        transformedSrc(maxWidth:160, crop: CENTER)
                    }
                }
            }
        }
    }
    """
    if not isinstance(tag, list):
        tag = [tag]

    result = shopify.GraphQL().execute(query % tag)
    data = json.loads(result)
    products = []

    if 'data' in data and 'products' in data['data'] and 'edges' in data['data']['products'] and len(
            data['data']['products']['edges']):
        for item in data['data']['products']['edges']:
            if 'node' in item:
                products.append({
                    "id": item['node']['id'],
                    "title": item['node']['title'],
                    "featured_image": item['node']['featuredImage']['originalSrc'] if item['node'][
                                                                                          'featuredImage'] is not None and 'originalSrc' in
                                                                                      item['node'][
                                                                                          'featuredImage'] else None,
                    "thumbnail": item['node']['featuredImage']['transformedSrc'] if item['node'][
                                                                                        'featuredImage'] is not None and 'transformedSrc' in
                                                                                    item['node'][
                                                                                        'featuredImage'] else None,
                })

    return products


def get_products_by_type(type, first, after='', search=''):
    query = """{
        products(%s) {
            pageInfo {
                hasNextPage
                hasPreviousPage
            }
            edges {
                cursor
                node {
                    id
                    title
                    featuredImage {
                        originalSrc
                        transformedSrc(maxWidth:160, crop: CENTER)
                    }
                }
            }
        }
    }
    """

    pagination = f'first: {first}' if after == '' else f'first: {first}, after: "{after}"'
    query_params = f'query: "product_type:{type}"' if search == '' else f'query: "product_type:{type}, title:{search}*"'

    result = shopify.GraphQL().execute(query % f'{pagination}, {query_params}')
    data = json.loads(result)
    pagination = None
    products = []

    if 'data' in data and 'products' in data['data']:
        if 'pageInfo' in data['data']['products']:
            pagination = data['data']['products']['pageInfo']

        if 'edges' in data['data']['products'] and len(data['data']['products']['edges']):
            for item in data['data']['products']['edges']:
                if 'node' in item:
                    products.append({
                        "cursor": item['cursor'],
                        "id": item['node']['id'],
                        "title": item['node']['title'],
                        "featured_image": item['node']['featuredImage']['originalSrc'] if item['node'][
                                                                                              'featuredImage'] is not None and 'originalSrc' in
                                                                                          item['node'][
                                                                                              'featuredImage'] else None,
                        "thumbnail": item['node']['featuredImage']['transformedSrc'] if item['node'][
                                                                                            'featuredImage'] is not None and 'transformedSrc' in
                                                                                        item['node'][
                                                                                            'featuredImage'] else None,
                    })

    return {
        'pagination': pagination,
        'products': products
    }


def get_orders(limit, after=None, status=''):
    if after:
        query = '{ orders(first:%LIMIT%, after: %AFTER%, query:"financial_status:AUTHORIZED") { edges { node { id displayFinancialStatus } } }}'
    else:
        query = '{ orders(first: %LIMIT%) {    edges { cursor node { id   }    }  }}'
    query = query.replace('%LIMIT%', str(limit))

    if after:
        query = query.replace('%AFTER%', after)

    result = shopify.GraphQL().execute(query)
    print(result)
    return json.loads(result)


def get_order_by_id(order_id):
    query = '{ order ( id: "%NODE_ID%" ) { name id } }'
    query = query.replace('%NODE_ID%', str(order_id))
    result = shopify.GraphQL().execute(query)

    return json.loads(result)

def get_orders_rest_api():
    pass
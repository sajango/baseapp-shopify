from django.db import models


# Create your models here.

class ShopifyStore(models.Model):
    shop_url = models.CharField(max_length=255, null=False, blank=False)
    access_token = models.CharField(max_length=2048, null=False, blank=False)

    class Meta:
        db_table = 'tbl_shopify_store'

from django.db import models

# Create your models here.


class LineItem(models.Model):
    line_item_id = models.BigIntegerField(null=True, blank=True)
    order_id = models.BigIntegerField(null=True, blank=True)
    customer_id = models.BigIntegerField(null=True, blank=True)
    variant_id = models.BigIntegerField(null=True, blank=True)
    product_id = models.BigIntegerField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(null=True, blank=True)
    properties = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)

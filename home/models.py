from django.db import models


# Create your models here.


class Order(models.Model):
    order_id = models.BigIntegerField(null=True, blank=True)
    order_number = models.PositiveSmallIntegerField(null=True, blank=True)
    customer_id = models.BigIntegerField(null=True, blank=True)
    customer_first_name = models.CharField(max_length=255, null=True, blank=True)
    customer_last_name = models.CharField(max_length=255, null=True, blank=True)
    created = models.CharField(max_length=255, null=True, blank=True)


class LineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='line_items', null=True, blank=True)
    line_item_id = models.BigIntegerField(null=True, blank=True)
    variant_id = models.BigIntegerField(null=True, blank=True)
    variant_title = models.CharField(max_length=255, null=True, blank=True)
    product_id = models.BigIntegerField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    images = models.CharField(max_length=255, null=True, blank=True)
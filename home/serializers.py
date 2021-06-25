import shopify

from rest_framework import serializers

from home.models import Order, LineItem


class LineItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = LineItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    line_items = LineItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_id', 'order_number', 'customer_id', 'customer_first_name', 'customer_last_name', 'line_items']

from rest_framework import serializers

from home.models import Order, LineItem


class LineItemSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = LineItem
        fields = '__all__'

    def get_created(self, instance):
        created = instance.order.created
        date = created.split('T')[0]
        return date.replace('-', '/')

    def get_status(self, instance):
        data = {
            'try-on': '未発送',
            'try-on-shiped': '試着中',
            'will-be-returned': '返品予定',
            'purchased': '購入済み',
            'returned': '返却済み',
        }
        return data.get(instance.status, 'try-on')


class OrderSerializer(serializers.ModelSerializer):
    line_items = LineItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_id', 'order_number', 'customer_id', 'customer_first_name', 'customer_last_name', 'line_items']

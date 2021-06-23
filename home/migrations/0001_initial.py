# Generated by Django 3.2 on 2021-06-23 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.BigIntegerField(blank=True, null=True)),
                ('customer_id', models.BigIntegerField(blank=True, null=True)),
                ('variant_id', models.BigIntegerField(blank=True, null=True)),
                ('product_id', models.BigIntegerField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('properties', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]

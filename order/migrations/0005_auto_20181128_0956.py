# Generated by Django 2.1.3 on 2018-11-28 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20181128_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordineinattesa',
            name='menues',
            field=models.ManyToManyField(blank=True, through='order.RichiedeM', to='localManagement.Menu'),
        ),
        migrations.AlterField(
            model_name='ordineinattesa',
            name='prodotti',
            field=models.ManyToManyField(blank=True, through='order.RichiedeP', to='localManagement.Prodotto'),
        ),
    ]

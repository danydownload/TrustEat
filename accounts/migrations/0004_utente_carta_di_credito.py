# Generated by Django 2.1.3 on 2018-11-22 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20181119_1426'),
        ('accounts', '0003_auto_20181119_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='utente',
            name='carta_di_credito',
            field=models.ManyToManyField(blank=True, null=True, related_name='carta_di_credito', to='user.CartaDiCredito'),
        ),
    ]

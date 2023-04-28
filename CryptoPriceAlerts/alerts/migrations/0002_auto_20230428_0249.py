# Generated by Django 3.2.16 on 2023-04-28 02:49

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alerts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='alert_price',
            field=models.DecimalField(decimal_places=10, help_text='The price that crypto currency must reach to trigger a price alert email to the user', max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='alert',
            name='alert_status',
            field=models.CharField(choices=[('created', 'Created'), ('triggered', 'Triggered'), ('deleted', 'Deleted')], default='created', help_text='Current status of this alert', max_length=32),
        ),
        migrations.AlterField(
            model_name='alert',
            name='coin_id',
            field=models.CharField(choices=[('btc', 'Bitcoin'), ('eth', 'Ethereum'), ('usdt', 'Tether'), ('bnb', 'Binancecoin'), ('xrp', 'Ripple'), ('ada', 'Cardano'), ('doge', 'Dogecoin')], help_text='An identifier for the coin. The value shown to the user would be common names but DB will store ticker symbol that is unique to each cryptocurrencyMore Info: https://coinmarketcap.com/alexandria/glossary/ticker-symbol', max_length=64),
        ),
        migrations.AlterField(
            model_name='alert',
            name='triggered_time',
            field=models.DateTimeField(blank=True, help_text='The time at which the alert email was triggered if triggered already', null=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='user',
            field=models.ForeignKey(help_text='User who set this alert', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
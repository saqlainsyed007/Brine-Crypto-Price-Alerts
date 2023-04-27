from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Alert(models.Model):

    class Coin:
        BITCOIN = "btc"
        ETHEREUM = "eth"
        TETHER = "usdt"
        BINANCECOIN = "bnb"
        RIPPLE = "xrp"
        CARDANO = "ada"
        DOGECOIN = "doge"

        CHOICES = (
            (BITCOIN, "Bitcoin"),
            (ETHEREUM, "Ethereum"),
            (TETHER, "Tether"),
            (BINANCECOIN, "Binancecoin"),
            (RIPPLE, "Ripple"),
            (CARDANO, "Cardano"),
            (DOGECOIN, "Dogecoin"),
        )

    class AlertStatus:
        CREATED = "created"
        TRIGGERED = "triggered"
        DELETED = "deleted"

        CHOICES = (
            (CREATED, "Created"),
            (TRIGGERED, "Triggered"),
            (DELETED, "Deleted"),
        )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    coin_id = models.CharField(
        max_length=64,
        choices=Coin.CHOICES,
    )
    alert_price = models.DecimalField(
        max_digits=20, decimal_places=10,
        validators=[MinValueValidator(Decimal(0.0))]
    )
    alert_status = models.CharField(
        max_length=32,
        choices=AlertStatus.CHOICES,
        default=AlertStatus.CREATED,
    )
    triggered_time = models.DateTimeField(
        blank=True, null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ("user", "coin_id", "alert_price",),
        )
        constraints = [
            models.CheckConstraint(
                check=models.Q(alert_price__gte=0),
                name="non_negative_alert_price_constraint",
            ),
        ]

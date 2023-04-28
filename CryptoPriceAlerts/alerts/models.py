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
        help_text="User who set this alert",
    )
    coin_id = models.CharField(
        max_length=64,
        choices=Coin.CHOICES,
        help_text=(
            "An identifier for the coin. The value shown to the user would be common "
            "names but DB will store ticker symbol that is unique to each cryptocurrency"
            "More Info: https://coinmarketcap.com/alexandria/glossary/ticker-symbol"
        ),
    )
    alert_price = models.DecimalField(
        max_digits=20, decimal_places=10,
        validators=[MinValueValidator(Decimal(0.0))],
        help_text="The price that crypto currency must reach to trigger a price alert email to the user",
    )
    alert_status = models.CharField(
        max_length=32,
        choices=AlertStatus.CHOICES,
        default=AlertStatus.CREATED,
        help_text="Current status of this alert",
    )
    triggered_time = models.DateTimeField(
        blank=True, null=True,
        help_text="The time at which the alert email was triggered if triggered already",
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

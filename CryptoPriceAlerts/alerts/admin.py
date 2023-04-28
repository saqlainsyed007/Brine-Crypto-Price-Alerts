from django.contrib import admin

from alerts.models import Alert


class AlertAdmin(admin.ModelAdmin):
    model = Alert
    list_display = (
        "id", "user", "coin_id", "alert_price", "alert_status",
        "triggered_time", "created", "updated",
    )
    search_fields = (
        "coin_id", "user__username", "alert_price",
    )
    list_filter = (
        "coin_id", "alert_status",
    )
    readonly_fields = ("created", "updated", )

    class Meta:
        ordering = ('-created',)


admin.site.register(Alert, AlertAdmin)

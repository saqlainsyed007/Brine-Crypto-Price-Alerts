from rest_framework import serializers

from alerts.models import Alert


class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = [
            "alert_status", "triggered_time", "created", "updated",
        ]

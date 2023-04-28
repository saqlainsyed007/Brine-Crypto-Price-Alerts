import logging

from django.core.cache import cache
from django.http import Http404

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView, RetrieveDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from alerts.models import Alert
from alerts.serializers import AlertSerializer

logger = logging.getLogger(__name__)


class AlertListCreateAPIView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AlertSerializer
    cache_key_template = "alerts_user_{user_id}_{alert_status}_{page_number}"

    def get_queryset(self):

        filter_params = {
            "user_id": self.request.user.id
        }

        alert_status = self.request.query_params.get("alert_status")
        if alert_status:
            filter_params["alert_status"] = alert_status

        return Alert.objects.filter(**filter_params)

    def list(self, request, *args, **kwargs):
        page_number = self.request.query_params.get("page", 1)
        alert_status = self.request.query_params.get("alert_status")
        cache_key = self.cache_key_template.format(
            user_id=request.user.id, alert_status=alert_status, page_number=page_number
        )
        cached_alerts = cache.get(cache_key)
        if cached_alerts:
            logger.info(
                f"Alert List Cached Response. User: {request.user.username}, "
                f"Alert Status: {alert_status}, Page: {page_number}"
            )
            return Response(data=cached_alerts)
        response = super().list(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            logger.info(
                f"Setting cache for --> User: {request.user.username}, "
                f"Alert Status: {alert_status}, Page: {page_number}"
            )
            cache.set(cache_key, response.data)
        return response

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        response = super().post(request, *args, **kwargs)
        return response


class AlertRetrieveDestroyAPIView(RetrieveDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AlertSerializer

    def get_queryset(self):
        return Alert.objects.filter(
            user_id=self.request.user.id
        )

    def destroy(self, *args, **kwargs):
        alert = self.get_object()
        if alert.alert_status == Alert.AlertStatus.DELETED:
            logger.error(
                f"Trying to delete a deleted alert. User: {self.request.user.id}, Alert: {alert.id}"
            )
            raise Http404
        alert.alert_status = Alert.AlertStatus.DELETED
        alert.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

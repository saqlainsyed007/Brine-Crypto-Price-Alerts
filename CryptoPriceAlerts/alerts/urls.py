from django.urls import path

from alerts.views import (
    AlertListCreateAPIView, AlertRetrieveDestroyAPIView,
)


urlpatterns = [
    path('', AlertListCreateAPIView.as_view(), name="list_alerts"),
    path('<int:pk>', AlertRetrieveDestroyAPIView.as_view(), name="retrieve_alert"),
]

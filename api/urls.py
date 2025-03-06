from django.urls import path
from .views import PlacementStatisticsView

urlpatterns = [
    path("statistics", PlacementStatisticsView.as_view(), name="placement_statistics"),
]

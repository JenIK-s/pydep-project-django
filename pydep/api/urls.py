from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "api"

router_1 = DefaultRouter()

urlpatterns = [
    path('', include(router_1.urls)),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CourseViewSet, ModuleViewSet, LessonViewSet

app_name = "api"

router_1 = DefaultRouter()
router_1.register("users", UserViewSet)
router_1.register("courses", CourseViewSet)
router_1.register("modules", ModuleViewSet)
router_1.register("lessons", LessonViewSet)

urlpatterns = [
    path('', include(router_1.urls)),
]

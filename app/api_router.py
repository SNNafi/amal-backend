from rest_framework.routers import DefaultRouter

from app.amal.api.views import AyahGroupViewSet, AyahViewSet

router = DefaultRouter()

app_name = "api/v1"

router.register(r'ayah-group', AyahGroupViewSet, basename='ayah-group')
router.register(r'ayah', AyahViewSet, basename='ayah')

urlpatterns = [
    *router.urls,
]

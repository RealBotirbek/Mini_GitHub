from rest_framework.routers import DefaultRouter
from projects.views.project import ProjectViewSet

router = DefaultRouter()

router.register("", ProjectViewSet, basename="project")

urlpatterns = router.urls
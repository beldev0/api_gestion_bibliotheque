from rest_framework.routers import DefaultRouter
from .views import AuthorViewset

router = DefaultRouter()
router.register('authors', AuthorViewset)

urlpatterns = router.urls
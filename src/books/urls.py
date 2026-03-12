from rest_framework.routers import DefaultRouter
from .views import BookViewset

router = DefaultRouter()
router.register('books', BookViewset)

urlpatterns = router.urls

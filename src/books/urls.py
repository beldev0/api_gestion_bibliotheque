from rest_framework.routers import DefaultRouter
from .views import BookViewset, CopiesViewset

router = DefaultRouter()
router.register('books', BookViewset)

urlpatterns = router.urls

router2  = DefaultRouter()
router2.register('copies', CopiesViewset)

urlpatterns += router2.urls
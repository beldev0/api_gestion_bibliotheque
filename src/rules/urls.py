from rest_framework.routers import DefaultRouter
from .views import SubscriptionRulesViewSet

router = DefaultRouter()
router.register('subscriptionPlan', SubscriptionRulesViewSet)

urlpatterns = router.urls
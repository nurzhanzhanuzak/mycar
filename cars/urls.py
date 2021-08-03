from rest_framework.routers import SimpleRouter
from cars import views


router = SimpleRouter()

router.register(r'cars', views.CarViewSet, 'Cars')

urlpatterns = router.urls

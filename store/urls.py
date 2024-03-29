from rest_framework.routers import DefaultRouter

from . import views

route = DefaultRouter()
route.register('customers', views.CustomerViewSet)
route.register('collections', views.CollectionViewSet)
route.register('products', views.ProductViewSet)
route.register('promotions', views.PromotionViewSet)

urlpatterns = route.urls
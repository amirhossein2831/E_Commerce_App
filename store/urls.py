from rest_framework_nested import routers

from . import views

route = routers.DefaultRouter()
route.register('customers', views.CustomerViewSet)
route.register('collections', views.CollectionViewSet)
route.register('products', views.ProductViewSet)
route.register('promotions', views.PromotionViewSet)

promotions_router = routers.NestedDefaultRouter(route, 'products', lookup='products')
promotions_router.register('promotions', views.ProductPromotionViewSet, basename='promotions')

urlpatterns = route.urls + promotions_router.urls
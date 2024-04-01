from rest_framework_nested import routers

from . import views

route = routers.DefaultRouter()
route.register('customers', views.CustomerViewSet)
route.register('collections', views.CollectionViewSet)
route.register('products', views.ProductViewSet)
route.register('promotions', views.PromotionViewSet)
route.register('carts', views.CartViewSet)
route.register('orders', views.OrderViewSet)
route.register('customers/me/addresses', views.LoginCustomerAddressViewSet)

promotions_router = routers.NestedDefaultRouter(route, 'products', lookup='products')
promotions_router.register('promotions', views.ProductPromotionViewSet, basename='promotions')

reviews_router = routers.NestedDefaultRouter(route, 'products', lookup='products')
reviews_router.register('reviews', views.ProductReviewViewSet, basename='reviews')

addresses_router = routers.NestedDefaultRouter(route, 'customers', lookup='customers')
addresses_router.register('addresses', views.CustomerAddressViewSet, basename='addresses')

cart_items_router = routers.NestedDefaultRouter(route, 'carts', lookup='carts')
cart_items_router.register('items', views.CartItemViewSet, 'items')

product_image_router = routers.NestedDefaultRouter(route, 'products', lookup='products')
product_image_router.register('images', views.ProductImageViewSet, basename='images')

urlpatterns = (
        route.urls +
        promotions_router.urls +
        reviews_router.urls +
        addresses_router.urls +
        cart_items_router.urls +
        product_image_router.urls
)

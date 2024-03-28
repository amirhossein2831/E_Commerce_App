from rest_framework.routers import DefaultRouter

from . import views

route = DefaultRouter()
route.register('customers', views.CustomerViewSet)

urlpatterns = route.urls
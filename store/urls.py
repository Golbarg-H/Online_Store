from pprint import pprint

from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_nested import routers

admin.site.site_header = 'Store Admin'
admin.site.index_title = 'Welcome to my store!'

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'collections', views.CollectionViewSet, basename='collection')
router.register(r'carts', views.ShoppingCartViewSet, basename='cart')
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'orders', views.OrderViewSet, basename='order')

products_router = routers.NestedDefaultRouter(router, r'products', lookup='product')
products_router.register(r'reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, r'carts', lookup='cart')
carts_router.register(r'items', views.CartItemViewSet, basename='cart-items')

urlpatterns = [
    # path('cart/', views.ShoppingCartView.as_view()),
    # path('cart/<uuid:pk>', views.CartItemView.as_view(), title='cart-detail'),
    # path('cart/<int:pk>', views.CartItemView.as_view(), name='cart-detail'),
]
urlpatterns += router.urls + products_router.urls + carts_router.urls

# path('product/', views.ProductView.as_view()),
# path('collection/', views.CollectionView.as_view()),

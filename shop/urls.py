from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # ------------------------
    # General pages
    # ------------------------
    path('', views.home, name='home'),

    # ------------------------
    # Authentication
    # ------------------------
    path('register/seller/', views.register_seller, name='register_seller'),
    path('register/buyer/', views.register_buyer, name='register_buyer'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),

    # ------------------------
    # Seller
    # ------------------------
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/product/add/', views.product_add, name='product_add'),

    # ------------------------
    # Product browsing
    # ------------------------
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # ------------------------
    # Cart & Checkout
    # ------------------------
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('checkout/', views.checkout, name='checkout'),

    # ------------------------
    # AI Recommendation & Feedback APIs
    # ------------------------
    path('api/recommendations/', views.api_recommendations, name='api_recommendations'),
    path('api/feedback/', views.api_feedback, name='api_feedback'),
]

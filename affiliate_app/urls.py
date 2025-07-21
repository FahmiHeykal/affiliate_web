from django.urls import path
from .views import (
    public_home, public_product_detail, public_category, public_category_list,
    DashboardLoginView, DashboardLogoutView, dashboard_home, 
    ProductListView, dashboard_product_create, dashboard_product_update, 
    dashboard_product_delete, dashboard_product_toggle_active,
    CategoryListView, dashboard_category_create, dashboard_category_update,
    dashboard_category_delete, dashboard_category_toggle_active,
)

urlpatterns = [
    # Public URLs
    path('', public_home, name='public_home'),
    path('product/<slug:slug>/', public_product_detail, name='public_product_detail'),
    path('category/<slug:slug>/', public_category, name='public_category'),
    path('categories/', public_category_list, name='public_category_list'),
    
    # Dashboard Auth URLs
    path('dashboard/login/', DashboardLoginView.as_view(), name='dashboard_login'),
    path('dashboard/logout/', DashboardLogoutView.as_view(), name='dashboard_logout'),
    
    # Dashboard URLs
    path('dashboard/', dashboard_home, name='dashboard_home'),
    
    # Product URLs
    path('dashboard/products/', ProductListView.as_view(), name='dashboard_product_list'),
    path('dashboard/products/create/', dashboard_product_create, name='dashboard_product_create'),
    path('dashboard/products/update/<int:pk>/', dashboard_product_update, name='dashboard_product_update'),
    path('dashboard/products/delete/<int:pk>/', dashboard_product_delete, name='dashboard_product_delete'),
    path('dashboard/products/toggle-active/<int:pk>/', dashboard_product_toggle_active, name='dashboard_product_toggle_active'),
    
    # Category URLs
    path('dashboard/categories/', CategoryListView.as_view(), name='dashboard_category_list'),
    path('dashboard/categories/create/', dashboard_category_create, name='dashboard_category_create'),
    path('dashboard/categories/update/<int:pk>/', dashboard_category_update, name='dashboard_category_update'),
    path('dashboard/categories/delete/<int:pk>/', dashboard_category_delete, name='dashboard_category_delete'),
    path('dashboard/categories/toggle-active/<int:pk>/', dashboard_category_toggle_active, name='dashboard_category_toggle_active'),
]
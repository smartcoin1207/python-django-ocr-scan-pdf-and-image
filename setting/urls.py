from django.urls import path
from . import views

app_name = 'setting'

urlpatterns = [
    path('clients/<slug:id>/', views.create_or_get_clients, name='create-or-get-clients'),
    path('client/<slug:id>/', views.manage_client, name='manage-client'),
    path('account-items/<slug:id>/', views.create_or_get_acount_items, name='create-or-get-account-items'),
    path('account-item/<slug:id>/', views.manage_account_item, name='manage-account-item'),
    path('keywords/<slug:id>/', views.create_or_get_keywords, name='create-or-get-keywords'),
    path('keyword/<slug:id>/', views.manage_keyword, name='manage-keyword'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_func, name="login" ),
    path('ad_dash', views.ad_dashboard, name='ad_dash'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('add_customer', views.add_customer, name="add_customer"),
    path('customers', views.customers, name="customers"),
    path('create_account/<int:id>', views.add_bank, name='create_account'),
    path('view_accounts/<int:id>', views.view_bank, name='view_accounts'),
    path('create_card/<int:id>', views.add_card, name='create_card'),
    path('view_cards/<int:id>', views.view_cards, name='view_cards'),

]

"""eco_retail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from eco_retail_app import views
from rest_framework.authtoken import views as authviews

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/process-products/', views.process_products),
    path('api/add-product/', views.add_product),
    path('api/get-tokens/', views.get_tokens),
    path('api/opt-in-asset-get-txn/', views.OptInAssetGetTxn.as_view()),
    path('api/opt-in-contract-get-txn/', views.OptInContractGetTxn.as_view()),
    path('api/opt-in-send-txn/', views.OptInSendTxn.as_view()),
    path('api/auth/register/', views.AuthRegister.as_view()),
    path('api/auth/login/', authviews.obtain_auth_token),
    path('api/auth/logout/', views.AuthLogout.as_view()),
    path('api/auth/me/', views.AuthMe.as_view()),
    path('api/get-account-balance/', views.GetAccountBalance.as_view()),
]

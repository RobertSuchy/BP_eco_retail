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

urlpatterns = [
    # registration process with opt-in EcoRetail Coin and smart contract
    path('api/opt-in-asset-get-txn/', views.OptInAssetGetTxn.as_view()),
    path('api/opt-in-contract-get-txn/', views.OptInContractGetTxn.as_view()),
    path('api/opt-in-send-txn/', views.OptInSendTxn.as_view()),
    path('api/auth/register/', views.AuthRegister.as_view()),

    # login, logout
    path('api/auth/login/', views.AuthGetToken.as_view()),
    path('api/auth/logout/', views.AuthLogout.as_view()),

    # authentication on reload with loading necessary data
    path('api/auth/me/', views.AuthMe.as_view()),
    path('api/get-account-balance/', views.GetAccountBalance.as_view()),
    path('api/get-customers/', views.GetCustomers.as_view()),
    
    # 
    path('api/update-rewards-policy/', views.UpdateRewardsPolicy.as_view()),
    path('api/buy-eco-coins-get-txn/', views.BuyEcoCoinsGetTxn.as_view()),
    path('api/add-product/', views.AddProduct.as_view()),
    path('api/get-all-products/', views.GetAllProducts.as_view()),
    path('api/process-purchase/', views.ProcessPurchase.as_view()),
    path('api/send-txn/', views.SendTxn.as_view()),
]

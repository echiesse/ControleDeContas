from django.urls import path, include

from .views import *


urlpatterns = [
    path('bill-types/', ListCreateBillTypes.as_view()),

    path('bills/', ListBills.as_view()),
    path('bills/create/', CreateBills.as_view()),
    path('bill/<int:pk>/', RetrieveUpdateDestroyBills.as_view()),
]


from django.urls import path
from borrow.views import BorrowView
urlpatterns = [
    path('borrow/<int:pk>/', BorrowView.as_view(), name = 'borrow'),
]

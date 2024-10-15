from django.urls import path
from .views import DepositView,RatingView, BookDetailView
urlpatterns = [
    path('deposit/', DepositView.as_view(), name = 'deposit'),
    path('rating/<int:pk>/', RatingView.as_view(), name = 'rating'),
    path('details/<int:pk>/', BookDetailView.as_view(), name = 'details'),
]

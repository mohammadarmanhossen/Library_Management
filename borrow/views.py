from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .models import Book, Borrow
from django.contrib import messages
from accounts.models import UserAccountModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

class BorrowView(LoginRequiredMixin, CreateView):
    model = Book
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs.get('pk'))
        account = get_object_or_404(UserAccountModel, user=request.user)
        
        if book.available_copies <= 0:
            messages.error(request, 'No available copies for this book')
            return render(request, 'books.html', {'books': Book.objects.all()})
        
        if account.balance < book.borrowing_price:
            messages.error(request, 'Insufficient balance')
            return render(request, 'books.html', {'books': Book.objects.all()})
        
        account.balance -= book.borrowing_price
        account.save()
        
        book.available_copies -= 1
        book.save()
        
        borrow, created = Borrow.objects.get_or_create(user=request.user, book=book)
        if not created:
            borrow.borrow_count += 1
            borrow.borrowing_date = timezone.now() 
            borrow.save()
        
        
        
        messages.success(request, f'You have successfully borrowed {book.title}')
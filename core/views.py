from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from .forms import DepositForm, RatingForm
from .models import Deposit, Book,RatingModel
from django.contrib import messages
from accounts.models import UserAccountModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.utils import timezone

class DepositView(LoginRequiredMixin, CreateView):
    model = Deposit
    form_class = DepositForm
    template_name = 'deposit.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = UserAccountModel.objects.get(user=self.request.user)
        account.balance += amount
        account.save()

        # Create Deposit instance with the associated account
        deposit = form.save(commit=False)
        deposit.account = account
        deposit.save()

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )



class RatingView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = RatingForm
    template_name = 'rate.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        rating = form.cleaned_data.get('rate')
        book = Book.objects.get(pk=self.kwargs.get('pk'))
        rating_obj, created = RatingModel.objects.update_or_create(user = self.request.user, book=book, defaults={'rate': rating})
        self.object = form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
    
class BookDetailView(DetailView):
    model = Book
    template_name = 'book_details.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['rating'] = RatingModel.objects.filter(book=book)
        return context

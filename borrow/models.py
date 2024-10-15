
from core.models import Book
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    borrow_count = models.IntegerField(default=1)
    borrowing_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"

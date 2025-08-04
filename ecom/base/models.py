from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User


# User Profile for Email Verification
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_token = models.CharField(max_length=100, blank=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Optional: Author model
class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Optional: Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Book model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    isbn = models.CharField(max_length=13)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

# Book Issue model
class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"Issue: {self.user.username} → {self.book.title}"


# Optional fallback model
# models.py

# models.py
class BookIssue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def _str_(self):
        return f"{self.book.title} issued to {self.user.username}"


class Return(models.Model):
    issue = models.OneToOneField(Issue, on_delete=models.CASCADE)
    return_date = models.DateTimeField(auto_now_add=True)

    def calculate_fine(self):
        if self.return_date.date() > self.issue.due_date.date():
            days_late = (self.return_date.date() - self.issue.due_date.date()).days
            return days_late * 10  # ₹10 per day late
        return 0




from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import (
    Book, Author, Category, Issue, Return, Profile, BookIssue
)
from .forms import CustomUserCreationForm, BookForm

# -------------------- AUTH + HOME ----------------------

def home(request):
    return render(request, 'base/home.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.get(user=user)

            # Send Activation Email
            subject = 'Activate Your Account'
            activation_link = f"http://127.0.0.1:8000/verify-email/?token={profile.email_token}"
            html_message = render_to_string('emails/activation_email.html', {
                'activation_link': activation_link
            })

            send_mail(
                subject=subject,
                message='',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                html_message=html_message,
            )

            messages.success(request, "Registration successful! Check your email to activate your account.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'base/signup.html', {'form': form})


def activation_email(request):
    try:
        email_token = request.GET.get('token')
        user_profile = Profile.objects.get(email_token=email_token)
        user_profile.is_email_verified = True
        user_profile.save()
        messages.success(request, 'Email Verified Successfully!')
        return redirect('login')
    except Exception:
        return HttpResponse('Invalid email token')

# -------------------- DASHBOARD ----------------------

@login_required
def dashboard_view(request):
    context = {
        'books_count': Book.objects.count(),
        'issues_count': Issue.objects.count(),
        'returns_count': Return.objects.count(),
        'users_count': User.objects.count(),
        'authors_count': Author.objects.count(),
        'categories_count': Category.objects.count(),
    }
    return render(request, 'base/dashboard.html', context)

# -------------------- BOOK CRUD ----------------------

@login_required
def add_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            author_name = request.POST.get('author')
            category_name = request.POST.get('category')

            author, _ = Author.objects.get_or_create(name=author_name)
            category = None
            if category_name:
                category, _ = Category.objects.get_or_create(name=category_name)

            Book.objects.create(
                title=title,
                description=description,
                author=author,
                category=category
            )

            messages.success(request, "Book added successfully!")
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'base/add_book.html', {'form': form})


@login_required
def edit_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'base/edit_book.html', {'form': form})


@login_required
def delete_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, "Book deleted successfully!")
        return redirect('book_list')
    return render(request, 'base/delete_book.html', {'book': book})


@login_required
def book_list_view(request):
    books = Book.objects.all()
    return render(request, 'base/book_list.html', {'books': books})

# -------------------- ISSUE & RETURN ----------------------

@login_required
def issue_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    users = User.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user')
        selected_user = get_object_or_404(User, id=user_id)

        already_issued = Issue.objects.filter(user=selected_user, book=book).exists()
        if already_issued:
            messages.warning(request, f"{selected_user.username} has already issued this book.")
        else:
            Issue.objects.create(user=selected_user, book=book, due_date=timezone.now() + timedelta(days=7))
            messages.success(request, f"Book issued to {selected_user.username} successfully!")
        return redirect('book_list')

    return render(request, 'base/issue_book_form.html', {'book': book, 'users': users})


@login_required
def issued_books_view(request):
    issued_books = Issue.objects.select_related('book', 'user')
    returns = {r.issue.id: r.return_date for r in Return.objects.all()}
    return render(request, 'base/issued_books.html', {'issued_books': issued_books, 'returns': returns})


@login_required
def return_book(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

    if Return.objects.filter(issue=issue).exists():
        messages.warning(request, "Book already returned.")
    else:
        Return.objects.create(issue=issue)
        messages.success(request, "Book returned successfully!")

    return redirect('issued_books')

# -------------------- NEW: VIEW RETURNED BOOKS ----------------------

from django.shortcuts import render
from .models import Return

def returned_books_view(request):
    returned_issues = Return.objects.select_related('issue__book', 'issue__user')
    return render(request, 'base/returned_books.html', {'returned_issues': returned_issues})
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def registered_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'base/registered_users.html', {'users': users})
from .models import Author
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def authors_listed(request):
    authors = Author.objects.all()
    return render(request, 'base/authors_listed.html', {'authors': authors})
from .models import Category  # Assuming your model is Category

@login_required
def listed_categories(request):
    categories = Category.objects.all()
    return render(request, 'base/listed_categories.html', {'categories': categories})


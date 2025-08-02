from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Book, Author, Category, Issue, Return, Profile
from .forms import CustomUserCreationForm, BookForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, BookIssue
from django.contrib.auth.decorators import login_required

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
    except Exception as e:
        return HttpResponse('Invalid email token')


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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, BookIssue

# View to issue a book to the currently logged-in user
@login_required
def issue_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        already_issued = BookIssue.objects.filter(user=request.user, book=book).exists()
        if already_issued:
            messages.warning(request, "You've already issued this book.")
        else:
            BookIssue.objects.create(user=request.user, book=book)
            messages.success(request, "Book issued successfully!")
        return redirect('book_list')

    return HttpResponse("Invalid request method", status=405)


# View to list all issued books
from .models import BookIssue

@login_required
def issued_books_view(request):
    issued_books = BookIssue.objects.select_related('book', 'user').all()
    return render(request, 'base/issued_books.html', {'issued_books': issued_books})
from django.contrib import admin
from django.urls import path
from base import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('verify-email/', views.activation_email, name='verify_email'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('books/', views.book_list_view, name='book_list'),
    path('books/add/', views.add_book_view, name='add_book'),
    path('books/edit/<int:pk>/', views.edit_book_view, name='edit_book'),
    path('books/delete/<int:pk>/', views.delete_book_view, name='delete_book'),
    path('issue-book/<int:pk>/', views.issue_book, name='issue_book'),
    path('issued-books/', views.issued_books_view, name='issued_books'),
]

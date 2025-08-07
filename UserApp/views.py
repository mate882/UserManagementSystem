from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import User, Article
from .forms import UserCreationForm, ArticleForm, UserEditForm

def is_admin(user):
    return user.role == 'admin'

def is_moderator_or_admin(user):
    return user.role in ['admin', 'moderator']

def is_writer_or_above(user):
    return user.role in ['admin', 'moderator', 'writer']

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    articles = Article.objects.all()
    if request.user.role == 'writer':
        articles = Article.objects.filter(author=request.user)
    return render(request, 'dashboard.html', {'articles': articles})

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    users = User.objects.all()
    return render(request, 'admin_panel.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('manage_users')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'edit_user.html', {'form': form, 'user': user})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        user.delete()
        messages.success(request, 'User deleted successfully!')
    return redirect('manage_users')

@login_required
@user_passes_test(is_writer_or_above)
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Article created successfully!')
            return redirect('dashboard')
    else:
        form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})

@login_required
@user_passes_test(is_writer_or_above)
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.user.role == 'writer' and article.author != request.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect('dashboard')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit_article.html', {'form': form, 'article': article})

@login_required
@user_passes_test(is_moderator_or_admin)
def moderate_articles(request):
    articles = Article.objects.all()
    return render(request, 'moderate_articles.html', {'articles': articles})

@login_required
@user_passes_test(is_moderator_or_admin)
def toggle_article_status(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.is_published = not article.is_published
    article.save()
    status = 'published' if article.is_published else 'unpublished'
    messages.success(request, f'Article {status} successfully!')
    return redirect('moderate_articles')

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if not article.is_published and request.user.role not in ['admin', 'moderator']:
        return HttpResponseForbidden()
    return render(request, 'article_detail.html', {'article': article})


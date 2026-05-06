from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Article

@login_required
def advice_list(request):
    advices = Article.objects.filter(category='advice')
    exercises = Article.objects.filter(category='exercise')
    return render(request, 'advice/advice_list.html', {
        'advices': advices,
        'exercises': exercises
    })

@login_required
def favorite_list(request):
    favorites = request.user.favorite_articles.all()
    return render(request, 'advice/favorites.html', {
        'favorites': favorites
    })

@login_required
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    is_fav = article.favorites.filter(id=request.user.id).exists()
    return render(request, 'advice/article_detail.html', {
        'article': article,
        'is_fav': is_fav
    })


@login_required
def toggle_favorite(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.favorites.filter(id=request.user.id).exists():
        article.favorites.remove(request.user)
    else:
        article.favorites.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'advice_list'))
from django.shortcuts import render, get_object_or_404
from .models import Article

def advice_list(request):
    advices = Article.objects.filter(category='advice')
    exercises = Article.objects.filter(category='exercise')
    return render(request, 'advice/advice_list.html', {
        'advices': advices,
        'exercises': exercises
    })
def favorite_list(request):
    favorites = Article.objects.filter(is_favorite=True)
    return render(request, 'advice/favorites.html', {
        'favorites': favorites
    })

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'advice/article_detail.html', {
        'article': article
    })
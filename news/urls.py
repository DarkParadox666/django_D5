from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetails, NewsCreate, NewsUpdate, ArticleCreate, ArticleUpdate, subscriptions


urlpatterns = [
   path('', PostsList.as_view(), name='posts_list'),
   path('<int:pk>', PostDetails.as_view(), name='post'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('article/create/', ArticleCreate.as_view(), name='article_create'),
   path('article/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]

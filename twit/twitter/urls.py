from django.urls import path
from .views import TweetListView, TweetDetailView, TweetCreateView, TweetUpdateView, TweetDeleteView
from . import views

app_name = 'twitter'
urlpatterns = [
    path('', TweetListView.as_view(), name='twitter_home'),
    path('<int:pk>/', TweetDetailView.as_view(), name='detail'),
    path('create/', TweetCreateView.as_view(), name="create"),
    path('<int:pk>/update/', TweetUpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', TweetDeleteView.as_view(), name="delete"),
]

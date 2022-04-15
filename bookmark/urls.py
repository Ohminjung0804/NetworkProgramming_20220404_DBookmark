from django.urls import path

<<<<<<< HEAD
from bookmark.views import BookmarkListView, BookmarkCreateView

app_name = 'bookmark'

urlpatterns = [
    path('list/', BookmarkListView.as_view(), name='list') , #bookmark:list
    path('add/', BookmarkCreateView.as_view(), name='Add')  #bookmark:list
=======
from bookmark.views import BookmarkListView

app_name = 'bookmark'
urlpatterns = [
    path('list/', BookmarkListView.as_view(), name='list') #bookmark:list
>>>>>>> origin/master
]
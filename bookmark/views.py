from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from accounts.models import Profile
from bookmark.models import Bookmark


class BookmarkListView(LoginRequiredMixin,ListView):
    model = Bookmark
    #bookmark_list.html, {'bookmark_list': Bookmark.objects.all()}

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            profile = Profile.objects.get(user = user)
            bookmark_list = Bookmark.objects.filter(profile=profile)
        else:
            bookmark_list = Bookmark.objects.none()
        return bookmark_list
class BookmarkCreateView(LoginRequiredMixin, CreateView):
    model = Bookmark
    fields = ['prifuke','name', 'url']    #'__all__'
    template_name_suffix = '_create'    #bookmark_form.html -> bookmark_create.html
    success_url = reverse_lazy('bookmark:list')

    def get_initial(self):
        user = self.request.user
        profile = Profile.objects.get(user = user)
        return{'profile':profile}

class BookmarkDetailView(DetailView):
    model = Bookmark

class BookmarkUpdateView(LoginRequiredMixin,UpdateView):
    model = Bookmark
    fields = ['name','url']     #'__all__'
    template_name_suffix = '_update'      #bookmark_update.html
    # success_url = reverse_lazy('bookmark:list') # success_url없으면 model의 get_abolute_url() 호출


class BookmarkDeleteView(LoginRequiredMixin,DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark:list')

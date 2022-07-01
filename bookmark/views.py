from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from accounts.models import Profile
from bookmark.forms import BookmarkCreationForm
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

def list_bookmark(request):
    #로그인 사용자 확인하자
    user = request.user

    if user.is_authenticated:#로그인 되어있으면
        profile = Profile.objects.get(user=user)
        bookmark_list = Bookmark.objects.filter(profile=profile)#그 사용자의 북마크 가져오자
    else:#로그인 안되어 있으면
        bookmark_list = Bookmark.objects.none() #북맡크 없는 것 가져오자

    return render(request, 'bookmark/bookmark_list.html',{'bookmark_list': bookmark_list})


def detail_bookmark(request, pk):
    bookmark = Bookmark.objects.get(pk=pk)
    return render(request, 'bookmark/bookmark_detail.html',{'bookmark':bookmark})


def delete_bookmark(request, pk):
    if request.method == 'POST':
        bookmark = Bookmark.objects.get(pk=pk)
        bookmark.delete()
        return redirect('bookmark:list')

    else:
        bookmark = Bookmark.objects.get(pk=pk)
        return render(request, 'bookmark/bookmark_confirm_delete.html',{'bookmark':bookmark})


def create_bookmark(request):
    if request.method == 'POST': #사용자가 입력하고 버튼 눌렀을 때
        form = BookmarkCreationForm(request.POST)#form 가져오자
        if form.is_valid():#is_valid()
            new_bookmark = form.save(commit=False)#new_bookmark 생성하자(name, urls)
        new_bookmark.profile = Profile.objects.get#new_bookmark에 profile 추가하자
        #new_bookmark.save()

        return redirect('bookmark:list') #new_bookmark:list 이동하자
    else:   #빈 폼
        form = BookmarkCreationForm()
        return render(request, 'bookmark/bookmark_create.html',{'form':form})
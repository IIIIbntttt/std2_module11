import django
from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User

from blog.models import Video, Like
# Create your views here.
def index(request):
    videos = Video.objects.order_by('-created_datetime')[0:10]
    return render(request, "video/index.html", {"videos": videos})

def userVideos(request):
    videos = Video.objects.filter(created_by=request.user.id).all()
    return render(request, 'video/myvideos.html', {"videos": videos})

class UserCreationFormWithEmail(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {'username': UsernameField, "email": forms.EmailField}


class SignUpView(generic.CreateView):
    form_class = UserCreationFormWithEmail
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class VideoCreateView(generic.CreateView):
    model = Video
    fields = [
        'name',
        'describtion',
        'category',
        'videofile',
    ]
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

def get_likes(video_id):
    v = Video.objects.get(id=video_id)

    return {
        'likes': v.like_set.filter(value__gt=0).count(),
        'dislikes': v.like_set.filter(value__lt=0).count()
    }, v

def video(request, id):
    likes, v = get_likes(id)

    return render(request, 'video/video.html', {
        'video': v,
        'is_liked': v.like_set.filter(user_id=request.user.id, value=1).count() == 1,
        'is_disliked': v.like_set.filter(user_id=request.user.id, value=1).count() == 1,
    })

def set_like(request, id):
    like, _ =  Like.objects.get_or_create(video_id__id=id, user_id__id=request.user.id)
    like.user_id = request.user
    like.video_id = Video.objects.get(id=id)
    like.value = 1
    like.save()

    likes, _ = get_likes(id)
    return JsonResponse(likes)

def set_dislike(request, id):
    like, _ = Like.objects.get_or_create(video_id__id=id, user_id__id=request.user.id)
    like.user_id = request.user
    like.video_id = Video.objects.get(id=id)
    like.value = -1
    like.save()

    likes, _ = get_likes(id)
    return JsonResponse(likes)

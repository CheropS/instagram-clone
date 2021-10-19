from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import forms 
from django.contrib import messages
from datetime import datetime

from insta.models import Post, Comment, Like, Profile
from .forms import PostForm, CommentForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def welcome(request):
    posts = Post.objects.all().filter(created_date__lte = timezone.now()).order_by('-created_date')
    user = request.user

    context={ 'posts':posts, 'user':user }
    return render(request, 'all-insta/home.html', context)

# def add(request):
#     return render (request, 'all-insta/add.html')

def create_post(request):
    current_user = request.user
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid:
            post = form.save(commit= False)
            post.author = current_user
            post.save()
        return redirect('welcome')
    else:
        form = PostForm()
    return render(request,'all-insta/add.html',{'form':form})

def add_comment(request,pk):
    post = Post.objects.get(pk = pk)
    form = CommentForm(request.POST,instance=post)
    if request.method == "POST":
        if form.is_valid():
            name = request.user.username
            comment_body = form.cleaned_data['comment_body']
            sharry = Comment(post=post,name =name,comment_body =comment_body,date_added=datetime.now())

            sharry.save()
            return redirect('welcome')
        else:
            print('form is invalid')

    else:
        form = CommentForm

    context = {
        'form':form
    }
    return render(request,'all-insta/comment.html',context)

def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        phone_post = Post.objects.get(id= post_id)

        if user in phone_post.liked.all():
            phone_post.liked.remove(user)
        else:
            phone_post.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id = post_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()

    return redirect('welcome')

def profile(request):
    user = request.user
    user = Profile.objects.get_or_create(user= request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)                         
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated successfully!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user

    }

    return render(request, 'all-insta/profile.html', context)

def search_results(request):

    if 'author' in request.GET and request.GET["author"]:
        search_term = request.GET.get("author")
        searched_profiles = Post.search_by_author(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"searched_profiles": searched_profiles})

    else:
        message = "You haven't searched for any person"
        return render(request, 'search.html',{"message":message})
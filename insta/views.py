from django.shortcuts import render

from insta.models import Post

# Create your views here.
def welcome(request):
    photos=Post.objects.all()

    context={ 'photos':photos}
    return render(request, 'all-insta/home.html', context)

def add(request):
    return render (request, 'all-insta/add.html')
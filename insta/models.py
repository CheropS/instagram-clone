from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.user',on_delete=models.CASCADE,related_name='author')
    image = models.ImageField(blank = True,null=True)
    caption = models.TextField()
    created_date = models.DateTimeField(default= timezone.now)
    updated = models.DateTimeField(auto_now= True)
    liked = models.ManyToManyField(User, default=None,blank= True,related_name='liked')

    @property
    def num_likes(self):
        return self.liked.all().count
   
    @classmethod
    def search_by_title(cls,search_term):
        author = cls.objects.filter(author__icontains=search_term)
        return author
        
    def __str__(self):
        return f'{self.author.username}'

class Comment(models.Model):
    post = models.ForeignKey('Post',related_name='comments',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    comment_body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post.caption,self.name}'


LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,default='Like',max_length=10)

    def __str__(self):
        return str(self.post)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='profile_pics')
    
    def save_profile(self):
        self.save()

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
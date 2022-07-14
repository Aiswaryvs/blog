from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.

class UserProfile(models.Model):
    profile_picture=models.ImageField(upload_to="profilepics",null=True)
    bio=models.CharField(max_length=20)
    phone=models.CharField(max_length=15)
    date_of_birth=models.DateField(null=True)
    options=(
        ("male","male"),
        ("female","female"),
        ("other","other")
    )
    gender=models.CharField(max_length=15,choices=options,default="male")
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="users")
    following=models.ManyToManyField(User,related_name="followings",blank=True)

    @property
    def fetch_followings(self):
        return self.following.all()

    @property
    def fetch_following_count(self):
        return self.fetch_followings.count()

    @property
    def get_followers(self):
        all_users=UserProfile.object.all()
        followers_list=[]
        for user in all_users:
            if self.user in user.fetch_followings:
                followers_list.append(user)
                followers_count=len(followers_list)
                return followers_count

    @property
    def get_invitations(self):
        all_users = UserProfile.objects.all().exclude(user=self.user)# fetch all users except current or loged user
        following_list = [u for u in self.fetch_followings]  # exclude my following from all users
        invitations = [user for user in all_users if user not in following_list]
        return random.sample(invitations,1)

class Blogs(models.Model):
    title=models.CharField(max_length=150)
    description=models.CharField(max_length=250)
    image=models.ImageField(upload_to="blogimages",null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="author")
    posted_date=models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(User)

    @property
    def get_like_count(self):
        like_count=self.liked_by.all().count()
        return like_count
    @property
    def get_liked_users(self):
        liked_users=self.liked_by.all()
        users=[user.username for user in liked_users]
        return users

    def __str__(self):
        return self.title


class Comments(models.Model):
    blog=models.ForeignKey(Blogs,on_delete=models.CASCADE)
    comment=models.CharField(max_length=190)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


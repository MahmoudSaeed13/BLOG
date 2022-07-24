from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

 
# Create your models here.
class User(AbstractUser):
    blocked = models.BooleanField(_('Blocked'), default=False)
    image = models.ImageField(_("User image"), upload_to='user/images/', null=True)

    def __str__(self):
        return f'{self.username}'

    def serialize(self):
        return{
            'username': self.username, 
            'email':self.email
        }

class Category(models.Model):
    title = models.CharField(_("Category name"), max_length=50)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.title}"

    def serialize(self):
        return{
            'title' : self.title
        } 
    

class Post(models.Model):
    title = models.CharField(_("Post title"), max_length=150)
    body = models.TextField(_("Post content"))
    image = models.ImageField(_("Post Image"), upload_to="blog/images/", null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="Category_Posts")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creators")
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  


    def __str__(self):
        return f"{self.title}"



class Comments(models.Model):
    body = models.TextField(_("comment body"))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commented_posts")
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentors')
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.body}"



class Reply(models.Model):
    body = models.TextField(_("comment body"))
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='replies')
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repliers')
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.body}"


class CategorySubscription(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user} follows {self.category}"

class Likes(models.Model):
    action = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_liked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="posts_liked")    
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

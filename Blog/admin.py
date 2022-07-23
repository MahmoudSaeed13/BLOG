from django.contrib import admin
from Blog.models import Category, Likes, Reply, User, Post, Comments, CategorySubscription
# Register your models here.

# Register user model 
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name','email','is_superuser', 'blocked']

admin.site.register(User, UserAdmin)

# Register Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']

admin.site.register(Category, CategoryAdmin)

# Register Post model
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at', 'updated_at']

admin.site.register(Post, PostAdmin)

# Register comments model
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['body', 'commentor', 'post']

admin.site.register(Comments, CommentsAdmin)

# Register comments Reply model
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['body', 'commentor', 'comment']

admin.site.register(Reply, ReplyAdmin)

# Regsiter category subscriptoin model
class CategorySubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'created_at']

admin.site.register(CategorySubscription, CategorySubscriptionAdmin)


# Regsiter category subscriptoin model
class LikesAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'action']

admin.site.register(Likes, LikesAdmin)
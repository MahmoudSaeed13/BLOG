from django.urls import path
from Blog import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogOutView.as_view(), name='logout'),
    path('post/<id>/', views.DetailPostView.as_view(), name='detailed-post'),
    path('category/<id>/', views.DetailCategoryView.as_view(), name='detailed-category'),
    path('createpost', views.CreatePostView.as_view(), name='create-post'),
    path('createcategory', views.CreateCategoryView.as_view(), name='create-category'),
    path('post/comment/<id>', views.CommentAddView.as_view(), name='add-comment'),
    path('post/reply/<id>', views.ReplyAddView.as_view(), name='add-reply'),
    path('subscribe/<id>', views.SubscribeCategory.as_view(), name='subscribe'),
    path('unsubscribe/<id>', views.UnsubscribeCategory.as_view(), name='unsubscribe'),
    path('deletepost/<id>', views.DeletePostView.as_view(), name='delete-post'),
    path('deletecategory/<id>', views.DeleteCategoryView.as_view(), name='delete-category'),
    path('editpost/<id>', views.EditPOstView.as_view(), name='edit-post'),
    path('editcategory/<id>', views.EditCategoryView.as_view(), name='edit-category'),
    path('users/', views.ListUsersView.as_view(), name='all-users'),
    path('block/<id>', views.BlockUsers.as_view(), name='block-user'),
    path('unblock/<id>', views.UnBlockUsers.as_view(), name='unblock-user'),
    path('pormote/<id>', views.MakeAdmin.as_view(), name='pormote-user'),
    path('makenormaluser/<id>', views.MakeNormalUser.as_view(), name='make-normal-user'),
    path('like/<id>', views.AddLike.as_view(), name='like-post'),
    path('dislike/<id>', views.AddDislike.as_view(), name='dislike-post'),
    path('search', views.Search.as_view(), name='search'),
]

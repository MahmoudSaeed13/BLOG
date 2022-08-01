from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from Blog.forms import LoginForm,CreatePostForm, CreateCategoryForm
from django.urls import reverse
from Blog.models import Category, CategorySubscription, Comments, Likes, User, Post, Reply
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from Blog.utils import AdminAccess
from django.contrib.auth.mixins import LoginRequiredMixin
from .tasks import send_subscription_email
import json
from Blog.utils import generate_html

# Create your views here.
class Custom404View(generic.View):
    def dispatch(self, request, *args, **kwargs):
        return render(request,'blog/404.html')


class Custom500View(generic.View):
    def dispatch(self, request, *args, **kwargs):
        return render(request,'blog/500.html')

class RegisterUser(generic.View):
    
    template_name = 'blog/registration.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
                
        if request.POST['password'] != request.POST['password_confirmation']:
            messages.error(request, "Password and confirmation must match.", extra_tags='danger')
            return HttpResponseRedirect(reverse("register")) 

        if len(request.POST['password']) < 8:
            messages.error(request, "password must be more than 8 charachters long.", extra_tags='danger')
            return HttpResponseRedirect(reverse("register")) 

        if not request.POST['first_name']:
            messages.error(request, "please enter your first name.", extra_tags='danger')
            return HttpResponseRedirect(reverse("register")) 

        if not request.POST['last_name']:
            messages.error(request, "please enter your last name.", extra_tags='danger')
            return HttpResponseRedirect(reverse("register")) 

        if not request.POST['email']:
            messages.error(request, "please enter your email.", extra_tags='danger')
            return HttpResponseRedirect(reverse("register")) 

        if not request.POST['username']:
            messages.error(request, "please enter your username.", extra_tags='danger')
            return HttpResponseRedirect(reverse("register")) 

        if User.objects.filter(email = request.POST['email']).first():
            messages.error(request, "Email already taken.", extra_tags='danger')
            return HttpResponseRedirect(reverse("register")) 
        
        try:
            user = User.objects.create_user(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                username = request.POST['username'],
                email = request.POST['email'],
                password = request.POST['password']
            )
            user.save()
            login(request, user)
        except IntegrityError:
            messages.error(request, "username already taken.", extra_tags='danger')
            return HttpResponseRedirect(reverse("register")) 
        
        return HttpResponseRedirect(reverse("home"))


class LoginView(generic.View):
    form_class = LoginForm
    template_name = 'blog/login.html'
    
    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class,})

    def post(self, request):
        form = LoginForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if not user.blocked:
                login(request, user)
                messages.success(request, f"{username} logged in successfully")
                return redirect('home')
            else:
                messages.error(request, "You are blocked please conatact admins.", extra_tags='danger')
        else:    
            messages.error(request, "Invalid username and/or password.", extra_tags='danger')
        
        form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})

class LogOutView(generic.View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully')
        return redirect('home')

class HomeView(generic.View):
    def get(self, request):
        
        posts = Post.objects.all().order_by('-created_at')
        categories = Category.objects.all()


        if request.user.is_authenticated:
            sub_categories = []
            subscriped_categories = CategorySubscription.objects.filter(user=request.user)
            for category in subscriped_categories:
                sub_categories.append(category.category)
        else:
            sub_categories = []

        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'blog/home.html', {
            'posts':posts,
            'categories': categories,
            'page_obj' : page_obj,
            'sub_categories':sub_categories
        })


class DetailPostView(generic.DetailView):
    model = Post
    template_name = 'blog/detail_post.html' 
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(DetailPostView, self).get_context_data(**kwargs)
        context['comments'] = Comments.objects.filter(post = kwargs['object'].id)
        context['replies'] = Reply.objects.filter(comment__in = list(context['comments']))
        context['likes'] = Likes.objects.filter(action=True).filter(post = kwargs['object'].id).count()
        context['dis_likes'] = Likes.objects.filter(action=False).filter(post = kwargs['object'].id).count()
        context['post_body'] = generate_html(context['post'].body)
        print(context['post_body'])
        return context

class DetailCategoryView(generic.DetailView):
    model = Category
    template_name = 'blog/category.html'
    pk_url_kwarg = 'id' 

    def get_context_data(self, **kwargs):
        context = super(DetailCategoryView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        subscriped_categories = CategorySubscription.objects.filter(user=self.request.user)
   
        sub_categories = []
        if self.request.user.is_authenticated:
            for category in subscriped_categories:
                sub_categories.append(category.category)
        else:
            sub_categories = []

        context['sub_categories'] = sub_categories
        return context


class CreatePostView(AdminAccess, generic.CreateView):
    model = Post
    template_name = 'blog/create_post.html'
    form_class = CreatePostForm

    def post(self, request):
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST['title']
            body = request.POST['body']
            category = request.POST['category']

            image = request.FILES.get('image')

            post = Post(
                title = title,
                body = body,
                image = image,
                category = Category.objects.filter(id=category).first(),
                creator = request.user
            )
            post.save()

        return HttpResponseRedirect(reverse("home"))
 

    def get_context_data(self, **kwargs):
        context = super(CreatePostView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


class CreateCategoryView(AdminAccess, generic.CreateView):
    model = Category
    template_name = 'blog/create_category.html'
    form_class = CreateCategoryForm

    def post(self, request):
        form = CreateCategoryForm(request.POST)

        if form.is_valid():
            title = request.POST['title']
            category = Category(
                title = title
            )
            category.save()
            return HttpResponseRedirect(reverse("home"))

    def get_context_data(self, **kwargs):
        context = super(CreateCategoryView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context

class CommentAddView(LoginRequiredMixin,generic.View):
    
    def post(self, request, id):
        user = request.user
        post = Post.objects.filter(id = id).first()
        body = request.POST['body']

        comment = Comments(
            commentor = user, 
            post = post,
            body = body
        )
        comment.save()
        return HttpResponseRedirect(reverse('detailed-post', args=[id,]))


class ReplyAddView(LoginRequiredMixin, generic.View):
    
    def post(self, request, id):
        user = request.user
        comment = Comments.objects.filter(id = id).first()
        body = request.POST['body']

        reply = Reply(
            commentor = user, 
            comment = comment,
            body = body
        )
        reply.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SubscribeCategory(LoginRequiredMixin,generic.View):

    def get(self,request, id):
        user = request.user
        category = get_object_or_404(Category, pk=id)
        subscription = CategorySubscription.objects.filter(user=request.user).filter(category=category)
        if not subscription:
            subscription = CategorySubscription(
                user = user,
                category = category
            )
            subscription.save()
            
            current_site = get_current_site(request).domain
            user_celery = json.dumps(user.serialize())
            category_celery = json.dumps(category.serialize())
            send_subscription_email.delay(user_celery, category_celery, current_site)
        else:
            messages.warning(request, "Category Already followed.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        return HttpResponseRedirect(reverse('home'))
        
class UnsubscribeCategory(LoginRequiredMixin,generic.View):
    def get(self,request, id):
        try: 
            subscribe = CategorySubscription.objects.filter(user=request.user, category=id)
            subscribe.delete()
        except Exception:
            raise Exception('could not unsubscribe you!')
        return HttpResponseRedirect(reverse('home'))


class DeletePostView(AdminAccess, SuccessMessageMixin,generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = '/'
    pk_url_kwarg = 'id'
    success_message = 'Post deleted successfully.'


class DeleteCategoryView(AdminAccess, SuccessMessageMixin,generic.DeleteView):
    model = Category
    template_name = 'blog/delete_category.html'
    success_url = '/'
    pk_url_kwarg = 'id'
    success_message = 'Category deleted successfully.'


class EditPOstView(AdminAccess, SuccessMessageMixin,generic.edit.UpdateView):
    model = Post
    template_name = 'blog/create_post.html'
    form_class = CreatePostForm
    success_url = '/'
    pk_url_kwarg = 'id'
    success_message = 'Post Updated successfully.'


class EditCategoryView(AdminAccess, SuccessMessageMixin,generic.edit.UpdateView):
    model = Category
    template_name = 'blog/create_category.html'
    form_class = CreateCategoryForm
    success_url = '/'
    pk_url_kwarg = 'id'
    success_message = 'Category Updated successfully.'


class ListUsersView(generic.ListView):
    model = User
    template_name = 'blog/users_page.html'

    def get_context_data(self, **kwargs):
        context = super(ListUsersView, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context

class BlockUsers(AdminAccess, generic.View):
    
    def get(self, request, id):
        user = get_object_or_404(User, pk = id)
        if not user.blocked:    
            user.blocked = True
            user.save()
            messages.success(request, f'{user.username} Blocked.')
            return HttpResponseRedirect(reverse('all-users'))
        else:
            messages.warning(request, 'user is already blocked')
            return HttpResponseRedirect(reverse('all-users'))

class UnBlockUsers(AdminAccess, generic.View):
    
    def get(self, request, id):
        user = get_object_or_404(User, pk = id)
        if user.blocked:    
            user.blocked = False
            user.save()
            messages.success(request, f'{user.username} unlocked.')
            return HttpResponseRedirect(reverse('all-users'))
        else:
            messages.warning(request, 'user is already unblocked')
            return HttpResponseRedirect(reverse('all-users'))

class MakeAdmin(AdminAccess, generic.View):
    
    def get(self, request, id):
        user = get_object_or_404(User, pk = id)
        if not user.is_superuser:    
            user.is_superuser = True
            user.save()
            messages.success(request, f'{user.username} is now admin.')
            return HttpResponseRedirect(reverse('all-users'))
        else:
            messages.warning(request, 'user is already admin')
            return HttpResponseRedirect(reverse('all-users'))

class MakeNormalUser(AdminAccess, generic.View):
        
    def get(self, request, id):
        user = get_object_or_404(User, pk = id)
        if user.is_superuser and not user.is_staff:    
            user.is_superuser = False
            user.save()
            messages.success(request, f'{user.username} is now normal user.')
            return HttpResponseRedirect(reverse('all-users'))
        else:
            messages.warning(request, 'user is already normal user')
            return HttpResponseRedirect(reverse('all-users'))

class AddLike(LoginRequiredMixin,generic.View):

    def get(self, request, id):
        object = Likes.objects.filter(post=id).filter(user=request.user).first()

        if object:
            if object.action:
                object.delete() 
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                object.action = True
                object.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        object = Likes(
            user = request.user,
            post = Post.objects.filter(id=id).first(),
            action = True
        )
        object.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddDislike(LoginRequiredMixin ,generic.View):

    def get(self, request, id):
        object = Likes.objects.filter(post=id).filter(user=request.user.id).first()

        if object:
            if object.action:
                object.action = False
                object.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                object.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        object = Likes(
            user = request.user,
            post = Post.objects.filter(id=id).first(),
            action=False
        )
        object.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class Search(generic.View):
    def get(self, request):
        return render(request, 'blog/search.html',{})
    
    def post(self, request):
        search_words = request.POST['words'].strip().split(' ')
        print(search_words)
        if search_words == ['']:
            print('here')
            return render(request, 'blog/search.html',{})

        result_posts = []
        result_categories = []

        for word in search_words:
            posts = Post.objects.filter(title__icontains = word)
            category = Category.objects.filter(title__icontains = word)
            for post in posts:
                result_posts.append(post)
            for cat in category:
                result_categories.append(cat)

        return render(request, 'blog/search.html',{
            'posts' : result_posts, 
            'categories' : result_categories,
            'searched' : search_words
        })
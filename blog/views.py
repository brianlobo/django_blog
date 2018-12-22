from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
    )
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
    )
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post

    # <app>/<model>_<viewtype>.html
    # blog/post_list.html <-Default ()
    template_name = 'blog/home.html' 
    # This will override the default location 
    # it searches for a tempate

    # By default, ListView will call 
    # context by the name object_list
    context_object_name = 'posts'   
    # This overrides it

    ordering = ['-date_posted'] 
     # '-' makes it from newest to oldest
    # 'date_post' from oldest to newest

    paginate_by = 4

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' 
    context_object_name = 'posts'   
    paginate_by = 4

    def get_queryset(self):
        # 404 if doesnt exist
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    # We wont set the 'template_name' so it will look in:
    # blog/post_detail.html
    # # <app>/<model>_<viewtype>.html

class PostCreateView(LoginRequiredMixin, CreateView):
    # LoginRequiredMixin wont allow you to access post/new unless 
    # you are logged in.
    # Will redirect to login page.
    model = Post
    # Sets the fields for the post
    fields = ['title', 'content']

    # Requires an author so we override it to make it the user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # LoginRequiredMixin wont allow you to access post/new unless 
    #      you are logged in. Will redirect to login page.
    # UserPassesTestMixin will be used with test_func function
    model = Post
    # Sets the fields for the post
    fields = ['title', 'content']

    # Requires an author so we override it to make it the user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # Gets post
        post = self.get_object()
        # Checks if user is tring to edit own post
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # LoginRequiredMixin wont allow you to access post/new unless 
    #      you are logged in. Will redirect to login page.
    # UserPassesTestMixin will be used with test_func function
    model = Post
    # Will redirect home after
    success_url = "/"

    def test_func(self):
        # Gets post
        post = self.get_object()
        # Checks if user is tring to edit own post
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', { 'title': 'About'})

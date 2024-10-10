from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CommentForm
from .models import post, Comment
from users.models import profile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy

@login_required
def index(request):
    context = {
        'post' : post.objects.all(),
    }
    return render(request, 'index.html', context,)

class PostListView(ListView):
    model = post
    template_name = 'index.html'
    context_object_name = 'post'
    ordering = ['-date_posted']
    paginate_by = 3

class UserPostListView(ListView):
    model = post
    template_name = 'user_post.html'
    context_object_name = 'post'
    paginate_by = 3
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')
class PostDetailView(DetailView):
    model = post
    template_name = 'post_detail.html'
    context_object_name = 'object'
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.all()
        form = CommentForm()
        context['comments'] = comments
        context['form'] = form
        return context
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        if request.method == 'POST':
            user = User
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, f'Comment by {comment.author} is posted successfully on {comment.post}')
                return redirect(reverse('post-detail', kwargs={'pk': post.pk}))
            return self.get(request, *args, **kwargs)
        else:
            form = CommentForm()
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'content']
    template_name = 'post_form.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title', 'content']
    template_name = 'post_form.html',
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self, **kwargs):
        post = self.get_object()
        return post.author == self.request.user
    def get_success_url(self):
        success_url =reverse_lazy('post-detail', args=[self.object.id])

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/'
    template_name = 'post_confirm_delete.html'
    context_object_name = 'object'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = '/'
    template_name = 'comment_delete.html'
    context_object_name = 'comment'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'post_form.html',
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
def search(request):
    query = request.GET.get('q')
    if query:
        results = post.objects.filter(title__icontains=query)
    else:
        results = post.objects.none()
    return render(request, 'search_result.html', {'results':results, 'query':query})
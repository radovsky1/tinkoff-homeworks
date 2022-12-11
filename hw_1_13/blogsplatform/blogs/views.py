from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView

from .models import Post, Comment
from .forms import PostForm, CommentForm


def posts(request):
    posts = Post.objects.all()
    return render(request, 'posts.html', {'posts': posts})


def search_post(request):
    posts = Post.objects.filter(title__contains=request.POST['searched'])
    return render(request, 'posts.html', {'posts': posts})


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})


def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return HttpResponseRedirect('/posts/post/%d/' % post.id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form, 'post': post})


def add_post(request):
    submitted = False
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/posts/?submitted=True')
    else:
        form = PostForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_post.html', {'form': form, 'submitted': submitted})


class PostListView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-created_at', '-rating']

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-created_at')
        if ordering not in ('-created_at', '-rating'):
            ordering = '-created_at'
        return ordering

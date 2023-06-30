from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.generic.edit import *
from .models import *
from .forms import *
from django.views.generic import *
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from rest_framework.generics import ListAPIView, ListCreateAPIView
from .serializer import PostSerializer


# Create your views here.

class IndexView(View):
    template_name = 'parent/base.html'

    def get(self, request):
        return render(request, self.template_name)


# Init post_list_view
class PostListView(ListView):
    queryset = Post.published.get_queryset()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post_list.html'


# Init post_detail_view
class PostDetailView(DetailView, FormMixin):
    model = Post
    form_class = CommentForm
    template_name = 'blog/post_detail.html'
    # context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(status=Post.Status.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comment.filter(active=True)
        form = CommentForm()
        context['comments'] = comments
        context['form'] = form
        return context

    def form_valid(self, form):
        post = self.get_object()
        form.instance.post = post
        return super().form_valid(form)


class PostListApiView(ListAPIView):
    queryset = Post.published.get_queryset()
    serializer_class = PostSerializer


class PostCreateApiView(ListCreateAPIView):
    queryset = Post.published.get_queryset()
    serializer_class = PostSerializer


# Init ticketview
class TicketView(CreateView):
    form_class = TicketForm
    model = Ticket
    template_name = 'forms/ticket.html'
    success_url = '/blog'

    def form_valid(self, form):
        return super().form_valid(form)


# Init commentview

class CommentView(CreateView):
    form_class = CommentForm
    template_name = 'forms/comments.html'
    model = PostComment
    queryset = Post.published.get_queryset()

    def form_valid(self, form):
        post_id = self.kwargs['post_id']
        post = Post.published.get(pk=post_id)
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return f'../{post_id}'

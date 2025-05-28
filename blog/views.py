from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Post
from django.views.generic import ListView
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from .forms import SearchForm


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search=SearchVector('title', 'body'),
                ).filter(search=query)
    return render(request, 'blog/post/search.html', 
                  {'form': form, 'query': query, 'results': results})

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    # pagination with 3 posts per page
    tag = None
    post_list = Post.published.all()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
 
    paginator = Paginator(post_list.all(), 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts, 'tag': tag }
    )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
            status=Post.Status.PUBLISHED, 
            slug=post, 
            publish__year=year, 
            publish__month=month, 
            publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
        ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
        ).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html', 
        {
        'post': post, 
        'comments': comments, 
        'form': form, 
        'similar_posts': similar_posts
        }
    )

from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    form = None
    if (request.method == 'POST'):
        # Form was submitted
        form = EmailPostForm(request.POST)
        if (form.is_valid()):
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read \"{post.title}\" at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, from_email=None, recipient_list=[cd['to']])
            sent = True
        else:
            form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
         {'post': post, 'form': form, 'sent': sent}
         )
    
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if (form.is_valid()):
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request, 'blog/post/comment.html', 
                   {'form': form, 'post': post, 'comment': comment}
                   )


    
# Create your views here.

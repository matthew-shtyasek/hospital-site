from django.shortcuts import render, get_object_or_404, redirect
from glav.forms import CommentForm
from glav.models import Post


def index(request):
    return render(request, 'index.html')


def post(request):
    posts = Post.objects.all()
    return render(request, 'post.html', {'posts': posts})


def about(request):
    about = Post.objects.all()
    return render(request, 'about.html', {'about': about})


def comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # или любой другой способ определения автора
            comment.save()
            return redirect('comment', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'comment.html', {'post': post, 'comments': comments, 'form': form})
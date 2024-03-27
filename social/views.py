from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

###############################  post views ###########################################
@login_required
def home(request):
    if request.method == 'POST': # create post form
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    
    posts = Post.objects.all().order_by('-timestamp') # get all posts form the database. order by timestamp
    return render(request, 'social/index.html', {'form': form, 'posts': posts})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    Like.objects.create(user=request.user, post=post)
    return redirect('home')

@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        text = request.POST.get('comment_text')
        Comment.objects.create(user=request.user, post=post, text=text)
        return redirect('home')
    return render(request, 'social/comment_post.html')



##########################  friend requests views #####################################

@login_required
def send_friend_request(request, to_user_id):
    to_user = User.objects.get(id=to_user_id)
    FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return redirect('profile', user_id=to_user.id)

@login_required
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.accepted = True
        friend_request.save()
    return redirect('profile', user_id=request.user.id)

@login_required
def reject_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
    return redirect('profile', user_id=request.user.id)
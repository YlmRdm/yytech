from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# Start process: Index
def post_index(request):
    post_list = Post.objects.all()
    #Searching statement Started...
    query = request.GET.get('q')
    if query:
         post_list = post_list.filter(
            Q(title__icontains=query) |                 #It searchs Title
            Q(content__icontains=query) |               #It searchs Content
            Q(user__first_name__icontains=query) |      #It searchs Name
            Q(user__last_name__icontains=query)         #It searchs Surname
        ).distinct()
    #Searching statement Ended...

    paginator = Paginator(post_list, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, "post/index.html", {'posts': posts})

# End process: Index
# Start process: Detail
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'post/detail.html', context)
# End process: Detail
# Start process: Create
def post_create(request):

    if not request.user.is_authenticated == True:
        return Http404()

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'Created successfully.', extra_tags='message-successful')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form,
    }

    return render(request, 'post/form.html', context)
# End process: Create
# Start process: Update
def post_update(request, slug):

    if not request.user.is_authenticated == True:
        return Http404()

    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, 'Updated successfully.', extra_tags='message-successful')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form
    }

    return render(request, "post/form.html", context)
# End process: Update
#Start process: Delete
def post_delete(request, slug):

    if not request.user.is_authenticated == True:
        return Http404()

    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post:index')
#End process: Delete

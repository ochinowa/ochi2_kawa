from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Post, Tag, Comment
from .forms import PostAddForm, ContactForm, CmtForm

from django.http import HttpResponse
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
 #ContactFormのみ！ PostAddFormは別のフォーム用です！


from django.template.loader import render_to_string
from django.http import JsonResponse


# def index(request):
#    posts = Post.objects.all().order_by('-created_at')
#    return render(request, 'blog_app/index.html', {'posts': posts})

def is_valid_q(q):
   return q != '' and q is not None


def index(request):
   query = request.GET.get('q')
   if query:
       posts = Post.objects.all().order_by('-created_at')
       posts = posts.filter(
       Q(title__icontains=query)|
       Q(user__username__icontains=query)
       ).distinct()
   else:
       posts = Post.objects.all().order_by('-created_at')
   return render(request, 'blog_app/index.html', {'posts': posts, 'query': query,})



# 1.これを「継承」して新しい関数を作る
# 2.indexの全ての記事から特定のカテゴリやタグを持つものを選ぶ
# 3.テンプレートで、< for post in XXX >で表示
# 4.でもそうしたら、カテゴリやタグの数だけ関数を作らなければならない。それは不可。解決策が必要
# 記事の絞り込み方の方法

# ※別の方法
# そもそもcategory_appやgenre_appで別アプリとして記事を作って表示させる。
# →しかしそうして作ったコンテンツもやはり「カテゴリやタグ」を持ち、その中から特定のカテゴリを持つ記事など
# を表示させなければならないから、上記の課題に戻ってしまう。


# def index(request):
#    query = request.GET.get('q')
#    if query:
#        posts = Post.objects.all().order_by('-created_at')
#        posts = posts.filter(
#        Q(title__icontains=query)|
#        Q(user__username__icontains=query)
#        ).distinct()
#    else:
#        posts = Post.objects.all().order_by('-created_at')
#    return render(request, 'blog_app/index.html', {'posts': posts, 'query': query,})



# ON Ajax
def detail(request, post_id):
   post = get_object_or_404(Post, id=post_id)
   comments = Comment.objects.filter(post=post).order_by('-created_at')
   liked = False
   if post.like.filter(id=request.user.id).exists():
       liked = True
   if request.method == "POST":
       form = CmtForm(request.POST or None)
       if form.is_valid():
           text = request.POST.get('text')
           comment = Comment.objects.create(post=post, user=request.user, text=text)
           comment.save()
   else:
       form = CmtForm()
       context = {
           'post': post,
           'comments': comments,
           'form': form,
           'liked': liked
       }

   if request.is_ajax():
       html = render_to_string('blog_app/comment.html', context, request=request )
       return JsonResponse({'form': html})
   return render(request, 'blog_app/detail.html', {'post': post, 'form': form, 'comments': comments, 'liked': liked})


# for NO Ajax
# def index(request):
#     posts = Post.objects.all().order_by('-created_at')
#     title_or_user = request.GET.get('title_or_user')
#     date_min = request.GET.get('date_min')
#     date_max = request.GET.get('date_max')
#     tag = request.GET.get('tag')
#
#     if is_valid_q(title_or_user):
#         posts = posts.filter(Q(title__icontains=title_or_user)
#                              | Q(user__username__icontains=title_or_user)
#                              ).distinct()
#
#     if is_valid_q(date_min):
#         posts = posts.filter(created_at__gte=date_min)
#
#     if is_valid_q(date_max):
#         posts = posts.filter(created_at__lt=date_max)
#
#     if is_valid_q(tag) and tag != 'タグを選択...':
#         posts = posts.filter(tag__tag=tag)
#
#     return render(request, 'blog_app/index.html',
#                   {'posts': posts, 'title_or_user': title_or_user, 'date_min': date_min, 'date_max': date_max,
#                    'tag': tag})
#
#
# def detail(request, post_id):
#    post = get_object_or_404(Post, id=post_id)
#    comments = Comment.objects.filter(post=post).order_by('-created_at')
#    liked = False
#    if post.like.filter(id=request.user.id).exists():
#        liked = True
#    if request.method == "POST":
#        form = CmtForm(request.POST or None)
#        if form.is_valid():
#            text = request.POST.get('text')
#            comment = Comment.objects.create(post=post, user=request.user, text=text)
#            comment.save()
#            return redirect('blog_app:detail', post_id=post.id)
#    else:
#        form = CmtForm()
#        context = {
#            'post': post,
#            'comments': comments,
#            'form': form,
#            'liked': liked
#        }
#
#    return render(request, 'blog_app/detail.html', {'post': post, 'form': form, 'comments': comments, 'liked': liked})


# def detail(request, post_id):
#    post = get_object_or_404(Post, id=post_id)
#    comments = Comment.objects.filter(post=post).order_by()
#    liked = False
#    if post.like.filter(id=request.user.id).exists():
#        liked = True
#    return render(request, 'blog_app/detail.html', {'post': post, 'liked': liked}


# for NO Ajax
# def like(request):
#    post = get_object_or_404(Post, id=request.POST.get('post_id'))
#    liked = False
#    if post.like.filter(id=request.user.id).exists():
#        post.like.remove(request.user)
#        liked = False
#    else:
#        post.like.add(request.user)
#        liked = True
#    return redirect('blog_app:detail', post_id=post.id)


# for Ajax
def like(request):
   post = get_object_or_404(Post, id=request.POST.get('post_id'))
   liked = False
   if post.like.filter(id=request.user.id).exists():
       post.like.remove(request.user)
       liked = False
   else:
       post.like.add(request.user)
       liked = True
   context={
       'post': post,
       'liked': liked,
   }
   if request.is_ajax():
       html = render_to_string('blog_app/like.html', context, request=request)
       return JsonResponse({'form': html})


@login_required
def add(request):
   if request.method == "POST":
      form = PostAddForm(request.POST, request.FILES)
      if form.is_valid():
         post = form.save(commit=False)
         post.user = request.user
         post.save()
         return redirect('blog_app:index')
   else:
       form = PostAddForm()
   return render(request, 'blog_app/add.html', {'form': form})


# ログインしていない人が、自分のアカウント以外の編集ページなどに遷移しようとしたら
# 強制的にloginページを返す
# 直接URLを入力されてもログインしていなければ、login.htmlに返されるようになる
@login_required
def edit(request, post_id):
   post = get_object_or_404(Post, id=post_id)
   if request.method == "POST":
       form = PostAddForm(request.POST, request.FILES, instance=post)
       if form.is_valid():
           form.save()
           return redirect('blog_app:detail', post_id=post.id)
   else:
       form = PostAddForm(instance=post)
   return render(request, 'blog_app/edit.html', {'form': form, 'post':post })


@login_required
def delete(request, post_id):
   post = get_object_or_404(Post, id=post_id)
   post.delete()
   return redirect('blog_app:index')


def contact(request):
   if request.method == 'POST':
       form = ContactForm(request.POST)
       if form.is_valid():
          name = form.cleaned_data['name']
          message = form.cleaned_data['message']
          email = form.cleaned_data['email']
          myself = form.cleaned_data['myself']
          recipients = [settings.EMAIL_HOST_USER]
          if myself:
               recipients.append(email)
          try:
               send_mail(name, message, email, recipients)
          except BadHeaderError:
               return HttpResponse('無効なヘッダーが見つかりました。')
          return redirect('blog_app:done')
   else:
       form = ContactForm()
   return render(request, 'blog_app/contact.html', {'form': form})

def done(request):
   return render(request, 'blog_app/done.html')


def comment_delete(request, comment_id):
   comment = get_object_or_404(Comment, id=comment_id)
   comment.delete()
   return redirect('blog_app:detail', post_id=comment.post.id)



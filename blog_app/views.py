from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Tag
from .forms import PostAddForm, ContactForm
from django.contrib.auth.decorators import login_required
import textwrap
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.views.generic import View


def index(request):
   posts = Post.objects.all().order_by('-created_at')
   return render(request, 'blog_app/index.html', {'posts': posts})

def detail(request, post_id):
     post = get_object_or_404(Post, id=post_id)
     return render(request, 'blog_app/detail.html', {'post': post})

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

class ContactView(View):
   def get(self, request, *args, **kwargs):
      form = ContactForm(request.POST or None)
      return render(request, 'blog_app/contact.html', {'form': form})


   def post(self, request, *args, **kwargs):
         form = ContactForm(request.POST or None)
         if form.is_valid():
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            subject = 'お問い合わせありがとうございます。'
            contact = textwrap.dedent('''
               ※このメールはシステムからの自動返信です。

               {name} 様
               
               お問い合わせありがとうございます。
               以下の内容でお問い合わせを受け付けました。
               内容を確認させていただき、ご返信させていただきますので、少々お待ちください。

               ----------------------------------

               ・お名前
               {name}

               ・メールアドレス
               {email}

               ・メッセージ
               {message}
               -----------------------------------
               株式会社　長町研磨
               〒700-0943
               岡山県岡山市南区新福1-14-4
               TEL 086-26-4-4111
               営業時間 8:15~17:00（月~金）
               WEB: https://www.nagamachi-kenma.com/
            ''').format(
               name=name,
               email=email,
               message=message
            )
            to_list = [email]
            bcc_list = [settings.EMAIL_HOST_USER]
            try:
               message = EmailMessage(subject=subject, body=contact, to=to_list, bcc=bcc_list)
               message.send()
            except BadHeaderError:
               return HttpResponse('無効なヘッダが検出されました。')
            return redirect('blog_app:done')

         return render(request, 'blog_app/contact.html',{'form': form})

class DoneViews(View):
  def get(self, request, *args, **kwargs):   
      return render(request, 'blog_app/done.html')  
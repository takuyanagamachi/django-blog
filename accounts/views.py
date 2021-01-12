from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from blog_app .models import Post
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required

def detail(request, pk):
   user = get_object_or_404(CustomUser, pk=pk)
   posts = user.post_set.all().order_by('-created_at')
   return render(request, 'account/detail.html', {'user': user, 'posts': posts})

@login_required
def edit(request, pk):
   user = get_object_or_404(CustomUser, pk=pk)
   if request.method == "POST":
       form = CustomUserChangeForm(request.POST, instance=request.user)
       if form.is_valid():
           form.save()
           return redirect('accounts:detail', pk=user.pk)
   else:
       form = CustomUserChangeForm(instance=user)
   return render(request, 'account/edit.html', {'form': form, 'user':user })

@login_required
def delete(request, pk):
   user = get_object_or_404(CustomUser, pk=pk)
   user.delete()
   return redirect('accounts:index')
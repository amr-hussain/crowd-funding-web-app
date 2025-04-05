# main/dashboard/category_views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from main.forms import CategoryForm
# You'll create this form
from main.models import Category


def is_admin(user):
    return user.is_staff


# @login_required
# @user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/category_list.html', {'categories': categories})


# @login_required
# @user_passes_test(lambda u: u.is_staff)
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'dashboard/category_form.html', {'form': form})
#
# # @login_required
# @user_passes_test(lambda u: u.is_staff)
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'dashboard/category_form.html', {'form': form})

# @login_required
# @user_passes_test(lambda u: u.is_staff)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'dashboard/category_confirm_delete.html', {'category': category})
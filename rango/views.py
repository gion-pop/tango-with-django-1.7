from django.shortcuts import render
from rango.models import (
    Category,
    Page,
)
from rango.forms import (
    CategoryForm,
    PageForm,
    UserForm,
    UserProfileForm,
)
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
)
from django.contrib.auth.decorators import login_required

from datetime import datetime


def index(req):
    category_list = Category.objects.order_by('-likes')[:5]
    most_viewed_pages = Page.objects.order_by('-views')[:5]
    ctx_dict = {
        'categories': category_list,
        'most_viewed_pages': most_viewed_pages,
    }

    visits = int(req.COOKIES.get('visits', 1))
    reset_last_visit_time = False

    last_visit = req.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], '%Y-%m-%d %H:%M:%S')

        if (datetime.now() - last_visit_time).days > 0:
            visits += 1
            reset_last_visit_time = True

    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        req.session['last_visit'] = str(datetime.now())
        req.session['visits'] = visits

    ctx_dict['visits'] = visits

    return render(req, 'rango/index.html', ctx_dict)


def about(req):
    visits = int(req.COOKIES.get('visits', 1))
    ctx_dict = {'visits': visits}
    return render(req, 'rango/about.html', ctx_dict)


def category(req, category_name_slug):
    ctx_dict = {}

    try:
        requested_category = Category.objects.get(slug=category_name_slug)
        ctx_dict['category'] = requested_category
        ctx_dict['category_name'] = requested_category.name

        pages = Page.objects.filter(category=requested_category)
        ctx_dict['pages'] = pages
    except Category.DoesNotExist:
        pass

    return render(req, 'rango/category.html', ctx_dict)


@login_required
def add_category(req):
    if req.method == 'POST':
        form = CategoryForm(req.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(req)
        else:
            print(form.errors)

    else:
        form = CategoryForm()

    ctx_dict = {'form': form}
    return render(req, 'rango/add_category.html', ctx_dict)


@login_required
def add_page(req, category_name_slug):
    try:
        requested_category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if req.method == 'POST':
        form = PageForm(req.POST)

        if requested_category and form.is_valid():
            page = form.save(commit=False)
            page.category = requested_category
            page.views = 0
            page.save()
            return category(req, category_name_slug)
        else:
            print(form.errors)

    else:
        form = PageForm()

    ctx_dict = {
        'form': form,
        'category': requested_category,
    }
    return render(req, 'rango/add_page.html', ctx_dict)


@login_required
def restricted(req):
    return render(req, 'rango/restricted.html', {})

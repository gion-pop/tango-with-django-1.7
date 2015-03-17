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


def index(req):
    category_list = Category.objects.order_by('-likes')[:5]
    most_viewed_pages = Page.objects.order_by('-views')[:5]
    ctx_dict = {
        'categories': category_list,
        'most_viewed_pages': most_viewed_pages,
    }

    return render(req, 'rango/index.html', ctx_dict)


def about(req):
    return render(req, 'rango/about.html')


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


def register(req):
    registered = False

    if req.method == 'POST':
        user_form = UserForm(data=req.POST)
        profile_form = UserProfileForm(data=req.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in req.FILES:
                profile.picture = req.FILES['picture']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    ctx_dict = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    }
    return render(req, 'rango/register.html', ctx_dict)


def user_login(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(req, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse('Your Rango account is disabled.')
        else:
            print('Invalid login details: {}, {}'.format(username, password))

    else:
        return render(req, 'rango/login.html', {})


@login_required
def restricted(req):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(req):
    logout(req)
    return HttpResponseRedirect('/rango/')

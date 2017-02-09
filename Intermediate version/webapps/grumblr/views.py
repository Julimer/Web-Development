from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.shortcuts import render, loader
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from grumblr.models import *
from grumblr.forms import *
import datetime
from django.shortcuts import get_object_or_404


def userlogin(request):
    print("enter login")

    if request.method == 'GET':
        if request.user.is_authenticated():
            print("a user has logged in")
            # return render(request, 'globalStream.html')
            return HttpResponseRedirect(reverse('globalStream'))
        context = {'login_form': LoginForm()}
        return render(request, 'login.html', context)

    elif request.method == 'POST':
        login_form = LoginForm(request.POST)

        if not login_form.is_valid():
            print(login_form.errors)
            print("enter login form invalid")
            context = {'login_form': login_form}
            return render(request, 'login.html', context)
        else:
            username = login_form.data.get('username')
            password = login_form.data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            print("enter login user")
            return HttpResponseRedirect(reverse('globalStream'))


def register(request):
    if request.method == 'GET':
        context = {'register_form': RegistrationForm()}
        return render(request, 'register.html', context)

    register_form = RegistrationForm(request.POST)

    context = {'register_form': register_form}

    if not register_form.is_valid():
        return render(request, 'register.html', context)

    new_username = register_form.cleaned_data.get('username')
    new_password = register_form.cleaned_data.get('password1')

    new_user = User.objects.create_user(username=new_username, password=new_password)
    new_user.first_name = register_form.cleaned_data.get('first_name')
    new_user.last_name = register_form.cleaned_data.get('last_name')
    new_user.email = register_form.cleaned_data.get('email')

    new_user.is_active = False
    new_user.save()

    new_profile = Profile(user=new_user)
    new_profile.age = 0
    new_profile.bio = 'Oh, you are looking at my page.'
    new_profile.picture = 'no-img.jpg'
    print("register PIC: ", new_profile.picture)
    new_profile.save()

    token = default_token_generator.make_token(new_user)

    email_body = """Welcome to Grumblr! Please click the link below to verify your email address and
    activate your account.\n This activation link will expire in 7 days. Start Grumblr now : )
    http://%s%s""" % (request.get_host(), reverse('confirm', args=(new_user.id, token)))

    send_mail(subject="Verify your email address for Grumblr",
              message=email_body,
              from_email='rlu1@ini.cmu.edu',
              recipient_list=[new_user.email],
              fail_silently=False)

    context = {'email': register_form.cleaned_data.get('email')}
    return render(request, 'confirmEmail.html', context)


def confirm(request, id, token):
    user = User.objects.get(id=id)
    already_active = False
    if user.is_active == False:
        user.is_active = True
        user.save()
    # If user is already active, display error message
    else:
        already_active = True
    context = {'already_active': already_active}
    return render(request, 'confirmSuccess.html', context)


@login_required
def editProfile(request):
    if request.method == 'GET':
        user_obj = User.objects.get(id=request.user.id)
        form = EditProfileForm(instance=user_obj)

        form.initial['bio'] = user_obj.profile.bio
        form.initial['age'] = user_obj.profile.age
        form.initial['picture'] = user_obj.profile.picture

        context = {'form': form, 'picture_url': user_obj.profile.picture.url}
        # form = EditProfileForm(user=request.user)
        # context = {'form', form}
        return render(request, 'edit.html', context)

    elif request.method == 'POST':

        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        context = {'form': form}

        if not form.is_valid():
            user_obj = User.objects.get(id=request.user.id)

            form.initial['bio'] = user_obj.profile.bio
            form.initial['age'] = user_obj.profile.age
            form.initial['picture'] = user_obj.profile.picture

            context = {'form': form, 'picture_url': user_obj.profile.picture.url}
            return render(request, 'edit.html', context)
        else:
            user = User.objects.get(id=request.user.id)
            user.username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.profile.age = form.cleaned_data.get('age')
            user.profile.bio = form.cleaned_data.get('bio')
            if request.FILES.get('picture'):
                user.profile.picture = request.FILES.get('picture')

            user.save()
            user.profile.save()
            return HttpResponseRedirect(reverse('globalStream'))


@login_required
def globalStream(request):
    print("enter globalStream")
    if request.method == "GET":
        posts = Post.objects.filter().order_by('time').reverse()
        post_form = PostForm(instance=request.user)
        max_time = Post.get_max_time()

        context = {'posts': posts, 'max_time': max_time, 'post_form': post_form}
        return render(request, 'globalStream.html', context)

    # elif request.method == "POST" and request.POST['formname'] == "postform":
    #     post_model = Post(user=request.user)
    #     post_form = PostForm(request.POST, instance=post_model)
    #
    #     if not post_form.is_valid():
    #         posts = Post.objects.filter().order_by('time').reverse()
    #         context = {'posts': posts, 'post_form': post_form}
    #         # return HttpResponseRedirect(reverse('globalStream'))
    #         return render(request, 'globalStream.html', context)
    #     else:
    #         newpost = post_form.cleaned_data.get('text')
    #         time = datetime.datetime.now()
    #         new_post = Post(text=newpost, user=request.user, time=time)
    #         new_post.save()
    #         return HttpResponseRedirect(reverse('globalStream'))
    else:
        raise Http404


@login_required
def followStream(request):
    print("enter followStream")
    errors = " "
    login_user = request.user
    if request.method == "GET":
        following = login_user.profile.follows.all()
        posts = Post.objects.filter(user__profile__in=following).order_by('time').reverse()
        context = {'posts': posts, 'errors': errors}
        return render(request, 'followStream.html', context)


@login_required
def updatePosts(request, time="1970-01-01T00:00+00:00"):
    print("enter updatePosts")
    posts = Post.get_changes(time)
    max_time = Post.get_max_time()
    print("max_time in posts", max_time)
    context = {"max_time": max_time, "posts": posts}
    return render(request, 'posts.json', context, content_type='application/json')


@login_required
def addComment(request):
    print("enter addComment")
    if 'comment' in request.POST and 'post_id' in request.POST and request.POST:
        print("enter comment POST")
        content = request.POST['comment']
        post_id = request.POST['post_id']
        time = datetime.datetime.now()

        if content and content.strip() and Post.objects.filter(id=post_id).exists():
            print("enter comment VALID")
            new_comment = Comment(user=request.user, content=content, time=time, post_id=post_id)
            new_comment.save()
            print("!!!new comment: ", new_comment.content)
            context = {"comment":new_comment}
            return render(request, 'comment.json', context, content_type='application/json')  # Empty response on success.
        else:
            return HttpResponseRedirect(reverse('globalStream'))
    else:
        raise Http404

@login_required
def post(request):

    if request.method == "GET":
        return HttpResponseRedirect(reverse('globalStream'))

    elif request.method == "POST":
        post_model = Post(user=request.user)
        post_form = PostForm(request.POST, instance=post_model)

        if not post_form.is_valid():
            posts = Post.objects.filter().order_by('time').reverse()
            context = {'posts': posts, 'post_form': post_form}
            #return HttpResponseRedirect(reverse('globalStream'))
            return render(request, 'globalStream.html', context)
        else:
            newpost = post_form.cleaned_data.get('text')
            time = datetime.datetime.now()
            new_post = Post(text=newpost, user=request.user, time=time)
            new_post.save()
            return HttpResponseRedirect(reverse('globalStream'))


@login_required
def profile(request, id):
    try:
        login_user = request.user
        current_user = User.objects.get(id=id)
        posts = Post.objects.filter(user=current_user).order_by('time').reverse()

        if login_user.profile in current_user.profile.followed_by.all():
            follow = 'unfollow'
        else:
            follow = 'follow'

        context = {'posts': posts, 'current_user': current_user, 'follow': follow}
        return render(request, "profile.html", context)

    except ObjectDoesNotExist:
        posts = Post.objects.filter().order_by('time').reverse()
        context = {'posts': posts}
        return render(request, "globalStream.html", context)


@login_required
def follow(request, id):
    login_user = request.user
    current_user = get_object_or_404(User, id=id)

    # current_user = User.objects.get(id=id)

    if login_user.profile in current_user.profile.followed_by.all():
        login_user.profile.follows.remove(current_user.profile)
    else:
        login_user.profile.follows.add(current_user.profile)

    login_user.profile.save()

    posts = Post.objects.filter(user=current_user).order_by('time').reverse()

    if login_user.profile in current_user.profile.followed_by.all():
        follow = 'unfollow'
    else:
        follow = 'follow'
    context = {'posts': posts, 'current_user': current_user, 'follow': follow}
    return render(request, "profile.html", context)


@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('userlogin'))

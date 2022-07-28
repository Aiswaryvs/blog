from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from blogapp.forms import UserRegistrationForm, LoginForm, UserProfileForm, PasswordResetForm, BlogForm,ChangePropicForm,CommentForm
from django.views.generic import View, CreateView, FormView, TemplateView, UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from blogapp.models import UserProfile, Blogs,Comments
from django.utils.decorators import method_decorator


# Create your views here.


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"user must login")
            return redirect("login")
    return wrapper




class SignUpView(CreateView):
    form_class = UserRegistrationForm
    template_name = "reg.html"
    model = User
    success_url = reverse_lazy("login")

    # def get(self,request,*args,**kwargs):
    #     form=self.form_class()
    #     return render(request,self.template_name,{"form":form})
    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "registration successful")
    #         return redirect("signup")
    #     else:
    #         messages.error(request, "registration failed")
    #         return render(request,self.template_name,{"form":form})


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    model = User

    # def get(self,request,*args,**kwargs):
    #     form=self.form_class()
    #     return render(request,self.template_name,{"form":form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pswd = form.cleaned_data.get("password")
            user = authenticate(request, username=uname, password=pswd)
            if user:
                login(request, user)
                print("success")
                return redirect("home")
            else:
                messages.error(request, "Invalid Credentials")
                return render(request, self.template_name, {"form": form})
        return render(request, self.template_name, {"form": form})

@method_decorator(signin_required,name="dispatch")
class IndexView(CreateView):
    model = Blogs
    form_class = BlogForm
    success_url = reverse_lazy("home")
    template_name = "home1.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        messages.success(self.request, "Post has been saved")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blg = Blogs.objects.all().order_by("-posted_date")
        context["blogs"] = blg
        comment_form=CommentForm()
        context["comment_form"]=comment_form
        return context

@method_decorator(signin_required,name="dispatch")
class CreateUserProfileView(CreateView):
    model = UserProfile
    template_name = "addprofile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Profile has been Added")
        self.object = form.save()
        return super().form_valid(form)

@method_decorator(signin_required,name="dispatch")
class ViewMyprofileView(TemplateView):
    template_name = "view-profile.html"

@signin_required
def sign_out(request, *args, **kwargs):
    logout(request)
    return redirect("login")

@method_decorator(signin_required,name="dispatch")
class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            oldpassword = form.cleaned_data.get("old_password")
            psw1 = form.cleaned_data.get("new_password")
            psw2 = form.cleaned_data.get("confirm_password")
            user = authenticate(request, username=request.user.username, password=oldpassword)
            if user:
                user.set_password(psw2)
                user.save()
                messages.success(request, "Password Changed")
                return redirect("login")
            else:
                messages.error(request, "Invalid Credentials")
                return render(request, self.template_name, {"form": form})

@method_decorator(signin_required,name="dispatch")
class ProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "profileupdate.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request, "Profile has been Updated")
        self.object = form.save()
        return super().form_valid(form)

@method_decorator(signin_required,name="dispatch")
class ChangeProfilePicView(UpdateView):
    template_name = "change-propic.html"
    form_class = ChangePropicForm
    model=UserProfile
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request, "Profile has been Updated")
        self.object = form.save()
        return super().form_valid(form)


@signin_required
def add_comment(request,*args,**kwargs):
    if request.method=="POST":
        blog_id=kwargs.get("post_id")
        blog=Blogs.objects.get(id=blog_id)
        user=request.user
        comment=request.POST.get("comment")
        Comments.objects.create(blog=blog,comment=comment,user=user)
        messages.success(request,"Comment has been posted")
        return redirect("home")


@signin_required
def add_like(request,*args,**kwargs):
    blog_id=kwargs.get("post_id")
    blog=Blogs.objects.get(id=blog_id)
    blog.liked_by.add(request.user)
    blog.save()
    return redirect("home")


@signin_required
def follow_friend(request,*args,**kwargs):
    friend_id=kwargs.get("user_id")
    friend_profile=User.objects.get(id=friend_id)
    request.user.users.following.add(friend_profile)
    friend_profile.save()
    messages.success(request,"your started following  "+friend_profile.username)
    return redirect("home")






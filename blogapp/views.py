from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from blogapp.forms import UserRegistrationForm,LoginForm,UserProfileForm
from django.views.generic import View,CreateView,FormView,TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from blogapp.models import UserProfile
# Create your views here.

class SignUpView(CreateView):
    form_class=UserRegistrationForm
    template_name="reg.html"
    model=User
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
    form_class=LoginForm
    template_name="login.html"
    model=User

    # def get(self,request,*args,**kwargs):
    #     form=self.form_class()
    #     return render(request,self.template_name,{"form":form})

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pswd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request,user)
                print("success")
                return redirect("home")
            else:
                messages.error(request,"Invalid Credentials")
                return render(request,self.template_name,{"form":form})
        return render(request,self.template_name, {"form": form})

class IndexView(TemplateView):
    template_name = "home.html"


class CreateUserProfileView(CreateView):
    model = UserProfile
    template_name = "addprofile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"Profile has been Added")
        self.object = form.save()
        return super().form_valid(form)

# class ViewMyprofileView(TemplateView):
#     template_name = "view-profile.html"

def sign_out(request,*args,**kwargs):
    logout(request)
    return redirect("login")





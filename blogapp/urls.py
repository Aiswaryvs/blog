from django.urls import path
from blogapp import views

urlpatterns = [
    path("accounts/signup",views.SignUpView.as_view(),name="signup"),
    path("accounts/signin",views.LoginView.as_view(),name="login"),
    path("home",views.IndexView.as_view(),name="home"),
    path("users/profile/add",views.CreateUserProfileView.as_view(),name="add-profile"),
    path("users/profile/view",views.ViewMyprofileView.as_view(),name="view-profile"),
    path("accounts/signout",views.sign_out,name="signout")

]
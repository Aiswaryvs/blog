from django.urls import path
from blogapp import views

urlpatterns = [
    path("accounts/signup",views.SignUpView.as_view(),name="signup"),
    path("accounts/signin",views.LoginView.as_view(),name="login"),
    path("home",views.IndexView.as_view(),name="home"),
    path("users/profile/add",views.CreateUserProfileView.as_view(),name="add-profile"),
    path("users/profile/view",views.ViewMyprofileView.as_view(),name="view-profile"),
    path("accounts/signout",views.sign_out,name="signout"),
    path("users/password/change",views.PasswordResetView.as_view(),name="password-reset"),
    path("user/profile/change/<int:user_id>",views.ProfileUpdateView.as_view(),name="profile-update"),
    path("user/propic/edit/<int:user_id>",views.ChangeProfilePicView.as_view(),name="pic-change"),
    path("post/comment/<int:post_id>",views.add_comment,name="add-comment"),
    path("post/like/add/<int:post_id>",views.add_like,name="add-like")

]
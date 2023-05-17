from django.urls import path,  include
# from django.contrib.auth import views as auth_views
# from django.urls import reverse_lazy
from . import views

app_name = 'account'

urlpatterns = [
     path(' ', views.dashboard,
          name='dashboard'),
     path('', include('django.contrib.auth.urls')),
     path('register/', views.register, name='register'),
     path('edit/', views.edit, name='edit'),
     path('users/', views.user_list, name='user_list'),
     path('users/follow/', views.user_follow, name='user_follow'),
     path('users/<username>/', views.user_detail, name='user_detail'),

     # path('login/', views.user_login, name='login'),
     # path('login/', auth_views.LoginView.as_view(),
     #      name='login'),
     # path('logout/', auth_views.LogoutView.as_view(),
     #      name='logout'),
     # path('password-change/', auth_views.PasswordChangeView.as_view(
     #      success_url=reverse_lazy('account:password_change_done')),
     #      name='password_change'),
     # path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),
     #      name='password_change_done'),
     # path('password-reset/', auth_views.PasswordResetView.as_view(
     #      success_url=reverse_lazy('account:password_reset_done')),
     #      name='password_reset'),
     # path('password-reset/done/',
     #      auth_views.PasswordResetDoneView.as_view(),
     #      name='password_reset_done'),
     # path('password-reset/<uidb64>/<token>/',
     #      auth_views.PasswordResetConfirmView.as_view(
     #           success_url=reverse_lazy('account:password_reset_complete')),
     #      name='password_reset_confirm'),
     # path('password-reset/complete/',
     #      auth_views.PasswordResetCompleteView.as_view(),
     #      name='password_reset_complete'),
]

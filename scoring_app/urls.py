from django.urls import path
from . import views
from .forms import SignInForm
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('calculation/', views.calculation, name='calculation'),
    path('contact/', views.contact, name='contact'),
    path('result/<calculation_id>', views.get_calculation_result, name='result'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-out/', views.sign_out, name='sign-out'),
    path('calculation/<calculation_id>/delete', views.delete_calculation, name='delete_calculation'),
    path('profile/', views.profile, name='profile'),
    path('download-result/', views.download_result, name='download_result'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='C:\\Users\\oleg.veselov\\Music\\Diploma_project\\scoring_project\\scoring_app\\templates\\scoring_app\\reset_password.html'), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='C:\\Users\\oleg.veselov\\Music\\Diploma_project\\scoring_project\\scoring_app\\templates\\scoring_app\\reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='C:\\Users\\oleg.veselov\\Music\\Diploma_project\\scoring_project\\scoring_app\\templates\\scoring_app\\reset.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='C:\\Users\\oleg.veselov\\Music\\Diploma_project\\scoring_project\\scoring_app\\templates\\scoring_app\\reset_password_complete.html'), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
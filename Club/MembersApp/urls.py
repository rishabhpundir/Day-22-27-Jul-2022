from django.urls import path
from MembersApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.user_login, name='login_link'),
    path('logout', views.user_logout, name='logout_link'),
    path('register', views.register_user, name='register_link'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
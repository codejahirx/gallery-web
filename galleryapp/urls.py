from django.urls import path

from galleryapp import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('<int:pk>/', views.detail_page, name='detail'),
    path('del/<int:pk>', views.del_album, name='delete'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('dashboard/', views.profile_page, name='profile'),
    path('upload/', views.upload_album, name='upload'),
    path('logout/', views.logout_page, name='logout'),
]

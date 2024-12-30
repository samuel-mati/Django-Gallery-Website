from django.urls import path
from . import views

urlpatterns = [
    #admin page url
    path('seoth/', views.admin, name='admin'),

    #gallery page urls
    path('',views.gallery,name='gallery'),
    path('load-images/', views.load_images, name='load-images'),
    path('download_image/', views.download_image, name='download_image'),
    path('like_image/', views.like_image, name='like_image'),
    path('search_image/', views.search_image, name='search_image'),
    path('filter-by-category/', views.filter_by_category, name='filter_by_category'),

    #authentication
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register_view'),
    path('password/', views.password_view, name='password'),

    #image management
    path('add_image/', views.add_image, name='add_image'),
    path('image/<int:id>/', views.view_image, name='view_image'),
    path('image/<int:id>/edit/', views.edit_image, name='edit_image'),
    path('image/<int:id>/delete/', views.delete_image, name='delete_image'),

    #user management
    path('users/', views.users, name='users'),
    path('users/view/<int:user_id>/', views.view_user, name='view_user'),  # View user details
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),  # Edit user details
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),  # Delete user


    path('categories/', views.categories, name='categories'),
    
    
]
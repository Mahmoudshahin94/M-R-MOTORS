from django.urls import path
from . import views
from . import views_admin

urlpatterns = [
    # Admin/Deployment utilities
    path('_admin/check-varchar/', views_admin.check_varchar_fields, name='check_varchar'),
    path('_admin/fix-schema/', views_admin.fix_database_schema, name='fix_schema'),
    path('_admin/run-migrations/', views_admin.run_migrations, name='run_migrations'),
    path('_admin/migration-status/', views_admin.migration_status, name='migration_status'),
    
    path('', views.home, name='home'),
    path('inventory/', views.inventory, name='inventory'),
    path('car/<str:car_id>/', views.car_detail, name='car_detail'),
    path('location/', views.location, name='location'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Password Reset
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # Email Verification
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('verify-email-sent/<str:email>/', views.verify_email_sent, name='verify_email_sent'),
    path('verify-email-prompt/', views.verify_email_prompt, name='verify_email_prompt'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    
    # Phone Verification
    path('verify-phone/', views.verify_phone_prompt, name='verify_phone_prompt'),
    path('send-phone-verification/', views.send_phone_verification, name='send_phone_verification'),
    
    # User Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/delete-account/', views.delete_account, name='delete_account'),
    path('profile/remove-picture/', views.remove_profile_picture, name='remove_profile_picture'),
    
    # Favorite Cars
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/add/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/check/<str:car_id>/', views.check_favorite, name='check_favorite'),
    path('favorites/list/', views.get_user_favorites, name='get_user_favorites'),
    
    # Car Management
    path('api/cars/', views.get_cars_api, name='get_cars_api'),
    path('api/admin/cars/', views.get_admin_cars_api, name='get_admin_cars_api'),
    path('api/cars/add/', views.add_car_view, name='add_car'),
    path('api/cars/<int:car_id>/update/', views.update_car_view, name='update_car'),
    path('api/cars/<int:car_id>/delete/', views.delete_car_view, name='delete_car'),
    path('api/cars/<int:car_id>/toggle-sold/', views.toggle_car_sold_status, name='toggle_car_sold'),
    path('api/cars/<int:car_id>/toggle-hidden/', views.toggle_car_hidden_status, name='toggle_car_hidden'),
    path('api/cars/image/<int:image_id>/delete/', views.delete_car_image_view, name='delete_car_image'),
    
    # Admin User Management
    path('api/admin-users/', views.get_admin_users, name='get_admin_users'),
    path('api/admin-users/add/', views.add_admin_user, name='add_admin_user'),
    path('api/admin-users/<int:admin_id>/remove/', views.remove_admin_user, name='remove_admin_user'),
]

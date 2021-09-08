from django.conf.urls import url
from UserApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^userLogin/([0-9]+)/([0-9]+)',views.userverify_otp),
    url(r'^sendOtp/([0-9]+)$',views.usersend_otp),
    url(r'^User$',views.User_data),
    url(r'^User/([0-9]+)$',views.User_data)
    
    
]
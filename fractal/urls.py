from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.conf.urls import include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
# from chats.api.views import FacebookLogin, FacebookConnect
# from rest_auth.registration.views import (
#     SocialAccountListView, SocialAccountDisconnectView
# )


# Have a separate module for the accounts

urlpatterns = [
	url(r'^admin/', admin.site.urls),

	#url(r'^accounts/', include('allauth.urls')),

	url(r'^api/', include('chats.api.urls'), name="api"),

	url(r'^api/realtime/', include('interactive.api.urls'), name="api_messaging"),

	url(r'^rest-auth/', include('rest_auth.urls')),

	# url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

	url(r'^api/auth/token', obtain_jwt_token),

	url(r'^api-token-refresh/', refresh_jwt_token),

	url(r'^api-token-verify/', verify_jwt_token),

	# url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),

	# url(r'^rest-auth/facebook/connect/$', FacebookConnect.as_view(), name='fb_connect'),

 #    url(r'^socialaccounts/$', SocialAccountListView.as_view(), name='social_account_list'),

 #    url(r'^socialaccounts/(?P<pk>\d+)/disconnect/$', SocialAccountDisconnectView.as_view(), name='social_account_disconnect'),    	
]



from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.conf.urls import include

urlpatterns = [
	url(r'^admin/', admin.site.urls),

	url(r'^accounts/', include('allauth.urls')),

	url(r'^api/', include('chats.api.urls'), name="api"),

	url(r'^api/realtime/', include('interactive.api.urls'), name="api_messaging"),


]



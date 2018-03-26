from django.shortcuts import render, get_object_or_404
from .models import Message, Post
from chats.models import Topic, LocalChat, GlobalChat, ChatGroup
from django.shortcuts import render, redirect
from django.views.generic import RedirectView, DetailView
from chats.forms import TopicUpdateForm, LocalChatCreateForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from django.http import HttpResponse
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from chats.utilities import unique_label_generator
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Notification

def single_post(request):
	template_name = 'notifications/single_post.html'

	post_id = request.GET.get("post_id")

	post = Post.objects.get(id=post_id)

	context = {'post': post}

	return render(request, template_name=template_name, context=context)

def user_notifications(request):


	template_name = 'notifications/user_notifications.html'

	user_id = request.user.id
	notifications = Notification.objects.filter(user__id=user_id)
	notifications = notifications.order_by('-timestamp')
	context = {'notifications': notifications}




	return render(request, template_name=template_name, context=context)
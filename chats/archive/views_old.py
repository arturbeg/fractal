from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from .forms import ChatGroupCreateForm, TopicCreateForm, LocalChatCreateForm
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, ChatGroup, Topic, LocalChat, GlobalChat
from django.http import Http404, JsonResponse
from django.views.generic.edit import FormMixin
from django.urls import reverse
from interactive.models import Post
import operator
from django.db.models import Q
import json
from .utilities import unique_label_generator

from functools import reduce

from .forms import ProfileEditForm
from interactive.models import Post, PostComment


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from notifications.models import Notification



def post_more(request):

    post_id = request.GET.get('id')
    post = Post.objects.get(id=post_id)
    full_text = post.message.text

    context = {'full_text': full_text, 'post_id': post_id}


    return JsonResponse(context)


def load_more_posts(request):
    template_name = 'chats/load_more_posts.html'

    posts = Post.objects.all()
        # Need to narrow this down to the posts of followed users

        
        

    user = request.user
    profile = user.profile


    users_you_follow = profile.user.is_following.all()

    # Below is the desired queryset
    queryset = Post.objects.filter(message__user__profile__in=users_you_follow)



    paginator = Paginator(queryset, 10) # Show 10 posts per page

    page = request.GET.get('page')
    
    posts = paginator.page(page)


    context = {'posts': posts}
    return render(request, template_name=template_name, context=context)




def like_post_comment(request):

    is_liked = False


    post_comment_id = request.POST.get('id')

    post_comment = PostComment.objects.get(id=post_comment_id)

    #message = post.message

    post_comment_owner = post_comment.user

    user = request.user

    
    if post_comment.likers.filter(id=user.id).exists():
        post_comment.likers.remove(user)

    else:
        post_comment.likers.add(user)

        notification = Notification.objects.create(text="like_post_comment",user=post_comment_owner, user_2=user, post_comment=post_comment)
        notification.save()

        is_liked = True

    
    #total_number_of_likes = post.get_total_number_of_likes()


    total_number_of_likes = post_comment.get_number_of_likes()





    context = {'is_liked': is_liked, 'likes_count':total_number_of_likes, 'post_comment_id': post_comment.id}

    return JsonResponse(context)



def load_post_likers(request,pk):

    template_name = 'chats/post_likers_snippet.html'
    post = Post.objects.get(id=pk)
    likers = post.likers.all()
    context = {'likers': likers}





    return render(request,template_name=template_name,context=context)



def like_post(request):

    is_liked = False



    post_id = request.POST.get('id')

    post = Post.objects.get(id=post_id)

    # need to get the user who the post belong to -> call post owner

    post_owner = post.message.user

    message = post.message

    user = request.user

    
    if post.likers.filter(id=user.id).exists():
        post.likers.remove(user)

    else:
        post.likers.add(user)
        is_liked = True
        # user in this case is the person who liked the post and the
        # post_owner is the user whose post was liked
        # Creating the notification saying that the post has been liked
        # For the 
        # dont really need the user filed, but will keep it for now
        notification = Notification.objects.create(text="like_post",user=post_owner, user_2=user, post=post)
        notification.save()
        # Saved the notification to the database


    
    #total_number_of_likes = post.get_total_number_of_likes()


    total_number_of_likes = post.get_number_of_likes()





    context = {'is_liked': is_liked, 'likes_count':total_number_of_likes, 'post_id': post.id}

    return JsonResponse(context)


def follow_a_user(request):

    user = request.user

    profile_to_follow_id = request.POST.get('id', None)

    profile_to_follow = get_object_or_404(Profile, id=profile_to_follow_id)

    user_to_follow = profile_to_follow.user



    if profile_to_follow.followers.filter(id=user.id).exists():
        profile_to_follow.followers.remove(user)
        is_following = False
    else:
        profile_to_follow.followers.add(user)

        notification = Notification.objects.create(text="follow_a_user",user=user_to_follow, user_2=user)
        notification.save()
        is_following = True



    number_of_followers = profile_to_follow.followers.count()

    context = {'number_of_followers': number_of_followers, 'profile_id': profile_to_follow_id, 'is_following': is_following}



    return JsonResponse(context)






def fav_localchat(request):

    print("Fav Localchat executing...")

    user = request.user
    localchat_id = request.POST.get('id', None)

    localchat = get_object_or_404(LocalChat, id=localchat_id)

    is_fav = False

    if localchat.participants.filter(id=user.id).exists():
        localchat.participants.remove(user)

    else:
        localchat.participants.add(user)
        is_fav = True



    number_of_participants = localchat.get_number_of_participants()

    print(number_of_participants)


    return JsonResponse({'number_of_participants': number_of_participants, 'localchat_id': localchat_id, 'is_fav': is_fav})





def load_more_comments(request):

    print("Loading more comments")

    post_id = request.POST.get('id')

    print(post_id)

    no_need_load_more_button = False


    post = Post.objects.get(id=post_id)

    total_comments = post.get_number_of_comments()


    old_number_of_comments = int(request.POST.get('old_number_of_comments'))

    new_number_of_comments = old_number_of_comments + 15

    if new_number_of_comments  >= total_comments:
        no_need_load_more_button = True



    all_comments = post.postcomment_set.all()

    required_comments = all_comments[old_number_of_comments:new_number_of_comments]

    list_of_usernames = []
    list_of_comment_texts = []
    list_of_links = []
    list_of_ids = []
    list_of_is_liked = []
    list_number_of_likes = []

    # later on change the code so that JSON passes comments in the form of dicrionaries

    for comment in required_comments:
        list_of_usernames.append(comment.user.username)
        list_of_comment_texts.append(comment.text)
        list_of_links.append(comment.user.profile.get_absolute_url())
        list_of_ids.append(comment.id)

        if comment.likers.filter(id=request.user.id).exists():
            is_liked = True
        else:
            is_liked = False

        list_of_is_liked.append(is_liked) 
        list_number_of_likes.append(comment.get_number_of_likes())       

    print(list_of_usernames)
    print(list_of_comment_texts)
    print(list_of_links)
    print(list_of_ids)
    print(list_of_is_liked)




    context = {'list_of_usernames': list_of_usernames, 'list_of_comment_texts': list_of_comment_texts, 'list_of_links': list_of_links, 'no_need_load':no_need_load_more_button, 'list_of_ids':list_of_ids, 'list_of_is_liked':list_of_is_liked, 'list_number_of_likes':list_number_of_likes}



    return JsonResponse(context)

def add_post_comment(request):

    user = request.user
    post_id = request.POST.get('id')


    post = Post.objects.get(id=post_id)



    comment_text = request.POST.get('comment_text')

    post_comment = PostComment.objects.create(post=post, text=comment_text, user=user)

    post_comment.save()

    # Fetching the owner of the post that was commented

    post_owner = post.message.user

    # Make the notification below


    notification = Notification.objects.create(text="add_post_comment",user=post_owner, user_2=user, post=post)


    notification.save()



    # Get the user and the text back again from the PostComment object

    username = post_comment.user.username
    comment_text = post_comment.text
    post_comment_id = post_comment.id
    post_comment_number_of_likes = post_comment.get_number_of_likes()
    user_profile_link = post_comment.user.profile.get_absolute_url()


    number_of_post_comments = post.postcomment_set.count()




    context = {'username': username, 'comment_text': comment_text, 'post_id': post_id, 'number_of_post_comments':number_of_post_comments, 'post_comment_id': post_comment_id, 'post_comment_number_of_likes':post_comment_number_of_likes, 'user_profile_link': user_profile_link}

    return JsonResponse(context)


def edit_profile(request, pk):
    newUsername = request.POST.get("username")

    pk = pk

    profile = Profile.objects.get(id=pk) 


    form = ProfileEditForm(request.POST, request.FILES, instance=profile)


    if form.is_valid():
        instance = form.save(commit=False)
        
        

        instance.save()

    
    
    try: 
        user_id = profile.user.id
        user = User.objects.get(id=user_id)

        user.username = newUsername

        user.save()
    except:
        print("Problem with saving the users")  

    
    return HttpResponseRedirect(profile.get_absolute_url())


class ProfileDetail(DetailView):
    model = Profile
    template_name = 'chats/profile.html'

    def get_context_data(self, **kwargs):
        print("Updating the get_context_data method")
        data = super(ProfileDetail, self).get_context_data(**kwargs)
        self.object = self.get_object()


        chatgroups = ChatGroup.objects.filter(members__id=self.object.user.id)



        data['chatgroups'] = chatgroups



        posts = Post.objects.filter(message__user__id = self.object.user.id)


        data['posts'] = posts


        requestUser = self.request.user

        profile = self.object

        if profile.followers.filter(id=requestUser.id).exists():
            is_following = True
        else:
            is_following = False



        data['is_following'] = is_following


        followers = profile.followers.all()

        data['followers'] = followers

        following = profile.user.is_following.all()

        data['following'] = following

        chatgroups_user_follows = ChatGroup.objects.filter(members__id=profile.user.id)

        data['chatgroups_user_follows'] = chatgroups_user_follows






        return data

    
class TrendingLocalChatsList(ListView):
    model = LocalChat
    template_name = 'chats/trending_localchats_list.html'


    def get_queryset(self):

        if self.request.user.is_authenticated:
            queryset = LocalChat.objects.all()
            user = self.request.user

            queryset = LocalChat.objects.filter(participants=user)  

            queryset = sorted(queryset, key=lambda x: x.get_number_of_participants(), reverse=True)        

        else:
            # Change to smth else later, like none/trending
            queryset = LocalChat.objects.all()    
            queryset = sorted(queryset, key=lambda x: x.get_number_of_participants(), reverse=True)        
        return queryset




def profile_followers(request, pk, *args, **kwargs):
    template_name = "chats/profile_followers.html"
    profile = Profile.objects.get(pk=pk)
    print(profile.user.username)

    queryset = profile.followers.all()
    print(queryset)

    c = {"followers" : queryset}
    return render(request, template_name, c)




def profile_following(request, pk, *args, **kwargs):
    template_name = "chats/profile_following.html"
    profile = Profile.objects.get(pk=pk)

    queryset = profile.user.is_following.all()
    print(queryset)

    c = {"following": queryset}
    return render(request, template_name, c)





def profile_chatgroups(request, pk, *args, **kwargs):
    template_name = "chats/profile_chatgroups.html"
    profile = Profile.objects.get(pk=pk)

    queryset = ChatGroup.objects.filter(members__id=profile.user.id)

    c = {"chatgroups": queryset}
    return render(request, template_name, c)




class TrendingGlobalChatsList(ListView):
    model = GlobalChat
    template_name = 'chats/trending_globalchats_list.html'



    def get_queryset(self):



        if self.request.user.is_authenticated:


            queryset = GlobalChat.objects.all()
            chatgroups_followed = self.request.user.is_member.all()
            queryset = GlobalChat.objects.filter(chatgroup__in=chatgroups_followed)

            queryset = sorted(queryset, key=lambda x: x.chatgroup.get_number_of_members(), reverse=True)        

        else:
            print("The use is not authenticated")

            queryset = GlobalChat.objects.all()
            queryset = sorted(queryset, key=lambda x: x.chatgroup.get_number_of_members(), reverse=True)        


        print(queryset)

        return queryset








class RecentActivityList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'chats/recent_activity_list.html'
    login_url = '/accounts/login/'


    def get_queryset(self):
        posts = Post.objects.all()
        # Need to narrow this down to the posts of followed users

        
        

        user = self.request.user
        profile = user.profile


        users_you_follow = profile.user.is_following.all()

        # Below is the desired queryset
        posts = Post.objects.filter(message__user__profile__in=users_you_follow)

        # Only retrive the first 20 posts
        posts = posts[0:10]

        return posts






def redirect_to_trending_topics(request):
    return HttpResponseRedirect(reverse("trending-topics"))



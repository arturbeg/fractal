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

def chatgroup_search_topic_create(request):

    print("Searching a chatgroup in order to create a topic")

    template_name = 'chats/chatgroup_search_topic_create.html'

    result = ChatGroup.objects.all()

 
      
    query = request.GET.get('q')
    if query:
        query_list = query.split()
        result = result.filter(
            reduce(operator.and_,
                    (Q(name__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                    (Q(about__icontains=q) for q in query_list))
        )

    # Only take the first 5 results for now    
    result = result[0:5]
    

    context = {'chatgroups': result}    

    return render(request, template_name=template_name, context=context)          





def global_search(request):


    print("GlobalSearch function is called")
    result = ChatGroup.objects.all()

 
      
    query = request.GET.get('q')
    if query:
        query_list = query.split()
        result = result.filter(
            reduce(operator.and_,
                    (Q(name__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                    (Q(about__icontains=q) for q in query_list))
        )    

    






    template = 'chats/chatgroup_search.html'
    context = {"search_results": result}



    print("The Chatgroup Search worked")

    print(result)



    return render(request, template_name=template, context=context)


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


def raise_topic(request):

    user = request.user
    topic_id = request.POST.get('id', None)
    is_raised = False

    topic = get_object_or_404(Topic, id=topic_id)

    if topic.arrow_ups.filter(id=user.id).exists():
        topic.arrow_ups.remove(user)
    elif topic.arrow_downs.filter(id=user.id).exists():
        topic.arrow_downs.remove(user)
        topic.arrow_ups.add(user)
        is_raised = True

    else:
        topic.arrow_ups.add(user)
        is_raised = True

    context = {'topic_rating': topic.get_topic_rating(), 'topic_id': topic.id, 'is_raised': is_raised}


    return JsonResponse(context)


def lower_topic(request):

    user = request.user
    topic_id = request.POST.get('id', None)
    is_lowered = False

    topic = get_object_or_404(Topic, id=topic_id)

    if topic.arrow_downs.filter(id=user.id).exists():
        topic.arrow_downs.remove(user)
    elif topic.arrow_ups.filter(id=user.id).exists():
        topic.arrow_ups.remove(user)
        topic.arrow_downs.add(user)
        is_lowered = True
    else:
        topic.arrow_downs.add(user)
        is_lowered = True

    context = {'topic_rating': topic.get_topic_rating(), 'topic_id': topic.id, 'is_lowered': is_lowered}

    return JsonResponse(context)

def follow_chatgroup(request):
    print("Trying to implement the follow")

    user = request.user
    chatgroup_id = request.POST.get('id', None)

    chatgroup = get_object_or_404(ChatGroup, id=chatgroup_id)

    if chatgroup.members.filter(id=user.id).exists():
        chatgroup.members.remove(user)
        is_following = False
    else:
        chatgroup.members.add(user)
        is_following = True


    number_of_followers = chatgroup.members.count()




    return JsonResponse({'num_followers': number_of_followers, 'is_following': is_following, 'chatgroup_id' : chatgroup_id})




def chatgroup_follow(request):
    print("Ajax follow has started...")


    if request.method == 'POST':

        user = request.user
        chatgroup_id = request.POST.get('chatgroup_id')

        chatgroup = get_object_or_404(ChatGroup, id=chatgroup_id)



        if chatgroup.members.filter(id=user.id).exists():
            chatgroup.members.remove(user)
        else:
            chatgroup.members.add(user)

        number_of_followers = int(chatgroup.members.count())

    context = {'number_of_followers': number_of_followers} # Working on the follow button for the chatgroup
    # The issue turns out to be with model of ChatGroup


    return None


    #HttpResponse(json.dumps(context), content_type='application/json')







def chargroup_search_list(request):

    query = request.GET.get("query")

    print(query)

    print("It worked")

    return None


 # Figure out how to make this search work, then release the app to a production level
    '''

    queryset = ChatGroup.objects.all()

    query = request.GET.get('q')
    if query:
        result = queryset.filter(

            Q(name__icontains=query) |
            Q(about__icontains=query)

        )








    template = 'chats/chatgroup_search.html'
    context = {}

    print("The Chatgroup Search worked")
    '''










'''class ChatgroupSearchList(ListView):

    model = ChatGroup
    template = 'chats/chatgroup_search.html'''
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


        



def chat_group_topics_more(request,pk):

    queryset = Topic.objects.all()
    queryset = queryset.filter(chatgroup__id=pk)
    queryset = sorted(queryset, key=lambda x: x.trending(), reverse=True)
    template_name = 'chats/chatgroup_topics_only.html'


    paginator = Paginator(queryset, 7) # Show 7 topics per page

    page = request.GET.get('page')
    
    topics = paginator.page(page)     




    return render(request, template_name, {'topics': topics})





def chat_group_localchats_more(request,pk):

    queryset = LocalChat.objects.all()
    queryset = queryset.filter(chatgroup__id=pk)
    template_name = 'chats/chatgroups_localchats_only.html'


    paginator = Paginator(queryset, 7) # Show 7 topics per page

    page = request.GET.get('page')
    
    localchats = paginator.page(page)        




    return render(request, template_name, {'localchats': localchats})

class ChatGroupDetailView(FormMixin, DetailView):
    model = ChatGroup
    template_name = 'chats/chatgroupdetail.html'
    form_class = LocalChatCreateForm

    def post(self, request, *args, **kwargs):

        pk = self.kwargs['pk']

        chatgroup = ChatGroup.objects.get(id=pk)

        print(chatgroup)

        form = ChatGroupCreateForm(self.request.POST, self.request.FILES, instance=chatgroup)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            new_label = unique_label_generator(instance)
            instance.label = new_label

            instance.save()

            instance.globalchat.label = instance.label

            instance.globalchat.save()


        return HttpResponseRedirect(chatgroup.get_absolute_url())    
            


    def get_success_url(self):
        return reverse('chatgroup-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        data = super(ChatGroupDetailView, self).get_context_data(**kwargs)
        data['form'] = self.get_form()
        print(self.request.user.id)
        self.object = self.get_object()
        print(self.object.owner.id)

        is_owner = self.object.owner.id == self.request.user.id
        print(is_owner)

        data['is_owner'] = is_owner


        chatgroup_topics = Topic.objects.filter(chatgroup__id = self.object.id)

        chatgroup_topics = sorted(chatgroup_topics, key=lambda x: x.trending(), reverse=True)

        chatgroup_topics = chatgroup_topics[0:6]

        data['topics'] = chatgroup_topics


        chatgroup_localchats = LocalChat.objects.filter(chatgroup__id = self.object.id)


        chatgroup_localchats = chatgroup_localchats[0:6]



        data['localchats'] = chatgroup_localchats

        chatgroup_followers = self.object.members.all()

        data['chatgroup_followers'] = chatgroup_followers

        return data

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.chatgroup = self.get_object()
        instance.save()


        return super(ChatGroupDetailView, self).form_valid(form)


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


    '''
    # The old get_queryset
    def get_queryset(self):

        if self.request.user.is_authenticated:

            queryset = LocalChat.objects.all()
            print(queryset)
            chatgroups_followed = self.request.user.is_member.all()
            print(chatgroups_followed)

            for localchat in queryset:
                print(localchat)
                chatgroups_counter = chatgroups_followed.count()

                for chatgroup in chatgroups_followed:
                    if localchat not in chatgroup.localchat_set.all():
                        chatgroups_counter -= 1
                print(chatgroups_counter)

                if chatgroups_counter == 0:
                    queryset = queryset.exclude(name = localchat.name)


        else:
            print("The user is not authenticated")
            queryset = LocalChat.objects.all()


        print(queryset)










        return queryset

        '''



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










    '''
    def get_queryset(self):
        chatgroups = self.request.user.is_member.all()
        queryset = LocalChat.objects.all() # initial unmodified queryset

        print('The user is ' + str(self.request.user))
        print(chatgroups)


        for localchat in queryset:
            for chatgroup in chatgroups:
                if localchat not in chatgroup.localchat_set.all():
                    queryset = queryset.exclude(name = localchat.name)
        print(queryset)



        return queryset
        '''




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










class TrendingTopicsList(ListView):
    model = Topic
    template_name = 'chats/trendingtopicslist.html'
    paginate_by = 15
    context_object_name = 'topics'




    def get_queryset(self):

        # Update the querying function, takes too long to execute
        # The updated version is below
        if self.request.user.is_authenticated:

            queryset = Topic.objects.all()
            chatgroups_followed = self.request.user.is_member.all()

            queryset = Topic.objects.filter(chatgroup__in = chatgroups_followed)
            print(queryset)
            queryset = list(queryset)
            print(queryset)
            queryset = sorted(queryset, key=lambda x: x.trending(), reverse=True)

       

        else:
            # Change this to none in the future!!!
            # At this point keep the most popular ones
            queryset = Topic.objects.all()
            queryset = sorted(queryset, key=lambda x: x.trending(), reverse=True)












        return queryset

def trending_topics_list_page(request):

    if request.user.is_authenticated:
        queryset = Topic.objects.all()
        chatgroups_followed = request.user.is_member.all()

        queryset = Topic.objects.filter(chatgroup__in = chatgroups_followed)
        print(queryset)
        queryset = list(queryset)
        print(queryset)
        queryset = sorted(queryset, key=lambda x: x.trending(), reverse=True)
        queryset = queryset[0:15]

    else:
        queryset = Topic.objects.all()
        queryset = sorted(queryset, key=lambda x: x.trending(), reverse=True)
        queryset = queryset[0:15]
            

    return render(request, 'chats/topics_list.html',{'topics':queryset})        


class TopicCreate(CreateView):
    model = Topic
    template_name = 'chats/topiccreate.html'
    
    form_class = TopicCreateForm

    def form_valid(self, form):
        instance_name = self.request.POST.get("name")
        print("The instance name is "+instance_name)
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.label = unique_label_generator(instance)
        print(instance.label)
        chatgroup_id = self.request.POST.get("chatgroup_id")
        chatgroup = ChatGroup.objects.get(id=chatgroup_id)
        instance.chatgroup = chatgroup
        instance.save()
        success_url = instance.get_absolute_url()


        


        return super(TopicCreate, self).form_valid(form)






class ChatGroupCreate(CreateView):
    model = ChatGroup
    template_name = 'chats/chatgroupcreate.html'

    form_class = ChatGroupCreateForm



    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        user = self.request.user
        instance.save()
        instance.members.add(user)
        instance.save()
        success_url = instance.get_absolute_url()


        return super(ChatGroupCreate, self).form_valid(form)



class ChatGroupList(ListView):
    model = ChatGroup
    template_name = 'chats/chatgrouplist.html'










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



    

'''





def edit_profile(request):

    profile_id = request.POST.get("id")




    return HttpResponseRedirect(profile.get_absolute_url())


'''
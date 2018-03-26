from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import (ChatGroupCreate,
                    ChatGroupList,
                    ChatGroupDetailView,
                    TopicCreate,
                    TrendingTopicsList,
                    TrendingLocalChatsList,
                    ProfileDetail,
                    TrendingGlobalChatsList,
                    RecentActivityList,
                    profile_followers,
                    profile_following,
                    profile_chatgroups,
                    chargroup_search_list,
                    chatgroup_follow,
                    follow_chatgroup,
                    raise_topic,
                    lower_topic,
                    fav_localchat,
                    follow_a_user,
                    global_search,
                    redirect_to_trending_topics,
                    add_post_comment,
                    load_more_comments,
                    trending_topics_list_page,
                    like_post,
                    chat_group_topics_more,
                    chat_group_localchats_more,
                    load_post_likers,
                    chatgroup_search_topic_create,
                    edit_profile,
                    like_post_comment,
                    load_more_posts,
                    post_more)
from django.contrib.auth.decorators import login_required

#app_name = 'chats'

urlpatterns = [

    url(r'^chatgroup/new/$', login_required(ChatGroupCreate.as_view()), name='chatgroup-new'),
    url(r'^chatgroups/$', ChatGroupList.as_view(), name='chatgroups'),
    url(r'^chatgroup/(?P<pk>[-\w]+)/$', ChatGroupDetailView.as_view(), name='chatgroup-detail'),
    url(r'^topic/new/$', login_required(TopicCreate.as_view()), name='topic-new'),


    url(r'^chatgroup/followit/$', chatgroup_follow, name='chatgroup-followit'),



    url(r'^$', redirect_to_trending_topics, name='redirect-to-trending-topics'),
    url(r'^trending/topics/$', trending_topics_list_page, name='trending-topics'),


    url(r'^trending/topics/data/$', TrendingTopicsList.as_view(), name='trending_topics_data'),


    url(r'^trending/localchats/$', TrendingLocalChatsList.as_view(), name='trending-localchats'),
    url(r'^trending/globalchats/$', TrendingGlobalChatsList.as_view(), name='trending-globalchats'),



    url(r'^recentactivity/$', RecentActivityList.as_view(), name='recent-activity'),


    #url(r'^chatgroup/search/$', chargroup_search_list, name='chatgroup-search'),


    url(r'^global_search/$', global_search, name='global_search'),





    url(r'^chatgroup_follow/$', follow_chatgroup, name='chatgroup_follow'),



    url(r'^raise_topic/$', raise_topic, name='raise_topic'),

    url(r'^lower_topic/$', lower_topic, name='lower_topic'),




    url(r'^fav_localchat/$', fav_localchat, name='fav_localchat'),



    url(r'^follow_a_user/$', follow_a_user, name='follow_a_user'),


    url(r'^add_post_comment/$', add_post_comment, name='add_post_comment'),

    url(r'^load_more_comments/$', load_more_comments, name='load_more_comments'),

    url(r'^load_post_likers/(?P<pk>[-\w]+)/$', load_post_likers, name='load_post_likers'),




    url(r'^like_post/$', like_post, name='like_post'),

    url(r'^like_post_comment/$', like_post_comment, name='like_post_comment'),



    url(r'^chat_group_topics_more/(?P<pk>[-\w]+)/$', chat_group_topics_more, name='chat_group_topics_more'),


    url(r'^chat_group_localchats_more/(?P<pk>[-\w]+)/$', chat_group_localchats_more, name='chat_group_localchats_more'),


    url(r'^chatgroup_search_topic_create/$', chatgroup_search_topic_create, name='chatgroup_search_topic_create'),


    url(r'^edit_profile/(?P<pk>[-\w]+)/$', edit_profile, name='edit_profile'),

    url(r'^load_more_posts/$', load_more_posts, name='load_more_posts'),

    url(r'^post_more/$', post_more, name='post_more'),








    #url(r'^edit/$', edit_profile, name='editUserProfile'),
















    url(r'^u/(?P<pk>[-\w]+)/$', ProfileDetail.as_view(), name='profile'),
    url(r'^u/(?P<pk>[-\w]+)/followers/$', profile_followers, name='profile-followers'),
    url(r'^u/(?P<pk>[-\w]+)/following/$', profile_following, name='profile-following'),
    url(r'^u/(?P<pk>[-\w]+)/chatgroups/$', profile_chatgroups, name='profile-chatgroups'),











]



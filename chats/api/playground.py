# Use this file for development puroses to play around with code


# ChatGroup related ad-hoc features

# Can be implemented using filters for the chatgroup
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



# Filters for a chatgroup
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



# More related to the Topic class
def chat_group_topics_more(request,pk):

    queryset = Topic.objects.all()
    queryset = queryset.filter(chatgroup__id=pk)
    queryset = sorted(queryset, key=lambda x: x.trending(), reverse=True)
    template_name = 'chats/chatgroup_topics_only.html'


    paginator = Paginator(queryset, 7) # Show 7 topics per page

    page = request.GET.get('page')
    
    topics = paginator.page(page)     




    return render(request, template_name, {'topics': topics})


# More related to the localchats class
def chat_group_localchats_more(request,pk):

    queryset = LocalChat.objects.all()
    queryset = queryset.filter(chatgroup__id=pk)
    template_name = 'chats/chatgroups_localchats_only.html'


    paginator = Paginator(queryset, 7) # Show 7 topics per page

    page = request.GET.get('page')
    
    localchats = paginator.page(page)        




    return render(request, template_name, {'localchats': localchats})


# Implemented by the ModelViewSet
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


# Implemented by the ModelViewSet
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




# With that we should be able to manipulate User models in
# a RESTful way


'''
Old URLs


    url(r'^', include(router.urls)),
    

    # Topic related urls
    url(r'^topics/(?P<pk>\d+)/$', TopicRudView.as_view(), name="topic-rud"),
    url(r'^topics/$', TopicAPIView.as_view(), name="topic-create"),


    # ChatGroup related urls
    url(r'^chatgroups/$', ChatGroupAPIView.as_view(), name="chatgroup-create"),
    url(r'^chatgroups/(?P<pk>\d+)/$', ChatGroupRudView.as_view(), name="chatgroup-rud"),


    # LocalChat related urls -> uncomment when the views and serializer are created
    url(r'^localchats/$', ChatGroupAPIView.as_view(), name="localchat-create"),
    url(r'^localchats/(?P<pk>\d+)/$', ChatGroupRudView.as_view(), name="localchat-rud"),


    # GlobalChat related urls




    # Profile related urls

'''

'''
class LocalChatAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = LocalChatSerializer

    def get_queryset(self):
        # Performing the search functionality in here

        qs = LocalChat.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(name__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)    

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self, *args, **kwargs):
        return  {'request': self.request}   



class LocalChatRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = LocalChatSerializer
    permission_classes = [IsOwnerOrReadOnly]


    def get_queryset(self):
        return LocalChat.objects.all()

    # getting the request for the serializer
    
    def get_serializer_context(self, *args, **kwargs):
        return  {'request': self.request}




class ChatGroupAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = ChatGroupSerializer

    def get_queryset(self):
        qs = ChatGroup.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(name__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.users)

    def get_serializer_context(self, *args, **kwargs):
        return {'request':self.request}         


class ChatGroupRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ChatGroupSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return ChatGroup.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {'request':self.request}



class TopicAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = TopicSerializer

    def get_queryset(self):
        # Performing the search functionality in here

        qs = Topic.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(name__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)    

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self, *args, **kwargs):
        return  {'request': self.request}   


class TopicRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = TopicSerializer
    permission_classes = [IsOwnerOrReadOnly]


    def get_queryset(self):
        return Topic.objects.all()

    # getting the request for the serializer
    
    def get_serializer_context(self, *args, **kwargs):
        return  {'request': self.request}





class UserViewSet(viewsets.ModelViewSet):
    '''
    '''

    queryset = User.objects.all()
    serializer_class = UserSerializer

    # There are more attributes and functions
    # one can override in ModelViewSet

    # queryset -> queryset that will return objects on .list()



'''
    
    # Topic Serializer
    #arrow_ups = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
    #arrow_downs = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
    #owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    #url = serializers.SerializerMethodField(read_only=True)
    #chatgroup = serializers.HyperlinkedRelatedField(view_name='chatgroup-rud')
    # Need to destinguish between those    

    # LocalChat Serializer
    #online_participants = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
    #owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    #url = serializers.SerializerMethodField(read_only=True)
    #saves = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
    #chatgroup = serializers.HyperlinkedRelatedField(view_name='chatgroup-rud')
    # use serializermethod field or some shit








    # Topic Related features






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



''' Done Topic


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



    
'''

                            
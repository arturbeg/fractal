List of views that need to be served by the REST framework

- CRUD Topics
- CRUD LocalChat
- CRUD Chatgroup
- Retreive GlobalChat (need a bit of thinking)
- CRUD Users
- CRUD Messages
- CRUD Posts
- CRUD PostComments
- CRUD Notifications
- CRUD Profiles


Actions on a message:

- like a message
- delete a message -> handled by a generic APIView
- share a message


Actions on a ChatGroup:

- follow (might be handled by the RUD view by just appending a follower to the memebers list?)


Actions on Profiles:

- follow/unfollow
- like about section ?

Actions on LocalChats/Topics/GlobalChats:

- save into MyChats section

Actions on Topics:

- arrow up/down


Actions on Post:

- like/dislike a post
- comment on a post
- (load more post comments) -> done by the list view using a query -> more thought


Actions on PostComments:

- like/dislike


http://www.django-rest-framework.org/topics/third-party-packages/



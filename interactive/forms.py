from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, TextInput, PasswordInput
from chats.models import Topic, GlobalChat, LocalChat

'''
class LocalChatUpdateForm(forms.ModelForm):
    class Meta:
        model = LocalChat



        fields = ['name','about']





class TopicUpdateForm(forms.ModelForm):
    class Meta:
        model = Topic



        fields = ['name','about']






'''
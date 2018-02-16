from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, TextInput, PasswordInput, CheckboxInput, FileInput, ModelChoiceField
from .models import ChatGroup, Topic, LocalChat, Profile
from django.core.files.images import get_image_dimensions


class LocalChatCreateForm(forms.ModelForm):
    class Meta:
        model = LocalChat
        fields = ['name', 'about', 'is_hidden', 'is_private', 'avatar']



class ProfileCreareForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about']


class ChatGroupCreateForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['name','about','avatar']

        widgets = {
            'name': TextInput(attrs={'placeholder': 'Group Name', 'class': 'input_new_chatgroup form-control'}),
            'about': TextInput(attrs={'placeholder': 'About', 'class': 'input_new_chatgroup form-control'}),

        }





class TopicCreateForm(forms.ModelForm):
    class Meta:
        model = Topic

        fields = ['name', 'about', 'avatar']

        widgets = {
            'name': TextInput(attrs={'placeholder': 'Name', 'class': 'input_new_chatgroup form-control'}),
            'about': TextInput(attrs={'placeholder': 'About', 'class': 'input_new_chatgroup form-control'}),
            'is_hidden': CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_private': CheckboxInput(attrs={'class': 'form-check-input'}),
            'avatar': FileInput(attrs={'class': 'form-control-file'}),


        }





class TopicUpdateForm(forms.ModelForm):
    class Meta:
        model = Topic

        fields = ['name', 'about', 'is_hidden', 'is_private', 'avatar']




class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = ['about', 'avatar']
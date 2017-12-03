from django import forms
from PassPercentage.models import Platform, TestLoop, Name, UserProfile,Comment
from django.contrib.auth.models import User

class PlatformForm(forms.ModelForm):
    name = forms.CharField(max_length=200, help_text='Please enter the platform name')

    class Meta:
        model = Platform
        fields = ('platform_name',)

class TestLoopForm(forms.ModelForm):
    name = forms.CharField(max_length=200, help_text='Please enter the test loop name')
    feature_name = forms.CharField(max_length=200)
    feature_owner = forms.CharField(max_length=200)
    qemu_ver = forms.CharField(max_length=200)
    host_kernel_ver = forms.CharField(max_length=200)
    host_ver = forms.CharField(max_length=200, help_text="Please use the following format: eg:rhel7.4")
    guest_kernel_ver = forms.CharField(max_length=200)
    guest_ver = forms.CharField(max_length=200, help_text="Please use the following format: eg:rhel7.4")

    class Meta:
        model = TestLoop
        exclude = ('platform_name',)

class LoopSelectForm(forms.Form):
    loop_select_name = forms.CharField(label='Select loop name', max_length=100)

class CommentForm(forms.ModelForm):
    comment_user = forms.CharField(widget=forms.TextInput(attrs={'size':10, 'maxlength':10, 'required': True}))
    comment_email = forms.CharField(widget=forms.EmailInput(attrs={'size':20, 'maxlength':20, 'required': True}))
    comment_title = forms.CharField(widget=forms.TextInput(attrs={'size':50, 'maxlength':200, 'required': True}))
    comment_context = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 5, 'required': True}))
    #comment_updated_time = forms.DateTimeField()

    class Meta:
        model = Comment
        fields = ('comment_user', 'comment_email', 'comment_title', 'comment_context',)
        #exclude = ('comment_updated_time',)
        #fields = '__all__'

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('account_picture',)

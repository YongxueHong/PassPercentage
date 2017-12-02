from django import forms
from PassPercentage.models import Platform, TestLoop, Name

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

class CommentForm(forms.Form):
    comment_name = forms.CharField(label='comment name')
    comment_context = forms.CharField(label='comment context', max_length=1000000)
    comment_update_time = forms.DateTimeField(label='comment update time')
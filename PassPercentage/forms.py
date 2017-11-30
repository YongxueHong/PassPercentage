from django import forms
from PassPercentage.models import Platform, TestLoop

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
from django import forms
from captcha.fields import CaptchaField


class MyForms(forms.Form):
    captcha = CaptchaField()

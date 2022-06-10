import profile

from django import forms
from django.contrib.auth.forms import UserCreationForm


class Registerform(UserCreationForm):
    username = forms.CharField(label='사용자명', widget=forms.TextInput(attrs={
        'pattern':'[a-zA-20-9]+',
        'title': '영어 소문자 대문자, 숫자만 가능. 특수문자, 공백 입력 안됨',

    }))
    nickname = forms.CharField(label='별명')

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',) #('username','email',)

    def save(self):
        user = super().save()
        new_profile = profile.objects.create(
            user = user,
            nickname =self.cleaned_data.get('nickname'), #self.cleaned_data['nickname']

        )
        return
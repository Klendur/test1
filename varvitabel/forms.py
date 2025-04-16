from django import forms
from django.forms import modelformset_factory
from .models import komplekteeri, projektivaade, task
from django.contrib.auth.models import User


class komplekteerikogus(forms.ModelForm):
    class Meta:
        model = komplekteeri
        fields = ['komplekteeritudkogus']


    komplekteeritudkogus = forms.IntegerField(initial=0)

class projektivaadeform(forms.ModelForm):
    class Meta:
        model = projektivaade
        fields = ['checkbox']


    checkbox = forms.IntegerField(initial=0)


class CreateTaskForm(forms.Form):
    responsible = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label="Vastutaja")
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)
    note = forms.CharField(widget=forms.Textarea, required=False, label="Märkmed")

class TaskSelectorForm(forms.Form):
    existing_task = forms.ModelChoiceField(
        queryset=task.objects.all(),
        required=False,
        label="Vali olemasolev töö"
    )
    create_new = forms.BooleanField(required=False, label="Loo uus töö")
    responsible = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label="Vastutaja")
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('create_new') and not (cleaned_data.get('responsible') and cleaned_data.get('deadline')):
            raise forms.ValidationError("Palun täida vastutaja ja tähtaeg uue töö loomiseks.")
        return cleaned_data

class SelectionForm(forms.Form):
    selected = forms.BooleanField(required=False)

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()




'''
KogusFormSet = modelformset_factory(
    komplekteeri,
    form=komplekteerikogus,
    fields=['kogus'],  # Only the 'kogus' field should be editable
    extra=0  # No extra empty forms

)


'''



from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'input'
        })
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'input'
        })
    )

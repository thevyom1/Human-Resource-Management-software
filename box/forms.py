from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Employee_Gmail,Employee_Private,Employee_Public,Interviewee, Vehicle, Feedback
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class Employee_GmailForm(forms.ModelForm):

    class Meta:
        model = Employee_Gmail

        fields = ['firstname', 'lastname', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Employee_Gmail.objects.filter(email=email).exists():
            raise ValidationError("details already exists")
        return email

    def __init__(self, *args, **kwargs):
        super(Employee_GmailForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['firstname'].widget.attrs['readonly'] = True
            self.fields['lastname'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True


class Employee_PublicForm(forms.ModelForm):

    class Meta:
        model = Employee_Public
        fields = ['photo_logo','mobile_number','emergency_contact_number','emergency_contact_number1','current_address' ,'field_of_intrest']

class Employee_PrivateForm(forms.ModelForm):

    class Meta:
        model = Employee_Private
        widgets = {'date_of_birth': DateInput()}
        fields = ['date_of_birth','resume','permanent_address','pan','passport_no','passport_expiry']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class VehicleForm(forms.ModelForm):

    class Meta:
        model= Vehicle
        fields = ['vechicle_type','vechicle_model','vechicle_number']


class IntervieweeForm(forms.ModelForm):

    class Meta:
        model= Interviewee
        fields = ['interviewee_name', 'interviewee_email_id','interviewee_resume', 'job_profile']


class Interviewee_SchedulingForm(forms.ModelForm):

    class Meta:
        model= Interviewee
        fields = ['interviewee_name', 'interviewee_email_id','interviewee_resume', 'job_profile']


class EmptyChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), empty_label=None, required=True, widget=None, label=None, initial=None, help_text=None, *args, **kwargs):


        if not required and empty_label is not None:
            choices = tuple([(u'', empty_label)] + list(choices))

        super(EmptyChoiceField, self).__init__(choices=choices, required=required, widget=widget, label=label, initial=initial, help_text=help_text, *args, **kwargs)

class InterviewForm(forms.Form):
        interview_date = forms.DateField(widget=DateInput())
        interview_time= forms.TimeField()

        interviewer_email_id1 = EmptyChoiceField(choices=[(x, x) for x in (Employee_Gmail.objects.all())], required=False, empty_label="Null")

        interviewer_email_id2 = EmptyChoiceField(choices=[(x, x) for x in (Employee_Gmail.objects.all())], required=False, empty_label="Null")
        interviewer_email_id3 = EmptyChoiceField(choices=[(x, x) for x in (Employee_Gmail.objects.all())], required=False, empty_label="Null")

class Employee1_FeedbackForm(forms.ModelForm):

        class Meta:
            model = Interviewee
            fields = ['interviewee_name', 'interviewee_email_id']

        def __init__(self, *args, **kwargs):
            super(Employee1_FeedbackForm, self).__init__(*args, **kwargs)
            instance = getattr(self, 'instance', None)
            if instance:
                self.fields['interviewee_name'].widget.attrs['readonly'] = True
                self.fields['interviewee_email_id'].widget.attrs['readonly'] = True

class Employee_FeedbackForm(forms.ModelForm):

    class Meta:
        model= Feedback
        fields = ['interview_date','level','feedback']

    def __init__(self, *args, **kwargs):
        super(Employee_FeedbackForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['interview_date'].widget.attrs['readonly'] = True
            self.fields['level'].widget.attrs['readonly'] = True

class StatusForm(forms.Form):
    status = forms.ChoiceField(choices=[(x, x) for x in ('hired', 'Rejected', 'Second Round','Third Round', 'On Hold')])

class ReschedulingForm(forms.Form):
    level = forms.ChoiceField(choices=[(x, x) for x in ('Level1','Level2','Level3')])
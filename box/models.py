from django.db import models
from django.core.validators import RegexValidator


class Employee_Gmail(models.Model):

    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length= 254)

    def __str__(self):
       return self.email


class Employee_Public(models.Model):
    employee_gmail = models.OneToOneField(Employee_Gmail, on_delete=models.CASCADE,default=1)
    photo_logo = models.FileField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered in the format: '7543036718'. Up to 10 digits allowed.")
    mobile_number = models.CharField(validators=[phone_regex],max_length=10)  # validators should be a list
    emergency_contact_number = models.CharField(validators=[phone_regex],max_length=10)
    emergency_contact_number1=models.CharField(max_length=10, blank=True,null=True,validators=[phone_regex])
    current_address = models.CharField(max_length = 250)
    field_of_intrest = models.CharField(max_length=100)



    def __str__(self):
        return self.employee_gmail.email


class Vehicle(models.Model):
    employee_gmail = models.ForeignKey(Employee_Gmail, on_delete=models.CASCADE,default=1)
    vechicle_type = models.CharField(max_length=20)
    vechicle_model = models.CharField(max_length=30)
    vechicle_number = models.CharField(max_length=30)

    def __str__(self):
        return self.employee_gmail.email

class Employee_Private(models.Model):
    employee_gmail = models.OneToOneField(Employee_Gmail, on_delete=models.CASCADE,default=1)
    date_of_birth = models.DateField()
    resume = models.FileField()
    permanent_address = models.CharField(max_length = 250)
    pan = models.CharField(max_length = 20)
    hr = models.BooleanField(default=False)
    passport_no = models.CharField(max_length=10, blank=True, null=True)
    passport_expiry = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.employee_gmail.email


class Interviewee(models.Model):
    employee_gmail = models.ForeignKey(Employee_Gmail, on_delete=models.CASCADE,default=1)
    interviewee_name = models.CharField(max_length=250)
    interviewee_email_id = models.EmailField(max_length=250)

    interviewee_resume = models.FileField()
    job_profile = models.CharField(max_length=200, blank=False, default='Not Set')
    status = models.CharField(max_length=100, default='Interview not yet done')

    def __str__(self):
        return self.interviewee_email_id


class Feedback(models.Model):
    interviewee_detail = models.ForeignKey(Interviewee, on_delete=models.CASCADE,default=1)
    interview_date = models.DateField(blank=True,null=True)
    interview_time = models.TimeField(blank=True,null=True)
    interviewer_email_id = models.EmailField(blank=True,null=True)
    feedback = models.TextField(max_length=1000,blank=True)
    level = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.interviewee_detail.interviewee_name + ':' + self.interviewee_detail.interviewee_email_id
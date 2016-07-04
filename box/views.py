from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import Employee_GmailForm,Interviewee_SchedulingForm,ReschedulingForm,Employee_PublicForm,StatusForm,Employee_PrivateForm, UserForm, Employee_FeedbackForm,Employee1_FeedbackForm, VehicleForm, IntervieweeForm, InterviewForm
from .models import Employee_Gmail , Employee_Public , Employee_Private,Vehicle, Interviewee,Feedback
RESUME_FILE_TYPES = ['pdf', 'PDF', 'doc']
INTERVIEWEE_RESUME_FILE_TYPES = ['pdf', 'PDF', 'doc']
IMAGE_FILE_TYPES = ['jpg','png','jpeg']
earlier_date = 0
earlier_time = 0


def create_employee_gmail(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        e=Employee_Gmail.objects.filter(email=request.user.email)
        if len(e)==0:
            form = Employee_GmailForm(request.POST or None,
                                      initial={'firstname': request.user.first_name, 'lastname': request.user.last_name,
                                               'email': request.user.email})
            form1 = Employee_PublicForm(request.POST or None, request.FILES or None)
            if all((form.is_valid(), form1.is_valid())):
                employee6=form.save(commit=False)
                employee1 = form1.save(commit=False)
                employee1.photo_logo = request.FILES['photo_logo']
                file_type1 = employee1.photo_logo.url.split('.')[-1]
                file_type1 = file_type1.lower()
                if file_type1 not in IMAGE_FILE_TYPES:
                    context = {
                        'employee6': employee6,
                        'employee1': employee1,
                        "form": form,
                        "form1": form1,

                        'error_message': 'photo file must be jpg, jpeg, or png',
                    }
                    return render(request, 'box/create_employee_gmail.html', context)
                employee6.save()

                employee1.employee_gmail = employee6
                employee1.save()
                employee_gmails = Employee_Gmail.objects.all()
                eb = request.user.email
                for employee_gmail in employee_gmails:
                    if str(employee_gmail.email) == str(eb):

                        return HttpResponseRedirect('/box/'+ str(employee_gmail.id)+'/create_employee_private/')
            else:
                context = {
                     "form": form,
                     "form1": form1,
                 }
                return render(request, 'box/create_employee_gmail.html', context)
        else:
            emp_details = Employee_Gmail.objects.all()
            for emp_detail in emp_details:
                if str(request.user.email) == str(emp_detail.email):
                    return HttpResponseRedirect('/box/' + str(emp_detail.id) + '/create_employee_private/')


def create_employee_private(request, employee_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        e = get_object_or_404(Employee_Gmail, pk=employee_id)
        employee_privates = Employee_Private.objects.all()

        for employee_private11 in employee_privates:
            if str(employee_private11.employee_gmail.email)== str(e.email):
                return HttpResponseRedirect("/box/" + str(e.id) + "/further/")


        form2 = Employee_PrivateForm(request.POST or None, request.FILES or None)
        form4 = VehicleForm(request.POST or None, request.FILES or None)
        if all((form2.is_valid(), form4.is_valid())):
            employee2 = form2.save(commit=False)
            employee4 = form4.save(commit=False)
            employee2.employee_gmail = e
            employee4.employee_gmail = e

            employee2.resume = request.FILES['resume']
            file_type2 = employee2.resume.url.split('.')[-1]
            file_type2 = file_type2.lower()
            if file_type2 not in RESUME_FILE_TYPES:
                context = {
                    'e': e,

                    'employee2': employee2,

                    'employee4': employee4,
                    "form2": form2,

                    "form4": form4,
                    'error_message': 'Resume file must be pdf, PDF, or doc',
                }
                return render(request, 'box/create_employee_private.html', context)
            employee2.save()
            employee4.save()

            return HttpResponseRedirect("/box/" + str(e.id) + "/further/")
        else:
            context = {
                'e': e,
                "form2": form2,

                "form4": form4
            }
            return render(request, 'box/create_employee_private.html', context)


def further(request,employee_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:

        employee_gmails = Employee_Gmail.objects.all()
        employee_privates = Employee_Private.objects.all()
        e = get_object_or_404(Employee_Gmail, pk=employee_id)
        for employee_gmail in employee_gmails:
            for employee_private in employee_privates:
                if str(employee_gmail.email) == str(e.email) and str(employee_private.employee_gmail) == str(e.email):
                    emp = employee_gmail.firstname
                    query = request.GET.get("q")
                    if query:
                        employee_gmails = employee_gmails.filter(
                        Q(firstname__icontains=query) |
                        Q(lastname__icontains=query)
                        ).distinct()
                        return render(request, 'box/further.html', {
                        'employee_gmails': employee_gmails,
                        'employee_private': employee_private,
                        'emp':emp,
                            'e':e,
                        })
                    else:
                        return render(request, 'box/further.html', {'e':e,'employee_private': employee_private,'employee_gmails': employee_gmails, 'emp':emp })


def detail(request , employee_id,employee_gmail_id ):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        employee_gmail = get_object_or_404(Employee_Gmail, pk=employee_gmail_id)
        employee_publics= Employee_Public.objects.all()
        for employee_public in employee_publics:
            if str(employee_gmail.email) ==  str(employee_public.employee_gmail):
                employee_vechicles= Vehicle.objects.all()
                for employee_vechicle in employee_vechicles:
                    if str(employee_gmail.email) == str(employee_vechicle.employee_gmail):
                        return render(request, 'box/detail.html', {'employee_id_taken':employee_id_taken,'employee_gmail': employee_gmail,'employee_vechicle':employee_vechicle,'employee_public':employee_public})


def update (request, employee_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        return render (request,'box/update.html',{'employee_id_taken':employee_id_taken})


def update_public(request , employee_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        vehicles =Employee_Public.objects.all()
        for vehicle11 in vehicles:
            if str(vehicle11.employee_gmail.email) == str(employee_id_taken.email):
                form = Employee_PublicForm(request.POST or None, request.FILES or None,
                                   initial={'photo_logo': vehicle11.photo_logo,
                                            'mobile_number': vehicle11.mobile_number,
                                            'emergency_contact_number': vehicle11.emergency_contact_number,
                                            'emergency_contact_number1': vehicle11.emergency_contact_number1,
                                            'current_address': vehicle11.current_address,
                                            'field_of_intrest': vehicle11.field_of_intrest,
                                            })
                if form.is_valid():
                    update_public = form.save(commit=False)

                    Employee_Publics = Employee_Public.objects.all()
                    for Employee_Public1 in Employee_Publics:
                        if str(employee_id_taken.email) == str(Employee_Public1.employee_gmail.email):
                            Employee_Public1.photo_logo = update_public.photo_logo
                            Employee_Public1.mobile_number = update_public.mobile_number
                            Employee_Public1.emergency_contact_number = update_public.emergency_contact_number
                            Employee_Public1.emergency_contact_number1 = update_public.emergency_contact_number1
                            Employee_Public1.current_address = update_public.current_address
                            Employee_Public1.field_of_intrest = update_public.field_of_intrest
                            Employee_Public1.save()

                            return HttpResponseRedirect('/box/' + str(employee_id_taken.id) + '/update/')
                        context = {
                            'form': form,
                            'employee_id_taken': employee_id_taken,
                        }

                        return render(request, 'box/update_public.html', context)
                else:
                    context = {
                        'form': form,
                        'employee_id_taken': employee_id_taken,
                    }
                    return render(request,'box/update_public.html', context)


def update_private(request , employee_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        vehicles =Employee_Private.objects.all()
        for vehicle11 in vehicles:
            if str(vehicle11.employee_gmail.email) == str(employee_id_taken.email):
                form = Employee_PrivateForm(request.POST or None, request.FILES or None,
                                   initial={'date_of_birth': vehicle11.date_of_birth,
                                            'resume': vehicle11.resume,
                                            'permanent_address': vehicle11.permanent_address,
                                            'pan': vehicle11.pan,
                                            'passport_no': vehicle11.passport_no,
                                            'passport_expiry': vehicle11.passport_expiry,
                                            })
                if form.is_valid():
                    update_public = form.save(commit=False)

                    Employee_Publics = Employee_Private.objects.all()
                    for Employee_Public1 in Employee_Publics:
                        if str(employee_id_taken.email) == str(Employee_Public1.employee_gmail.email):
                            Employee_Public1.date_of_birth = update_public.date_of_birth
                            Employee_Public1.resume = update_public.resume
                            Employee_Public1.permanent_address = update_public.permanent_address
                            Employee_Public1.pan = update_public.pan
                            Employee_Public1.passport_no = update_public.passport_no
                            Employee_Public1.passport_expiry = update_public.passport_expiry
                            Employee_Public1.save()
                            return HttpResponseRedirect('/box/' + str(employee_id_taken.id) + '/update/')
                        context = {
                            'form': form,
                            'employee_id_taken': employee_id_taken,
                        }

                        return render(request, 'box/update_private.html', context)
                else:
                    context = {
                        'form': form,
                        'employee_id_taken': employee_id_taken,
                    }
                    return render(request,'box/update_private.html',context)


def update_vehicle (request , employee_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        vehicles = Vehicle.objects.all()
        for vehicle11 in vehicles:
            if str(vehicle11.employee_gmail.email)== str(employee_id_taken.email):
                form = VehicleForm(request.POST or None, request.FILES or None,initial={'vechicle_type': vehicle11.vechicle_type,'vechicle_model':vehicle11.vechicle_model,'vechicle_number':vehicle11.vechicle_number})
                if (form.is_valid()):
                    update_public = form.save(commit=False)

                    Employee_Publics = Vehicle.objects.all()
                    for Employee_Public1 in Employee_Publics:
                        if str(employee_id_taken.email) == str(Employee_Public1.employee_gmail.email):
                            Employee_Public1.vechicle_type = update_public.vechicle_type
                            Employee_Public1.vechicle_model = update_public.vechicle_model
                            Employee_Public1.vechicle_number = update_public.vechicle_number
                            Employee_Public1.save()
                            return HttpResponseRedirect("/box/" + str(employee_id_taken.id) + "/update/")
                context = {
                    'form': form,
                    'employee_id_taken': employee_id_taken,
                }

                return render(request, 'box/update_vehicle.html', context)


def logout_user(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        try:
            logout(request)
            form = UserForm(request.POST or None)
            context = {
            "form": form,
            }
        except:
            pass
        return render(request, 'box/logout.html', context)


def scheduling(request,employee_id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/box/login/")
        else:
            employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
            form = Interviewee_SchedulingForm(request.POST or None, request.FILES or None)
            form1 = InterviewForm(request.POST or None)

            if all((form.is_valid(), form1.is_valid())):
                employee = form.save(commit=False)
                employee.save()
                count = 0
                while count < 4:
                    count = count + 1
                    if form1.cleaned_data.get('interviewer_email_id'+str(count)):
                        feedback_detail = Feedback.objects.create()
                        feedback_detail.level = 'Level1'
                        feedback_detail.interviewee_detail = employee
                        feedback_detail.interview_date = form1.cleaned_data.get('interview_date')
                        feedback_detail.interview_time = form1.cleaned_data.get('interview_time')
                        feedback_detail.interviewer_email_id = form1.cleaned_data.get('interviewer_email_id' + str(count))
                        feedback_detail.save()

                c =0
                subject = 'Regarding Interview'
                message = 'Hey ' + str(employee.interviewee_name) + ' your interview is on ' + str(form1.cleaned_data.get('interview_date')) + ' at ' + str(form1.cleaned_data.get('interview_time')) + '. Please bring your supporting documents.'
                messagei = 'Hey, you have an interview scheduled on ' + str(form1.cleaned_data.get('interview_date')) + ' at ' + str(form1.cleaned_data.get('interview_time')) + '. The name of the candidate is ' + str(employee.interviewee_name)
                to_email = [employee.interviewee_email_id]
                send_mail(subject, message, settings.EMAIL_HOST_USER, to_email),

                to_email1 = form1.cleaned_data.get('interviewer_email_id1')
                if to_email1:
                    send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email1])

                to_email2 = form1.cleaned_data.get('interviewer_email_id2')
                if to_email2:
                    send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email2])

                to_email3 = form1.cleaned_data.get('interviewer_email_id3')
                if to_email3:
                    send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email3])
                messages.success(request, 'Interview details recorded and the required mails sent')

                return HttpResponseRedirect("/box/" + str(employee_id_taken.id) + "/" + str(employee.id) +"/scheduling2/")
            context = {
                'form': form,
                'form1': form1,
                'employee_id_taken': employee_id_taken,
            }
            return render(request, 'box/scheduling1.html', context)

def scheduling2 (request , employee_id,interviewee_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        interviewee_id_taken = get_object_or_404(Interviewee, pk=interviewee_id)
        form = IntervieweeForm(request.POST or None, initial={'interviewee_name': interviewee_id_taken.interviewee_name, 'interviewee_email_id': interviewee_id_taken.interviewee_email_id, 'job_profile': interviewee_id_taken.job_profile, 'interviewee_resume': interviewee_id_taken.interviewee_resume})
        form1 = InterviewForm(request.POST or None)

        if all((form.is_valid(), form1.is_valid())):
            employee = form.save(commit=False)

            count = 0
            while count < 4:
                count = count + 1
                if form1.cleaned_data.get('interviewer_email_id' + str(count)):
                    feedback_detail = Feedback.objects.create()
                    feedback_detail.level = 'Level2'
                    feedback_detail.interviewee_detail = interviewee_id_taken
                    feedback_detail.interview_date = form1.cleaned_data.get('interview_date')
                    feedback_detail.interview_time = form1.cleaned_data.get('interview_time')
                    feedback_detail.interviewer_email_id = form1.cleaned_data.get('interviewer_email_id' + str(count))
                    feedback_detail.save()

            subject = 'Regarding Interview'
            messagei = 'Hey, you have an interview scheduled on ' + str(
                form1.cleaned_data.get('interview_date')) + ' at ' + str(
                form1.cleaned_data.get('interview_time')) + '. The name of the candidate is ' + str(
                employee.interviewee_name)
            to_email1 = form1.cleaned_data.get('interviewer_email_id1')
            if to_email1:
                send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email1])

            to_email2 = form1.cleaned_data.get('interviewer_email_id2')
            if to_email2:
                send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email2])

            to_email3 = form1.cleaned_data.get('interviewer_email_id3')
            if to_email3:
                send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email3])
            messages.success(request, 'Interview details recorded and the required mails sent')

            return HttpResponseRedirect("/box/" + str(employee_id_taken.id) + "/" + str(interviewee_id_taken.id) + "/scheduling3/")
        context = {
            'form': form,
            'form1': form1,
            'employee_id_taken': employee_id_taken,
            'interviewee_id_taken':interviewee_id_taken,

        }
        return render(request, 'box/scheduling2.html', context)

def scheduling3 (request , employee_id,interviewee_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        interviewee_id_taken = get_object_or_404(Interviewee, pk=interviewee_id)
        form = IntervieweeForm(request.POST or None,
                               initial={'interviewee_name': interviewee_id_taken.interviewee_name,
                                          'interviewee_email_id': interviewee_id_taken.interviewee_email_id,
                                          'job_profile': interviewee_id_taken.job_profile,
                                          'interviewee_resume': interviewee_id_taken.interviewee_resume})
        form1 = InterviewForm(request.POST or None)

        if all((form.is_valid(), form1.is_valid())):
            employee = form.save(commit=False)

            count = 0
            while count < 4:
                count = count + 1
                if form1.cleaned_data.get('interviewer_email_id' + str(count)):
                    feedback_detail = Feedback.objects.create()
                    feedback_detail.level = 'Level3'
                    feedback_detail.interviewee_detail = interviewee_id_taken
                    feedback_detail.interview_date = form1.cleaned_data.get('interview_date')
                    feedback_detail.interview_time = form1.cleaned_data.get('interview_time')
                    feedback_detail.interviewer_email_id = form1.cleaned_data.get('interviewer_email_id' + str(count))
                    feedback_detail.save()
            subject = 'Regarding Interview'
            messagei = 'Hey, you have an interview scheduled on ' + str(
                form1.cleaned_data.get('interview_date')) + ' at ' + str(
                form1.cleaned_data.get('interview_time')) + '. The name of the candidate is ' + str(
                employee.interviewee_name)


            to_email1 = form1.cleaned_data.get('interviewer_email_id1')
            if to_email1:
                send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email1])

            to_email2 = form1.cleaned_data.get('interviewer_email_id2')
            if to_email2:
                send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email2])

            to_email3 = form1.cleaned_data.get('interviewer_email_id3')
            if to_email3:
                send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email3])
            messages.success(request, 'Interview details recorded and the required mails sent')

            return HttpResponseRedirect("/box/" + str(employee_id_taken.id) + "/further")
        context = {
            'form': form,
            'form1': form1,
            'employee_id_taken': employee_id_taken,
            'interviewee_id_taken': interviewee_id_taken,

        }
        return render(request, 'box/scheduling3.html', context)

def rescheduling(request, employee_id, interviewee_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        interviewee_id_taken = get_object_or_404(Interviewee, pk=interviewee_id)
        form = ReschedulingForm(request.POST or None)
        if form.is_valid():
            if str(form.cleaned_data.get('level')) == 'Level1':
                return HttpResponseRedirect("/box/" + str(employee_id_taken.id) + "/"+ str(interviewee_id)+"/rescheduling1/")
            elif str(form.cleaned_data.get('level')) == 'Level2':
                return HttpResponseRedirect("/box/" + str(employee_id_taken.id) + "/" + str(interviewee_id) + "/rescheduling2/")
            elif str(form.cleaned_data.get('level')) == 'Level3':
                return HttpResponseRedirect("/box/" + str(employee_id_taken.id) + "/" + str(interviewee_id) + "/rescheduling3/")
        else:
            return render(request, 'box/rescheduling.html',
                          {'form': form, 'employee_id_taken': employee_id_taken,
                           'interviewee_id_taken': interviewee_id_taken})

def rescheduling1(request, employee_id, interviewee_id):
    global earlier_date
    global earlier_time

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        interviewee_id_taken = get_object_or_404(Interviewee, pk=interviewee_id)
        feed_details = Feedback.objects.all()
        form = IntervieweeForm(request.POST or None,
                                 initial={'interviewee_name': interviewee_id_taken.interviewee_name,
                                          'interviewee_email_id': interviewee_id_taken.interviewee_email_id,
                                          'job_profile': interviewee_id_taken.job_profile,
                                          'interviewee_resume': interviewee_id_taken.interviewee_resume})
        form1 = InterviewForm(request.POST or None)

        if all((form.is_valid(), form1.is_valid())):
            employee = form.save(commit=False)

            count = 0

            for feed_detail in feed_details:
                if str(feed_detail.interviewee_detail.interviewee_email_id) == str(interviewee_id_taken.interviewee_email_id) and str(feed_detail.level) == 'Level1':
                    earlier_date = feed_detail.interview_date
                    earlier_time = feed_detail.interview_time
                    feed_detail.delete()

            while count < 4:
                count = count + 1
                if form1.cleaned_data.get('interviewer_email_id' + str(count)):
                    feedback_detail = Feedback.objects.create()
                    feedback_detail.level = 'Level1'
                    feedback_detail.interviewee_detail = interviewee_id_taken
                    feedback_detail.interview_date = form1.cleaned_data.get('interview_date')
                    feedback_detail.interview_time = form1.cleaned_data.get('interview_time')
                    feedback_detail.interviewer_email_id = form1.cleaned_data.get('interviewer_email_id' + str(count))
                    feedback_detail.save()

                subject = 'Regarding Interview'
                messagei = 'Hey, your interview of ' + str(
                    employee.interviewee_name) + ' has been rescheduled on ' + str(
                    form1.cleaned_data.get('interview_date')) + ' at ' + str(
                    form1.cleaned_data.get('interview_time')) + '. It was earlier Scheduled on ' + str(
                    earlier_date) + ' at ' + str(earlier_time) + '.'

                to_email1 = form1.cleaned_data.get('interviewer_email_id1')
                if to_email1:
                    send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email1])

                to_email2 = form1.cleaned_data.get('interviewer_email_id2')
                if to_email2:
                    send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email2])

                to_email3 = form1.cleaned_data.get('interviewer_email_id3')
                if to_email3:
                    send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email3])




            return HttpResponseRedirect("/box/" + str(employee_id_taken.id) + "/hr_all")
        context = {
            'form': form,
            'form1': form1,
            'employee_id_taken': employee_id_taken,
            'interviewee_id_taken': interviewee_id_taken,

        }
        return render(request, 'box/rescheduling_level1.html', context)

def rescheduling2(request, employee_id, interviewee_id):
    global earlier_date
    global earlier_time

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        interviewee_id_taken = get_object_or_404(Interviewee, pk=interviewee_id)
        feed_details = Feedback.objects.all()
        form = IntervieweeForm(request.POST or None,
                                 initial={'interviewee_name': interviewee_id_taken.interviewee_name,
                                          'interviewee_email_id': interviewee_id_taken.interviewee_email_id,
                                          'job_profile': interviewee_id_taken.job_profile,
                                          'interviewee_resume': interviewee_id_taken.interviewee_resume})
        form1 = InterviewForm(request.POST or None)

        if all((form.is_valid(), form1.is_valid())):
            employee = form.save(commit=False)

            count = 0

            for feed_detail in feed_details:
                if str(feed_detail.interviewee_detail.interviewee_email_id) == str(interviewee_id_taken.interviewee_email_id) and str(feed_detail.level) == 'Level2':
                    earlier_date = feed_detail.interview_date
                    earlier_time = feed_detail.interview_time
                    feed_detail.delete()

            while count < 4:
                count = count + 1
                if form1 .cleaned_data.get('interviewer_email_id' + str(count)):
                    feedback_detail = Feedback.objects.create()
                    feedback_detail.level = 'Level2'
                    feedback_detail.interviewee_detail = interviewee_id_taken
                    feedback_detail.interview_date = form1 .cleaned_data.get('interview_date')
                    feedback_detail.interview_time = form1 .cleaned_data.get('interview_time')
                    feedback_detail.interviewer_email_id = form1 .cleaned_data.get('interviewer_email_id' + str(count))
                    feedback_detail.save()

                subject = 'Regarding Interview'
                messagei = 'Hey, your interview of ' + str(
                    employee.interviewee_name) + ' has been rescheduled on ' + str(
                    form1 .cleaned_data.get('interview_date')) + ' at ' + str(
                    form1 .cleaned_data.get('interview_time')) + '. It was earlier Scheduled on ' + str(
                    earlier_date) + ' at ' + str(earlier_time) + '.'

                to_email1 = form1 .cleaned_data.get('interviewer_email_id1')
                if to_email1:
                    send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email1])

                to_email2 = form1 .cleaned_data.get('interviewer_email_id2')
                if to_email2:
                    send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email2])

                to_email3 = form1 .cleaned_data.get('interviewer_email_id3')
                if to_email3:
                    send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email3])




            return HttpResponseRedirect("/box/" + str(employee_id_taken.id) + "/hr_all")
        context = {
            'form': form,
            'form1': form1 ,
            'employee_id_taken': employee_id_taken,
            'interviewee_id_taken': interviewee_id_taken,

        }
        return render(request,'box/rescheduling_level2.html', context)

def rescheduling3(request, employee_id, interviewee_id):
    global earlier_date
    global earlier_time

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        interviewee_id_taken = get_object_or_404(Interviewee, pk=interviewee_id)
        feed_details = Feedback.objects.all()
        form = IntervieweeForm(request.POST or None,
                                 initial={'interviewee_name': interviewee_id_taken.interviewee_name,
                                          'interviewee_email_id': interviewee_id_taken.interviewee_email_id,
                                          'job_profile': interviewee_id_taken.job_profile,
                                          'interviewee_resume': interviewee_id_taken.interviewee_resume})
        form1 = InterviewForm(request.POST or None)
        if all((form.is_valid(), form1.is_valid())):
            employee = form.save(commit=False)

            count = 0

            for feed_detail in feed_details:
                if str(feed_detail.interviewee_detail.interviewee_email_id) == str(interviewee_id_taken.interviewee_email_id) and str(feed_detail.level) == 'Level3':
                    earlier_date = feed_detail.interview_date
                    earlier_time = feed_detail.interview_time
                    feed_detail.delete()

            while count < 4:
                count = count + 1
                if form1.cleaned_data.get('interviewer_email_id' + str(count)):
                    feedback_detail = Feedback.objects.create()
                    feedback_detail.level = 'Level3'
                    feedback_detail.interviewee_detail = interviewee_id_taken
                    feedback_detail.interview_date = form1.cleaned_data.get('interview_date')
                    feedback_detail.interview_time = form1.cleaned_data.get('interview_time')
                    feedback_detail.interviewer_email_id = form1.cleaned_data.get('interviewer_email_id' + str(count))
                    feedback_detail.save()

                subject = 'Regarding Interview'
                messagei = 'Hey, your interview of ' + str(
                    employee.interviewee_name) + ' has been rescheduled on ' + str(
                    form1.cleaned_data.get('interview_date')) + ' at ' + str(
                    form1.cleaned_data.get('interview_time')) + '. It was earlier Scheduled on ' + str(
                    earlier_date) + ' at ' + str(earlier_time) + '.'

                to_email1 = form1.cleaned_data.get('interviewer_email_id1')
                if to_email1:
                    send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email1])

                to_email2 = form1.cleaned_data.get('interviewer_email_id2')
                if to_email2:
                    send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email2])

                to_email3 = form1.cleaned_data.get('interviewer_email_id3')
                if to_email3:
                    send_mail(subject, messagei, settings.EMAIL_HOST_USER, [to_email3])




            return HttpResponseRedirect("/box/" + str(employee_id_taken.id) + "/hr_all")
        context = {
            'form': form,
            'form1': form1,
            'employee_id_taken': employee_id_taken,
            'interviewee_id_taken': interviewee_id_taken,

        }
        return render(request, 'box/rescheduling_level3.html', context)

def feedback(request,employee_id,interviewee_id,feedback_id ):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        interviewee = get_object_or_404(Interviewee, pk=interviewee_id)
        feedback_id_taken = get_object_or_404(Feedback, pk=feedback_id)
        feedbacks = Feedback.objects.all()
        form = Employee1_FeedbackForm(request.POST or None,
                                          initial={'interviewee_name': interviewee.interviewee_name,
                                                   'interviewee_email_id': interviewee.interviewee_email_id})
        form1 = Employee_FeedbackForm(request.POST or None,initial = {'interview_date': feedback_id_taken.interview_date,'level':feedback_id_taken.level , 'feedback':feedback_id_taken.feedback})
        if all((form.is_valid(), form1.is_valid())):
            info = form.save(commit=False)
            feedinfo = form1.save(commit=False)
            for feedback1 in feedbacks:
                if all((str(interviewee.interviewee_email_id) == str(feedback1.interviewee_detail.interviewee_email_id),
                        str(employee_id_taken.email) == str(feedback1.interviewer_email_id), str(feedback_id_taken.level)==str(feedback1.level))):
                    feedback1.feedback = feedinfo.feedback
                    feedback1.save()
                    return HttpResponseRedirect("/box/" + str(employee_id_taken.id) + "/interview_details/")
        context = {
            'form': form,
            'form1': form1,
            'employee_id_taken': employee_id_taken,
            'feedback_id_taken':feedback_id_taken,

        }
        return render(request, 'box/feedback.html', context)

def interview_details(request,employee_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        employee_privates = Employee_Private.objects.all()
        interviewees = Interviewee.objects.all()
        count = 0
        feedbacks = Feedback.objects.all()

        for feedback11 in feedbacks:
            if str(feedback11.interviewer_email_id) == str(employee_id_taken.email):
                count = 1

        for employee_private in employee_privates:
            if str(employee_private.employee_gmail.email) == str(employee_id_taken.email):
                e = employee_private.hr

        query = request.GET.get("q")
        if query:
            interviewees = interviewees.filter(
                Q(interviewee_name__icontains=query)
            ).distinct()
            feedbacks = Feedback.objects.order_by('interview_date').filter(
                Q(interview_date__icontains=query)
            ).distinct()
            return render(request, 'box/inter_details.html', {'e':e,'count':count,'employee_private':employee_privates,'employee_id_taken':employee_id_taken,'interviewees':interviewees,'feedbacks': feedbacks})

        return render(request, 'box/inter_details.html',{'e':e,'count':count,'employee_private':employee_privates,'employee_id_taken':employee_id_taken,'interviewees':interviewees,'feedbacks': Feedback.objects.order_by('interview_date')})

def status (request, employee_id,interviewee_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        interviewee_id_taken = get_object_or_404(Interviewee, pk=interviewee_id)
        feedback_details = Feedback.objects.all()
        fe="12:00"
        fed="2016-05-01"
        form = StatusForm(request.POST or None)
        if form.is_valid():
            interviewee_id_taken.status = form.cleaned_data.get('status')
            if str(form.cleaned_data.get('status')) == 'Second Round':
                for feedback_detail in feedback_details:
                    if all((str(feedback_detail.interviewee_detail.interviewee_email_id)==str(interviewee_id_taken.interviewee_email_id) , str(feedback_detail.level)== "Level2")):
                        fe = str(feedback_detail.interview_time)
                        fed = str(feedback_detail.interview_date)
                subject = 'Regarding Interview'
                messagei = 'Hey, your second round of interview is scheduled on ' + fed + ' at ' + fe + '. The name of the candidate is ' + str(
                        interviewee_id_taken.interviewee_name)
                to_email = [interviewee_id_taken.interviewee_email_id]
                send_mail(subject, messagei, settings.EMAIL_HOST_USER, to_email),

                messages.success(request, 'Interview details recorded and the required mails sent')
                interviewee_id_taken.save()

            elif str(form.cleaned_data.get('status')) == 'Third Round':
                for feedback_detail in feedback_details:
                    if all((str(feedback_detail.interviewee_detail.interviewee_email_id) == str(interviewee_id_taken.interviewee_email_id), str(feedback_detail.level) == "Level3")):
                        fe = str(feedback_detail.interview_time)
                        fed = str(feedback_detail.interview_date)

                interviewee_id_taken.status = form.cleaned_data.get('status')

                subject = 'Regarding Interview'
                messagei = 'Hey, your third round of interview is scheduled on ' +fed + ' at ' + fe + '. The name of the candidate is ' + str(interviewee_id_taken.interviewee_name)
                to_email = [interviewee_id_taken.interviewee_email_id]
                send_mail(subject, messagei, settings.EMAIL_HOST_USER, to_email),

                messages.success(request, 'Interview details recorded and the required mails sent')
                interviewee_id_taken.save()

            elif str(form.cleaned_data.get('status')) == 'hired':
                interviewee_id_taken.status = form.cleaned_data.get('status')
                interviewee_id_taken.save()

            elif str(form.cleaned_data.get('status')) == 'Rejected':
                interviewee_id_taken.status = form.cleaned_data.get('status')
                interviewee_id_taken.save()
                subject = 'Regarding Interview'
                for feedback_detail in feedback_details:
                    if all((str(feedback_detail.interviewee_detail.interviewee_email_id) == str(interviewee_id_taken.interviewee_email_id),str(feedback_detail.feedback)== 'Interview not yet done')):
                        feedback_detail.feedback = str("REJECTED")
                        feedback_detail.save()
                        messagei = 'Hey, your interview scheduled on ' + str(
                            feedback_detail.interview_date) + ' at ' + str(
                            feedback_detail.interview_time) + 'has been cancelled . The candidate ' + str(
                            interviewee_id_taken.interviewee_name) + ' has been REJECTED.'
                        to_email = [feedback_detail.interviewer_email_id]
                        send_mail(subject, messagei, settings.EMAIL_HOST_USER, to_email)


            elif str(form.cleaned_data.get('status')) == 'On Hold':
                interviewee_id_taken.status = form.cleaned_data.get('status')
                interviewee_id_taken.save()

            return HttpResponseRedirect("/box/" + str(employee_id_taken.id) + "/hr_all/")
        else:
            return render(request, 'box/status.html',
                          {'form': form, 'employee_id_taken': employee_id_taken, 'interviewee_id_taken': interviewee_id_taken})

def inter_all(request, employee_id, interviewee_id ,feedback_id):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/box/login/")
        else:
            employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
            feedback_id_taken = get_object_or_404(Feedback, pk=feedback_id)
            interviewee = get_object_or_404(Interviewee, pk=interviewee_id)
            interviewer_details = Feedback.objects.all()
            return render(request, 'box/inter_all.html',
                                  { 'feedback_id_taken':feedback_id_taken,'employee_id_taken': employee_id_taken, 'interviewee': interviewee,
                                   'interviewer_details': interviewer_details})

def hr_all(request, employee_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        interviewee_details = Interviewee.objects.all()
        feedbacks = Feedback.objects.all()
        query = request.GET.get("q")
        if query:
            interviewee_details = interviewee_details.filter(
                Q(interviewee_name__icontains=query)
            ).distinct()
            return render(request,  'box/hr_all.html', {
                'interviewee_details': interviewee_details,
                'employee_id_taken': employee_id_taken,
                'feedbacks': feedbacks,
            })

        return render (request, 'box/hr_all.html',{'feedbacks':feedbacks,'employee_id_taken':employee_id_taken,'interviewee_details':interviewee_details})

def hr_inter_all(request,employee_id,interviewee_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/box/login/")
    else:
        employee_id_taken = get_object_or_404(Employee_Gmail, pk=employee_id)
        interviewee = get_object_or_404(Interviewee, pk=interviewee_id)
        return render(request, 'box/hr_inter_all.html',{'employee_id_taken': employee_id_taken,'interviewee': interviewee,'interviewer_details': Feedback.objects.order_by('level')})


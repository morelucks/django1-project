from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Meetup, Participant
from .forms import RegistrationForm
# Create your views here.
def index(request):
    meetups= Meetup.objects.all()
    return render (request, 'meetups/index.html', {
        'meetups':meetups
    })

def meetups_details(request, meetup_slug ):
    try:
        selected_meetup = Meetup.objects.get(slug=meetup_slug)

        if request.method =='GET':
            registration_form=RegistrationForm()
        else:
            registration_form=RegistrationForm(request.POST)
            if registration_form.is_valid():
                user_email = registration_form.cleaned_data['email']
                participant,_=Participant.objects.get_or_create(email=user_email)
                selected_meetup.participant.add(participant)
                return redirect('confirm-registration')
        return render(request, 'meetups/m_details.html', {
                    'meetup_found':True,
                    'meetup':selected_meetup, 
                    'form':registration_form  
                })  
    except Exception as exc:
        print(exc)
        return render(request, 'meetups/m_details.html',{
            'meetup_found':False
        } )
def confirm_registration(request):
    return render(request, 'meetups/registration-success.html')
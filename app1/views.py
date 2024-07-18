from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

from app1.models import Profile
from pro1 import settings


# Create your views here.
def index(request):
    return render(request, 'index.html')



def testing(request):
    return render(request, 'testing.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        place = request.POST.get('place')
        if email and password:
            if User.objects.filter(email=email).exists():
                return render(request, 'signup.html')
            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )
                profile = Profile.objects.create(
                    user=user,
                    name=name,
                    phone=phone,
                    place=place
                )
                return redirect('signin')
        else:
            return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'signin.html', {'error': 'Invalid email or password.'})

        if user.check_password(password):
            auth.login(request, user)
            return redirect('destination')  # Replace 'testing' with your desired redirect URL
        else:
            return render(request, 'signin.html', {'error': 'Invalid email or password.'})

    # This line ensures that even for GET requests, the view returns a response
    return render(request, 'signin.html')
#showing name of user in destination page
def destination(request):
    user=request.user
    profile_data=Profile.objects.filter(user_id=user.id)
    return render(request,'destination.html',{'profile_data':profile_data})


def form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        destination = request.POST.get('destination')
        date = request.POST.get('date')

        # Print statements for debugging
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Destination: {destination}")
        print(f"Date: {date}")

        # Basic form validation
        if not (name and email and destination and date):
            return HttpResponseBadRequest('All fields are required')

        # Send email
        subject = f'Booking request for {destination}'
        message = (f'Hi {name},\n\nThank you for booking your destination with Travelera.\n\n'
                   f'Destination: {destination}\n'
                   f'Date: {date}\n\n'
                   f'We will contact you soon.')
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]

        try:
            send_mail(subject, message, from_email, to_email, fail_silently=False)
        except Exception as e:
            print(f"Error sending email: {e}")
            return HttpResponseBadRequest('Error sending email. Please try again later.')

        # Optionally, redirect to a success page or render a success message
        return render(request, 'index.html', {'name': name})
    else:
        return redirect('destination')

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from G4Marketplace import settings
from item.models import Category, Item
from .forms import SignupForm
from .tokens import account_activation_token
from verify_email.email_handler import send_verification_email




# Create your views here.
def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    user_color = request.session.get('user_color', None)
    categories = Category.objects.all()
    context = {
        'items': items,
        'categories': categories,
        'user_color': user_color if user_color else 'primary'
    }
    return render(request, 'core/index.html', context)

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')
def terms_of_use(request):
    return render(request, 'core/terms_of_use.html')
def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send email for account activation
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('core/acc_active_email.html', {
                'user': user.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),  # Use default token generator
                'protocol': 'https' if request.is_secure() else 'http'
            })
            email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[user.email])
            email.send()

            messages.success(request, 'Please confirm your email address to complete the registration')
            return redirect('/login/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})

def activateEmail(request, user, email):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    user = get_user_model().objects.get(email=email)
    message = render_to_string('core/acc_active_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject,message, settings.EMAIL_HOST_USER, to=[email])
    if email.send():
        messages.success(request, 'Please confirm your email address to complete the registration')
    else:
        messages.error(request, 'Failed to send email confirmation. Please try again later.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request, 'Thank you for your email confirmation.')
        return redirect('/login/')
    else:
        messages.error(request, 'Activation link is invalid!')



def logout(request):
    return redirect(request, 'core/login.html')

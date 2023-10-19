from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django_registration.forms import User

from G4Marketplace import settings
from item.models import Category, Item
from .forms import SignupForm
from .models import Contact
from .tokens import account_activation_token
from verify_email.email_handler import send_verification_email

from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_encode

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
    if request.method=="POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        comment = request.POST.get("comment")
        query = Contact(name=name, email=email, subject=subject, comment=comment)
        query.save()
        # messages.info(request, "Thanks For Reaching Us! We will get back you soon...")
        return redirect('/contact')
    return render(request, 'core/contact.html')


def about(request):
    return render(request, 'core/about.html')


def terms_of_use(request):
    return render(request, 'core/terms_of_use.html')


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


#GINALAW
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Store the email in the session to use for resending the activation link
            request.session['user_email'] = user.email

            # Send activation email
            send_activation_email(request, user)

            return redirect('request_new_activation_link')

    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})


def send_activation_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('core/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': user.pk,  # No need for encoding here
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })

    email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[user.email])

    if email.send():
        messages.success(request, 'Please confirm your email address to complete the registration')
    else:
        messages.error(request, 'Failed to send email confirmation. Please try again later.')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()  # Decode the UID
        user = User.objects.get(pk=user_id)
    except (User.DoesNotExist, ValueError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation.')
        return redirect('login')  # You can redirect to your login page here

    messages.error(request, 'Activation link is invalid!')
    return HttpResponse('Activation link is invalid.')



def request_new_activation_link(request):
    if request.user.is_authenticated:
        # If the user is logged in, redirect them to the index page or any other page as desired.
        return redirect('index')  # Redirect to the 'index' page or another page

    # Check the number of resend attempts stored in the session
    resend_attempts = request.session.get('resend_attempts', 0)

    if resend_attempts >= 3:
        # If the user has reached the resend limit, you can redirect them to a specific page or show an error message.
        # For example, you can redirect to the index page with an error message.
        messages.error(request, 'You have reached the maximum number of resend attempts.')
        return redirect('signup')  # Redirect to the 'index' page or another page

    user_email = request.session.get('user_email')
    if user_email:
        try:
            user = User.objects.get(email=user_email)
            if not user.is_active:
                uid = urlsafe_base64_encode(str(user.pk).encode())  # Encode the UID
                token = account_activation_token.make_token(user)
                activation_link = f"{request.scheme}://{request.get_host()}/activate/{uid}/{token}/"
                mail_subject = 'Activate your account.'
                message = render_to_string('core/acc_active_email.html', {
                    'user': user,
                    'domain': request.get_host(),
                    'uid': uid,
                    'token': token,
                    'activation_link': activation_link,
                })

                email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[user.email])

                if email.send():
                    # Increment the resend attempts count
                    resend_attempts += 1
                    request.session['resend_attempts'] = resend_attempts
                    messages.success(request, 'A new activation link has been sent to your email address.')
                else:
                    messages.error(request, 'Failed to send email confirmation. Please try again later.')
            else:
                messages.warning(request, 'Your account is already active.')
        except User.DoesNotExist:
            messages.error(request, 'User with that email address does not exist')
    else:
        messages.error(request, 'User email not found in the session.')

    return render(request, 'core/request_activation_link.html')



def logout(request):
    return redirect(request, 'core/login.html')
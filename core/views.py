from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
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
    contacts = None  # Initialize the variable outside of the if block

    if request.user.is_superuser:
        contacts = Contact.objects.all().order_by('created_at')

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        comment = request.POST.get("comment")
        query = Contact(name=name, email=email, subject=subject, comment=comment)
        query.save()
        # messages.info(request, "Thanks For Reaching Us! We will get back to you soon...")
        return redirect('/contact')

    return render(request, 'core/contact.html', {'contacts': contacts})

# def contact_list(request):
#     queryset = Contact.objects.all().order_by('created_at')
#     paginator = Paginator(queryset, 10)  # Show 25 contacts per page
#
#     page= request.GET.get('page')
#     try:
#         contacts= paginator.page('page')
#     except PageNotAnInteger:
#         contacts= paginator.page(1)
#     except EmptyPage:
#         contacts= paginator.page(paginator.num_pages)
#
#     context = {
#         "object_list": queryset,
#         "contacts": contacts,
#     }
#     return render(request, "core/contact_list.html", context)


def send_email(request, subject, email, name):
    subject = ('Re:' + subject)
    email = email
    name = name
    # comment = comment
    print(subject)

    if request.method == "POST":
        print("request.POST")
        message = request.POST.get("message")
        message_data = {
            'name': name,
            'email': email,
            'comment': message,
            # 'comment': comment,
            'subject': subject,

        }
        html_message = render_to_string('core/email_template.html', message_data)
        plain_message = strip_tags(html_message)

        if subject and message and email:
            try:
                send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [email], html_message=html_message)
                return redirect('/')
                # return render(request, 'core/contact.html', {'message': 'Message sent successfully'})
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
                # return render("core:contact-list")
                # return redirect('success')
        else:
            return HttpResponse('Invalid form data')
    context = {
        'subject': subject,
        'email': email,
        'name': name,
    }
    return render(request, 'dashboard/email_response.html', context) #eto yung wala mo kanina. kaya kahit ano
#mangyare sa code ma rereceive nya is None kase walang return mismo ung Function
#
# bute sir need ng context pa kung may message data na po?
# kase ung context need natin irender dun sa form na gngwa which is eto




def about(request):
    return render(request, 'core/about.html')


def terms_of_use(request):
    return render(request, 'core/terms_of_use.html')


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


#GINALAW
from django.contrib.auth import login

def signup(request):
    if request.user.is_authenticated: return redirect('index')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            # Send activation email
            send_verification_email(request, form)
            return redirect('request_new_activation_link')

    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = uidb64  # No need for decoding here
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation.')
        return redirect('login')

    messages.error(request, 'Activation link is invalid!')
    return HttpResponse('Activation link is invalid.')

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

def request_new_activation_link(request):
    if request.user.is_authenticated: return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                send_activation_email(request, user)
                messages.success(request, 'A new activation link has been sent to your email address.')
            else:
                messages.warning(request, 'Your account is already active.')
        except User.DoesNotExist:
            messages.error(request, 'User with that email address does not exist.')

    return render(request, 'core/request_activation_link.html')



def logout(request):
    return redirect(request, 'core/login.html')







def login_required_redirect(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return function(request, *args, **kwargs)
    return wrap



from django.contrib.auth        import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts           import render, redirect
from django.template.loader     import render_to_string
from django.utils               import six
from django.utils.encoding      import force_text, force_bytes
from django.utils.http          import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.exceptions     import PermissionDenied
from warehouse.models           import *
from registration.forms         import *


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.username) + six.text_type(timestamp) + six.text_type(user.is_active)


def register(request):
    if request.user.is_authenticated:
        raise PermissionDenied("Please log out before registering.")
    registration_form = RegistrationForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and registration_form.is_valid():
        user = registration_form.save(commit=False)
        user.is_active = False

        subject = render_to_string("registration/register_subject.txt", {})
        message = render_to_string("registration/register_email.html", {
            'user': user,
            'domain': request.build_absolute_uri('/')[:-1],
            'uid': urlsafe_base64_encode(force_bytes(user.username)).decode(),
            'token': AccountActivationTokenGenerator().make_token(user),
        })
        user.email_user(subject, message)

        user.save()
        return register_done(request)

    return render(request, "registration/register_form.html", {'form':registration_form})


def register_done(request):
    return render(request, "registration/register_done.html", locals())


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(username=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and AccountActivationTokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('warehouse:home')
    else:
        return render(request, "registration/register_error.html")

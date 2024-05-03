from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from datetime import datetime, timedelta


from .forms import SignUpForm, LoginForm, ProfileForm, ContactForm
from .models import Profile, Contact


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
              
            return redirect("news:index")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})


def loginuser(request):
    error_message = None
    if request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is None:
            error_message = "Username or password didn't match"
        else:
            login(request, user)
            return redirect(to="users:profile")

    return render(request, "users/login.html", context={"form": LoginForm(), "error_message": error_message})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to="news:index")


@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("users:profile")
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, "users/profile.html", context={"profile": profile, "profile_form": profile_form})


@login_required
def contact_list(request):
    user_contacts = Contact.objects.filter(user=request.user)
    return render(request, "users/contacts.html", {"contacts": user_contacts})


@login_required
def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect("users:contacts")
    else:
        form = ContactForm()
    return render(request, "users/contact_create.html", {"form": form})



def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect("users:contacts")
    else:
        form = ContactForm(instance=contact)
    return render(request, "users/contact_edit.html", {"form": form})


def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        contact.delete()
        return redirect("users:contacts")
    return render(request, "users/contact_confirm_delete.html", {"contact": contact})
    
def upcoming_birthdays(request):
    days = int(request.GET.get('days', 7))
    current_date = datetime.now().date()
    future_date = current_date + timedelta(days=days)
    
    upcoming_contacts = Contact.objects.filter(
        birthday__range=[current_date, future_date]
    ).order_by("birthday")
    
    return render(request, "users/upcoming_birthdays.html", {
        "upcoming_contacts": upcoming_contacts,
        "days": days
    })


def contact_search(request):
    query = request.GET.get('query')
    if query:
      
        contacts = Contact.objects.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query) |
            Q(birthday__icontains=query) 
        )
    else:
        contacts = Contact.objects.all()
    return render(request, 'users/contacts.html', {'contacts': contacts})

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = "users/password_reset_subject.txt"

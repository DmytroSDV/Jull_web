import cloudinary.uploader
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
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
from django.utils import timezone
from app_photo.models import Picture
today = timezone.now().date()
yesterday = today - timezone.timedelta(days=1)

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
        # else:
        #     # Обработка ошибок для отдельных полей
        #     for field in form.errors:
        #         for error in form.errors[field]:
        #             messages.error(request, f"{field}: {error}")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})


def loginuser(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:profile')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please enter both username and password.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to="news:index")


today = timezone.now().date()
yesterday = today - timezone.timedelta(days=1)

@login_required
def profile(request):
    user = request.user
    contacts_count = Contact.objects.filter(user=user).count()
    current_time = datetime.now()
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)


    user.last_profile_visit = timezone.now()
    user.save()

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("users:profile")
    else:
        profile_form = ProfileForm(instance=profile)
    last_login_time = user.last_login
    context = {
        "profile": profile,
        "profile_form": profile_form,
        "contacts_count": contacts_count,
        "last_login_time": last_login_time,
        "current_time": current_time,
    }
    return render(request, "users/profile.html", context=context)


@login_required
def contact_list(request,page=1):
    user_contacts = Contact.objects.all()
    user = request.user
    user_contacts = Contact.objects.filter(user=user.id)
    paginator = Paginator(user_contacts, 5)
    try:
        user_contacts = paginator.page(page)
    except PageNotAnInteger:
        user_contacts = paginator.page(1)
    except EmptyPage:
        user_contacts = paginator.page(paginator.num_pages)
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

        # messages.success(request, 'Contact successfully deleted.')
        
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
def contact_confirm_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, 'users/contact_confirm_delete.html', {'contact': contact})

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = "users/password_reset_subject.txt"



@login_required
def add_avatar(request):
    if request.method == 'POST':
        user = request.user
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            avatar_file = request.FILES.get('avatar')

            uploaded_file = cloudinary.uploader.upload(avatar_file, resource_type="image")
            profile = Profile.objects.get_or_create(user=user)[0]
            profile.avatar = uploaded_file['url']
            profile.save()
            messages.success(request, "Avatar successfully changed", extra_tags='success')
            return redirect('users:profile')
        else:
            messages.error(request, "You didn't choose the file")
    return render(request, "users/change_avatar_profile.html")


def choose_new_avatar(request):
    return render(request, "users/change_avatar_profile.html")


def some_view(request):
    request_paths = ['/users/login/', '/users/signup/']
    return render(request, 'base_form.html', {'request_paths': request_paths})
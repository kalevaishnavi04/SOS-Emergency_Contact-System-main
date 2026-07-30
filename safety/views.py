import os
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from .models import EmergencyContact


TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "YOUR_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "YOUR_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")


def get_twilio_client():
    """Create the Twilio client lazily so a missing/placeholder key
    doesn't crash the whole app at import time."""
    return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_alert(message, phone):
    client = get_twilio_client()
    phone = "".join(phone.split())
    to_number = "whatsapp:+91" + phone.replace("+91", "").lstrip("+")
    client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        body=message,
        to=to_number,
    )


@login_required(login_url='login')
def home(request):
    contacts = EmergencyContact.objects.filter(user=request.user)
    return render(request, "home.html", {"contacts": contacts})


def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken.")
            return render(request, "register.html")

        user = User.objects.create_user(username=username, password=password)
        auth_login(request, user)
        messages.success(request, "Account created! You're logged in.")
        return redirect('home')

    return render(request, "register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            return redirect('home')

        messages.error(request, "Invalid username or password.")
        return render(request, "login.html")

    return render(request, "login.html")


def logout_user(request):
    auth_logout(request)
    return redirect('login')


@login_required(login_url='login')
def add_contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        place = request.POST.get('place', '').strip()

        if not name or not phone:
            messages.error(request, "Name and phone number are required.")
        else:
            phone = "".join(phone.split())  # remove any internal spaces
            if not phone.startswith("+"):
                phone = "+91" + phone

            EmergencyContact.objects.create(
                user=request.user,
                name=name,
                phone=phone,
                place=place,
            )
            messages.success(request, f"{name} added as an emergency contact.")
            return redirect('add_contact')

    contacts = EmergencyContact.objects.filter(user=request.user)
    return render(request, "add_contact.html", {"contacts": contacts})


@login_required(login_url='login')
def delete_contact(request, contact_id):
    contact = EmergencyContact.objects.filter(id=contact_id, user=request.user).first()

    if not contact:
        messages.error(request, "Contact not found.")
    else:
        name = contact.name
        contact.delete()
        messages.success(request, f"{name} was removed from your emergency contacts.")

    return redirect('add_contact')


@login_required(login_url='login')
def sos_trigger(request):
    user = request.user

    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    place = request.GET.get('place')

    if not lat or not lon:
        return JsonResponse(
            {"status": "error", "message": "Location (lat/lon) missing. Please allow location access."},
            status=400,
        )

    location_link = f"https://maps.google.com/?q={lat},{lon}"
    contacts = EmergencyContact.objects.filter(user=user)

    if not contacts.exists():
        return JsonResponse(
            {"status": "error", "message": "No emergency contacts saved yet. Add one first."},
            status=400,
        )

    message = (
        f"🚨 SOS ALERT 🚨\n"
        f"User: {user.username}\n\n"
        f"Location: {location_link}\n"
        f"Place: {place if place else 'Unknown'}"
    )

    sent, failed = [], []
    for contact in contacts:
        try:
            send_alert(message, contact.phone)
            sent.append(contact.name)
        except TwilioRestException as exc:
            failed.append({"name": contact.name, "error": str(exc)})

    return JsonResponse({
        "status": "SOS processed",
        "location": location_link,
        "sent_to": sent,
        "failed": failed,
    })

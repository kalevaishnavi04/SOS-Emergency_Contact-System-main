# 🚨 SOS Emergency Contact & Location Tracking System

A Django-based emergency safety application that sends SOS alerts with live location to saved emergency contacts using the Twilio WhatsApp API.

## 🔥 Features
* User registration & login
* Add / manage emergency contacts
* One-tap SOS button with live GPS location
* Google Maps location link sent over WhatsApp
* Twilio WhatsApp integration
* Session-based authentication

## 🛠️ Technologies Used
* Python 3 + Django 5.2
* SQLite (default dev database)
* Twilio API (WhatsApp)
* HTML / CSS (no frontend framework needed)

## 📍 How It Works
1. User registers and logs in
2. Adds one or more emergency contacts (name, phone, place)
3. Taps the **SOS** button on the home page
4. Browser fetches live GPS coordinates
5. Server sends a WhatsApp message with a Google Maps link to every saved contact

## 🚀 Installation & Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/kalevaishnavi04/SOS-Emergency_Contact-System
cd SOS-Emergency_Contact-System

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate       # on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# then open .env and fill in your real Twilio credentials

# 5. Apply database migrations
python manage.py migrate

# 6. Create an admin user (optional, for /admin/)
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser, register an account, add an emergency contact, and try the SOS button.

## 🔑 Twilio Setup (WhatsApp Sandbox)
1. Create a free account at https://www.twilio.com
2. Go to **Messaging → Try it out → Send a WhatsApp message** to activate the sandbox
3. Copy your **Account SID** and **Auth Token** from the Twilio console
4. Put them in your `.env` file:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
   ```
5. Each recipient must first send the Twilio sandbox join code to the sandbox WhatsApp number, or messages won't be delivered.

## ⚠️ Important
* Never commit your real `.env` file or Twilio credentials to GitHub — `.env` is already in `.gitignore`.
* This project uses SQLite and `DEBUG=True` by default, which is fine for local development only. For a real deployment, set `DJANGO_DEBUG=False`, use a proper database, and set `DJANGO_ALLOWED_HOSTS`.

## 📁 Project Structure
```
SOS-Emergency_Contact-System/
├── manage.py
├── requirements.txt
├── .env.example
├── safety_project/       # Django project settings & URLs
└── safety/               # Main app: models, views, templates
    ├── models.py         # EmergencyContact, SOSAlert
    ├── views.py          # auth, add contact, SOS trigger
    ├── urls.py
    ├── templates/
    └── ...
```

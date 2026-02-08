# Email & SMS Configuration Guide

This guide will help you set up email verification and SMS phone verification for your M&R Motors application.

## 📧 Email Setup (Gmail)

### Step 1: Create a Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Select **Security** from the left menu
3. Under "How you sign in to Google," select **2-Step Verification** (you must enable this first)
4. At the bottom, select **App passwords**
5. Select **Mail** and **Other (Custom name)**
6. Name it "M&R Motors" and click **Generate**
7. Copy the 16-character password (you'll need this in Step 2)

### Step 2: Add Email Variables to Vercel

1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Select your **m-r-motors** project
3. Go to **Settings** → **Environment Variables**
4. Add the following variables:

```
EMAIL_BACKEND = django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = your-gmail@gmail.com
EMAIL_HOST_PASSWORD = your-16-char-app-password
DEFAULT_FROM_EMAIL = M&R Motors <your-gmail@gmail.com>
```

**Replace:**
- `your-gmail@gmail.com` with your actual Gmail address
- `your-16-char-app-password` with the password from Step 1

5. Click **Save** for each variable
6. Redeploy your application (it will redeploy automatically after saving)

---

## 📱 SMS Setup (Twilio)

### Step 1: Create a Twilio Account

1. Go to: https://www.twilio.com/try-twilio
2. Sign up for a free account (no credit card required for trial)
3. Verify your email and phone number
4. You'll get **$15 in free credits** for testing

### Step 2: Get Your Twilio Credentials

1. Go to the Twilio Console: https://console.twilio.com/
2. Find your **Account SID** and **Auth Token** on the dashboard
3. Click **Get a Trial Number** or go to **Phone Numbers** → **Manage** → **Buy a number**
4. Select a phone number (with SMS capability)
5. Copy your:
   - Account SID
   - Auth Token
   - Phone Number (in E.164 format, e.g., +14155552671)

### Step 3: Add Twilio Variables to Vercel

1. Go to your Vercel dashboard
2. Select your **m-r-motors** project
3. Go to **Settings** → **Environment Variables**
4. Add the following variables:

```
TWILIO_ACCOUNT_SID = your-account-sid
TWILIO_AUTH_TOKEN = your-auth-token
TWILIO_PHONE_NUMBER = +1234567890
```

**Replace:**
- `your-account-sid` with your Twilio Account SID
- `your-auth-token` with your Twilio Auth Token
- `+1234567890` with your Twilio phone number (include the +)

5. Click **Save** for each variable
6. Redeploy your application

### Step 4: Verify Phone Numbers (Trial Account)

**Important:** Twilio trial accounts can only send SMS to verified phone numbers.

To verify a phone number:
1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified
2. Click **Add a new number**
3. Enter the phone number you want to verify
4. Enter the verification code sent to that number

For production (paid account), you can send to any number without verification.

---

## 🧪 Testing

### Test Email Verification:
1. Register a new account or go to your profile
2. Click "Verify Now" next to email
3. Check your email inbox for a 6-digit code
4. Enter the code on the verification page

### Test SMS Verification:
1. Go to your profile
2. Add a phone number (including country code)
3. Click "Verify Now" next to phone
4. Check your phone for an SMS with a 6-digit code
5. Enter the code on the verification page

---

## 💰 Pricing

### Gmail (Free)
- ✅ Completely free
- ✅ Up to 500 emails per day
- ✅ Perfect for small to medium projects

### Twilio
- **Trial Account:** $15 free credit
  - SMS: ~$0.0075 per message (≈2000 messages)
  - Limited to verified numbers only

- **Paid Account:** Pay as you go
  - SMS: $0.0075 - $0.0079 per message
  - No phone number verification required
  - Monthly phone number fee: ~$1.15/month

### Alternative: SendGrid (for Email)
If you prefer SendGrid over Gmail:
- Free tier: 100 emails/day forever
- Good for transactional emails
- Better deliverability for marketing emails

---

## 🔧 Troubleshooting

### Email Not Sending:
1. Check if `EMAIL_BACKEND` is set to `smtp.EmailBackend` (not `console.EmailBackend`)
2. Verify your Gmail App Password is correct (16 characters, no spaces)
3. Make sure 2-Step Verification is enabled on your Google account
4. Check Vercel logs for error messages

### SMS Not Sending:
1. Verify Twilio credentials are correct
2. Make sure phone number includes country code (e.g., +14155552671)
3. For trial accounts, verify the recipient's phone number in Twilio Console
4. Check Vercel logs for Twilio error messages

### Still Not Working:
1. Check Vercel deployment logs
2. Redeploy after adding environment variables
3. Contact support if issues persist

---

## 📝 Environment Variables Summary

Add these to Vercel **Settings** → **Environment Variables**:

```env
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=M&R Motors <your-gmail@gmail.com>

# SMS Configuration
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# Site URL (update if using custom domain)
SITE_URL=https://m-r-motors.vercel.app
```

---

## ✅ Verification Checklist

- [ ] Gmail 2-Step Verification enabled
- [ ] Gmail App Password generated
- [ ] Email environment variables added to Vercel
- [ ] Twilio account created
- [ ] Twilio phone number purchased/activated
- [ ] SMS environment variables added to Vercel
- [ ] Application redeployed
- [ ] Test email verification
- [ ] Test SMS verification

---

## 🎉 You're All Set!

Once you've completed these steps, your email and SMS verification will work perfectly!

For questions or support, check the Vercel logs or Django documentation.

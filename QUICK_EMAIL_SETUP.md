# 🚀 Quick Email Setup for mahmoud_ria@hotmail.com

Follow these simple steps to enable email verification on your site.

## Step 1: Get Hotmail App Password

1. Go to: https://account.microsoft.com/security
2. Sign in with **mahmoud_ria@hotmail.com**
3. Click **Advanced security options**
4. Under **App passwords**, click **Create a new app password**
5. Copy the generated password (it looks like: `abcd efgh ijkl mnop`)

**Note:** If you don't see "App passwords", you need to enable **Two-step verification** first.

## Step 2: Add to Vercel

1. Go to: https://vercel.com/dashboard
2. Click on your **m-r-motors** project
3. Go to **Settings** → **Environment Variables**
4. Add these 7 variables (click Add → Name → Value → Save for each):

| Name | Value |
|------|-------|
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST` | `smtp-mail.outlook.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `True` |
| `EMAIL_HOST_USER` | `mahmoud_ria@hotmail.com` |
| `EMAIL_HOST_PASSWORD` | `your-app-password-from-step1` |
| `DEFAULT_FROM_EMAIL` | `M&R Motors <noreply@mrmotors.com>` |

**Important:** 
- Replace `your-app-password-from-step1` with the actual password you got in Step 1
- The `DEFAULT_FROM_EMAIL` is what users will see - you can customize it to any professional name!

**Note:** The emails will **display** as coming from "M&R Motors <noreply@mrmotors.com>" but will actually be sent through your Hotmail account. This is normal and professional - users won't see your personal email!

5. After adding all 7 variables, your app will automatically redeploy

## Step 3: Test It!

1. Go to: https://m-r-motors.vercel.app/profile/
2. If your email is not verified, click "Send Verification Email"
3. Check your **mahmoud_ria@hotmail.com** inbox (and spam folder)
4. Click the verification link in the email
5. Done! Your email is verified ✅

---

## Troubleshooting

### No email received?
- Check your **Junk/Spam** folder
- Make sure you saved all 6 environment variables correctly
- Check Vercel deployment logs for errors
- Wait 2-3 minutes after adding variables (app needs to redeploy)

### Still not working?
- Make sure the app password is correct (no spaces)
- Verify that 2-Step Verification is enabled on your Microsoft account
- Try regenerating a new app password

### Want to change the sender name?
You can customize `DEFAULT_FROM_EMAIL` to anything you like:
- `M&R Motors <noreply@mrmotors.com>` (professional)
- `M&R Texas Motors <support@mrmotors.com>` (with support)
- `Your Friends at M&R Motors <hello@mrmotors.com>` (friendly)

The email in brackets doesn't have to be real - it's just for display!

---

## Alternative: Use Gmail Instead

If you prefer Gmail, you can use your Gmail account:
1. Follow the Gmail setup instructions in `EMAIL_SMS_SETUP.md`
2. Use these values instead:
   - `EMAIL_HOST`: `smtp.gmail.com`
   - `EMAIL_HOST_USER`: your Gmail address
   - `EMAIL_HOST_PASSWORD`: Gmail App Password (get from Google Account Security)

---

## Quick Command to Check Logs

If emails aren't sending, check the Vercel logs:

```bash
vercel logs m-r-motors --prod
```

Look for any email-related errors in the output.

---

## ✅ Success Indicators

You'll know it's working when:
- ✅ No errors in Vercel logs
- ✅ Email appears in inbox within 1-2 minutes
- ✅ Clicking the link verifies your email
- ✅ Profile shows "✓ Email verified"

---

**Need more help?** Check the detailed guide: `EMAIL_SMS_SETUP.md`

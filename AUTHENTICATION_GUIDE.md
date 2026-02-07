# Authentication System Guide

## Overview
M&R Motors now has a comprehensive authentication system that supports **two login methods**:

1. **Traditional Email/Password Login** - Users can create an account with email and password
2. **Google OAuth Login** - Users can sign in with their Google account

## Features

### For Users Without Google Account
- Create a new account with email and password
- Minimum 8 characters password required
- Full name, email, and password required for signup
- Secure password storage using Django's built-in authentication

### For Users With Google Account
- One-click sign in with Google
- No password management needed
- Uses InstantDB Google OAuth integration

### Security Features
- Password validation (minimum 8 characters)
- Password confirmation on signup
- Email uniqueness validation
- CSRF protection on all forms
- Remember me option for persistent sessions
- Session expires when browser closes (if remember me not checked)

## Pages

### Login Page (`/login/`)
- **Login Tab**: Enter email and password to sign in
- **Sign Up Tab**: Create a new account
- **Google Sign In**: Available on both tabs for quick authentication

### User Interface Updates
- **Logged Out**: Shows "Login / Sign Up" button in navbar
- **Logged In**: Shows "Hi, [Name]" and "Logout" link
- Works on both desktop and mobile menus

## Admin Panel Access
- The admin panel (`/admin-panel/`) now requires authentication
- Users must be logged in to access it
- Redirects to login page if not authenticated

## Technical Details

### Django Views
- `login_view`: Handles traditional email/password login
- `signup_view`: Handles new user registration
- `logout_view`: Logs out the user
- Uses Django's built-in `User` model

### Database
- Users are stored in Django's default SQLite database
- User model includes: username, email, password (hashed), first_name, last_name

### Session Management
- Sessions stored in Django's session framework
- Configurable session expiry based on "Remember me" checkbox
- Secure session cookies

## How to Use

### As a Regular User:
1. Click "Login / Sign Up" in the navbar
2. Choose either:
   - **Sign Up tab**: Create a new account with email/password
   - **Login tab**: Log in with existing credentials
   - **Google button**: Sign in with Google (either tab)

### As an Admin:
1. Log in with your credentials
2. Access the admin panel at `/admin-panel/`
3. Manage inventory, view analytics, etc.

## Future Enhancements
- Password reset functionality
- Email verification
- Social login for other providers (Facebook, Apple, etc.)
- User profile page
- Order history for customers

## Configuration

### Environment Variables (.env)
```
# Django settings
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# InstantDB (for Google OAuth)
INSTANTDB_APP_ID=a169709c-d938-4489-b196-63dcc30a53ca
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id

# Admin emails
ADMIN_EMAILS=mrtexasmotors@gmail.com
```

### URLs
- Login: `http://127.0.0.1:8000/login/`
- Signup: `http://127.0.0.1:8000/login/` (Sign Up tab)
- Logout: `http://127.0.0.1:8000/logout/`
- Admin Panel: `http://127.0.0.1:8000/admin-panel/`

## Troubleshooting

### Google Sign In Not Working
- Check that InstantDB is properly configured
- Verify INSTANTDB_APP_ID in your .env file
- Make sure Google OAuth is enabled in InstantDB dashboard

### Email Already Exists Error
- User with that email already registered
- Try logging in instead or use a different email

### Can't Access Admin Panel
- Make sure you're logged in
- Check that your account has admin privileges
- Contact system administrator if needed

---

For any issues or questions, contact the development team.

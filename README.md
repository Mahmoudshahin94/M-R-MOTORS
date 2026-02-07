# M&R Motors - Car Dealership Website

A modern, real-time car dealership website built with Django and Instant DB.

## Features

- 🚗 Real-time car inventory management
- 🔐 Google OAuth authentication via Instant DB
- ❤️ Interactive likes and comments on car listings
- 📱 WhatsApp integration for easy customer contact
- 🎨 Modern, responsive design with Tailwind CSS
- ⚡ Real-time updates with Instant DB
- 👨‍💼 Admin panel for inventory management

## Tech Stack

- **Backend**: Django 5.2
- **Frontend**: HTML, Tailwind CSS, Vanilla JavaScript
- **Database**: Instant DB (real-time NoSQL)
- **Authentication**: Google OAuth via Instant DB
- **Deployment**: Vercel

## Local Development Setup

### Prerequisites

- Python 3.11+
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "M&R motors"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and update the values:
   - `DJANGO_SECRET_KEY`: Generate a new secret key
   - `DEBUG`: Set to `True` for development
   - `ALLOWED_HOSTS`: Add `localhost,127.0.0.1`
   - Other variables are pre-configured

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the website**
   Open your browser and go to: `http://localhost:8000`

## Project Structure

```
M&R motors/
├── mrmotors/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                 # Main application
│   ├── templates/         # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── inventory.html
│   │   ├── car_detail.html
│   │   ├── location.html
│   │   └── admin_panel.html
│   ├── static/
│   │   └── js/           # JavaScript files
│   │       ├── auth.js
│   │       ├── instant_db.js
│   │       └── admin.js
│   ├── views.py
│   └── urls.py
├── requirements.txt
├── vercel.json           # Vercel deployment config
└── README.md
```

## Instant DB Configuration

This project uses Instant DB for real-time data and authentication.

**App ID**: `a169709c-d938-4489-b196-63dcc30a53ca`

### Data Schema

The following collections are used in Instant DB:

- **posts**: Car listings
  - `id`, `title`, `car_model`, `year`, `price`, `description`, `image_url`, `created_at`, `owner_id`

- **comments**: Comments on cars
  - `id`, `post_id`, `user_id`, `text`, `created_at`

- **likes**: Likes on cars
  - `id`, `post_id`, `user_id`, `created_at`

- **users**: User accounts (managed by Instant DB)
  - `id`, `email`, `google_id`, `name`, `is_admin`

## Deployment to Vercel

### Step 1: Prepare for Deployment

1. **Create a GitHub repository** (if not already done)
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Update settings for production**
   - Ensure `.env` is in `.gitignore` (already done)
   - Set `DEBUG=False` in production environment variables

### Step 2: Deploy to Vercel

1. **Install Vercel CLI** (optional, or use Vercel dashboard)
   ```bash
   npm install -g vercel
   ```

2. **Deploy using Vercel CLI**
   ```bash
   vercel
   ```
   
   Or **deploy via Vercel Dashboard**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Configure environment variables (see below)
   - Deploy

3. **Set Environment Variables in Vercel**
   
   In Vercel dashboard → Project Settings → Environment Variables, add:
   - `DJANGO_SECRET_KEY`: Your secret key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `.vercel.app`
   - `INSTANTDB_APP_ID`: `a169709c-d938-4489-b196-63dcc30a53ca`
   - `ADMIN_EMAILS`: `mrtexasmotors@gmail.com`

### Step 3: Configure Google OAuth

After deployment, you'll have a production URL (e.g., `https://your-app.vercel.app`).

1. **Go to Google Cloud Console**
   - Create a new OAuth 2.0 Client ID
   - Add authorized redirect URIs:
     - `https://your-app.vercel.app`
     - Other Instant DB required URLs

2. **Configure in Instant DB Dashboard**
   - Go to [instantdb.com/dash](https://www.instantdb.com/dash)
   - Select your app
   - Configure Google OAuth with your Client ID

3. **Update Environment Variables**
   - Add `GOOGLE_OAUTH_CLIENT_ID` in Vercel

## Admin Panel Access

The admin panel is located at `/admin-panel/`

**Default Admin Email**: `mrtexasmotors@gmail.com`

To add more admin users:
1. Edit the `ADMIN_EMAILS` environment variable
2. Or update the admin whitelist in `admin_panel.html`

## Usage

### For Customers

1. **Browse Inventory**: Visit `/inventory` to see all available cars
2. **View Car Details**: Click on any car to see full details
3. **Like & Comment**: Login with Google to like cars and leave comments
4. **Contact**: Use WhatsApp buttons to contact the dealer

### For Admins

1. **Login**: Click "Login with Google" using an admin email
2. **Access Admin Panel**: Navigate to `/admin-panel/`
3. **Add Cars**: Fill out the form to add new vehicles
4. **Manage Inventory**: Edit or delete existing cars
5. **Monitor**: Real-time updates reflect immediately on the site

## WhatsApp Numbers

- Primary: (409) 499-8722
- Secondary: (254) 450-1993

## Contact

- **Email**: mrtexasmotors@gmail.com
- **Location**: Texas, United States
- **Google Maps**: [View Location](https://share.google/U4CY4cFise25BjBrm)

## Troubleshooting

### Issue: Static files not loading on Vercel
- Ensure `vercel.json` is properly configured
- Check that `STATIC_URL` is set in `settings.py`

### Issue: Google OAuth not working
- Verify redirect URIs are configured correctly
- Check that the Client ID is set in Instant DB dashboard
- Ensure the domain is authorized in Google Cloud Console

### Issue: Admin panel access denied
- Verify your email is in the `ADMIN_EMAILS` list
- Check that you're logged in with the correct Google account
- Clear browser cache and try again

## License

Copyright © 2026 M&R Motors. All rights reserved.

## Support

For technical support or questions, contact: mrtexasmotors@gmail.com

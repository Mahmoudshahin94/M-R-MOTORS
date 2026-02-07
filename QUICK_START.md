# M&R Motors - Quick Start Guide

## 🎉 Project Complete!

Your M&R Motors car dealership website is now fully built and ready to use!

## What's Been Built

### ✅ Core Features Implemented

1. **Home Page** (`/`)
   - Modern hero section with M&R Motors branding
   - Feature highlights (Quality Cars, Trusted Service, Easy Contact)
   - Call-to-action buttons
   - Contact information section

2. **Inventory Page** (`/inventory`)
   - Real-time car listings from Instant DB
   - Responsive grid layout (1/2/3 columns)
   - Car cards with image, title, year, price
   - WhatsApp contact buttons for each car
   - "View Details" button for each car
   - Loading and empty states

3. **Car Detail Page** (`/car/<id>`)
   - Full car information display
   - Large car image
   - Interactive "Like" button (requires login)
   - Real-time like count
   - Comments section with real-time updates
   - Add comment form (requires login)
   - Two WhatsApp contact buttons

4. **Location Page** (`/location`)
   - Contact information (phones, email)
   - Google Maps link
   - Business hours
   - Quick action buttons (WhatsApp, Email, Call)
   - Directions information

5. **Admin Panel** (`/admin-panel/`)
   - Protected access (requires admin email)
   - Add new cars form
   - Manage inventory table
   - Edit cars (modal popup)
   - Delete cars (with confirmation)
   - Real-time updates

### 🔧 Technical Implementation

- **Backend**: Django 5.2
- **Frontend**: Tailwind CSS (via CDN), Vanilla JavaScript
- **Database**: Instant DB (App ID: `a169709c-d938-4489-b196-63dcc30a53ca`)
- **Authentication**: Google OAuth via Instant DB
- **Real-time**: Instant DB subscriptions for live updates

### 📁 Project Structure

```
M&R motors/
├── manage.py
├── requirements.txt
├── README.md
├── QUICK_START.md
├── .env.example
├── .gitignore
├── vercel.json
├── mrmotors/
│   ├── settings.py (configured with env vars)
│   ├── urls.py
│   └── wsgi.py
└── store/
    ├── views.py
    ├── urls.py
    ├── templates/
    │   ├── base.html (navbar, footer, Instant DB setup)
    │   ├── home.html
    │   ├── inventory.html
    │   ├── car_detail.html
    │   ├── location.html
    │   └── admin_panel.html
    └── static/
        └── js/
            ├── auth.js (Google OAuth)
            ├── instant_db.js (helper functions)
            └── admin.js (admin utilities)
```

## 🚀 Running Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

4. **Open your browser**:
   - Go to: `http://localhost:8000`
   - Home page will load immediately
   - Click "Browse Inventory" to see the inventory page

## 📝 Important Notes

### Instant DB Setup

The app is already configured with your Instant DB App ID:
- **App ID**: `a169709c-d938-4489-b196-63dcc30a53ca`
- The database schema will be created automatically as you use the app
- No manual schema setup required in Instant DB

### Google OAuth

Google OAuth is **not yet configured** because you need a deployment URL first.

**To enable Google login:**
1. Deploy the app to Vercel (see below)
2. Get your deployment URL (e.g., `https://your-app.vercel.app`)
3. Go to [Google Cloud Console](https://console.cloud.google.com)
4. Create OAuth 2.0 credentials with your deployment URL
5. Configure the Client ID in [Instant DB dashboard](https://www.instantdb.com/dash)

**Until then:** The login button will show but won't work. All other features work without login except:
- Liking cars
- Adding comments
- Accessing admin panel

### Admin Access

The admin panel (`/admin-panel/`) is restricted to:
- **Default admin email**: `mrtexasmotors@gmail.com`

To add more admins, edit the `ADMIN_EMAILS` in `.env` or directly in `admin_panel.html`.

## 🌐 Deployment to Vercel

### Option 1: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### Option 2: GitHub + Vercel Dashboard

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will auto-detect Django settings
   - Add environment variables (see below)
   - Click "Deploy"

### Environment Variables for Vercel

Add these in Vercel Dashboard → Settings → Environment Variables:

```
DJANGO_SECRET_KEY=<generate-a-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=.vercel.app
INSTANTDB_APP_ID=a169709c-d938-4489-b196-63dcc30a53ca
ADMIN_EMAILS=mrtexasmotors@gmail.com
```

## 📱 Contact Information

The website displays:
- **Phone 1**: (409) 499-8722
- **Phone 2**: (254) 450-1993
- **Email**: mrtexasmotors@gmail.com
- **WhatsApp**: Both phone numbers linked

## 🎨 Design & Theme

- **Primary Color**: Black (#0a0a0a)
- **Accent Color**: Red (#dc2626)
- **Secondary Color**: Silver (#cbd5e1)
- **Font**: System fonts (San Francisco, Segoe UI, etc.)
- **Responsive**: Mobile-first design with Tailwind breakpoints

## 🔄 Real-time Features

All data updates in real-time thanks to Instant DB:
- Adding a car → Instantly appears in inventory
- Editing a car → Updates everywhere immediately
- Deleting a car → Removes from all views
- Adding a comment → Shows up for all viewers
- Liking a car → Like count updates instantly

## 📋 Next Steps

1. **Test locally** - Run the server and browse all pages
2. **Add test cars** - Use the admin panel to add some cars
3. **Deploy to Vercel** - Follow deployment steps above
4. **Configure Google OAuth** - Set up after deployment
5. **Share your website** - Send the link to customers!

## 🐛 Troubleshooting

### Issue: "No cars available"
- **Solution**: Login with admin email and go to `/admin-panel/` to add cars

### Issue: "Login button doesn't work"
- **Solution**: Google OAuth needs to be configured after deployment

### Issue: "Access denied to admin panel"
- **Solution**: Make sure you're logged in with `mrtexasmotors@gmail.com` or an admin email

### Issue: Static files not loading
- **Solution**: Run `python manage.py collectstatic` (for production)

## 📞 Support

For questions or issues with the website:
- **Email**: mrtexasmotors@gmail.com

## ✨ Features to Add Later (Optional)

- Image upload functionality (instead of URLs)
- Car specifications fields (mileage, color, transmission)
- Search and filter in inventory
- Email notifications for new comments
- Analytics dashboard in admin panel
- Multiple image galleries per car
- Favorite/saved cars feature
- Customer testimonials section

---

**Built with ❤️ for M&R Motors**

Enjoy your new website! 🚗💨

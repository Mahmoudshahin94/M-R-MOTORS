# Vercel Database Setup Guide

## Issue
Your M&R Motors app needs a database to handle user authentication and car inventory. Vercel's serverless environment doesn't support SQLite, so we need to use a cloud database.

## Solution: Set Up Vercel Postgres

### Step 1: Create Vercel Postgres Database

1. Go to your Vercel Dashboard: https://vercel.com/dashboard
2. Select your `m-r-motors` project
3. Go to the **Storage** tab
4. Click **Create Database**
5. Select **Postgres**
6. Choose a name (e.g., "m-r-motors-db")
7. Select a region close to your users
8. Click **Create**

### Step 2: Connect Database to Your Project

Vercel will automatically add the `DATABASE_URL` environment variable to your project. This happens automatically when you create the database.

### Step 3: Run Database Migrations

After the database is connected, you need to run Django migrations. You can do this in two ways:

#### Option A: Using Vercel CLI (Recommended)

```bash
# Install Vercel CLI if not already installed
npm install -g vercel

# Login to Vercel
vercel login

# Link your project
vercel link

# Run migrations using Vercel's environment
vercel exec -- python manage.py migrate

# Create a superuser (for admin access)
vercel exec -- python manage.py createsuperuser
```

#### Option B: Temporarily Set DATABASE_URL Locally

```bash
# Get your DATABASE_URL from Vercel Dashboard > Settings > Environment Variables
export DATABASE_URL="postgres://your-database-url-here"

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Step 4: Verify Setup

1. Redeploy your app: `vercel --prod`
2. Visit https://m-r-motors.vercel.app/login/
3. Try logging in with your credentials

## Alternative: Free Database Providers

If you prefer not to use Vercel Postgres, here are free alternatives:

### 1. Supabase (Recommended)
- Free tier with PostgreSQL
- Sign up: https://supabase.com/
- Get connection string and add as `DATABASE_URL` in Vercel environment variables

### 2. Railway
- Free tier with PostgreSQL
- Sign up: https://railway.app/
- Create PostgreSQL database
- Add connection string to Vercel

### 3. ElephantSQL
- Free tier: 20MB PostgreSQL
- Sign up: https://www.elephantsql.com/
- Create instance and add connection string to Vercel

## Adding Database URL to Vercel

1. Go to Vercel Dashboard > Your Project > Settings > Environment Variables
2. Add new variable:
   - **Name**: `DATABASE_URL`
   - **Value**: `postgres://username:password@host:port/database`
3. Click **Save**
4. Redeploy: `vercel --prod`

## Current Status

Right now, your app will show a friendly message when users try to log in without a database configured. Once you set up the database, all authentication features will work automatically.

## Need Help?

If you need assistance with any of these steps, let me know!

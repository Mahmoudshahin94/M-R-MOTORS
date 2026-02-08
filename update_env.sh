#!/bin/bash
echo "Adding correct DATABASE_URL to Vercel..."
echo "postgresql://neondb_owner:npg_j0pYvOLI1ksd@ep-flat-mouse-ai17ajbm-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require" | vercel env add DATABASE_URL production

# Profile Pictures & Favorite Cars - M&R Motors

## 🎉 New Features

Your M&R Motors website now includes two exciting new features:

### 1. 📸 **Profile Picture Upload**
Upload and manage your profile picture with easy controls

### 2. ❤️ **Favorite Cars**
Save cars you're interested in and access them quickly from your favorites page

---

## 📸 Profile Picture Feature

### What You Can Do

#### **Upload Profile Picture**
- Supported formats: JPG, PNG, GIF, WEBP
- Maximum file size: 5MB
- Automatic resizing and optimization
- Replaces old picture automatically

#### **Where It Shows**
- Profile page sidebar (large avatar)
- Navigation bar (when you click your name)
- Favorites page
- Admin panel (coming soon)

#### **Manage Your Picture**
- Upload new picture anytime
- Remove picture (reverts to initials avatar)
- Instant preview after upload

### How to Upload

1. **Go to Profile Page:**
   - Click your name in navbar
   - Or visit `/profile/`

2. **Upload Picture:**
   - Find "Profile Picture" section (top of page)
   - Click "Choose File" button
   - Select an image (JPG, PNG, GIF, or WEBP)
   - Picture uploads automatically when selected!

3. **Remove Picture:**
   - Click "Remove Picture" button below your photo
   - Confirm removal
   - Avatar returns to initials (e.g., "JS" for John Smith)

### Technical Details

**File Storage:**
- Pictures stored in `/media/profile_pictures/`
- Named as `profile_{user_id}.{extension}`
- Old pictures automatically deleted when uploading new ones

**Database:**
- `UserProfile.profile_picture` field (ImageField)
- Stores file path relative to MEDIA_ROOT
- Nullable (users can have no picture)

**Security:**
- File type validation (only images allowed)
- Size validation (max 5MB)
- Automatic sanitization of filenames
- Secure file storage outside web root

---

## ❤️ Favorite Cars Feature

### What You Can Do

#### **Save Favorite Cars**
- Click the heart icon on any car in inventory
- Instantly add to your favorites
- No page reload required
- Visual feedback (red heart when favorited)

#### **View All Favorites**
- Access from navbar ("❤️ Favorites" link)
- Or visit `/favorites/`
- See all saved cars in one place
- Shows when each car was added

#### **Remove from Favorites**
- Click red X button on favorite car
- Or click heart icon again in inventory
- Instant removal with animation
- Confirmation before removal

### How to Use

#### **Adding to Favorites (From Inventory Page)**

1. **Browse Inventory:**
   - Visit `/inventory/` page
   - Browse available cars

2. **Add to Favorites:**
   - Find a car you like
   - Click the **heart icon** (top-left of car image)
   - Heart turns red = added to favorites!
   - See success notification

3. **Remove from Favorites:**
   - Click the red heart again
   - Heart turns gray = removed from favorites

#### **Managing Favorites (From Favorites Page)**

1. **Access Favorites:**
   - Click **"❤️ Favorites"** in navbar
   - Or visit `/favorites/`

2. **View Your Collection:**
   - See all saved cars
   - View car details (title, price, image)
   - See when added ("Added 2 days ago")

3. **Remove Cars:**
   - Click red **X button** (top-right of car image)
   - Confirm removal
   - Car removed with fade animation

4. **Contact About Cars:**
   - Click "View Details" for full info
   - Use WhatsApp buttons to inquire
   - All contact options available

### Features

#### **Real-Time Updates**
- Favorite status syncs across tabs
- No page refresh needed
- Instant visual feedback
- Smooth animations

#### **Persistent Storage**
- Favorites saved to database
- Available across all devices
- Never lost on logout
- Linked to your account

#### **Smart Integration**
- Heart icon shows favorite status
- Red heart = in favorites
- Gray heart = not in favorites
- Counts shown in profile

#### **Quick Access**
- Navigate from navbar
- See count in profile page
- Direct links to each car
- WhatsApp integration

### Where to Find

#### **Heart Icon Locations:**
- Inventory page (top-left of each car image)
- Car detail page (coming soon)

#### **Favorites Link:**
- Main navbar (desktop)
- Mobile menu
- Profile page (quick link button)

#### **Favorite Count:**
- Profile page sidebar ("Favorite Cars: 5")
- Favorites page header ("5 cars")

---

## 🎯 User Experience Flow

### Complete Journey

1. **Sign Up / Log In**
   - Create account or sign in
   - Upload profile picture (optional)

2. **Browse Cars**
   - Visit inventory page
   - Click hearts on cars you like
   - See real-time favorite status

3. **Manage Favorites**
   - Access favorites page anytime
   - Review your saved cars
   - Remove ones you're no longer interested in

4. **Take Action**
   - View full car details
   - Contact via WhatsApp
   - Visit dealership
   - Make a purchase!

---

## 💻 Technical Implementation

### Database Models

#### **UserProfile Updates**
```python
profile_picture = ImageField(
    upload_to='profile_pictures/',
    blank=True,
    null=True
)
```

#### **FavoriteCar Model**
```python
class FavoriteCar:
    - user (ForeignKey to User)
    - car_id (CharField - InstantDB ID)
    - car_title (CharField)
    - car_price (DecimalField)
    - car_image_url (URLField)
    - created_at (DateTimeField)
```

### API Endpoints

#### **Favorites Management**
- `POST /favorites/add/` - Add car to favorites
- `POST /favorites/remove/` - Remove from favorites
- `GET /favorites/` - View favorites page
- `GET /favorites/check/<car_id>/` - Check favorite status
- `GET /favorites/list/` - Get user's favorite IDs (JSON)

#### **Profile Picture**
- `POST /profile/update/` - Upload new picture
- `POST /profile/remove-picture/` - Remove picture

### Frontend JavaScript

#### **Favorite Toggle Function**
```javascript
async function toggleFavorite(carId, carTitle, carPrice, carImageUrl) {
    // Checks login status
    // Sends request to add/remove
    // Updates UI instantly
    // Shows notification
}
```

#### **Features:**
- AJAX requests (no page reload)
- CSRF token handling
- Error handling
- Visual feedback
- Optimistic UI updates

---

## 🔒 Security & Validation

### Profile Pictures
- ✅ File type validation (only images)
- ✅ File size limit (5MB max)
- ✅ Secure file storage
- ✅ Old file cleanup
- ✅ Filename sanitization

### Favorites
- ✅ Login required (@login_required)
- ✅ User-specific data (filtered by user)
- ✅ CSRF protection
- ✅ Unique constraints (one favorite per user per car)
- ✅ JSON validation

---

## 📱 Responsive Design

### Mobile Optimized
- ✅ Touch-friendly heart buttons
- ✅ Optimized image sizing
- ✅ Mobile navigation includes favorites
- ✅ Responsive favorites grid
- ✅ Fast loading on mobile

### Desktop Enhanced
- ✅ Hover effects on hearts
- ✅ Smooth animations
- ✅ Quick access from navbar
- ✅ Large, clear images
- ✅ Grid layout optimization

---

## 🎨 UI/UX Features

### Visual Feedback
- ✅ Heart animation on click
- ✅ Color change (gray → red)
- ✅ Success notifications
- ✅ Smooth transitions
- ✅ Loading states

### User-Friendly
- ✅ No login popup for guests
- ✅ Clear call-to-actions
- ✅ Helpful empty states
- ✅ Confirmation dialogs
- ✅ Error messages

### Consistency
- ✅ Matches brand colors
- ✅ Consistent with site theme
- ✅ Same card design
- ✅ Familiar interactions
- ✅ Professional appearance

---

## 📊 Profile Page Updates

### New Sections

#### **1. Profile Picture Section** (Top)
- Current picture or initials avatar
- Upload button with file picker
- Remove button (if picture exists)
- File requirements info
- Instant upload on selection

#### **2. Favorites Quick Link** (Sidebar)
- Shows favorite count
- Links to favorites page
- Red accent color
- Heart emoji

#### **3. Sidebar Stats** (Updated)
- Member since date
- Email verification status
- **Favorite cars count** (NEW)

---

## 🚀 Getting Started

### For Users

1. **Upload Profile Picture:**
   ```
   1. Go to profile page
   2. Click "Choose File" under profile picture
   3. Select an image
   4. Done! (uploads automatically)
   ```

2. **Start Favoriting Cars:**
   ```
   1. Visit inventory page
   2. Click heart on cars you like
   3. View favorites anytime from navbar
   4. Remove as needed
   ```

### For Developers

1. **Media Files Setup:**
   - Media files stored in `/media/`
   - Served automatically in development
   - Configure for production (S3, CDN, etc.)

2. **Dependencies:**
   - Pillow (installed) for image handling
   - PIL for image processing
   - Django's ImageField

3. **Migrations:**
   - Already applied!
   - `0002_userprofile_profile_picture_favoritecar.py`

---

## 🛠️ Configuration

### Settings (Already Configured)

```python
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Requirements (Already Added)

```python
Pillow==11.1.0
```

### URL Configuration (Already Set)

```python
# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 📈 Future Enhancements

### Possible Features
- [ ] Favorite cars share link
- [ ] Email alerts for price changes
- [ ] Compare favorited cars
- [ ] Favorite collections/folders
- [ ] Export favorites list
- [ ] Public wishlist sharing
- [ ] Advanced profile customization
- [ ] Multiple profile pictures
- [ ] Cover photos
- [ ] Profile themes

---

## 🐛 Troubleshooting

### Profile Picture Issues

**Problem:** Can't upload picture
- Check file size (<5MB)
- Verify file type (JPG, PNG, GIF, WEBP)
- Try different browser
- Check permissions

**Problem:** Picture not showing
- Hard refresh page (Ctrl+F5)
- Check media files are being served
- Verify MEDIA_URL setting
- Check browser console for errors

### Favorites Issues

**Problem:** Can't add to favorites
- Make sure you're logged in
- Check browser console for errors
- Verify JavaScript is enabled
- Try refreshing page

**Problem:** Favorites not saving
- Check internet connection
- Verify login session
- Clear browser cache
- Check for JavaScript errors

**Problem:** Heart button not working
- Refresh the page
- Check if logged in
- Disable ad blockers
- Try different browser

---

## 📝 Notes

### Important

- **Login Required:** Must be logged in to use favorites
- **Guest Users:** Can view inventory but can't save favorites
- **Auto Redirect:** Guests clicking heart are redirected to login
- **Data Persistence:** Favorites saved permanently
- **Cross-Device:** Access favorites from any device
- **Privacy:** Your favorites are private

### Best Practices

- Upload clear, recent profile picture
- Use favorites to shortlist cars
- Remove cars you're no longer interested in
- Contact sellers from favorites page
- Keep favorites list updated

---

## ✨ Summary

### Profile Pictures
- ✅ Easy upload system
- ✅ Multiple format support
- ✅ Size validation
- ✅ Remove option
- ✅ Instant preview

### Favorite Cars
- ✅ One-click favoriting
- ✅ Dedicated favorites page
- ✅ Real-time updates
- ✅ Persistent storage
- ✅ Quick access
- ✅ Mobile-friendly
- ✅ Smooth animations

---

**Both features are now live and ready to use!**

Visit your profile at `/profile/` to upload a picture, and start favoriting cars at `/inventory/`! 

🚗 ❤️ Happy car shopping at M&R Motors!

// Authentication System using Instant DB
// This file handles Google OAuth authentication

// Check if db is initialized
if (!window.db) {
    console.error('Instant DB not initialized');
}

// Get UI elements
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const userProfile = document.getElementById('user-profile');
const userName = document.getElementById('user-name');

// Initialize auth state
let currentUser = null;

// Subscribe to auth changes
window.db.subscribeAuth((auth) => {
    console.log('Auth state changed:', auth);
    
    if (auth.user) {
        // User is signed in
        currentUser = auth.user;
        showUserProfile(auth.user);
    } else {
        // User is signed out
        currentUser = null;
        showLoginButton();
    }
});

// Show login button
function showLoginButton() {
    if (loginBtn && userProfile) {
        loginBtn.classList.remove('hidden');
        userProfile.classList.add('hidden');
    }
}

// Show user profile
function showUserProfile(user) {
    if (loginBtn && userProfile && userName) {
        loginBtn.classList.add('hidden');
        userProfile.classList.remove('hidden');
        userProfile.classList.add('flex');
        
        // Display user name or email
        const displayName = user.email ? user.email.split('@')[0] : 'User';
        userName.textContent = `Hi, ${displayName}`;
    }
}

// Handle login
if (loginBtn) {
    loginBtn.addEventListener('click', async () => {
        try {
            loginBtn.disabled = true;
            loginBtn.textContent = 'Logging in...';
            
            // Sign in with Google using Instant DB
            // Note: This will require Google OAuth Client ID to be configured
            await window.db.auth.signInWithPopup({ clientName: 'google' });
            
        } catch (error) {
            console.error('Login error:', error);
            alert('Login failed. Please make sure Google OAuth is configured in Instant DB dashboard.');
            
            loginBtn.disabled = false;
            loginBtn.textContent = 'Login with Google';
        }
    });
}

// Handle logout
if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
        try {
            await window.db.auth.signOut();
            console.log('Signed out successfully');
        } catch (error) {
            console.error('Logout error:', error);
            alert('Logout failed. Please try again.');
        }
    });
}

// Export current user for use in other scripts
window.getCurrentUser = () => currentUser;

// Helper function to check if user is authenticated
window.isAuthenticated = () => currentUser !== null;

// Helper function to check if user is admin
window.isAdmin = () => {
    if (!currentUser) return false;
    
    // Check if user has admin flag in Instant DB
    // This will be set in the admin panel
    return currentUser.is_admin === true;
};

console.log('Auth system initialized');

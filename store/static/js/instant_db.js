// Instant DB Helper Functions
// This file provides helper functions for all Instant DB operations

// Ensure db is available
if (!window.db) {
    console.error('Instant DB not initialized. Make sure base.html is loaded.');
}

/**
 * Fetch all cars from the database
 * @returns {Promise} Promise that resolves with cars data
 */
window.fetchAllCars = async () => {
    try {
        const { data, isLoading, error } = await window.db.useQuery({ posts: {} });
        
        if (error) {
            console.error('Error fetching cars:', error);
            return { cars: [], error, isLoading };
        }
        
        return { 
            cars: data?.posts || [], 
            isLoading,
            error: null 
        };
    } catch (error) {
        console.error('Exception fetching cars:', error);
        return { cars: [], error, isLoading: false };
    }
};

/**
 * Fetch a single car by ID
 * @param {string} carId - The ID of the car to fetch
 * @returns {Promise} Promise that resolves with car data
 */
window.fetchCarById = async (carId) => {
    try {
        const { data, isLoading, error } = await window.db.useQuery({
            posts: {
                $: {
                    where: {
                        id: carId
                    }
                }
            }
        });
        
        if (error) {
            console.error('Error fetching car:', error);
            return { car: null, error, isLoading };
        }
        
        const car = data?.posts?.[0] || null;
        return { car, isLoading, error: null };
    } catch (error) {
        console.error('Exception fetching car:', error);
        return { car: null, error, isLoading: false };
    }
};

/**
 * Add a new car to the database
 * @param {Object} carData - The car data to add
 * @returns {Promise} Promise that resolves when car is added
 */
window.addCar = async (carData) => {
    try {
        const user = window.getCurrentUser();
        if (!user) {
            throw new Error('Must be logged in to add a car');
        }
        
        const carId = window.id();
        
        await window.db.transact([
            window.tx.posts[carId].update({
                ...carData,
                owner_id: user.id,
                created_at: Date.now()
            })
        ]);
        
        console.log('Car added successfully:', carId);
        return { success: true, carId };
    } catch (error) {
        console.error('Error adding car:', error);
        return { success: false, error: error.message };
    }
};

/**
 * Update an existing car
 * @param {string} carId - The ID of the car to update
 * @param {Object} updates - The fields to update
 * @returns {Promise} Promise that resolves when car is updated
 */
window.updateCar = async (carId, updates) => {
    try {
        await window.db.transact([
            window.tx.posts[carId].update(updates)
        ]);
        
        console.log('Car updated successfully:', carId);
        return { success: true };
    } catch (error) {
        console.error('Error updating car:', error);
        return { success: false, error: error.message };
    }
};

/**
 * Delete a car from the database
 * @param {string} carId - The ID of the car to delete
 * @returns {Promise} Promise that resolves when car is deleted
 */
window.deleteCar = async (carId) => {
    try {
        await window.db.transact([
            window.tx.posts[carId].delete()
        ]);
        
        console.log('Car deleted successfully:', carId);
        return { success: true };
    } catch (error) {
        console.error('Error deleting car:', error);
        return { success: false, error: error.message };
    }
};

/**
 * Add a comment to a car
 * @param {string} postId - The ID of the car
 * @param {string} text - The comment text
 * @returns {Promise} Promise that resolves when comment is added
 */
window.addComment = async (postId, text) => {
    try {
        const user = window.getCurrentUser();
        if (!user) {
            throw new Error('Must be logged in to comment');
        }
        
        const commentId = window.id();
        
        await window.db.transact([
            window.tx.comments[commentId].update({
                post_id: postId,
                user_id: user.id,
                text: text,
                created_at: Date.now()
            })
        ]);
        
        console.log('Comment added successfully:', commentId);
        return { success: true, commentId };
    } catch (error) {
        console.error('Error adding comment:', error);
        return { success: false, error: error.message };
    }
};

/**
 * Toggle like on a car
 * @param {string} postId - The ID of the car
 * @returns {Promise} Promise that resolves when like is toggled
 */
window.toggleLike = async (postId) => {
    try {
        const user = window.getCurrentUser();
        if (!user) {
            throw new Error('Must be logged in to like');
        }
        
        // Query existing likes for this post by this user
        const { data } = await window.db.useQuery({
            likes: {
                $: {
                    where: {
                        post_id: postId,
                        user_id: user.id
                    }
                }
            }
        });
        
        const existingLike = data?.likes?.[0];
        
        if (existingLike) {
            // Unlike - delete the like
            await window.db.transact([
                window.tx.likes[existingLike.id].delete()
            ]);
            console.log('Post unliked:', postId);
            return { success: true, liked: false };
        } else {
            // Like - add a new like
            const likeId = window.id();
            await window.db.transact([
                window.tx.likes[likeId].update({
                    post_id: postId,
                    user_id: user.id,
                    created_at: Date.now()
                })
            ]);
            console.log('Post liked:', postId);
            return { success: true, liked: true };
        }
    } catch (error) {
        console.error('Error toggling like:', error);
        return { success: false, error: error.message };
    }
};

/**
 * Subscribe to comments for a specific car
 * @param {string} postId - The ID of the car
 * @param {Function} callback - Callback function to handle comment updates
 * @returns {Function} Unsubscribe function
 */
window.subscribeToComments = (postId, callback) => {
    try {
        const query = {
            comments: {
                $: {
                    where: {
                        post_id: postId
                    }
                }
            }
        };
        
        const unsubscribe = window.db.subscribeQuery(query, (result) => {
            if (result.error) {
                console.error('Error in comments subscription:', result.error);
                callback({ comments: [], error: result.error });
            } else {
                callback({ comments: result.data?.comments || [], error: null });
            }
        });
        
        return unsubscribe;
    } catch (error) {
        console.error('Error subscribing to comments:', error);
        return () => {};
    }
};

/**
 * Subscribe to likes for a specific car
 * @param {string} postId - The ID of the car
 * @param {Function} callback - Callback function to handle like updates
 * @returns {Function} Unsubscribe function
 */
window.subscribeToLikes = (postId, callback) => {
    try {
        const query = {
            likes: {
                $: {
                    where: {
                        post_id: postId
                    }
                }
            }
        };
        
        const unsubscribe = window.db.subscribeQuery(query, (result) => {
            if (result.error) {
                console.error('Error in likes subscription:', result.error);
                callback({ likes: [], error: result.error });
            } else {
                callback({ likes: result.data?.likes || [], error: null });
            }
        });
        
        return unsubscribe;
    } catch (error) {
        console.error('Error subscribing to likes:', error);
        return () => {};
    }
};

/**
 * Format price as USD currency
 * @param {number} price - The price to format
 * @returns {string} Formatted price string
 */
window.formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format(price);
};

/**
 * Format timestamp as readable date
 * @param {number} timestamp - The timestamp to format
 * @returns {string} Formatted date string
 */
window.formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    // Less than 1 minute
    if (diff < 60000) {
        return 'Just now';
    }
    
    // Less than 1 hour
    if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    }
    
    // Less than 1 day
    if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    }
    
    // Less than 1 week
    if (diff < 604800000) {
        const days = Math.floor(diff / 86400000);
        return `${days} day${days > 1 ? 's' : ''} ago`;
    }
    
    // Otherwise, show the date
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
};

/**
 * Generate WhatsApp link with pre-filled message
 * @param {string} phoneNumber - The WhatsApp phone number (with country code)
 * @param {Object} car - The car object
 * @returns {string} WhatsApp link
 */
window.getWhatsAppLink = (phoneNumber, car) => {
    const message = `Hi, I'm interested in the ${car.car_model || car.title} listed for ${window.formatPrice(car.price)}. Is it still available?`;
    return `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;
};

console.log('Instant DB helper functions loaded');

// Admin Panel Helper Functions
// This file provides additional helper functions for the admin panel

console.log('Admin helper functions loaded');

// Additional helper functions can be added here as needed
// For example: image upload helpers, bulk operations, etc.

/**
 * Validate car data before submission
 * @param {Object} carData - The car data to validate
 * @returns {Object} Validation result with success flag and errors array
 */
window.validateCarData = (carData) => {
    const errors = [];
    
    if (!carData.title || carData.title.trim().length < 3) {
        errors.push('Title must be at least 3 characters long');
    }
    
    if (!carData.car_model || carData.car_model.trim().length < 2) {
        errors.push('Car model must be at least 2 characters long');
    }
    
    if (!carData.year || carData.year < 1900 || carData.year > 2030) {
        errors.push('Please enter a valid year between 1900 and 2030');
    }
    
    if (!carData.price || carData.price < 0) {
        errors.push('Price must be a positive number');
    }
    
    if (!carData.image_url || !isValidUrl(carData.image_url)) {
        errors.push('Please enter a valid image URL');
    }
    
    if (!carData.description || carData.description.trim().length < 10) {
        errors.push('Description must be at least 10 characters long');
    }
    
    return {
        success: errors.length === 0,
        errors: errors
    };
};

/**
 * Check if a string is a valid URL
 * @param {string} url - The URL to validate
 * @returns {boolean} True if valid URL
 */
function isValidUrl(url) {
    try {
        new URL(url);
        return true;
    } catch (e) {
        return false;
    }
}

/**
 * Format car data for display in admin tables
 * @param {Object} car - The car object
 * @returns {Object} Formatted car data
 */
window.formatCarForAdmin = (car) => {
    return {
        id: car.id,
        title: car.title || car.car_model || 'Untitled',
        model: car.car_model || '-',
        year: car.year || '-',
        price: window.formatPrice(car.price || 0),
        priceRaw: car.price || 0,
        imageUrl: car.image_url || 'https://via.placeholder.com/80x60?text=No+Image',
        description: car.description || '',
        createdAt: car.created_at,
        ownerId: car.owner_id
    };
};

/**
 * Export inventory data as CSV
 * (Can be extended in the future)
 */
window.exportInventoryCSV = async () => {
    try {
        const { data } = await window.db.useQuery({ posts: {} });
        const cars = data?.posts || [];
        
        if (cars.length === 0) {
            alert('No cars to export');
            return;
        }
        
        // Create CSV content
        const headers = ['Title', 'Model', 'Year', 'Price', 'Image URL', 'Description'];
        const rows = cars.map(car => [
            car.title || '',
            car.car_model || '',
            car.year || '',
            car.price || '',
            car.image_url || '',
            car.description || ''
        ]);
        
        let csvContent = headers.join(',') + '\n';
        rows.forEach(row => {
            csvContent += row.map(field => `"${field}"`).join(',') + '\n';
        });
        
        // Download CSV
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `inventory-${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
        window.URL.revokeObjectURL(url);
        
        console.log('Inventory exported successfully');
    } catch (error) {
        console.error('Error exporting inventory:', error);
        alert('Failed to export inventory');
    }
};

console.log('Admin panel ready');

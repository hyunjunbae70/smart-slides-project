import { writable } from 'svelte/store';

// Create a writable store for slide data
export const slideData = writable(null);

// Store for loading state
export const isLoading = writable(false);

// Store for error messages
export const error = writable(null);

/**
 * Call the generate-slides API endpoint and store the result in the slideData store.
 * 
 * @param {string} prompt - The user's prompt/query for generating slides
 * @returns {Promise<Object>} The slide data object containing the list of slides
 * @throws {Error} If the API request fails
 */
export async function callGenerateAPI(prompt) {
  // Reset error and set loading state
  error.set(null);
  isLoading.set(true);
  
  try {
    const response = await fetch('/api/generate-slides', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: prompt }),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error occurred' }));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    // Update the slide data store
    slideData.set(data);
    
    return data;
  } catch (err) {
    // Set error in store
    error.set(err.message || 'Failed to generate slides');
    // Clear slide data on error
    slideData.set(null);
    throw err;
  } finally {
    // Always set loading to false when done
    isLoading.set(false);
  }
}


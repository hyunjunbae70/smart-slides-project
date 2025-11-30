import { writable } from 'svelte/store';
import { messages, getClientId } from './websocket.js';
import { get } from 'svelte/store';

// Create a writable store for slide data
export const slideData = writable(null);

// Store for loading state
export const isLoading = writable(false);

// Store for error messages
export const error = writable(null);

// Track processed messages to avoid reprocessing
const processedMessages = new Set();
let lastMessageCount = 0;

/**
 * Process incoming WebSocket edit payloads and update the slide data store.
 * This function listens for 'edit' type messages and applies them to the store.
 * 
 * @param {string} message - The raw message from WebSocket
 * @param {number} messageIndex - The index of the message in the messages array
 */
function processEditPayload(message, messageIndex) {
  // Create a unique key for this message to track if we've processed it
  const messageKey = `${messageIndex}_${message}`;
  
  // Skip if we've already processed this message
  if (processedMessages.has(messageKey)) {
    return;
  }
  
  try {
    // Try to parse as JSON
    const payload = JSON.parse(message);
    
    // Check if it's an edit payload
    if (payload && payload.type === 'edit') {
      const currentClientId = getClientId();
      
      // Ignore edits from the current client to prevent feedback loops
      // (we already applied our own edits locally)
      if (payload.client_id === currentClientId) {
        processedMessages.add(messageKey);
        return;
      }
      
      // Validate the edit payload
      if (
        typeof payload.slide_index === 'number' &&
        payload.field &&
        payload.value !== undefined
      ) {
        // Get current slide data
        const currentData = get(slideData);
        
        if (!currentData || !currentData.slides) {
          console.warn('Cannot apply edit: No slide data available');
          processedMessages.add(messageKey);
          return;
        }
        
        const slideIndex = payload.slide_index;
        
        // Validate slide index
        if (slideIndex < 0 || slideIndex >= currentData.slides.length) {
          console.warn(`Cannot apply edit: Invalid slide index ${slideIndex}`);
          processedMessages.add(messageKey);
          return;
        }
        
        // Create a deep copy of the slide data to update
        const updatedData = {
          ...currentData,
          slides: currentData.slides.map((slide, index) => {
            if (index === slideIndex) {
              // Create a new slide object with the updated field
              const updatedSlide = { ...slide };
              
              if (payload.field === 'title') {
                updatedSlide.title = payload.value;
              } else if (payload.field === 'content') {
                // For content, we need to handle it as an array
                updatedSlide.content = Array.isArray(payload.value) 
                  ? [...payload.value] 
                  : payload.value;
              } else if (payload.field === 'theme') {
                updatedSlide.theme = payload.value;
              } else {
                // Handle nested field updates (e.g., 'content.0' for first bullet point)
                const fieldParts = payload.field.split('.');
                if (fieldParts.length === 2 && fieldParts[0] === 'content') {
                  const contentIndex = parseInt(fieldParts[1]);
                  if (!isNaN(contentIndex) && Array.isArray(updatedSlide.content)) {
                    updatedSlide.content = [...updatedSlide.content];
                    updatedSlide.content[contentIndex] = payload.value;
                  }
                }
              }
              
              return updatedSlide;
            }
            return { ...slide };
          })
        };
        
        // Update the store
        slideData.set(updatedData);
        
        // Mark this message as processed
        processedMessages.add(messageKey);
      }
    }
  } catch (err) {
    // Not JSON or invalid JSON, ignore (might be a chat message)
    // This is expected for non-edit messages
    // Mark as processed to avoid trying again
    processedMessages.add(messageKey);
  }
}

/**
 * Initialize the WebSocket edit listener.
 * This sets up a subscription to the messages store to process edit payloads.
 * 
 * @returns {Function} Unsubscribe function to clean up the listener
 */
export function initializeEditListener() {
  // Subscribe to messages store and process new messages
  const unsubscribe = messages.subscribe((msgs) => {
    if (msgs && msgs.length > 0) {
      // Only process new messages that we haven't seen before
      const currentMessageCount = msgs.length;
      
      if (currentMessageCount > lastMessageCount) {
        // Process only the new messages
        for (let i = lastMessageCount; i < currentMessageCount; i++) {
          processEditPayload(msgs[i], i);
        }
        lastMessageCount = currentMessageCount;
      }
    }
  });
  
  return unsubscribe;
}

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


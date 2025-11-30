import { writable } from 'svelte/store';

// Store for incoming messages
export const messages = writable([]);

// Store for connection state
export const isConnected = writable(false);

// Store for connection errors
export const connectionError = writable(null);

// WebSocket instance
let ws = null;
let clientId = null;

/**
 * Initialize the WebSocket connection to the chat endpoint.
 * 
 * @param {string} id - The client ID to use for the connection
 */
export function initializeWebSocket(id) {
  // Close existing connection if any
  if (ws) {
    ws.close();
  }
  
  clientId = id;
  connectionError.set(null);
  
  // Determine WebSocket URL based on current location
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = window.location.host;
  const wsUrl = `${protocol}//${host}/ws/chat/${id}`;
  
  try {
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
      isConnected.set(true);
      connectionError.set(null);
      console.log('WebSocket connected');
    };
    
    ws.onmessage = (event) => {
      // Add the new message to the messages store
      messages.update(msgs => [...msgs, event.data]);
    };
    
    ws.onerror = (error) => {
      connectionError.set('WebSocket connection error');
      console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
      isConnected.set(false);
      console.log('WebSocket disconnected');
    };
    
  } catch (err) {
    connectionError.set(`Failed to initialize WebSocket: ${err.message}`);
    console.error('WebSocket initialization error:', err);
  }
}

/**
 * Send a message through the WebSocket connection.
 * 
 * @param {string} message - The message to send
 * @throws {Error} If the WebSocket is not connected
 */
export function sendMessage(message) {
  if (!ws || ws.readyState !== WebSocket.OPEN) {
    throw new Error('WebSocket is not connected');
  }
  
  ws.send(message);
}

/**
 * Close the WebSocket connection.
 */
export function closeWebSocket() {
  if (ws) {
    ws.close();
    ws = null;
    clientId = null;
    isConnected.set(false);
    messages.set([]);
  }
}

/**
 * Get the current client ID.
 * 
 * @returns {string|null} The current client ID or null if not connected
 */
export function getClientId() {
  return clientId;
}


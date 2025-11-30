<script>
  import { messages, isConnected, connectionError, sendMessage, getClientId } from './websocket.js';
  import { onMount, onDestroy } from 'svelte';
  
  let messageInput = '';
  let messagesContainer;
  let currentClientId = null;
  let lastMessageCount = 0;
  
  // Function to scroll to bottom
  function scrollToBottom() {
    if (messagesContainer) {
      requestAnimationFrame(() => {
        if (messagesContainer) {
          messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
      });
    }
  }
  
  // Get client ID on mount and scroll to bottom if messages exist
  onMount(() => {
    currentClientId = getClientId();
    lastMessageCount = $messages.length;
    // Scroll to bottom on initial mount if messages exist
    if ($messages.length > 0) {
      setTimeout(scrollToBottom, 100);
    }
  });
  
  // Auto-scroll to bottom when new messages arrive
  $: if ($messages && messagesContainer) {
    const newMessageCount = $messages.length;
    if (newMessageCount > lastMessageCount) {
      scrollToBottom();
      lastMessageCount = newMessageCount;
    }
  }
  
  // Parse message format: "client_id: message"
  function parseMessage(messageText) {
    const colonIndex = messageText.indexOf(':');
    if (colonIndex === -1) {
      return { clientId: 'Unknown', message: messageText };
    }
    return {
      clientId: messageText.substring(0, colonIndex).trim(),
      message: messageText.substring(colonIndex + 1).trim()
    };
  }
  
  // Check if message is from current client
  function isOwnMessage(clientId) {
    return clientId === currentClientId;
  }
  
  // Handle sending a message
  function handleSend() {
    if (!messageInput.trim()) {
      return;
    }
    
    if (!$isConnected) {
      alert('WebSocket is not connected. Please connect first.');
      return;
    }
    
    try {
      sendMessage(messageInput.trim());
      messageInput = '';
    } catch (error) {
      alert(`Failed to send message: ${error.message}`);
    }
  }
  
  // Handle Enter key press
  function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  }
</script>

<div class="chat-container">
  <div class="chat-header">
    <h2>Chat</h2>
    <div class="connection-status">
      {#if $isConnected}
        <span class="status-indicator connected"></span>
        <span class="status-text">Connected</span>
      {:else}
        <span class="status-indicator disconnected"></span>
        <span class="status-text">Disconnected</span>
      {/if}
    </div>
  </div>
  
  {#if $connectionError}
    <div class="error-banner">
      <span>⚠️ {$connectionError}</span>
    </div>
  {/if}
  
  <div class="messages-container" bind:this={messagesContainer}>
    {#if $messages.length === 0}
      <div class="empty-state">
        <p>No messages yet</p>
        <p class="hint">Start chatting to see messages here</p>
      </div>
    {:else}
      {#each $messages as message, index}
        {@const parsed = parseMessage(message)}
        {@const isOwn = isOwnMessage(parsed.clientId)}
        <div class="message" class:own-message={isOwn} data-message-index={index}>
          <div class="message-header">
            <span class="client-id">
              {parsed.clientId}
              <span class="colon">:</span>
            </span>
            {#if isOwn}
              <span class="you-badge">You</span>
            {/if}
          </div>
          <div class="message-content">{parsed.message}</div>
        </div>
      {/each}
    {/if}
  </div>
  
  <div class="chat-input-container">
    <div class="input-wrapper">
      <input
        type="text"
        class="message-input"
        bind:value={messageInput}
        on:keypress={handleKeyPress}
        placeholder={$isConnected ? "Type a message..." : "Not connected"}
        disabled={!$isConnected}
      />
      <button
        class="send-button"
        on:click={handleSend}
        disabled={!$isConnected || !messageInput.trim()}
        type="button"
        aria-label="Send message"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </div>
  </div>
</div>

<style>
  .chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #fff;
    border-left: 1px solid #e0e0e0;
  }
  
  .chat-header {
    padding: 1rem 1.5rem;
    background-color: #f8f9fa;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .chat-header h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #333;
  }
  
  .connection-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .status-indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
  }
  
  .status-indicator.connected {
    background-color: #4caf50;
    box-shadow: 0 0 4px rgba(76, 175, 80, 0.5);
  }
  
  .status-indicator.disconnected {
    background-color: #f44336;
  }
  
  .status-text {
    font-size: 0.875rem;
    color: #666;
    font-weight: 500;
  }
  
  .error-banner {
    background-color: #ffebee;
    color: #c62828;
    padding: 0.75rem 1.5rem;
    font-size: 0.875rem;
    border-bottom: 1px solid #ffcdd2;
  }
  
  .messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    background-color: #fafafa;
    scroll-behavior: smooth;
  }
  
  .empty-state {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #999;
    text-align: center;
  }
  
  .empty-state p {
    margin: 0.25rem 0;
  }
  
  .hint {
    font-size: 0.875rem;
    font-style: italic;
  }
  
  .message {
    max-width: 75%;
    padding: 0.75rem 1rem;
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    border: 1px solid #e0e0e0;
  }
  
  .message.own-message {
    align-self: flex-end;
    background-color: #4a90e2;
    color: white;
    border-color: #357abd;
  }
  
  .message-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  .client-id {
    font-size: 0.8125rem;
    font-weight: 700;
    opacity: 1;
    text-transform: none;
    letter-spacing: 0.3px;
    color: inherit;
  }
  
  .own-message .client-id {
    opacity: 1;
  }
  
  .colon {
    margin-right: 0.25rem;
    opacity: 0.7;
  }
  
  .you-badge {
    font-size: 0.7rem;
    background-color: rgba(255, 255, 255, 0.3);
    padding: 0.125rem 0.5rem;
    border-radius: 10px;
    font-weight: 500;
  }
  
  .message-content {
    font-size: 0.9375rem;
    line-height: 1.5;
    word-wrap: break-word;
  }
  
  .chat-input-container {
    padding: 1rem 1.5rem;
    background-color: #f8f9fa;
    border-top: 1px solid #e0e0e0;
  }
  
  .input-wrapper {
    display: flex;
    gap: 0.75rem;
    align-items: center;
  }
  
  .message-input {
    flex: 1;
    padding: 0.75rem 1rem;
    font-size: 0.9375rem;
    border: 2px solid #e0e0e0;
    border-radius: 24px;
    font-family: inherit;
    transition: border-color 0.2s ease;
  }
  
  .message-input:focus {
    outline: none;
    border-color: #4a90e2;
  }
  
  .message-input:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
  }
  
  .send-button {
    width: 44px;
    height: 44px;
    background-color: #4a90e2;
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    flex-shrink: 0;
    padding: 0;
  }
  
  .send-button:hover:not(:disabled) {
    background-color: #357abd;
    transform: scale(1.05);
  }
  
  .send-button:active:not(:disabled) {
    transform: scale(0.95);
  }
  
  .send-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
    opacity: 0.6;
  }
  
  .send-button svg {
    stroke: currentColor;
  }
</style>


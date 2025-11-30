<script>
  import { callGenerateAPI, isLoading, error } from './api.js';
  
  let prompt = '';
  let localError = null;
  
  async function handleGenerate() {
    if (!prompt.trim()) {
      localError = 'Please enter a prompt to generate slides';
      return;
    }
    
    localError = null;
    
    try {
      await callGenerateAPI(prompt.trim());
      // Optionally clear the prompt after successful generation
      // prompt = '';
    } catch (err) {
      // Error is already set in the store, but we can also set local error
      localError = err.message || 'Failed to generate slides';
    }
  }
  
  function handleKeyDown(event) {
    // Allow Ctrl+Enter or Cmd+Enter to submit
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
      event.preventDefault();
      handleGenerate();
    }
  }
  
  // Clear local error when prompt changes
  $: if (prompt && localError) {
    localError = null;
  }
</script>

<div class="generate-container">
  <div class="generate-header">
    <h2>Generate Slides</h2>
    <p class="subtitle">Enter a natural language prompt to create your presentation</p>
  </div>
  
  <div class="input-section">
    <label for="prompt-input" class="input-label">
      What would you like to create a presentation about?
    </label>
    <textarea
      id="prompt-input"
      class="prompt-input"
      bind:value={prompt}
      on:keydown={handleKeyDown}
      placeholder="e.g., Create a presentation about artificial intelligence and its impact on modern society..."
      rows="8"
      disabled={$isLoading}
    ></textarea>
    <div class="input-hint">
      <span>Tip: Press Ctrl+Enter (or Cmd+Enter on Mac) to generate</span>
    </div>
  </div>
  
  {#if localError || $error}
    <div class="error-message">
      <span class="error-icon">⚠️</span>
      <span>{localError || $error}</span>
    </div>
  {/if}
  
  <div class="button-section">
    <button
      class="generate-button"
      on:click={handleGenerate}
      disabled={$isLoading || !prompt.trim()}
      type="button"
    >
      {#if $isLoading}
        <span class="spinner"></span>
        <span>Generating...</span>
      {:else}
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
        <span>Generate Slides</span>
      {/if}
    </button>
  </div>
</div>

<style>
  .generate-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .generate-header {
    text-align: center;
  }
  
  .generate-header h2 {
    margin: 0 0 0.5rem 0;
    font-size: 2rem;
    font-weight: 700;
    color: #333;
  }
  
  .subtitle {
    margin: 0;
    font-size: 1rem;
    color: #666;
    font-weight: 400;
  }
  
  .input-section {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .input-label {
    font-size: 0.9375rem;
    font-weight: 600;
    color: #555;
    margin-bottom: 0.25rem;
  }
  
  .prompt-input {
    width: 100%;
    padding: 1rem;
    font-size: 1rem;
    font-family: inherit;
    line-height: 1.6;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    resize: vertical;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    background-color: #fff;
  }
  
  .prompt-input:focus {
    outline: none;
    border-color: #4a90e2;
    box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
  }
  
  .prompt-input:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
    opacity: 0.7;
  }
  
  .prompt-input::placeholder {
    color: #999;
  }
  
  .input-hint {
    font-size: 0.8125rem;
    color: #999;
    font-style: italic;
    text-align: right;
  }
  
  .error-message {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background-color: #ffebee;
    border: 1px solid #ffcdd2;
    border-radius: 6px;
    color: #c62828;
    font-size: 0.9375rem;
  }
  
  .error-icon {
    font-size: 1.125rem;
  }
  
  .button-section {
    display: flex;
    justify-content: center;
  }
  
  .generate-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.875rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    color: white;
    background-color: #4a90e2;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    min-width: 180px;
    justify-content: center;
  }
  
  .generate-button:hover:not(:disabled) {
    background-color: #357abd;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(74, 144, 226, 0.3);
  }
  
  .generate-button:active:not(:disabled) {
    transform: translateY(0);
  }
  
  .generate-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
    opacity: 0.7;
    transform: none;
  }
  
  .generate-button svg {
    stroke: currentColor;
  }
  
  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>


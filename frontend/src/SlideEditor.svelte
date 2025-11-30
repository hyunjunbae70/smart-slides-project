<script>
  import { createEventDispatcher } from 'svelte';
  
  export let selectedSlide = null;
  export let slideIndex = null;
  
  const dispatch = createEventDispatcher();
  
  // Local state for editing
  let editedTitle = '';
  let editedContent = [];
  
  // Reactive statement to update local state when selectedSlide changes
  $: if (selectedSlide) {
    editedTitle = selectedSlide.title || '';
    editedContent = selectedSlide.content ? [...selectedSlide.content] : [];
  }
  
  // Handle title change
  function handleTitleChange(event) {
    editedTitle = event.target.value;
    dispatch('slideUpdated', {
      index: slideIndex,
      slide: {
        ...selectedSlide,
        title: editedTitle,
        content: editedContent
      }
    });
  }
  
  // Handle content bullet point change
  function handleContentChange(index, event) {
    editedContent[index] = event.target.value;
    dispatch('slideUpdated', {
      index: slideIndex,
      slide: {
        ...selectedSlide,
        title: editedTitle,
        content: editedContent
      }
    });
  }
  
  // Add a new bullet point
  function addBulletPoint() {
    editedContent = [...editedContent, ''];
    dispatch('slideUpdated', {
      index: slideIndex,
      slide: {
        ...selectedSlide,
        title: editedTitle,
        content: editedContent
      }
    });
  }
  
  // Remove a bullet point
  function removeBulletPoint(index) {
    editedContent = editedContent.filter((_, i) => i !== index);
    dispatch('slideUpdated', {
      index: slideIndex,
      slide: {
        ...selectedSlide,
        title: editedTitle,
        content: editedContent
      }
    });
  }
</script>

<div class="slide-editor">
  {#if selectedSlide}
    <div class="editor-header">
      <h2>Edit Slide {slideIndex !== null ? slideIndex + 1 : ''}</h2>
      <span class="theme-badge">{selectedSlide.theme}</span>
    </div>
    
    <div class="editor-content">
      <div class="field-group">
        <label for="slide-title">Title</label>
        <textarea
          id="slide-title"
          class="title-input"
          bind:value={editedTitle}
          on:input={handleTitleChange}
          placeholder="Enter slide title..."
          rows="2"
        ></textarea>
      </div>
      
      <div class="field-group">
        <div class="content-header">
          <label for="slide-content">Content (Bullet Points)</label>
          <button 
            class="add-bullet-btn"
            on:click={addBulletPoint}
            type="button"
            aria-label="Add bullet point"
          >
            + Add Point
          </button>
        </div>
        
        <div class="content-list">
          {#each editedContent as bullet, index}
            <div class="bullet-item">
              <span class="bullet-marker">•</span>
              <textarea
                class="bullet-input"
                value={bullet}
                on:input={(e) => handleContentChange(index, e)}
                placeholder="Enter bullet point..."
                rows="2"
              ></textarea>
              <button
                class="remove-bullet-btn"
                on:click={() => removeBulletPoint(index)}
                type="button"
                aria-label="Remove bullet point"
              >
                ×
              </button>
            </div>
          {/each}
          
          {#if editedContent.length === 0}
            <div class="empty-content">
              <p>No content yet. Click "Add Point" to add bullet points.</p>
            </div>
          {/if}
        </div>
      </div>
    </div>
  {:else}
    <div class="no-slide-selected">
      <div class="empty-state">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="3" y="3" width="18" height="18" rx="2" stroke-linecap="round"/>
          <path d="M9 9h6M9 15h6M9 12h6" stroke-linecap="round"/>
        </svg>
        <h3>No Slide Selected</h3>
        <p>Select a slide from the sidebar to edit it</p>
      </div>
    </div>
  {/if}
</div>

<style>
  .slide-editor {
    flex: 1;
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #fff;
    overflow-y: auto;
  }
  
  .editor-header {
    padding: 1.5rem 2rem;
    background-color: #f8f9fa;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 10;
  }
  
  .editor-header h2 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: #333;
  }
  
  .theme-badge {
    font-size: 0.875rem;
    color: #666;
    background-color: #e8e8e8;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    text-transform: capitalize;
    font-weight: 500;
  }
  
  .editor-content {
    flex: 1;
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
  }
  
  .field-group {
    margin-bottom: 2rem;
  }
  
  .field-group label {
    display: block;
    font-size: 0.875rem;
    font-weight: 600;
    color: #555;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .title-input {
    width: 100%;
    padding: 0.75rem;
    font-size: 1.25rem;
    font-weight: 600;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-family: inherit;
    resize: vertical;
    transition: border-color 0.2s ease;
  }
  
  .title-input:focus {
    outline: none;
    border-color: #4a90e2;
  }
  
  .content-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }
  
  .add-bullet-btn {
    background-color: #4a90e2;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  
  .add-bullet-btn:hover {
    background-color: #357abd;
  }
  
  .add-bullet-btn:active {
    transform: scale(0.98);
  }
  
  .content-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .bullet-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.75rem;
    background-color: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    transition: border-color 0.2s ease;
  }
  
  .bullet-item:focus-within {
    border-color: #4a90e2;
  }
  
  .bullet-marker {
    color: #4a90e2;
    font-size: 1.5rem;
    font-weight: bold;
    line-height: 1.2;
    flex-shrink: 0;
    margin-top: 0.25rem;
  }
  
  .bullet-input {
    flex: 1;
    padding: 0.5rem;
    font-size: 1rem;
    border: 1px solid transparent;
    border-radius: 4px;
    font-family: inherit;
    resize: vertical;
    background-color: transparent;
    transition: background-color 0.2s ease;
  }
  
  .bullet-input:focus {
    outline: none;
    background-color: #fff;
    border-color: #4a90e2;
  }
  
  .remove-bullet-btn {
    background-color: transparent;
    border: none;
    color: #999;
    font-size: 1.5rem;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.2s ease;
    flex-shrink: 0;
    line-height: 1;
    padding: 0;
  }
  
  .remove-bullet-btn:hover {
    background-color: #ffebee;
    color: #f44336;
  }
  
  .empty-content {
    padding: 2rem;
    text-align: center;
    color: #999;
    background-color: #f8f9fa;
    border-radius: 8px;
    border: 2px dashed #e0e0e0;
  }
  
  .empty-content p {
    margin: 0;
    font-size: 0.875rem;
  }
  
  .no-slide-selected {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }
  
  .empty-state {
    text-align: center;
    color: #999;
  }
  
  .empty-state svg {
    margin-bottom: 1rem;
    opacity: 0.5;
  }
  
  .empty-state h3 {
    margin: 0.5rem 0;
    font-size: 1.25rem;
    color: #666;
  }
  
  .empty-state p {
    margin: 0;
    font-size: 0.875rem;
  }
</style>


<script>
  import { slideData } from './api.js';
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher();
  
  // Reactive statement to get slides from store
  $: slides = $slideData?.slides || [];
  
  // Handle slide click
  function handleSlideClick(slide, index) {
    dispatch('slideSelected', { slide, index });
  }
</script>

<aside class="slide-list">
  <div class="slide-list-header">
    <h2>Slides</h2>
    <span class="slide-count">{slides.length} {slides.length === 1 ? 'slide' : 'slides'}</span>
  </div>
  
  {#if slides.length === 0}
    <div class="empty-state">
      <p>No slides available</p>
      <p class="hint">Generate slides to see them here</p>
    </div>
  {:else}
    <div class="slides-container">
      {#each slides as slide, index (index)}
        <button
          class="slide-thumbnail"
          class:active={false}
          on:click={() => handleSlideClick(slide, index)}
          role="button"
          tabindex="0"
        >
          <div class="slide-number">{index + 1}</div>
          <div class="slide-content">
            <h3 class="slide-title">{slide.title}</h3>
            <div class="slide-preview">
              {#if slide.content && slide.content.length > 0}
                <ul class="preview-list">
                  {#each slide.content.slice(0, 2) as bullet}
                    <li>{bullet}</li>
                  {/each}
                  {#if slide.content.length > 2}
                    <li class="more-indicator">+{slide.content.length - 2} more</li>
                  {/if}
                </ul>
              {/if}
            </div>
            <span class="slide-theme">{slide.theme}</span>
          </div>
        </button>
      {/each}
    </div>
  {/if}
</aside>

<style>
  .slide-list {
    width: 300px;
    height: 100vh;
    background-color: #f5f5f5;
    border-right: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
  }
  
  .slide-list-header {
    padding: 1.5rem 1rem;
    background-color: #fff;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 10;
  }
  
  .slide-list-header h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #333;
  }
  
  .slide-count {
    font-size: 0.875rem;
    color: #666;
    background-color: #e8e8e8;
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
  }
  
  .empty-state {
    padding: 3rem 1.5rem;
    text-align: center;
    color: #999;
  }
  
  .empty-state p {
    margin: 0.5rem 0;
  }
  
  .hint {
    font-size: 0.875rem;
    font-style: italic;
  }
  
  .slides-container {
    flex: 1;
    padding: 0.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .slide-thumbnail {
    background-color: #fff;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 1rem;
    cursor: pointer;
    text-align: left;
    transition: all 0.2s ease;
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    position: relative;
  }
  
  .slide-thumbnail:hover {
    border-color: #4a90e2;
    box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2);
    transform: translateY(-2px);
  }
  
  .slide-thumbnail:active {
    transform: translateY(0);
  }
  
  .slide-thumbnail:focus {
    outline: 2px solid #4a90e2;
    outline-offset: 2px;
  }
  
  .slide-thumbnail.active {
    border-color: #4a90e2;
    background-color: #f0f7ff;
  }
  
  .slide-number {
    min-width: 32px;
    height: 32px;
    background-color: #4a90e2;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.875rem;
    flex-shrink: 0;
  }
  
  .slide-content {
    flex: 1;
    min-width: 0;
  }
  
  .slide-title {
    margin: 0 0 0.5rem 0;
    font-size: 0.9375rem;
    font-weight: 600;
    color: #333;
    line-height: 1.3;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }
  
  .slide-preview {
    margin-bottom: 0.5rem;
  }
  
  .preview-list {
    margin: 0;
    padding-left: 1.25rem;
    list-style: disc;
    font-size: 0.8125rem;
    color: #666;
    line-height: 1.4;
  }
  
  .preview-list li {
    margin-bottom: 0.25rem;
  }
  
  .more-indicator {
    color: #999;
    font-style: italic;
    list-style: none;
    padding-left: 0;
  }
  
  .slide-theme {
    display: inline-block;
    font-size: 0.75rem;
    color: #666;
    background-color: #f0f0f0;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    text-transform: capitalize;
  }
</style>


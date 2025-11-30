<script>
  import { onMount, onDestroy } from 'svelte';
  import { slideData } from './api.js';
  import { initializeWebSocket, closeWebSocket, sendMessage } from './websocket.js';
  import { initializeEditListener } from './api.js';
  import GenerateSlides from './GenerateSlides.svelte';
  import SlideList from './SlideList.svelte';
  import SlideEditor from './SlideEditor.svelte';
  import Chat from './Chat.svelte';
  
  let selectedSlide = null;
  let selectedIndex = null;
  let unsubscribeEditListener = null;
  
  // Generate a unique client ID for this session
  const clientId = `client_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  
  onMount(() => {
    // Initialize WebSocket connection
    initializeWebSocket(clientId);
    
    // Initialize edit listener for WebSocket slide edits
    unsubscribeEditListener = initializeEditListener();
  });
  
  onDestroy(() => {
    // Clean up WebSocket connection
    closeWebSocket();
    
    // Clean up edit listener
    if (unsubscribeEditListener) {
      unsubscribeEditListener();
    }
  });
  
  // Handle slide selection from SlideList
  function handleSlideSelected(event) {
    selectedSlide = event.detail.slide;
    selectedIndex = event.detail.index;
  }
  
  // Handle slide updates from SlideEditor
  function handleSlideUpdated(event) {
    const { slide, index } = event.detail;
    
    // Update the store
    $slideData.slides[index] = slide;
    slideData.set($slideData);
    
    // Update selected slide if it's the one being edited
    if (index === selectedIndex) {
      selectedSlide = slide;
    }
    
    // Note: WebSocket edits are handled automatically by the edit listener in api.js
    // Local edits are already in the store, and remote edits will be applied via WebSocket
  }
  
  // Check if we have slides
  $: hasSlides = $slideData && $slideData.slides && $slideData.slides.length > 0;
</script>

<main>
  {#if !hasSlides}
    <!-- Show generate slides interface when no slides exist -->
    <GenerateSlides />
  {:else}
    <!-- Show full interface when slides exist -->
    <div class="app-layout">
      <div class="sidebar">
        <SlideList on:slideSelected={handleSlideSelected} />
      </div>
      <div class="main-content">
        <SlideEditor 
          {selectedSlide} 
          slideIndex={selectedIndex}
          on:slideUpdated={handleSlideUpdated}
        />
      </div>
      <div class="chat-panel">
        <Chat />
      </div>
    </div>
  {/if}
</main>

<style>
  main {
    min-height: 100vh;
    font-family: system-ui, -apple-system, sans-serif;
    background-color: #fafafa;
  }
  
  .app-layout {
    display: flex;
    height: 100vh;
    overflow: hidden;
  }
  
  .sidebar {
    flex-shrink: 0;
  }
  
  .main-content {
    flex: 1;
    min-width: 0;
    overflow: hidden;
  }
  
  .chat-panel {
    flex-shrink: 0;
    width: 350px;
    border-left: 1px solid #e0e0e0;
  }
</style>

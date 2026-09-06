<script lang="ts">
  import '../app.css';
  import { onMount, setContext } from 'svelte';
  import { page } from '$app/state';
  import { loadArchive, type Archive } from '$lib/data';
  let { children } = $props();
  let archive = $state<Archive | null>(null);
  let loading = $state(true);
  let error = $state('');
  let fallback = $state(false);
  let controller: AbortController | undefined;
  setContext('archive', () => ({ archive, loading, error, fallback }));
  async function refresh() {
    controller?.abort();
    controller = new AbortController();
    loading = true;
    error = '';
    const current = controller;
    try {
      const result = await loadArchive(current.signal);
      if (!current.signal.aborted) {
        archive = result.archive;
        fallback = result.fallback;
      }
    } catch (e) {
      if (!current.signal.aborted)
        error = 'The archive could not be loaded. Check your connection and retry.';
    } finally {
      if (!current.signal.aborted) loading = false;
    }
  }
  onMount(() => {
    refresh();
    return () => controller?.abort();
  });
</script>

<svelte:head
  ><meta name="theme-color" content="#0e1117" /><meta
    name="description"
    content="Explore Chennai Metro's archived ridership, station activity, parking and peak-hour traffic."
  /></svelte:head
>
<a class="skip" href="#content">Skip to content</a>
<div class="site">
  <header class="site-header">
    <a class="brand" href="/"><span>CHENNAI METRO<small>RIDERSHIP ARCHIVE</small></span></a>
    <nav aria-label="Main navigation">
      <a class:active={page.url.pathname === '/dashboard'} href="/dashboard">Dashboard</a><a
        class:active={page.url.pathname.startsWith('/explore')}
        href="/explore/map">Explore</a
      ><a class:active={page.url.pathname === '/about'} href="/about">About &amp; sources</a>
    </nav>
    <span class="build-label"><span></span>Work in progress</span>
  </header>
  {#if page.url.pathname.startsWith('/explore')}<nav class="subnav" aria-label="Explore views">
      <a class:active={page.url.pathname === '/explore/map'} href="/explore/map">Station heatmap</a
      ><a class:active={page.url.pathname === '/explore/trends'} href="/explore/trends"
        >Station trends</a
      >
    </nav>{/if}
  <main id="content">
    {#if page.url.pathname !== '/' && loading}<div class="loading" role="status">
        <span class="loader"></span>Loading the ridership archive…
      </div>{:else if page.url.pathname !== '/' && error}<section class="panel empty">
        <h1>Archive unavailable</h1>
        <p role="alert">{error}</p>
        <button onclick={refresh}>Try again</button>
      </section>{:else}{#if fallback && page.url.pathname !== '/'}<p class="notice">
          Showing a saved development snapshot because the live archive is unavailable. <button
            onclick={refresh}>Retry live data</button
          >
        </p>{/if}{@render children()}{/if}
  </main>
  <footer>
    <span>Chennai Metro Ridership Archive <span class="muted">· An independent project</span></span>
    <div>
      <a
        href="https://github.com/PratyushBalaji/chennai-metro-ridership-tracker"
        target="_blank"
        rel="noreferrer">Data source ↗</a
      ><a
        href="https://github.com/PratyushBalaji/chennai-metro-ridership-visualisation"
        target="_blank"
        rel="noreferrer">GitHub ↗</a
      >
    </div>
    <small>Data published by CMRL. Not an official CMRL website.</small>
  </footer>
</div>

<script lang="ts">
  import { getContext } from 'svelte';
  import type { ArchiveContext } from '$lib/context';
  import Dashboard from '$lib/Dashboard.svelte';
  const state = getContext<ArchiveContext>('archive');
</script>

<svelte:head><title>Dashboard · Chennai Metro</title></svelte:head>
{#if state().archive}<Dashboard archive={state().archive!} />{/if}

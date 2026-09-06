<script lang="ts">
  import { getContext } from 'svelte';
  import type { ArchiveContext } from '$lib/context';
  import StationTrends from '$lib/StationTrends.svelte';
  const state = getContext<ArchiveContext>('archive');
</script>

<svelte:head><title>Station trends · Chennai Metro</title></svelte:head>
{#if state().archive}<StationTrends rows={state().archive!.ridership_station} />{/if}

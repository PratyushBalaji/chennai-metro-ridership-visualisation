<script lang="ts">
  import { getContext } from 'svelte';
  import type { ArchiveContext } from '$lib/context';
  import StationMap from '$lib/StationMap.svelte';
  const state = getContext<ArchiveContext>('archive');
</script>

<svelte:head><title>Station heatmap · Chennai Metro</title></svelte:head>
{#if state().archive}<StationMap rows={state().archive!.ridership_station} />{/if}

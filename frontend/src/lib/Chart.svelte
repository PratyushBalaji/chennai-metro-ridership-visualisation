<script lang="ts">
  import { onMount } from 'svelte';
  import type { Data, Layout, PlotlyHTMLElement } from 'plotly.js';
  let {
    traces,
    layout = {},
    height = 430,
    minMapZoom,
  }: { traces: Data[]; layout?: Partial<Layout>; height?: number; minMapZoom?: number } = $props();
  let element: HTMLDivElement;
  let api: typeof import('plotly.js') | undefined;
  let ready = $state(false);
  let error = $state('');
  let queue = Promise.resolve();
  let zoomBound = false;
  let enforceMinZoom: ((event: unknown) => void) | undefined;
  onMount(() => {
    let alive = true;
    let observer: ResizeObserver | undefined;
    import('plotly.js-dist-min')
      .then((module) => {
        if (!alive) return;
        api = module.default;
        ready = true;
        observer = new ResizeObserver(() => {
          if (element?.classList.contains('js-plotly-plot'))
            api?.Plots.resize(element as unknown as PlotlyHTMLElement);
        });
        observer.observe(element);
      })
      .catch(() => {
        error = 'Chart could not load. The data table is still available below.';
      });
    return () => {
      alive = false;
      ready = false;
      observer?.disconnect();
      if (zoomBound && enforceMinZoom) {
        (element as unknown as PlotlyHTMLElement).removeAllListeners?.('plotly_relayout');
      }
      queue.finally(() => api?.purge(element));
    };
  });
  $effect(() => {
    if (!ready || !api) return;
    const nextTraces = traces;
    const nextLayout = layout;
    const h = height;
    queue = queue
      .then(async () => {
        if (!ready || !api) return;
        await api.react(
          element,
          nextTraces,
          {
            paper_bgcolor: '#171c24',
            plot_bgcolor: '#171c24',
            font: { family: 'Inter, system-ui, sans-serif', color: '#bac5d4', size: 12 },
            margin: { l: 60, r: 24, t: 24, b: 95 },
            height: h,
            autosize: true,
            colorway: ['#69b7ff', '#5dd7c3', '#b3a0ff', '#f1b06e', '#f17da7', '#b8d879'],
            xaxis: { gridcolor: '#28313e', zeroline: false, automargin: true },
            yaxis: { gridcolor: '#28313e', zeroline: false, automargin: true },
            legend: { orientation: 'h', y: -0.2 },
            hovermode: 'x unified',
            ...nextLayout,
          },
          {
            responsive: true,
            displaylogo: false,
            scrollZoom: false,
            modeBarButtonsToRemove: ['lasso2d', 'select2d'],
            toImageButtonOptions: { filename: 'chennai-metro', format: 'png', scale: 2 },
          },
        );
        if (minMapZoom !== undefined && !zoomBound) {
          enforceMinZoom = (rawEvent) => {
            const event = rawEvent as Record<string, unknown>;
            const zoom = event['map.zoom'] ?? event['mapbox.zoom'];
            if (typeof zoom === 'number' && zoom < minMapZoom) {
              void api?.relayout(
                element as unknown as PlotlyHTMLElement,
                { 'map.zoom': minMapZoom } as unknown as Partial<Layout>,
              );
            }
          };
          (element as unknown as PlotlyHTMLElement).on('plotly_relayout', enforceMinZoom);
          zoomBound = true;
        }
      })
      .catch(() => {
        error = 'Unable to draw this chart. Use the data table below.';
      });
  });
</script>

{#if error}<p role="alert">{error}</p>{/if}
<div
  class="plot"
  bind:this={element}
  style:min-height={height + 'px'}
  aria-label="Interactive chart"
></div>

<style>
  .plot {
    width: 100%;
    min-width: 0;
  }
</style>

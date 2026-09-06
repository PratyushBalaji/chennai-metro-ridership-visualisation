# Svelte frontend

Standalone dark Svelte interface for the existing ridership, parking, PHPDT, heatmap and station-history views. Python/Streamlit remains at the repository root.

Run `npm install`, `npm run data:refresh`, then `npm run dev`. Check with `npm run check`, `npm test`, and `npm run build`.

The browser reads the public tracker CSVs and defaults to the latest available date. `data:refresh` creates an ignored local fallback snapshot for offline development. When fallback data is used, the UI identifies it explicitly. No finality or reconciliation status is inferred. Local snapshots are not updated automatically; rerun the command to refresh them.

Reusable views accept datasets as props. The standalone route owns loading and navigation. There is no dependency on a parent website or platform.

The initial scope is existing Streamlit functionality only. Case studies, additional analyses, route overlays, and collection-finality handling are deferred.

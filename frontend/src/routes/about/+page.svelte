<svelte:head>
  <title>About &amp; sources · Chennai Metro Ridership Archive</title>
</svelte:head>

<section class="about-intro">
  <p class="eyebrow">ABOUT THIS ARCHIVE</p>
  <h1>A small public record of how Chennai moves.</h1>
  <p class="lead">
    This is an independent project for making Chennai Metro’s published ridership data easier to
    explore, compare and reuse. The site is still under construction; this page records the work and
    sources behind it as they grow.
  </p>
</section>

<div class="about-grid">
  <section class="panel about-section">
    <p class="eyebrow">PROJECTS</p>
    <h2>Built from open work</h2>
    <ul class="source-list">
      <li>
        <a
          href="https://github.com/PratyushBalaji/chennai-metro-ridership-visualisation"
          target="_blank"
          rel="noreferrer"
        >
          Chennai Metro Ridership Visualisation ↗
        </a>
        <span>This Svelte frontend and its visualisation code.</span>
      </li>
      <li>
        <a
          href="https://github.com/PratyushBalaji/chennai-metro-ridership-tracker"
          target="_blank"
          rel="noreferrer"
        >
          Chennai Metro Ridership Tracker ↗
        </a>
        <span>Data collection, cleaning and the original Streamlit application.</span>
      </li>
      <li>
        <a
          href="https://github.com/PratyushBalaji/trainset-tracker"
          target="_blank"
          rel="noreferrer"
        >
          Trainset Tracker ↗
        </a>
        <span>A related Metro Central project that informs the frontend approach.</span>
      </li>
    </ul>
  </section>

  <section class="panel about-section">
    <p class="eyebrow">DATA &amp; MAPS</p>
    <h2>Sources and attribution</h2>
    <ul class="source-list">
      <li>
        <a href="https://chennaimetrorail.org/" target="_blank" rel="noreferrer"
          >Chennai Metro Rail Limited ↗</a
        >
        <span>Published ridership, parking and peak-hour source data.</span>
      </li>
      <li>
        <a href="https://www.openstreetmap.org/" target="_blank" rel="noreferrer">OpenStreetMap ↗</a
        >
        <span>Open geographic data used for map context and future route layers.</span>
      </li>
      <li>
        <a href="https://carto.com/attributions" target="_blank" rel="noreferrer">CARTO ↗</a>
        <span>Dark basemap tiles currently used in the station heatmap.</span>
      </li>
    </ul>
  </section>
</div>

<section class="about-note">
  <span class="status-dot"></span>
  <p>
    Data and map sources are credited here as the project develops. This is not an official CMRL
    website.
  </p>
</section>

<svelte:head><title>Chennai Metro · Ridership Archive</title></svelte:head>
<section class="hero">
  <div class="hero-copy">
    <p class="eyebrow">A PUBLIC DATA EXPLORATION</p>
    <h1>Every day,<br />a different Chennai.</h1>
    <p class="hero-description">
      A growing archive of how Chennai moves by metro. Explore daily ridership, station activity,
      parking and peak-hour traffic.
    </p>
    <p class="construction">
      <span class="status-dot"></span>This website is under construction. The introduction and the
      story behind this project are coming soon.
    </p>
    <div class="hero-actions">
      <a class="primary-link" href="/dashboard">Open the dashboard <span>↗</span></a><a
        class="secondary-link"
        href="/explore/map">Explore the map →</a
      >
    </div>
  </div>
  <div class="hero-art" aria-hidden="true">
    <div class="orb"></div>
    <div class="art-label">CHENNAI / DAILY OBSERVATIONS</div>
    <div class="abstract-chart">
      {#each [28, 35, 24, 48, 59, 45, 67, 81, 72, 51, 68, 91, 78, 65, 85, 96, 73, 53, 66, 44, 32, 39, 22, 17] as h, i}<span
          style:height={h + '%'}
          style:background={i > 11 ? '#5dd7c3' : '#69b7ff'}
        ></span>{/each}
    </div>
    <div class="art-baseline"><span>THE CITY IN NUMBERS</span><span>01 — 02</span></div>
    <p>Patterns worth looking at.</p>
  </div>
</section>
<div class="home-cards">
  <a class="panel home-card" href="/dashboard"
    ><span class="eyebrow">01 / DASHBOARD</span>
    <h2>A day on the network <span>↗</span></h2>
    <p>Browse the archived daily, hourly and station-level statistics.</p></a
  ><a class="panel home-card" href="/explore/map"
    ><span class="eyebrow">02 / MAP</span>
    <h2>Activity across Chennai <span>↗</span></h2>
    <p>Move through dates and explore station ridership geographically.</p></a
  ><a class="panel home-card" href="/explore/trends"
    ><span class="eyebrow">03 / TRENDS</span>
    <h2>A station through time <span>↗</span></h2>
    <p>Follow fare modes and weekday or weekend patterns in the archive.</p></a
  >
</div>

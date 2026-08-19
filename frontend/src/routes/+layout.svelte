<script lang="ts">
  // SvelteKit passes params to layout/page components; declare it to suppress the warning
  export let params: Record<string, string> | undefined = undefined;
</script>

<nav class="navbar">
  <a href="/" class="brand">RentFlow</a>
  <div class="nav-links">
    <a href="/equipment">Equipment</a>
  </div>
</nav>

<main>
  <slot />
</main>

<style>
  .navbar {
    background-color: #2c3e50;
    color: white;
    padding: 0.75rem 2rem;
    display: flex;
    align-items: center;
    gap: 2rem;
  }
  .brand {
    font-size: 1.2rem;
    font-weight: 700;
    color: white;
    text-decoration: none;
  }
  .nav-links {
    display: flex;
    gap: 1.5rem;
  }
  .nav-links a {
    color: #ecf0f1;
    text-decoration: none;
    font-size: 0.95rem;
  }
  .nav-links a:hover {
    color: white;
    text-decoration: underline;
  }
  main {
    min-height: calc(100vh - 48px);
    background-color: #f5f6fa;
  }
</style>

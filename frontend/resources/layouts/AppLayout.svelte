<script lang="ts">
  let { title = "subscription-server", children } = $props<{
    title?: string;
    children?: import("svelte").Snippet;
  }>();
</script>

<svelte:head>
  <title>{title}</title>
</svelte:head>

<div class="min-h-screen bg-base-200 text-base-content">
  <div class="navbar border-b border-base-300 bg-base-100 px-6 shadow-sm">
    <div class="flex-1">
      <a href="/" class="text-lg font-semibold">subscription-server</a>
    </div>
  </div>

  <main class="mx-auto max-w-5xl px-4 py-10">
    {@render children?.()}
  </main>
</div>

<script lang="ts">
  import AppLayout from "../layouts/AppLayout.svelte";

  let { title, message }: { title: string; message: string } = $props();
</script>

<AppLayout {title}>
  <div class="hero rounded-box border border-base-300 bg-base-100 shadow-sm">
    <div class="hero-content py-16 text-center">
      <div class="max-w-2xl space-y-6">
        <div class="badge badge-primary badge-outline">Litestar + Inertia</div>
        <h1 class="text-4xl font-bold sm:text-5xl">
          Simple backend-first Svelte boilerplate
        </h1>
        <p class="text-base-content/70 text-lg">{message}</p>
        <div class="alert alert-info text-left">
          <span
            >Use Inertia pages when you want backend-controlled screens without
            building a separate API layer first.</span
          >
        </div>
      </div>
    </div>
  </div>
</AppLayout>

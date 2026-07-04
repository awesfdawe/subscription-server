<script lang="ts">
  import { UserRound, KeyRound } from "@lucide/svelte";
</script>

<form action="" class="card w-full max-w-md bg-base-200 shadow-xl">
  <div class="card-body">
    <div class="text-center">
      <h1 class="card-title justify-center text-2xl font-bold">
        Create Account
      </h1>
    </div>

    <div class="flex flex-col gap-4">
      <fieldset class="fieldset">
        <legend class="fieldset-legend">Username</legend>
        <label class="input flex w-full items-center gap-3 bg-base-300">
          <UserRound size={18} class="text-base-content/40" />
          <input
            type="text"
            class="grow"
            placeholder="johndoe"
            name="username"
            required
          />
        </label>
      </fieldset>
      <fieldset class="fieldset">
        <legend class="fieldset-legend">Password</legend>
        <label class="input flex w-full items-center gap-3 bg-base-300">
          <KeyRound size={18} class="text-base-content/40" />
          <input
            type="password"
            class="grow"
            placeholder="••••••••"
            name="password"
            required
          />
        </label>
      </fieldset>
    </div>

    <button class="btn w-full btn-primary">Register</button>
  </div>
</form>

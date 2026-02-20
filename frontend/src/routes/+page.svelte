<script lang="ts">
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { isAuthenticated } from "$lib/auth";

	let health = { status: "loading" };
	const apiUrl = import.meta.env.PUBLIC_API_URL || "http://localhost:8000";

	onMount(async () => {
		if (isAuthenticated()) {
			goto("/dashboard");
			return;
		}
		try {
			const res = await fetch(`${apiUrl}/api/health`);
			health = await res.json();
		} catch {
			health = { status: "error", message: "API unreachable" };
		}
	});
</script>

<main class="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8">
	<h1 class="text-3xl font-bold text-gray-900 mb-4">Cultivar</h1>
	<p class="text-gray-600 mb-6">From seed to harvest</p>
	{#if health.status === "ok"}
		<div class="px-4 py-2 bg-green-100 text-green-800 rounded-lg mb-6">
			API connected: {health.service}
		</div>
	{:else if health.status === "error"}
		<div class="px-4 py-2 bg-red-100 text-red-800 rounded-lg mb-6">
			{health.message || "API unreachable"}
		</div>
	{:else}
		<div class="px-4 py-2 bg-gray-100 text-gray-600 rounded-lg mb-6">Connecting...</div>
	{/if}
	<div class="flex gap-4">
		<a
			href="/login"
			class="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800"
		>
			Sign in
		</a>
		<a
			href="/register"
			class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
		>
			Create account
		</a>
	</div>
</main>

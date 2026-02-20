<script lang="ts">
	import { onMount } from 'svelte';

	let health = { status: 'loading' };

	onMount(async () => {
		const apiUrl = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';
		try {
			const res = await fetch(`${apiUrl}/api/health`);
			health = await res.json();
		} catch {
			health = { status: 'error', message: 'API unreachable' };
		}
	});
</script>

<main class="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8">
	<h1 class="text-3xl font-bold text-gray-900 mb-4">Cultivar</h1>
	<p class="text-gray-600 mb-6">SvelteKit + FastAPI template</p>
	{#if health.status === 'ok'}
		<div class="px-4 py-2 bg-green-100 text-green-800 rounded-lg">
			API connected: {health.service}
		</div>
	{:else if health.status === 'error'}
		<div class="px-4 py-2 bg-red-100 text-red-800 rounded-lg">
			{health.message || 'API unreachable'}
		</div>
	{:else}
		<div class="px-4 py-2 bg-gray-100 text-gray-600 rounded-lg">Connecting...</div>
	{/if}
</main>

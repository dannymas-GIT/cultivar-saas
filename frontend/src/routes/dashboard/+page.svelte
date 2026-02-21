<script lang="ts">
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { getToken, clearToken } from "$lib/auth";

	const apiUrl = import.meta.env.PUBLIC_API_URL || "";
	let ideas: { id: string; title: string; status: string }[] = $state([]);
	let loading = $state(true);
	let error = $state("");

	onMount(() => {
		const token = getToken();
		if (!token) {
			goto("/login");
			return;
		}
		const controller = new AbortController();
		const timeout = setTimeout(() => controller.abort(), 15000);
		fetch(`${apiUrl}/api/ideas`, {
			headers: { Authorization: `Bearer ${token}` },
			signal: controller.signal,
		})
			.then(async (res) => {
				clearTimeout(timeout);
				if (res.status === 401) {
					clearToken();
					goto("/login");
					return;
				}
				if (!res.ok) throw new Error("Failed to load ideas");
				ideas = await res.json();
			})
			.catch((e) => {
				clearTimeout(timeout);
				if (e instanceof Error) {
					error = e.name === "AbortError" ? "Request timed out." : e.message;
				} else {
					error = "Failed to load";
				}
			})
			.finally(() => {
				loading = false;
			});
	});

	function logout() {
		clearToken();
		goto("/login");
	}
</script>

<main class="min-h-screen bg-gray-50 p-8">
	<div class="max-w-2xl mx-auto">
		<div class="flex justify-between items-center mb-6">
			<h1 class="text-2xl font-bold text-gray-900">Cultivar Dashboard</h1>
			<button
				onclick={logout}
				class="text-sm text-gray-600 hover:text-gray-900"
			>
				Sign out
			</button>
		</div>
		{#if loading}
			<p class="text-gray-500">Loading...</p>
		{:else if error}
			<p class="text-red-600">{error}</p>
		{:else}
			<div class="space-y-4">
				<h2 class="text-lg font-semibold text-gray-800">Your Ideas</h2>
				{#if ideas.length === 0}
					<p class="text-gray-500">No ideas yet. Add one to get started.</p>
				{:else}
					<ul class="space-y-2">
						{#each ideas as idea}
							<li class="p-4 bg-white rounded-lg shadow">
								<a href="/ideas/{idea.id}" class="font-medium text-gray-900">{idea.title}</a>
								<span class="text-sm text-gray-500 ml-2">({idea.status})</span>
							</li>
						{/each}
					</ul>
				{/if}
			</div>
		{/if}
	</div>
</main>

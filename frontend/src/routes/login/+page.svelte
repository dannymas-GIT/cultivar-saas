<script lang="ts">
	import { goto } from "$app/navigation";
	import { setToken } from "$lib/auth";

	const apiUrl = import.meta.env.PUBLIC_API_URL || "";
	let email = "";
	let password = "";
	let error = "";
	let loading = false;

	async function handleSubmit() {
		error = "";
		loading = true;
		try {
			const res = await fetch(`${apiUrl}/api/auth/login`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ email, password }),
			});
			const data = await res.json();
			if (!res.ok) throw new Error(data.detail || "Login failed");
			setToken(data.access_token);
			goto("/dashboard");
		} catch (e) {
			error = e instanceof Error ? e.message : "Login failed";
		} finally {
			loading = false;
		}
	}
</script>

<main class="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8">
	<h1 class="text-3xl font-bold text-gray-900 mb-2">Cultivar</h1>
	<p class="text-gray-600 mb-6">Seed to harvest</p>
	<form on:submit|preventDefault={handleSubmit} class="w-full max-w-sm space-y-4">
		<input
			type="email"
			bind:value={email}
			placeholder="Email"
			class="w-full px-4 py-2 border rounded-lg"
			required
		/>
		<input
			type="password"
			bind:value={password}
			placeholder="Password"
			class="w-full px-4 py-2 border rounded-lg"
			required
		/>
		{#if error}
			<p class="text-red-600 text-sm">{error}</p>
		{/if}
		<button
			type="submit"
			disabled={loading}
			class="w-full py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 disabled:opacity-50"
		>
			{loading ? "Signing in..." : "Sign in"}
		</button>
	</form>
	<p class="mt-4 text-gray-500 text-sm">
		<a href="/register" class="underline">Create account</a>
	</p>
</main>

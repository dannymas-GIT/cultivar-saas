<script lang="ts">
	import type { Snippet } from "svelte";
	import { goto } from "$app/navigation";
	import { getToken, clearToken } from "$lib/auth";
	import { browser } from "$app/environment";
	import Sidebar from "$lib/components/Sidebar.svelte";
	import Breadcrumb from "$lib/components/Breadcrumb.svelte";
	import { themeStore } from "$lib/stores/theme";
	import "$lib/components/dashboard/dashboard.css";

	let { children }: { children?: Snippet } = $props();

	if (browser) {
		const token = getToken();
		if (!token) {
			goto("/login");
		}
		themeStore.init();
		authChecked = true;
	}

	function logout() {
		clearToken();
		goto("/login");
	}
</script>

{#if browser && !getToken()}
	<p>Redirecting to login...</p>
{:else}
	<div class="dashboard-layout">
		<aside class="dashboard-sidebar">
			<Sidebar />
		</aside>
		<div class="dashboard-main">
			<header class="dashboard-topbar">
				<div class="dashboard-topbar-brand">
					<span class="topbar-logo" aria-hidden="true"></span>
					<h1>Cultivar</h1>
				</div>
				<div class="dashboard-topbar-controls">
					<label class="theme-label">
						<span class="theme-label-text">Theme</span>
						<select
							value={themeStore.theme}
							onchange={(e) => (themeStore.theme = (e.currentTarget.value as "light" | "dark" | "system"))}
							class="theme-select"
						>
							<option value="system">system</option>
							<option value="light">light</option>
							<option value="dark">dark</option>
						</select>
					</label>
					<button type="button" class="profile-btn" onclick={logout} aria-label="Sign out">
						Sign out
					</button>
				</div>
			</header>
			<main class="dashboard-content">
				{@render children?.()}
			</main>
		</div>
	</div>
{/if}

<style>
	.topbar-logo {
		display: block;
		width: 28px;
		height: 28px;
		flex-shrink: 0;
		background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%239cdb74' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83M8 12a4 4 0 1 0 8 0 4 4 0 0 0-8 0z'/%3E%3Ccircle cx='12' cy='12' r='3' fill='%239cdb74' opacity='0.6'/%3E%3C/svg%3E") center/contain
			no-repeat;
	}
	.theme-label {
		display: flex;
		align-items: center;
		gap: 8px;
	}
	.theme-label-text {
		font-size: 0.875rem;
		color: var(--cultivar-muted);
	}
	.theme-select {
		padding: 6px 10px;
		border: 1px solid var(--cultivar-border);
		border-radius: 8px;
		background: var(--cultivar-surface-alt);
		color: var(--cultivar-text);
		font-size: 0.875rem;
		cursor: pointer;
	}
	.profile-btn {
		padding: 6px 12px;
		border: 1px solid var(--cultivar-border);
		border-radius: 8px;
		background: var(--cultivar-surface-alt);
		color: var(--cultivar-text);
		font-size: 0.875rem;
		cursor: pointer;
	}
	.profile-btn:hover {
		background: var(--cultivar-surface);
	}
</style>

<script lang="ts">
	import { browser } from "$app/environment";
	import { goto } from "$app/navigation";
	import Breadcrumb from "$lib/components/Breadcrumb.svelte";
	import Card from "$lib/components/Card.svelte";
	import JourneyPathway from "$lib/components/JourneyPathway.svelte";
	import { apiGet } from "$lib/api";

	interface Overview {
		counts: { ideas: number; initiatives: number; goals: number; tasks: number };
		taskStatus: { planned: number; approved: number; running: number; completed: number };
	}

	let overview = $state<Overview | null>(null);
	let loading = $state(true);
	let error = $state("");

	if (browser) {
		apiGet<Overview>("/api/dashboard/overview")
			.then((data) => {
				overview = data;
			})
			.catch((e) => {
				error = e instanceof Error ? e.message : "Failed to load";
			})
			.finally(() => {
				loading = false;
			});
	}
</script>

<Breadcrumb items={[{ label: "Greenhouse", href: "/dashboard/overview" }, { label: "Overview" }]} />
<h2 class="page-title">Greenhouse</h2>
<p class="nav-flow-hint">
	You are here: <strong>Overview</strong> · Use <strong>Create idea/seed</strong> to start; <strong>Idea Garden</strong> for project views.
</p>

{#if loading}
	<p class="muted-note">Loading...</p>
{:else if error}
	<p class="error-note">{error}</p>
{:else if overview}
	<div class="overview-layout">
		<JourneyPathway counts={overview.counts} />
		<p class="guided-setup-cta">
			<button type="button" class="primary-button" onclick={() => goto("/dashboard/create")}>
				Create idea/seed
			</button>
		</p>

		<section id="initiatives-section">
			<h3 class="section-heading">Status breakdown</h3>
			<div class="card-grid">
				<Card>
					<div class="card-label">Planned</div>
					<div class="card-value">{overview.taskStatus.planned ?? 0}</div>
				</Card>
				<Card>
					<div class="card-label">Approved</div>
					<div class="card-value">{overview.taskStatus.approved ?? 0}</div>
				</Card>
				<Card>
					<div class="card-label">Running</div>
					<div class="card-value">{overview.taskStatus.running ?? 0}</div>
				</Card>
				<Card>
					<div class="card-label">Completed</div>
					<div class="card-value">{overview.taskStatus.completed ?? 0}</div>
				</Card>
			</div>
		</section>
		<section id="goals-section">
			<h3 class="section-heading">Goals</h3>
			<p class="muted-note">
				View goals in <a href="/dashboard/ideas" class="link">Idea Garden</a>.
			</p>
		</section>
		<section id="tasks-section">
			<h3 class="section-heading">Tasks</h3>
			<p class="muted-note">
				View tasks in <a href="/dashboard/ideas" class="link">Idea Garden</a> or
				<a href="/dashboard/create" class="link">Create idea/seed</a>.
			</p>
		</section>
	</div>
{/if}

<style>
	.overview-layout {
		margin-top: 16px;
	}
	.guided-setup-cta {
		margin: 16px 0;
	}
	.primary-button {
		padding: 10px 20px;
		border: none;
		border-radius: 8px;
		background: linear-gradient(90deg, var(--cultivar-accent), var(--cultivar-accent-green));
		color: var(--cultivar-bg);
		font-weight: 600;
		cursor: pointer;
	}
	.primary-button:hover {
		opacity: 0.95;
	}
	.section-heading {
		margin: 24px 0 12px 0;
		font-size: 1.1rem;
		color: var(--cultivar-text);
	}
	.card-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
		gap: 12px;
	}
	.card-label {
		font-size: 0.8rem;
		color: var(--cultivar-muted);
	}
	.card-value {
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--cultivar-text);
	}
	.muted-note {
		color: var(--cultivar-muted);
		font-size: 0.9rem;
	}
	.error-note {
		color: #f87171;
	}
	.link {
		color: var(--cultivar-accent);
		text-decoration: none;
	}
	.link:hover {
		text-decoration: underline;
	}
</style>

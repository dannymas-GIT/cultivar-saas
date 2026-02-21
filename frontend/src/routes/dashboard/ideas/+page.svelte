<script lang="ts">
	import { browser } from "$app/environment";
	import Breadcrumb from "$lib/components/Breadcrumb.svelte";
	import StatusBadge from "$lib/components/StatusBadge.svelte";
	import JourneyPathway from "$lib/components/JourneyPathway.svelte";
	import Card from "$lib/components/Card.svelte";
	import EmptyState from "$lib/components/EmptyState.svelte";
	import { apiGet } from "$lib/api";

	interface Idea {
		id: string;
		title: string;
		description?: string;
		tags: string[];
		status: string;
	}
	interface Initiative {
		id: string;
		name: string;
		idea_id: string;
		status: string;
		priority: string;
	}
	interface Overview {
		counts: { ideas: number; initiatives: number; goals: number; tasks: number };
	}

	let ideas = $state<Idea[]>([]);
	let initiatives = $state<Initiative[]>([]);
	let overview = $state<Overview | null>(null);
	let loading = $state(true);
	let statusFilter = $state("");
	let tagFilter = $state("");

	if (browser) {
		Promise.all([
			apiGet<Idea[]>("/api/ideas").then((d) => (ideas = Array.isArray(d) ? d : [])),
			apiGet<Initiative[]>("/api/initiatives").then((d) => (initiatives = Array.isArray(d) ? d : [])),
			apiGet<Overview>("/api/dashboard/overview").then((d) => (overview = d)),
		]).finally(() => (loading = false));
	}

	const filteredIdeas = $derived(
		ideas.filter((i) => {
			if (statusFilter && i.status !== statusFilter) return false;
			if (tagFilter && !(i.tags || []).includes(tagFilter)) return false;
			return true;
		})
	);
	const allTags = $derived([...new Set(ideas.flatMap((i) => i.tags || []))]);
</script>

<Breadcrumb items={[{ label: "Greenhouse", href: "/dashboard/overview" }, { label: "Idea Garden" }]} />
<h2 class="page-title">Idea Garden</h2>
<p class="nav-flow-hint">Pick a seed to see its plans, goals, and tasks.</p>

{#if overview}
	<JourneyPathway counts={overview.counts} />
{/if}

<section class="filters">
	<label class="compact-label">
		Status
		<select bind:value={statusFilter}>
			<option value="">All</option>
			<option value="new">new</option>
			<option value="planning">planning</option>
			<option value="active">active</option>
			<option value="done">done</option>
		</select>
	</label>
	<label class="compact-label">
		Tag
		<select bind:value={tagFilter}>
			<option value="">All</option>
			{#each allTags as tag}
				<option value={tag}>{tag}</option>
			{/each}
		</select>
	</label>
</section>

{#if loading}
	<p class="muted-note">Loading...</p>
{:else if filteredIdeas.length === 0}
	<EmptyState message={ideas.length === 0 ? "No ideas yet. Create one in Create idea/seed." : "No ideas match the filter."} />
{:else}
	<div class="idea-grid">
		{#each filteredIdeas as idea}
			<a href="/dashboard/ideas/{idea.id}" class="idea-card-link">
				<Card>
					<span class="seed-icon">🌱</span>
					<h4 class="idea-title">{idea.title}</h4>
					<StatusBadge status={idea.status} />
					{#if idea.tags?.length}
						<div class="idea-tags">
							{#each idea.tags as tag}
								<span class="tag">{tag}</span>
							{/each}
						</div>
					{/if}
					{@const initCount = initiatives.filter((i) => i.idea_id === idea.id).length}
					<p class="idea-meta">{initCount} initiative(s)</p>
				</Card>
			</a>
		{/each}
	</div>
{/if}

<style>
	.filters {
		display: flex;
		gap: 16px;
		margin: 16px 0;
	}
	.compact-label {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 0.875rem;
		color: var(--cultivar-muted);
	}
	.compact-label select {
		padding: 6px 10px;
		border: 1px solid var(--cultivar-border);
		border-radius: 8px;
		background: var(--cultivar-surface-alt);
		color: var(--cultivar-text);
	}
	.idea-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
		gap: 16px;
		margin-top: 16px;
	}
	.idea-card-link {
		text-decoration: none;
		color: inherit;
	}
	.idea-card-link .card {
		height: 100%;
		cursor: pointer;
	}
	.idea-card-link .card:hover {
		border-color: var(--cultivar-accent);
	}
	.seed-icon {
		font-size: 1.5rem;
		display: block;
		margin-bottom: 8px;
	}
	.idea-title {
		margin: 0 0 8px 0;
		font-size: 1rem;
		color: var(--cultivar-text);
	}
	.idea-tags {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;
		margin: 8px 0;
	}
	.tag {
		padding: 2px 6px;
		border-radius: 4px;
		background: var(--cultivar-surface-alt);
		font-size: 0.75rem;
		color: var(--cultivar-muted);
	}
	.idea-meta {
		margin: 8px 0 0 0;
		font-size: 0.8rem;
		color: var(--cultivar-muted);
	}
</style>

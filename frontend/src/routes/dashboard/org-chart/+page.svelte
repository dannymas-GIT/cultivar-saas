<script lang="ts">
	import { browser } from "$app/environment";
	import Breadcrumb from "$lib/components/Breadcrumb.svelte";
	import Card from "$lib/components/Card.svelte";
	import StatusBadge from "$lib/components/StatusBadge.svelte";
	import EmptyState from "$lib/components/EmptyState.svelte";
	import { apiGet } from "$lib/api";

	interface Goal {
		id: string | null;
		title: string;
		status: string;
		tasks: { id: string; title: string; status: string }[];
	}
	interface Initiative {
		id: string;
		name: string;
		ideaId: string;
		status: string;
		priority: string;
		goals: Goal[];
	}
	interface OrgTree {
		initiatives: Initiative[];
	}

	let tree = $state<OrgTree | null>(null);
	let loading = $state(true);
	let error = $state("");

	if (browser) {
		apiGet<OrgTree>("/api/dashboard/org-tree")
			.then((d) => (tree = d))
			.catch((e) => (error = e instanceof Error ? e.message : "Failed"))
			.finally(() => (loading = false));
	}
</script>

<Breadcrumb items={[{ label: "Greenhouse", href: "/dashboard/overview" }, { label: "Org Chart" }]} />
<h2 class="page-title">Org Chart</h2>
<p class="nav-flow-hint">Visual tree of initiatives, goals, and tasks.</p>

{#if loading}
	<p class="muted-note">Loading...</p>
{:else if error}
	<p class="error-note">{error}</p>
{:else if !tree?.initiatives?.length}
	<EmptyState message="No initiatives yet. Create ideas and apply plans in Create idea/seed." />
{:else}
	<div class="org-tree">
		{#each tree.initiatives as init}
			<Card class="org-initiative">
				<div class="org-node org-init">
					<span class="org-icon">🌿</span>
					<span class="org-label">{init.name}</span>
					<StatusBadge status={init.status} variant="muted" />
					<span class="org-priority">{init.priority}</span>
				</div>
				{#each init.goals as goal}
					<div class="org-goal-wrap">
						<div class="org-node org-goal">
							<span class="org-icon">🌳</span>
							<span class="org-label">{goal.title}</span>
							<StatusBadge status={goal.status} variant="muted" />
						</div>
						{#each goal.tasks as task}
							<div class="org-node org-task">
								<span class="org-icon">🌸</span>
								<span class="org-label">{task.title}</span>
								<StatusBadge status={task.status} variant="muted" />
							</div>
						{/each}
					</div>
				{/each}
			</Card>
		{/each}
	</div>
{/if}

<style>
	.org-tree {
		display: flex;
		flex-direction: column;
		gap: 16px;
		margin-top: 20px;
	}
	.org-initiative {
		padding: 16px;
	}
	.org-node {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 8px 12px;
		margin: 4px 0;
		border-radius: 8px;
		background: var(--cultivar-surface-alt);
		border: 1px solid var(--cultivar-border);
	}
	.org-init {
		font-weight: 600;
		background: var(--cultivar-surface);
	}
	.org-goal-wrap {
		margin-left: 24px;
		border-left: 2px solid var(--cultivar-border);
		padding-left: 12px;
	}
	.org-goal {
		font-size: 0.95rem;
	}
	.org-task {
		margin-left: 24px;
		font-size: 0.9rem;
	}
	.org-icon {
		font-size: 1rem;
	}
	.org-label {
		flex: 1;
	}
	.org-priority {
		font-size: 0.75rem;
		color: var(--cultivar-muted);
	}
</style>

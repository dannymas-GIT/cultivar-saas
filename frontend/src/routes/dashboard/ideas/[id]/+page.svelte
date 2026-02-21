<script lang="ts">
	import { page } from "$app/stores";
	import { browser } from "$app/environment";
	import Breadcrumb from "$lib/components/Breadcrumb.svelte";
	import StatusBadge from "$lib/components/StatusBadge.svelte";
	import Card from "$lib/components/Card.svelte";
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
	interface Goal {
		id: string;
		title: string;
		initiative_id: string;
		status: string;
	}
	interface Task {
		id: string;
		title: string;
		initiative_id: string;
		goal_id?: string;
		status: string;
	}

	const id = $derived($page.params.id);
	let idea = $state<Idea | null>(null);
	let initiatives = $state<Initiative[]>([]);
	let goals = $state<Goal[]>([]);
	let tasks = $state<Task[]>([]);
	let loading = $state(true);
	let error = $state("");

	$effect(() => {
		const currentId = $page.params.id;
		if (!browser || !currentId) return;
		loading = true;
		error = "";
		Promise.all([
			apiGet<Idea>(`/api/ideas/${currentId}`).then((d) => (idea = d)),
			apiGet<Initiative[]>(`/api/initiatives?idea_id=${currentId}`).then((d) => (initiatives = Array.isArray(d) ? d : [])),
			apiGet<Goal[]>("/api/goals").then((d) => (goals = Array.isArray(d) ? d : [])),
			apiGet<Task[]>("/api/tasks").then((d) => (tasks = Array.isArray(d) ? d : [])),
		]).catch((e) => (error = e instanceof Error ? e.message : "Failed")).finally(() => (loading = false));
	});

	const initiativeIds = $derived(new Set(initiatives.map((i) => i.id)));
	const goalsForIdea = $derived(goals.filter((g) => initiativeIds.has(g.initiative_id)));
	const tasksForIdea = $derived(tasks.filter((t) => initiativeIds.has(t.initiative_id)));
	const goalsByInit = $derived.by(() => {
		const m = new Map<string, Goal[]>();
		for (const g of goalsForIdea) {
			const list = m.get(g.initiative_id) ?? [];
			list.push(g);
			m.set(g.initiative_id, list);
		}
		return m;
	});
	const tasksByGoal = $derived.by(() => {
		const m = new Map<string, Task[]>();
		for (const t of tasksForIdea) {
			if (t.goal_id) {
				const list = m.get(t.goal_id) ?? [];
				list.push(t);
				m.set(t.goal_id, list);
			}
		}
		return m;
	});
</script>

<Breadcrumb
	items={[
		{ label: "Greenhouse", href: "/dashboard/overview" },
		{ label: "Idea Garden", href: "/dashboard/ideas" },
		{ label: idea?.title ?? id }
	]}
/>

{#if loading}
	<p class="muted-note">Loading...</p>
{:else if error || !idea}
	<p class="error-note">{error || "Idea not found"}</p>
{:else}
	<h2 class="page-title">{idea.title}</h2>
	<div class="idea-detail">
		<Card>
			<div class="card-label">Seed</div>
			<StatusBadge status={idea.status} />
			{#if idea.description}
				<p class="idea-desc">{idea.description}</p>
			{/if}
			{#if idea.tags?.length}
				<div class="tags">
					{#each idea.tags as tag}
						<span class="tag">{tag}</span>
					{/each}
				</div>
			{/if}
		</Card>

		<section class="hierarchy">
			<h3 class="section-heading">From seed to tasks</h3>
			<ul class="tree-root">
				<li class="tree-node tree-seed">
					<span class="tree-icon">🌱</span>
					<span>{idea.title}</span>
				</li>
				{#each initiatives as init}
					<li class="tree-branch">
						<details open>
							<summary class="tree-node tree-init">
								<span class="tree-icon">🌿</span>
								<span>{init.name}</span>
								<StatusBadge status={init.status} variant="muted" />
							</summary>
							<ul>
								{#each (goalsByInit.get(init.id) ?? []) as goal}
									<li>
										<details open>
											<summary class="tree-node tree-goal">
												<span class="tree-icon">🌳</span>
												<span>{goal.title}</span>
											</summary>
											<ul>
												{#each (tasksByGoal.get(goal.id) ?? []) as task}
													<li class="tree-node tree-task">
														<span class="tree-icon">🌸</span>
														<span>{task.title}</span>
													</li>
												{/each}
											</ul>
										</details>
									</li>
								{/each}
							</ul>
						</details>
					</li>
				{/each}
			</ul>
		</section>
	</div>
{/if}

<style>
	.idea-detail {
		margin-top: 20px;
	}
	.idea-desc {
		margin: 8px 0;
		font-size: 0.9rem;
		color: var(--cultivar-muted);
	}
	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
	}
	.tag {
		padding: 2px 8px;
		border-radius: 4px;
		background: var(--cultivar-surface-alt);
		font-size: 0.75rem;
		color: var(--cultivar-muted);
	}
	.section-heading {
		margin: 24px 0 12px 0;
		font-size: 1rem;
		color: var(--cultivar-text);
	}
	.tree-root,
	.tree-branch ul {
		list-style: none;
		margin: 0;
		padding-left: 20px;
	}
	.tree-node {
		padding: 6px 8px;
		margin: 2px 0;
		border-radius: 6px;
		display: flex;
		align-items: center;
		gap: 8px;
	}
	.tree-icon {
		font-size: 1rem;
	}
</style>

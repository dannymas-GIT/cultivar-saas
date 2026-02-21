<script lang="ts">
	import { browser } from "$app/environment";
	import Breadcrumb from "$lib/components/Breadcrumb.svelte";
	import Card from "$lib/components/Card.svelte";
	import StatusBadge from "$lib/components/StatusBadge.svelte";
	import EmptyState from "$lib/components/EmptyState.svelte";
	import { apiGet, apiPost } from "$lib/api";

	interface Agent {
		id: string;
		name: string;
		role: string;
		description?: string;
		status: string;
	}

	let agents = $state<Agent[]>([]);
	let loading = $state(true);
	let feedback = $state("");
	let showForm = $state(false);
	let formName = $state("");
	let formRole = $state("gardener");
	let formDesc = $state("");

	if (browser) {
		apiGet<Agent[]>("/api/agents")
			.then((d) => (agents = Array.isArray(d) ? d : []))
			.catch(() => {})
			.finally(() => (loading = false));
	}

	function setFeedback(msg: string) {
		feedback = msg;
		setTimeout(() => (feedback = ""), 3000);
	}

	async function createAgent() {
		const name = formName.trim();
		if (!name) {
			setFeedback("Name is required.");
			return;
		}
		try {
			const a = await apiPost<Agent>("/api/agents", {
				name,
				role: formRole,
				description: formDesc.trim() || undefined,
			});
			agents = [a, ...agents];
			showForm = false;
			formName = "";
			formDesc = "";
			setFeedback("Agent created.");
		} catch (e) {
			setFeedback(e instanceof Error ? e.message : "Failed");
		}
	}
</script>

<Breadcrumb items={[{ label: "Greenhouse", href: "/dashboard/overview" }, { label: "Gardeners" }]} />
<h2 class="page-title">Gardeners</h2>
<p class="nav-flow-hint">
	A gardener is an agent that handles specific tasks. Here you can add and manage your gardener profiles.
</p>

{#if feedback}
	<div class="inline-feedback">{feedback}</div>
{/if}

<section class="gardener-intro">
	<p>
		Use <strong>Create idea/seed</strong> to add ideas and run task actions; use <strong>Idea Garden</strong> to
		view a seed's plan.
	</p>
</section>

<button type="button" class="btn-primary" onclick={() => (showForm = !showForm)}>
	{showForm ? "Cancel" : "Add Gardener"}
</button>

{#if showForm}
	<Card class="form-card">
		<h4>New Gardener</h4>
		<label class="compact-label">
			Name
			<input type="text" bind:value={formName} placeholder="e.g. Content Writer" />
		</label>
		<label class="compact-label">
			Role
			<select bind:value={formRole}>
				<option value="gardener">gardener</option>
				<option value="researcher">researcher</option>
				<option value="marketer">marketer</option>
				<option value="security">security</option>
				<option value="operations">operations</option>
			</select>
		</label>
		<label class="compact-label">
			Description
			<textarea bind:value={formDesc} placeholder="What this gardener does" rows="2"></textarea>
		</label>
		<button type="button" class="btn" onclick={createAgent}>Create</button>
	</Card>
{/if}

{#if loading}
	<p class="muted-note">Loading...</p>
{:else if agents.length === 0}
	<EmptyState message="No gardeners yet. Add one to get started." />
{:else}
	<div class="agent-grid">
		{#each agents as agent}
			<Card>
				<div class="agent-header">
					<span class="agent-icon">🌱</span>
					<h4 class="agent-name">{agent.name}</h4>
					<StatusBadge status={agent.status} variant="muted" />
				</div>
				<p class="agent-role">{agent.role}</p>
				{#if agent.description}
					<p class="agent-desc">{agent.description}</p>
				{/if}
			</Card>
		{/each}
	</div>
{/if}

<style>
	.inline-feedback {
		padding: 8px 12px;
		background: var(--cultivar-accent-bg, rgba(86, 182, 255, 0.15));
		border-radius: 8px;
		margin-bottom: 12px;
		font-size: 0.9rem;
	}
	.gardener-intro {
		margin: 16px 0;
		padding: 12px;
		border: 1px solid var(--cultivar-border);
		border-radius: 8px;
		background: var(--cultivar-surface-alt);
		font-size: 0.9rem;
		color: var(--cultivar-muted);
	}
	.btn-primary {
		padding: 8px 16px;
		border: none;
		border-radius: 8px;
		background: var(--cultivar-accent);
		color: var(--cultivar-bg);
		font-weight: 600;
		cursor: pointer;
		margin-bottom: 16px;
	}
	.form-card {
		margin-bottom: 20px;
	}
	.form-card h4 {
		margin: 0 0 12px 0;
	}
	.compact-label {
		display: block;
		margin: 12px 0 4px 0;
		font-size: 0.875rem;
		color: var(--cultivar-muted);
	}
	.compact-label input,
	.compact-label select,
	.compact-label textarea {
		width: 100%;
		padding: 8px 12px;
		border: 1px solid var(--cultivar-border);
		border-radius: 8px;
		background: var(--cultivar-surface-alt);
		color: var(--cultivar-text);
	}
	.btn {
		margin-top: 12px;
		padding: 8px 16px;
		border: 1px solid var(--cultivar-border);
		border-radius: 8px;
		background: var(--cultivar-surface-alt);
		color: var(--cultivar-text);
		cursor: pointer;
	}
	.agent-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
		gap: 16px;
		margin-top: 16px;
	}
	.agent-header {
		display: flex;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
	}
	.agent-icon {
		font-size: 1.2rem;
	}
	.agent-name {
		margin: 0;
		font-size: 1rem;
	}
	.agent-role {
		margin: 8px 0 0 0;
		font-size: 0.85rem;
		color: var(--cultivar-muted);
	}
	.agent-desc {
		margin: 4px 0 0 0;
		font-size: 0.8rem;
		color: var(--cultivar-muted);
	}
</style>

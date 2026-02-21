<script lang="ts">
	import { browser } from "$app/environment";
	import Breadcrumb from "$lib/components/Breadcrumb.svelte";
	import Card from "$lib/components/Card.svelte";
	import { apiGet, apiPost } from "$lib/api";

	let title = $state("");
	let description = $state("");
	let tags = $state("");
	let feedback = $state("");
	let loading = $state(false);
	let ideas = $state<{ id: string; title: string; description?: string }[]>([]);
	let planMarkdown = $state("");
	let planGenerating = $state(false);
	let applyingPlan = $state(false);
	let selectedIdeaId = $state("");

	if (browser) {
		apiGet<{ id: string; title: string; description?: string }[]>("/api/ideas")
			.then((data) => {
				ideas = Array.isArray(data) ? data : [];
				if (ideas.length > 0 && !selectedIdeaId) selectedIdeaId = ideas[0].id;
			})
			.catch(() => {});
	}

	function setFeedback(msg: string) {
		feedback = msg;
		setTimeout(() => (feedback = ""), 4000);
	}

	async function createIdea() {
		const t = title.trim();
		if (!t) {
			setFeedback("Please enter a title.");
			return;
		}
		loading = true;
		try {
			const idea = await apiPost<{ id: string; title: string; description?: string }>("/api/ideas", {
				title: t,
				description: description.trim() || undefined,
				tags: tags.split(",").map((s) => s.trim()).filter(Boolean),
			});
			ideas = [...ideas, idea];
			selectedIdeaId = idea.id;
			title = "";
			description = "";
			tags = "";
			setFeedback("Idea created.");
		} catch (e) {
			setFeedback(e instanceof Error ? e.message : "Failed");
		} finally {
			loading = false;
		}
	}

	async function generatePlan() {
		const ideaId = selectedIdeaId;
		if (!ideaId) {
			setFeedback("Select or create an idea first.");
			return;
		}
		const idea = ideas.find((i) => i.id === ideaId);
		const ideaText = idea
			? `${idea.title}${idea.description ? ": " + idea.description : ""}`
			: title || description;
		if (!ideaText.trim()) {
			setFeedback("Enter idea text to generate a plan.");
			return;
		}
		planGenerating = true;
		try {
			const res = await apiPost<{ plan_markdown: string }>("/api/plan", { idea: ideaText });
			planMarkdown = res.plan_markdown || "";
			setFeedback(planMarkdown ? "Plan generated." : "No plan content returned.");
		} catch (e) {
			setFeedback(e instanceof Error ? e.message : "Plan generation failed");
		} finally {
			planGenerating = false;
		}
	}

	async function applyPlan() {
		if (!selectedIdeaId) {
			setFeedback("Select an idea first.");
			return;
		}
		if (!planMarkdown.trim()) {
			setFeedback("Generate a plan first.");
			return;
		}
		applyingPlan = true;
		try {
			await apiPost(`/api/ideas/${selectedIdeaId}/apply-plan`, { plan_markdown: planMarkdown });
			setFeedback("Plan applied. Initiative, goals, and tasks created.");
			planMarkdown = "";
		} catch (e) {
			setFeedback(e instanceof Error ? e.message : "Apply plan failed");
		} finally {
			applyingPlan = false;
		}
	}
</script>

<Breadcrumb items={[{ label: "Greenhouse", href: "/dashboard/overview" }, { label: "Create idea/seed" }]} />
<h2 class="page-title">Create idea/seed</h2>
<p class="nav-flow-hint">Create a new seed, generate a plan, and apply it to create initiatives, goals, and tasks.</p>

{#if feedback}
	<div class="inline-feedback show">{feedback}</div>
{/if}

<div class="create-layout">
	<Card>
		<div class="card-label">Create Idea</div>
		<label class="compact-label">
			Title
			<input type="text" bind:value={title} placeholder="New idea" />
		</label>
		<label class="compact-label">
			Description
			<input type="text" bind:value={description} placeholder="Context" />
		</label>
		<label class="compact-label">
			Tags (comma-separated)
			<input type="text" bind:value={tags} placeholder="growth,ops" />
		</label>
		<button type="button" class="btn" onclick={createIdea} disabled={loading}>Create Idea</button>
	</Card>

	<Card>
		<div class="card-label">Generate & Apply Plan</div>
		<p class="hint">Select an idea, generate a plan, then apply it to create initiatives, goals, and tasks.</p>
		<label class="compact-label">
			Select idea
			<select bind:value={selectedIdeaId}>
				<option value="">— Choose —</option>
				{#each ideas as idea}
					<option value={idea.id}>{idea.title}</option>
				{/each}
			</select>
		</label>
		<button type="button" class="btn" onclick={generatePlan} disabled={planGenerating || !selectedIdeaId}>
			{planGenerating ? "Generating..." : "Generate Plan"}
		</button>
		{#if planMarkdown}
			<details class="plan-details">
				<summary>View plan</summary>
				<pre class="plan-content">{planMarkdown}</pre>
			</details>
			<button type="button" class="btn btn-primary" onclick={applyPlan} disabled={applyingPlan}>
				{applyingPlan ? "Applying..." : "Apply Plan"}
			</button>
		{/if}
	</Card>
</div>

<style>
	.inline-feedback {
		padding: 8px 12px;
		border-radius: 8px;
		font-size: 0.9rem;
		margin-bottom: 12px;
		opacity: 0;
		transition: opacity 0.2s;
	}
	.inline-feedback.show {
		opacity: 1;
		background: var(--cultivar-accent-bg, rgba(86, 182, 255, 0.15));
		color: var(--cultivar-text);
	}
	.create-layout {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 20px;
		margin-top: 20px;
	}
	.compact-label {
		display: block;
		margin: 12px 0 4px 0;
		font-size: 0.875rem;
		color: var(--cultivar-muted);
	}
	.compact-label input,
	.compact-label select {
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
	.btn:hover:not(:disabled) {
		background: var(--cultivar-surface);
	}
	.btn-primary {
		background: var(--cultivar-accent);
		color: var(--cultivar-bg);
		border-color: var(--cultivar-accent);
	}
	.hint {
		font-size: 0.85rem;
		color: var(--cultivar-muted);
		margin: 0 0 12px 0;
	}
	.plan-details {
		margin-top: 12px;
		border: 1px solid var(--cultivar-border);
		border-radius: 8px;
		padding: 8px;
	}
	.plan-content {
		margin: 8px 0 0 0;
		padding: 12px;
		background: var(--cultivar-bg);
		border-radius: 6px;
		font-size: 0.8rem;
		overflow-x: auto;
		white-space: pre-wrap;
	}
</style>

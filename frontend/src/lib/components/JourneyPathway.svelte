<script lang="ts">
	interface Stage {
		id: string;
		label: string;
		subtitle: string;
		icon: string;
		countKey?: keyof { ideas: number; initiatives: number; goals: number; tasks: number };
		target?: string;
	}
	interface Props {
		counts: { ideas?: number; initiatives?: number; goals?: number; tasks?: number };
	}

	let { counts = {} }: Props = $props();

	const STAGES: Stage[] = [
		{ id: "ideas", label: "Idea", subtitle: "The Seed", icon: "🌱", countKey: "ideas", target: "initiatives-section" },
		{ id: "initiatives", label: "Initiative", subtitle: "The Sprout", icon: "🌿", countKey: "initiatives", target: "initiatives-section" },
		{ id: "goals", label: "Goal", subtitle: "Growth", icon: "🌳", countKey: "goals", target: "goals-section" },
		{ id: "tasks", label: "Task", subtitle: "In Bloom", icon: "🌸", countKey: "tasks", target: "tasks-section" },
		{ id: "market", label: "Market", subtitle: "The Harvest", icon: "🍎" },
	];

	const progress = $derived(
		Math.min(
			80,
			(counts.ideas ? 20 : 0) +
				(counts.initiatives ? 20 : 0) +
				(counts.goals ? 20 : 0) +
				(counts.tasks ? 20 : 0)
		)
	);

	function getState(index: number): "done" | "active" | "future" {
		const keys = ["ideas", "initiatives", "goals", "tasks"];
		for (let i = keys.length - 1; i >= 0; i--) {
			if ((counts[keys[i] as keyof typeof counts] || 0) > 0 && index <= i) {
				return index < i ? "done" : "active";
			}
		}
		return index === 0 ? "active" : "future";
	}

	function scrollToTarget(target: string | undefined) {
		if (!target || typeof document === "undefined") return;
		const el = document.getElementById(target);
		if (el) {
			el.scrollIntoView({ behavior: "smooth", block: "start" });
		}
	}
</script>

<div class="journey-pathway" role="navigation" aria-label="Journey progress">
	<div class="journey-progress-bar">
		<div class="journey-progress-fill" style="width: {progress}%"></div>
	</div>
	<div class="journey-nodes">
		{#each STAGES as stage, i}
			<button
				type="button"
				class="journey-node journey-{getState(i)}"
				onclick={() => scrollToTarget(stage.target)}
				aria-label="{stage.label}: {stage.subtitle}"
			>
				<span class="journey-icon" aria-hidden="true">{stage.icon}</span>
				<span class="journey-label">{stage.label}</span>
				<span class="journey-subtitle">{stage.subtitle}</span>
				{#if stage.countKey && counts[stage.countKey as keyof typeof counts] !== undefined}
					<span class="journey-count">{counts[stage.countKey as keyof typeof counts] ?? 0}</span>
				{/if}
			</button>
			{#if i < STAGES.length - 1}
				<span class="journey-connector" aria-hidden="true"></span>
			{/if}
		{/each}
	</div>
</div>

<style>
	.journey-pathway {
		margin: 16px 0;
		padding: 12px;
		border: 1px solid var(--cultivar-border);
		border-radius: 10px;
		background: var(--cultivar-surface-alt);
	}
	.journey-progress-bar {
		height: 4px;
		background: var(--cultivar-border);
		border-radius: 2px;
		overflow: hidden;
		margin-bottom: 12px;
	}
	.journey-progress-fill {
		height: 100%;
		background: var(--cultivar-accent-green, #9cdb74);
		transition: width 0.3s ease;
	}
	.journey-nodes {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 4px;
	}
	.journey-node {
		display: inline-flex;
		flex-direction: column;
		align-items: center;
		padding: 8px 10px;
		border: none;
		border-radius: 8px;
		background: transparent;
		color: var(--cultivar-muted);
		font-size: 0.8rem;
		cursor: pointer;
	}
	.journey-node:hover {
		background: var(--cultivar-surface);
	}
	.journey-node.journey-active {
		color: var(--cultivar-text);
		background: var(--cultivar-surface);
	}
	.journey-node.journey-done {
		color: var(--cultivar-accent-green, #9cdb74);
	}
	.journey-icon {
		font-size: 1.2rem;
		margin-bottom: 2px;
	}
	.journey-subtitle {
		font-size: 0.7rem;
		opacity: 0.8;
	}
	.journey-count {
		margin-left: 4px;
		padding: 2px 6px;
		border-radius: 999px;
		background: var(--cultivar-accent-bg, rgba(86, 182, 255, 0.2));
		font-size: 0.7rem;
	}
	.journey-connector {
		width: 12px;
		height: 1px;
		background: var(--cultivar-border);
		opacity: 0.5;
	}
</style>

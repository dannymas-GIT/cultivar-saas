<script lang="ts">
	interface Props {
		status: string;
		variant?: "default" | "success" | "warn" | "muted";
	}

	let { status, variant = "default" }: Props = $props();
</script>

<span class="status-badge" data-variant={variant}>{status}</span>

<style>
	.status-badge {
		display: inline-block;
		padding: 2px 8px;
		border-radius: 999px;
		font-size: 0.75rem;
		font-weight: 500;
		text-transform: lowercase;
	}
	.status-badge[data-variant="default"] {
		background: var(--cultivar-accent-bg, rgba(86, 182, 255, 0.2));
		color: var(--cultivar-accent, #56b6ff);
	}
	.status-badge[data-variant="success"] {
		background: rgba(156, 219, 116, 0.2);
		color: #9cdb74;
	}
	.status-badge[data-variant="warn"] {
		background: rgba(255, 213, 127, 0.2);
		color: #ffd57f;
	}
	.status-badge[data-variant="muted"] {
		background: var(--cultivar-surface-alt);
		color: var(--cultivar-muted);
	}
</style>

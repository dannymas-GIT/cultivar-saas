<script lang="ts">
	import type { Snippet } from "svelte";

	interface Props {
		message?: string;
		children?: Snippet;
	}

	let { message = "No data yet.", children }: Props = $props();
</script>

<div class="empty-state">
	<p class="empty-state-message">{message}</p>
	{#if children}
		{@render children?.()}
	{/if}
</div>

<style>
	.empty-state {
		padding: 32px;
		text-align: center;
		color: var(--cultivar-muted);
		font-size: 0.95rem;
	}
	.empty-state-message {
		margin: 0 0 12px 0;
	}
</style>

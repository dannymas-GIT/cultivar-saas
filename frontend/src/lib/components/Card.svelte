<script lang="ts">
	import type { Snippet } from "svelte";

	interface Props {
		children?: Snippet;
		class?: string;
	}

	let { children, class: className = "" }: Props = $props();
</script>

<article class="card {className}">
	{@render children?.()}
</article>

<style>
	.card {
		padding: 16px;
		border: 1px solid var(--cultivar-card-border);
		border-radius: 10px;
		background: var(--cultivar-surface);
	}
</style>

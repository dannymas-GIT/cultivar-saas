<script lang="ts">
	interface BreadcrumbItem {
		label: string;
		href?: string;
	}

	interface Props {
		items: BreadcrumbItem[];
	}

	let { items = [] }: Props = $props();
</script>

<nav class="breadcrumb" aria-label="Breadcrumb">
	<ol class="breadcrumb-list">
		{#each items as item, i}
			<li class="breadcrumb-item">
				{#if i < items.length - 1 && item.href}
					<a href={item.href} class="breadcrumb-link">{item.label}</a>
				{:else}
					<span class="breadcrumb-current" aria-current="page">{item.label}</span>
				{/if}
				{#if i < items.length - 1}
					<span class="breadcrumb-sep" aria-hidden="true">/</span>
				{/if}
			</li>
		{/each}
	</ol>
</nav>

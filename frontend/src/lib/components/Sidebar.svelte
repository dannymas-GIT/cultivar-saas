<script lang="ts">
	import { page } from "$app/stores";

	interface NavItem {
		href: string;
		label: string;
		order: number;
	}
	interface NavGroup {
		label: string;
		items: NavItem[];
	}

	const groups: NavGroup[] = [
		{
			label: "Greenhouse",
			items: [
				{ href: "/dashboard/overview", label: "Overview", order: 0 },
				{ href: "/dashboard/create", label: "Create idea/seed", order: 1 },
				{ href: "/dashboard/ideas", label: "Idea Garden", order: 2 },
				{ href: "/dashboard/agents", label: "Gardeners", order: 3 },
				{ href: "/dashboard/org-chart", label: "Org Chart", order: 4 },
			],
		},
	];

	let openGroups = $state<Record<string, boolean>>({ Greenhouse: true });

	function toggleGroup(label: string) {
		openGroups = { ...openGroups, [label]: !openGroups[label] };
	}

	function isActive(href: string): boolean {
		const p = $page.url.pathname;
		if (href === "/dashboard/overview") return p === "/dashboard" || p === "/dashboard/overview";
		if (href.startsWith("/dashboard/ideas")) return p.startsWith("/dashboard/ideas");
		return p === href || p.startsWith(href + "/");
	}
</script>

<nav class="sidebar" aria-label="Application navigation">
	{#each groups as group}
		<div class="nav-group">
			<button
				type="button"
				class="nav-group-title"
				onclick={() => toggleGroup(group.label)}
				aria-expanded={openGroups[group.label] ?? true}
			>
				<span class="nav-group-chevron" class:open={openGroups[group.label] ?? true}>›</span>
				{group.label}
			</button>
			{#if openGroups[group.label] ?? true}
				<ul class="nav-list">
					{#each group.items.toSorted((a, b) => a.order - b.order) as item}
						<li>
							<a
								href={item.href}
								class="nav-link"
								class:active={isActive(item.href)}
							>
								{item.label}
							</a>
						</li>
					{/each}
				</ul>
			{/if}
		</div>
	{/each}
</nav>

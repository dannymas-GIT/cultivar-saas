<script lang="ts">
	interface Column {
		key: string;
		label: string;
	}
	interface Props {
		columns: Column[];
		rows: Record<string, unknown>[];
	}

	let { columns, rows }: Props = $props();
</script>

<div class="table-wrap">
	<table class="data-table">
		<thead>
			<tr>
				{#each columns as col}
					<th>{col.label}</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each rows as row}
				<tr>
					{#each columns as col}
						<td>{String(row[col.key] ?? "")}</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<style>
	.table-wrap {
		overflow-x: auto;
	}
	.data-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.875rem;
	}
	.data-table th,
	.data-table td {
		padding: 8px 12px;
		border-bottom: 1px solid var(--cultivar-border);
		text-align: left;
	}
	.data-table th {
		font-weight: 600;
		color: var(--cultivar-muted);
	}
</style>

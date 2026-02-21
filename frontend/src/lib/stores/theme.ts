/** Theme store: light | dark | system - uses writable for SSR compatibility */
import { writable } from "svelte/store";

const STORAGE_KEY = "cultivar_theme";

function getStoredTheme(): "light" | "dark" | "system" {
	if (typeof window === "undefined") return "system";
	const v = localStorage.getItem(STORAGE_KEY) as "light" | "dark" | "system" | null;
	return v === "light" || v === "dark" || v === "system" ? v : "system";
}

function applyTheme(v: "light" | "dark" | "system") {
	if (typeof document === "undefined") return;
	const root = document.documentElement;
	let resolved: "light" | "dark" = "dark";
	if (v === "system") {
		resolved = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
	} else {
		resolved = v;
	}
	root.setAttribute("data-theme", resolved);
}

export const themeStore = writable<"light" | "dark" | "system">(getStoredTheme());

if (typeof window !== "undefined") {
	themeStore.subscribe((v) => {
		localStorage.setItem(STORAGE_KEY, v);
		applyTheme(v);
	});
	applyTheme(getStoredTheme());
	window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
		themeStore.update((v) => {
			if (v === "system") applyTheme("system");
			return v;
		});
	});
}

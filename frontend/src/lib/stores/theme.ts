/** Theme store: light | dark | system */
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

export function createThemeStore() {
	let theme = $state<"light" | "dark" | "system">(getStoredTheme());

	return {
		get theme() {
			return theme;
		},
		set theme(v: "light" | "dark" | "system") {
			theme = v;
			if (typeof window !== "undefined") {
				localStorage.setItem(STORAGE_KEY, v);
				applyTheme(v);
			}
		},
		init() {
			if (typeof window !== "undefined") {
				applyTheme(theme);
				window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
					if (theme === "system") applyTheme("system");
				});
			}
		},
	};
}

export const themeStore = createThemeStore();

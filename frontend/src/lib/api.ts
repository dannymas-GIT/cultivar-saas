/** API client with auth */
import { getToken } from "$lib/auth";

const apiUrl = typeof import.meta !== "undefined" ? (import.meta.env?.PUBLIC_API_URL || "") : "";

export function apiFetch(path: string, init?: RequestInit): Promise<Response> {
	const token = getToken();
	const headers = new Headers(init?.headers);
	if (token) {
		headers.set("Authorization", `Bearer ${token}`);
	}
	return fetch(`${apiUrl}${path}`, { ...init, headers });
}

export async function apiGet<T = unknown>(path: string): Promise<T> {
	const res = await apiFetch(path);
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: res.statusText }));
		throw new Error(typeof err.detail === "string" ? err.detail : JSON.stringify(err.detail));
	}
	return res.json();
}

export async function apiPost<T = unknown>(path: string, body?: object): Promise<T> {
	const res = await apiFetch(path, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: body ? JSON.stringify(body) : undefined,
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: res.statusText }));
		throw new Error(typeof err.detail === "string" ? err.detail : JSON.stringify(err.detail));
	}
	return res.json();
}

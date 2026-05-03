import { dev } from '$app/environment';
import { goto } from '$app/navigation';
import { resolve } from '$app/paths';

export const customFetch = async <T>(url: string, options?: RequestInit): Promise<T> => {
	const targetUrl = dev ? `http://127.0.0.1:8000${url}` : url;

	const response = await fetch(targetUrl, {
		...options,
		credentials: 'include',
		headers: {
			...options?.headers
		}
	});

	if (response.status === 401) {
		await goto(resolve('/auth'));
		throw new Error('Unauthorized');
	}

	if (!response.ok) {
		let errorData;
		try {
			errorData = await response.json();
		} catch {
			errorData = { message: response.statusText };
		}
		throw errorData;
	}

	if (response.status === 204 || response.status === 205) {
		return {} as T;
	}

	const text = await response.text();
	if (!text) return {} as T;

	try {
		return JSON.parse(text);
	} catch {
		return text as unknown as T;
	}
};

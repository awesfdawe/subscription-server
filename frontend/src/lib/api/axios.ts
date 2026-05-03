import axios from 'axios';
import { dev } from '$app/environment';
import { goto } from '$app/navigation';
import { resolve } from '$app/paths';

const api = axios.create({
	baseURL: dev ? 'http://127.0.0.1:8000' : '/api',
	withCredentials: true
});

api.interceptors.response.use(
	(response) => response,
	async (error) => {
		if (error.response?.status === 401) {
			await goto(resolve('/auth'));
		}
		return Promise.reject(error);
	}
);

export default api;

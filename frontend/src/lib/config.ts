import { env } from '$env/dynamic/public';
import { z } from 'zod';

const configSchema = z.object({
	PUBLIC_API_URL: z.string().default('http://127.0.0.1:8000/api')
});

export const config = configSchema.parse(env);

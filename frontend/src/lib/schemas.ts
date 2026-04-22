import { z } from 'zod';

export const registerRequest = z.object({
	username: z.string().min(3).max(30),
	password: z.string().min(8).max(200)
});

export type RegisterRequest = z.infer<typeof registerRequest>;

export const initResponseSchema = z.object({
	ready: z.boolean()
});

export type InitResponse = z.infer<typeof initResponseSchema>;

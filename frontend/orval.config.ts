import { defineConfig } from 'orval';

export default defineConfig({
	api: {
		input: {
			target: '../backend/openapi.json'
		},
		output: {
			mode: 'tags-split',
			client: 'svelte-query',
			target: 'src/lib/api/endpoints',
			schemas: 'src/lib/api/models',
			override: {
				mutator: {
					path: 'src/lib/api/mutator.ts',
					name: 'customFetch'
				}
			},
			clean: true
		}
	},
	apiZod: {
		input: {
			target: '../backend/openapi.json'
		},
		output: {
			mode: 'tags-split',
			client: 'zod',
			target: 'src/lib/api/endpoints',
			fileExtension: '.zod.ts'
		}
	}
});

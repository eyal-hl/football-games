import { Filter } from './interfaces';

export const getRandomFilters = (filters: Filter[], count: number): Filter[] => {
	const randomFilters: Filter[] = [];
	for (let i = 0; i < count; i++) {
		const randomIndex = Math.floor(Math.random() * filters.length);
		randomFilters.push(filters[randomIndex]);
	}
	return randomFilters;
};

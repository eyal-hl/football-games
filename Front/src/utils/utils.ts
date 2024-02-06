import { Filter } from './interfaces';

interface gameFilters {
	topFilters: Filter[];
	sideFilters: Filter[];
}

export const getRandomFilters = (filters: Filter[], sideCount: number, topCount: number): gameFilters => {
    let newFilters = [...filters]
	const topFilters = [];
	const sideFilters = [];
	for (let i = 0; i < topCount; i++) {
		topFilters.push(newFilters.splice(Math.floor(Math.random() * newFilters.length), 1)[0]);
	}
    newFilters = newFilters.filter((filter) => filter.type !== 'nationality');
	for (let i = 0; i < sideCount; i++) {
		sideFilters.push(newFilters.splice(Math.floor(Math.random() * newFilters.length), 1)[0]);
	}
	return { topFilters, sideFilters };
};

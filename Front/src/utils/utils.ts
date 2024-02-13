import { filterSchema } from './api.interfaces.ts';
import { Filter } from './interfaces.ts';

interface gameFilters {
  topFilters: Filter[];
  sideFilters: Filter[];
}

export const getRandomFilters = (filters: Filter[], sideCount: number, topCount: number): gameFilters => {
  let newFilters = [...filters];
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

export const translateFilters = (filterShemas: filterSchema[] | undefined): Filter[] => {
  if (!filterShemas) return [];
  const specialType = { manager: 'manager', cup_winner: 'title', league_winner: 'title' };
  return filterShemas.map((filter) => {
    if ('team_id' in filter) {
      return { type: 'team', code: filter.team_id, name: filter.name, image: filter.img_ref.replace('tiny', 'big') };
    }
    if ('league_id' in filter) {
      return {
        type: 'league',
        code: filter.league_id,
        name: filter.name,
        image: filter.img_ref.replace('tiny', 'big'),
      };
    }
    if ('special_id' in filter) {
      return { type: specialType[filter.type], code: filter.special_id, name: filter.name, image: filter.img_ref };
    }
    if ('player_id' in filter) {
      return {
        type: 'player',
        code: String(filter.player_id),
        name: filter.name,
        image: filter.img_ref.replace('medium', 'big'),
      };
    }

    return { type: 'nationality', code: filter.name, name: filter.name, image: '' };
  });
};

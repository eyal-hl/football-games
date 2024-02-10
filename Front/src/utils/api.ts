import { teamSchema } from './api.interfaces';
import { API_BASE } from './consts';
import { Filter, Player } from './interfaces';

export const fetch_all_players = async (): Promise<Player[]> => {
	const response = await fetch(`${API_BASE}/players`);

	return response.json();
};

export const fetch_players_by_name = async (name: string, searchFromMiddle = true): Promise<Player[]> => {
	const response = await fetch(`${API_BASE}/players/search?name=${name}&search_from_middle=${searchFromMiddle}`);

	return response.json();
};

export const fetch_players_with_filters = async (filter1: Filter, filter2: Filter): Promise<Player[]> => {
	const response = await fetch(
		`${API_BASE}/games/grid/all_answers?type1=${filter1.type}&value1=${filter1.code}&type2=${filter2.type}&value2=${filter2.code}`,
	);

	return response.json();
};

export const fetch_teams = async (): Promise<Filter[]> => {
	const response = await fetch(`${API_BASE}/teams`);

	return (await response.json()).map((team: teamSchema) => {
		return { type: 'team', code: team.team_id, name: team.name, image: team.img_ref.replace('tiny', 'big') };
	});
};

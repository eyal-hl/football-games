import { API_BASE } from './consts';
import { Player } from './interfaces';

export const fetch_all_players = async (): Promise<Player[]> => {
	const response = await fetch(`${API_BASE}/players`);
	return response.json();
};

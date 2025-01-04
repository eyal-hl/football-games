import { connection_details, mass_connection_details, playerTeamHistory, teamSchema } from './api.interfaces';
import { API_BASE } from './consts';
import { playerSchema } from './api.interfaces';
import { Filter } from './interfaces';

export const fetch_all_players = async (): Promise<playerSchema[]> => {
  const response = await fetch(`${API_BASE}/players/`);

  return response.json();
};

export const fetch_players_by_name = async (name: string, searchFromMiddle = true): Promise<playerSchema[]> => {
  const response = await fetch(`${API_BASE}/players/search?name=${name}&search_from_middle=${searchFromMiddle}`);

  return response.json();
};

export const fetch_players_with_filters = async (filter1: Filter, filter2: Filter): Promise<playerSchema[]> => {
  const response = await fetch(
    `${API_BASE}/games/grid/all_answers?type1=${filter1.type}&value1=${filter1.code}&type2=${filter2.type}&value2=${filter2.code}`
  );

  return response.json();
};

export const fetch_teams = async (): Promise<Filter[]> => {
  const response = await fetch(`${API_BASE}/teams`);

  return (await response.json()).map((team: teamSchema) => {
    return { type: 'team', code: team.team_id, name: team.name, image: team.img_ref.replace('tiny', 'big') };
  });
};

export const fetch_connections = async (player_id1: string, player_id2: string): Promise<connection_details[]> => {
  const response = await fetch(
    `${API_BASE}/games/connect_players/connection_details?player1=${player_id1}&player2=${player_id2}`
  );

  return response.json();
};

export const mass_fetch_connections = async (
  player_id: string,
  players: string[]
): Promise<mass_connection_details[]> => {
  const response = await fetch(
    `${API_BASE}/games/connect_players/mass_connection_details?player_id=${player_id}&players=${players.join(',')}`
  );

  return response.json();
};

export const fetch_all_players_from_league_year = async (league_id: string, year: string): Promise<playerSchema[]> => {
  const response = await fetch(`${API_BASE}/players/league/${league_id}/${year}`);

  return response.json();
};

export const fetch_all_players_from_team = async (team_id: string, year: string): Promise<playerSchema[]> => {
  const response = await fetch(`${API_BASE}/players/team/${team_id}/${year}`);

  return response.json();
};

export const fetch_player_history = async (player_id: string): Promise<playerTeamHistory[]> => {
  const response = await fetch(`${API_BASE}/player_teams/team_history/${player_id}`);
  return response.json();
};

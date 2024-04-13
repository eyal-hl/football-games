export interface teamSchema {
  name: string;
  league_id: string;
  ref: string;
  team_id: string;
  img_ref: string;
}

export interface leagueSchema {
  league_id: string;
  name: string;
  img_ref: string;
}

export interface nationalitySchema {
  name: string;
}

export interface playerSchema {
  player_id: number;
  name: string;
  name_unaccented: string;
  birth_date: string;
  img_ref: string;
}

interface specialSchema {
  special_id: string;
  name: string;
  ref: string;
  img_ref: string;
  type: string;
}

export interface managerSchema extends specialSchema {
  type: 'manager';
}

export interface titleSchema extends specialSchema {
  type: 'cup_winner' | 'league_winner';
}

export type filterSchema = teamSchema | leagueSchema | nationalitySchema | playerSchema | managerSchema | titleSchema;

export interface connection_details {
  team_name: string;
  years: string;
}

export interface mass_connection_details {
  player_id: string;
  connections: connection_details[];
}

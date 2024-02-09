export interface Player {
	player_id: number;
	name: string;
	name_unaccented: string;
	birth_date: string;
	img_ref: string;
}

export interface Filter {
	code: string;
	type: string;
	image: string;
	name: string;
}

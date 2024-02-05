export interface Player {
	player_id: number;
	name: string;
	nationality: string;
	birth_date: string;
	img_ref: string;
}

export interface Filter {
	code: string;
	type: string;
	image: string;
	name: string;
}

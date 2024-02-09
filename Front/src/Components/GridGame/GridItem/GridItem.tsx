import { useEffect, useState } from 'react';
import { fetch_players_with_filters } from '../../../utils/api';
import { Filter, Player } from '../../../utils/interfaces';
import css from './GridItem.module.css';
import { Tooltip } from '@mui/material';
import classNames from 'classnames';

interface GridItemProps {
	filter1: Filter;
	filter2: Filter;
	id: string;
	currentFocused: string;
	searchedPlayer: number;
	onClick?: () => void;
}
const GridItem = ({ filter1, filter2, id, currentFocused, searchedPlayer, onClick }: GridItemProps) => {
	const [resultsState, setResultsState] = useState<Player[]>([]);
	const [confirmedPlayers, setConfirmedPlayers] = useState<Player[]>([]);

	useEffect(() => {
		(async () => {
			if (!filter1 || !filter2) return;
			const players = await fetch_players_with_filters(filter1, filter2);

			setResultsState(players);
		})();
	}, [filter1, filter2]);

	useEffect(() => {
		if (currentFocused === id || currentFocused === 'all') {
			const player = resultsState.find(player => player.player_id === searchedPlayer);
			if (player) {
				setConfirmedPlayers(a => [...a, player]);
			}
		}
	}, [searchedPlayer]);
	return (
		<div className={classNames(css.gridItem, { [css.selected]: currentFocused === id })} onClick={onClick}>
			{confirmedPlayers.length === 0 ? null : (
				<Tooltip title={confirmedPlayers[-1].name}>
					<img src={confirmedPlayers[-1].img_ref} className={css.image} />
				</Tooltip>
			)}
		</div>
	);
};

export default GridItem;

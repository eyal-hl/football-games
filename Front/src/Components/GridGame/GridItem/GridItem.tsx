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
	searchedPlayer: { player_id: number };
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
			const player = resultsState.find(player => player.player_id === searchedPlayer.player_id);
			if (player) {
				setConfirmedPlayers(a => [...a, player]);
			}
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [searchedPlayer]);
	return (
		<div className={classNames(css.gridItem, { [css.selected]: currentFocused === id })} onClick={onClick}>
			{confirmedPlayers.length === 0 ? null : (
				<Tooltip title={confirmedPlayers[confirmedPlayers.length - 1].name}>
					<img src={confirmedPlayers[confirmedPlayers.length - 1].img_ref} className={css.image} />
				</Tooltip>
			)}
			{confirmedPlayers.length !== 0 && <div className={css.confirmedAmount}>{confirmedPlayers.length}</div>}
		</div>
	);
};

export default GridItem;

import { useEffect, useState } from 'react';
import { fetch_players_with_filters } from '../../../utils/api';
import { playerSchema } from '../../../utils/api.interfaces';
import { Filter } from '../../../utils/interfaces';
import css from './GridItem.module.css';
import { Tooltip } from '@mui/material';
import classNames from 'classnames';
import CloseIcon from '@mui/icons-material/Close';

interface GridItemProps {
	filter1: Filter;
	filter2: Filter;
	id: string;
	currentFocused: string;
	searchedPlayer: { player_id: number };
	onClick?: () => void;
}
const GridItem = ({ filter1, filter2, id, currentFocused, searchedPlayer, onClick }: GridItemProps) => {
	const [resultsState, setResultsState] = useState<playerSchema[]>([]);
	const [confirmedPlayers, setConfirmedPlayers] = useState<playerSchema[]>([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		(async () => {
			if (!filter1 || !filter2) return;
			setLoading(true);
			setConfirmedPlayers([]);
			const players = await fetch_players_with_filters(filter1, filter2);

			await setResultsState(players);
			setLoading(false);
		})();
	}, [filter1, filter2]);

	useEffect(() => {
		if (
			(currentFocused === id || currentFocused === 'all') &&
			confirmedPlayers.find(player => player.player_id === searchedPlayer.player_id) === undefined
		) {
			const player = resultsState.find(player => player.player_id === searchedPlayer.player_id);
			if (player) {
				setConfirmedPlayers(a => [...a, player]);
			}
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [searchedPlayer]);
	if (loading) return <div className={css.gridItem}>Loading...</div>;
	return (
		<div
			className={classNames(
				css.gridItem,
				{ [css.selected]: currentFocused === id },
				{ [css.complete]: resultsState.length === confirmedPlayers.length && resultsState.length !== 0 },
			)}
			onClick={onClick}
		>
			{resultsState.length === 0 ? (
				<Tooltip title='No players exist'>
					<CloseIcon className={css.noPlayers} />
				</Tooltip>
			) : confirmedPlayers.length === 0 ? null : (
				<Tooltip title={confirmedPlayers[confirmedPlayers.length - 1].name}>
					<img src={confirmedPlayers[confirmedPlayers.length - 1].img_ref} className={css.image} />
				</Tooltip>
			)}
			{confirmedPlayers.length !== 0 && <div className={css.confirmedAmount}>{confirmedPlayers.length}</div>}
		</div>
	);
};

export default GridItem;

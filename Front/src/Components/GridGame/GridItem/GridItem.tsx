import { useEffect, useState } from 'react';
import { fetch_players_with_filters } from '../../../utils/api';
import { Filter, Player } from '../../../utils/interfaces';
import css from './GridItem.module.css';
import { Tooltip } from '@mui/material';

interface GridItemProps {
	filter1: Filter;
	filter2: Filter;
}
const GridItem = ({ filter1, filter2 }: GridItemProps) => {
	const [resultsState, setResultsState] = useState<Player[]>([]);

	useEffect(() => {
		(async () => {
			const players = await fetch_players_with_filters(filter1, filter2);
			console.log(players.length);
			
			setResultsState(players);
		})();
	}, [filter1, filter2]);
	return (
		<div className={css.gridItem}>
			{resultsState.length === 0 ? null : (
				<Tooltip title={`${resultsState[0].name} ${filter1.name} ${filter2.name}`}>
					<img src={resultsState[0].img_ref} className={css.image} />
				</Tooltip>
			)}
		</div>
	);
};

export default GridItem;

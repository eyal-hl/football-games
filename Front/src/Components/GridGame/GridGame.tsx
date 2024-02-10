import GridFilter from './GridFilter/GridFilter';
import css from './GridGame.module.css';
import { useEffect, useState } from 'react';
import { Filter } from '../../utils/interfaces';
import { fetch_teams } from '../../utils/api';
import { top_left_image } from '../../utils/consts';
import { getRandomFilters } from '../../utils/utils';
import GridItem from './GridItem/GridItem';
import SearchBox from '../SearchBox/SearchBox';
import { FormControl, InputLabel, MenuItem, Select } from '@mui/material';

const GridGame = () => {
	const [gridSizeState, setGridSizeState] = useState<[number, number]>([5, 5]);
	const [filterState, setFilterState] = useState<Filter[]>([]);
	const [currentFocused, setCurrentFocused] = useState<string>('all');
	const [searchedPlayer, setSearchedPlayer] = useState<{ player_id: number }>({ player_id: 0 });
	const [choseFilters, setChoseFilters] = useState<{ sideFilters: Filter[]; topFilters: Filter[] }>({ sideFilters: [], topFilters: [] });

	useEffect(() => {
		(async () => {
			setFilterState(await fetch_teams());
		})();
	}, []);

	useEffect(() => {
		setChoseFilters(getRandomFilters(filterState, gridSizeState[0], gridSizeState[1]));
	}, [gridSizeState, filterState]);

	const getGrid = () => {
		const rows = [];
		const { sideFilters, topFilters } = choseFilters;
		for (let i = 0; i < gridSizeState[0] + 1; i++) {
			const row = [];

			for (let j = 0; j < gridSizeState[1] + 1; j++) {
				if (i === 0 && j === 0) {
					row.push(
						<div className={css.topLeft} key={`${i}-${j}`} onClick={() => setCurrentFocused('all')}>
							<img src={top_left_image} />
						</div>,
					);
					continue;
				}
				if (i === 0) {
					row.push(<GridFilter {...topFilters[j - 1]} key={`${i}-${j}`} />);
					continue;
				}
				if (j === 0) {
					row.push(<GridFilter {...sideFilters[i - 1]} key={`${i}-${j}`} />);
					continue;
				}

				row.push(
					<GridItem
						filter1={topFilters[j - 1]}
						filter2={sideFilters[i - 1]}
						key={`${i}-${j}`}
						id={`${i}-${j}`}
						currentFocused={currentFocused}
						searchedPlayer={searchedPlayer}
						onClick={() => setCurrentFocused(`${i}-${j}`)}
					/>,
				);
			}
			rows.push(
				<div className={css.row} key={i}>
					{row}
				</div>,
			);
		}

		return <div>{rows}</div>;
	};

	return (
		<div className={css.page} style={{ '--grid-item-size': '10rem' } as React.CSSProperties}>
			<div className={css.gridGame}>
				<div className={css.topBar}>
					<SearchBox onSelect={playerid => setSearchedPlayer({ player_id: playerid })} />

					<FormControl className={css.gridSizeSelector}>
						<InputLabel id='demo-simple-select-label'>Grid size</InputLabel>
						<Select
							className={css.select}
							labelId='demo-simple-select-label'
							id='demo-simple-select'
							value={`${gridSizeState[0]}x${gridSizeState[1]}` as string}
							label='Grid size'
							renderValue={() => `${gridSizeState[0]}x${gridSizeState[1]}`}
							defaultValue={'[5, 5]'}
							onChange={e => setGridSizeState(JSON.parse(e.target.value))}
						>
							<MenuItem value={'[3, 3]'}>3x3</MenuItem>
							<MenuItem value={'[4, 4]'}>4x4</MenuItem>
							<MenuItem value={'[5, 5]'}>5x5</MenuItem>
							<MenuItem value={'[5, 6]'}>5x6</MenuItem>
							<MenuItem value={'[5, 7]'}>5x7</MenuItem>
						</Select>
					</FormControl>
				</div>
				{filterState.length === 0 ? null : getGrid()}
			</div>
		</div>
	);
};

export default GridGame;

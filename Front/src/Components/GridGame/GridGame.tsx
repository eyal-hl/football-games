import GridFilter from './GridFilter/GridFilter';
import css from './GridGame.module.css';
import GridItem from './GridItem/GridItem';
import { temp_filters } from '../../utils/consts';

const GridGame = () => {
	return (
		<div className={css.gridGame}>
			<GridFilter {...temp_filters[0]} />
			<GridItem filter1={temp_filters[0]} filter2={temp_filters[1]} />
		</div>
	);
};

export default GridGame;

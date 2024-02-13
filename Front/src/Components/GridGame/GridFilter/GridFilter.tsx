import { Tooltip } from '@mui/material';
import css from './GridFilter.module.css';
import { Filter } from '../../../utils/interfaces';

interface GridFilterProps extends Filter {}
const GridFilter = ({ image, name }: GridFilterProps) => {
  return (
    <div className={css.gridFilter}>
      {/* increase font size in tooltip */}
      <Tooltip title={name}>
        <img className={css.image} src={image} />
      </Tooltip>
    </div>
  );
};

export default GridFilter;

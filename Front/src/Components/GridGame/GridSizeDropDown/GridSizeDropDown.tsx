import css from './GridSizeDropDown.module.css';
import { FormControl, InputLabel, MenuItem, Select } from '@mui/material';

const GridSizeDropDown = ({
  gridSizeState,
  setGridSizeState,
}: {
  gridSizeState: [number, number];
  setGridSizeState: React.Dispatch<React.SetStateAction<[number, number]>>;
}) => {
  return (
    <FormControl className={css.gridSizeSelector}>
      <InputLabel id="demo-simple-select-label">Grid size</InputLabel>
      <Select
        className={css.select}
        labelId="demo-simple-select-label"
        id="demo-simple-select"
        value={`${gridSizeState[0]}x${gridSizeState[1]}` as string}
        label="Grid size"
        renderValue={() => `${gridSizeState[0]}x${gridSizeState[1]}`}
        defaultValue={'[5, 5]'}
        onChange={(e) => setGridSizeState(JSON.parse(e.target.value))}
      >
        <MenuItem value={'[3, 3]'}>3x3</MenuItem>
        <MenuItem value={'[4, 4]'}>4x4</MenuItem>
        <MenuItem value={'[5, 5]'}>5x5</MenuItem>
        <MenuItem value={'[5, 6]'}>5x6</MenuItem>
        <MenuItem value={'[5, 7]'}>5x7</MenuItem>
      </Select>
    </FormControl>
  );
};

export default GridSizeDropDown;

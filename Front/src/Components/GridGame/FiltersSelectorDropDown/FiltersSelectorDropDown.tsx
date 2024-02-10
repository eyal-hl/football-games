import css from './FilterSelectorDropDown.module.css';
import { Filter } from '../../../utils/interfaces';
import { filterSchema } from '../../../utils/api.interfaces';
import { FormControl, InputLabel, MenuItem, Select } from '@mui/material';
import { useState } from 'react';
import { translateFilters } from '../../../utils/utils';
import { defaultPresets } from '../../../utils/consts';

interface FiltersSelectorDropDownProps {
	onChange: (filters: Filter[]) => void;
}

const FiltersSelectorDropDown = ({ onChange }: FiltersSelectorDropDownProps) => {
	const [selectedFilters, setSelectedFilters] = useState<string>('default');
	const localStoragePresets = localStorage.getItem('presets');
	const presets: { [key: string]: filterSchema[] } = localStoragePresets ? JSON.parse(localStoragePresets) : defaultPresets;
	const handlePresetChange = (preset: string) => {
		setSelectedFilters(preset);
		onChange(translateFilters(presets[preset]));
	};

	return (
		<FormControl className={css.filterSelectorDropDown}>
			<InputLabel id='demo-simple-select-label'>Filters</InputLabel>
			<Select
				className={css.select}
				labelId='demo-simple-select-label'
				id='demo-simple-select'
				value={selectedFilters}
				label='Filters'
				defaultValue={'default'}
				onChange={e => handlePresetChange(e.target.value as string)}
			>
				{Object.keys(presets).map(preset => (
					<MenuItem key={preset} value={preset}>
						{preset}
					</MenuItem>
				))}
			</Select>
		</FormControl>
	);
};

export default FiltersSelectorDropDown;

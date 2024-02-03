import React, { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';
import TextField from '@mui/material/TextField';
import Autocomplete, { autocompleteClasses } from '@mui/material/Autocomplete';
import useMediaQuery from '@mui/material/useMediaQuery';
import Popper from '@mui/material/Popper';
import { useTheme, styled } from '@mui/material/styles';
import { VariableSizeList } from 'react-window';
// import { fetchAllPlayers } from '../api';
import { MenuItem } from '@mui/material';
import { fetch_all_players } from '../../utils/api';
import { Player } from '../../utils/interfaces';

const LISTBOX_PADDING = 8; // px

/*
 played_id: number,
 name: string,
 nationality: string,
 birth_date: string,
 image_ref: string
*/

function renderRow(props) {
	const { data, index, style } = props;
	// console.log(data)
	const dataSet = data[index];
	const inlineStyle = {
		...style,
		top: style.top + LISTBOX_PADDING,
	};

	return (
		<MenuItem style={inlineStyle} onClick={() => console.log(dataSet)}>
			{dataSet.name}
		</MenuItem>
	);
}

const OuterElementContext = React.createContext({});

const OuterElementType = React.forwardRef((props, ref) => {
	const outerProps = React.useContext(OuterElementContext);
	return <div ref={ref} {...props} {...outerProps} />;
});

function useResetCache(data) {
	const ref = React.useRef(null);
	React.useEffect(() => {
		if (ref.current != null) {
			ref.current.resetAfterIndex(0, true);
		}
	}, [data]);
	return ref;
}

const ListboxComponent = React.forwardRef(function ListboxComponent(props, ref) {
	const { children, ...other } = props;
	const itemData: any[] = [];
	children.forEach(item => {
		itemData.push(item);
	});

	const theme = useTheme();
	const smUp = useMediaQuery(theme.breakpoints.up('sm'), {
		noSsr: true,
	});
	const itemCount = itemData.length;
	const itemSize = smUp ? 36 : 48;

	const getChildSize = child => {
		if (child.hasOwnProperty('group')) {
			return 48;
		}

		return itemSize;
	};

	const getHeight = () => {
		if (itemCount > 8) {
			return 8 * itemSize;
		}
		return itemData.map(getChildSize).reduce((a, b) => a + b, 0);
	};

	const gridRef = useResetCache(itemCount);

	return (
		<div ref={ref}>
			<OuterElementContext.Provider value={other}>
				<VariableSizeList
					itemData={itemData}
					height={getHeight() + 2 * LISTBOX_PADDING}
					width='100%'
					ref={gridRef}
					outerElementType={OuterElementType}
					innerElementType='ul'
					itemSize={index => getChildSize(itemData[index])}
					overscanCount={5}
					itemCount={itemCount}
				>
					{renderRow}
				</VariableSizeList>
			</OuterElementContext.Provider>
		</div>
	);
});

ListboxComponent.propTypes = {
	children: PropTypes.node,
};

const StyledPopper = styled(Popper)({
	[`& .${autocompleteClasses.listbox}`]: {
		boxSizing: 'border-box',
		'& ul': {
			padding: 0,
			margin: 0,
		},
	},
});

export default function SearchBox() {
	const searchRef = useRef();
	const [players, setPlayers] = useState<Player[]>([]);
	useEffect(() => {
		fetch_players();
	}, []);
	const fetch_players = async () => {
		setPlayers(await fetch_all_players());
	};

	// const [options, setOptions] = useState([]);

	// useEffect(() => {
	// 	const loadOptions = async () => {
	// 		const playerOptions = await fetchAllPlayers();
	// 		console.log(playerOptions);
	// 		setOptions(playerOptions);
	// 		console.log(playerOptions.map(value => value.long_name));
	// 	};
	// 	loadOptions();
	// }, []);

	return (
		<div style={{ width: '20vw' }}>
			<Autocomplete
				id='virtualize-demo'
				sx={{ margin: '1vh auto' }}
				disableListWrap
				PopperComponent={StyledPopper}
				ListboxComponent={ListboxComponent}
				options={players}
				onSelect={value => console.log(value)}
				renderInput={params => <TextField inputRef={searchRef} {...params} label='Player search' />}
				renderOption={(props, option, state) => option}
				getOptionLabel={option => option.name}
			/>
		</div>
	);
}

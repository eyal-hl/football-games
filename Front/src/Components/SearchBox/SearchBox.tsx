import React, { useEffect, useRef, useState } from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete, { autocompleteClasses } from '@mui/material/Autocomplete';
import useMediaQuery from '@mui/material/useMediaQuery';
import Popper from '@mui/material/Popper';
import { useTheme, styled } from '@mui/material/styles';
import { VariableSizeList, ListChildComponentProps } from 'react-window';
// import { fetchAllPlayers } from '../api';
import { MenuItem } from '@mui/material';
import { fetch_all_players, fetch_players_by_name } from '../../utils/api';
import { playerSchema } from '../../utils/api.interfaces';

const LISTBOX_PADDING = 2; // px

/*
 played_id: number,
 name: string,
 nationality: string,
 birth_date: string,
 image_ref: string
*/

type SearchBoxProps = {
	onSelect: (player_id: number) => void;
};

export default function SearchBox({ onSelect }: SearchBoxProps) {
	function renderRow(props: ListChildComponentProps) {
		const { data, index, style } = props;
		// console.log(data)
		const dataSet = data[index];
		// const inlineStyle = {
		// 	...style,
		// 	top: style.top + LISTBOX_PADDING,
		// };

			// 
		return (
			// <ListSubheader key={dataSet.player_id} onClick={() => onSelect(dataSet.player_id)} style={style} component='div'>
			<MenuItem key={dataSet.player_id} onClick={() => onSelect(dataSet.player_id)} sx={{ ...style, top: style.top as number + LISTBOX_PADDING}} >
				{dataSet.name} &nbsp; &nbsp; &nbsp; <span style={{position: 'absolute', right: '50%'}}><img src={dataSet.img_ref} style={{width: '1.5vw'}}/></span>  <span style={{position: 'absolute', right: '1vw'}}>{dataSet.birth_date}</span>
			</MenuItem>
		);
		
	}

	const OuterElementContext = React.createContext({});

	const OuterElementType = React.forwardRef<HTMLDivElement>((props, ref) => {
		const outerProps = React.useContext(OuterElementContext);
		return <div ref={ref} {...props} {...outerProps} />;
	});

	function useResetCache(data: any) {
		const ref = React.useRef<VariableSizeList>(null);
		React.useEffect(() => {
			if (ref.current != null) {
				ref.current.resetAfterIndex(0, true);
			}
		}, [data]);
		return ref;
	}

	const ListboxComponent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLElement>>(function ListboxComponent(props, ref) {
		const { children, ...other } = props;
		const itemData: React.ReactElement[] = [];
		(children as React.ReactElement[]).forEach(item => {
			itemData.push(item);
		});

		const theme = useTheme();
		const smUp = useMediaQuery(theme.breakpoints.up('sm'), {
			noSsr: true,
		});
		const itemCount = itemData.length;
		const itemSize = smUp ? 36 : 48;

		const getChildSize = (child: React.ReactElement) => {
			if (Object.prototype.hasOwnProperty.call(child, 'group')) {
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
						height={getHeight() + 10 * LISTBOX_PADDING}
						width='100%'
						ref={gridRef}
						outerElementType={OuterElementType}
						innerElementType='ul'
						itemSize={(index) => getChildSize(itemData[index])}
						overscanCount={5}
						itemCount={itemCount}
					>
						{renderRow}
					</VariableSizeList>
				</OuterElementContext.Provider>
			</div>
		);
	});

	const StyledPopper = styled(Popper)({
		[`& .${autocompleteClasses.listbox}`]: {
			boxSizing: 'border-box',
			'& ul': {
				padding: 0,
				margin: 0,
			},
		},
	});
	const searchRef = useRef<HTMLInputElement>();
	const [isLoading, setIsLoading] = useState(false);
	const [players, setPlayers] = useState<playerSchema[]>([]);
	// A state that will hold the seach value



	const fetch_options_by_search = async (value: string) => {
		const options = await fetch_players_by_name(value);
		setPlayers(options)
		
		setIsLoading(() => false)
	}

	const updateSearch = async () => {
		if (searchRef.current == undefined) return;
		setIsLoading(() => true)
		await fetch_options_by_search(searchRef.current.value);
	}

	return (
		<div style={{ width: '20vw' }}>
			<Autocomplete
				id='virtualize-demo'
				sx={{ margin: '1vh auto' }}
				disableListWrap
				PopperComponent={StyledPopper}
				ListboxComponent={ListboxComponent}
				// options={players.filter((player) => player.player_id < 10000)}
				loading={isLoading}
				noOptionsText={"Learn how to fucking spell ronaldo"}
				options={players}
				// renderInput={params => <TextField inputRef={searchRef} {...params} label='Player search' />}
				renderInput={params => <TextField inputRef={searchRef} onChange={() => updateSearch()} {...params} label='Player search' />}
				renderOption={(props, option, state) => option as React.ReactNode}
				getOptionLabel={option => option.name_unaccented}
			/>
		</div>
	);
}

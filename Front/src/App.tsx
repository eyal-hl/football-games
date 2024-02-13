import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './Components/Home/Home';
import About from './Components/About/About';
import GridGame from './Components/GridGame/GridGame';
import { ThemeProvider, createTheme } from '@mui/material';

function App() {
	const theme = createTheme({
		components: {
			MuiTooltip: {
				styleOverrides: {
					tooltip: {
						fontSize: '1.2rem'
					}
				}
			}
		},
		typography: {
			fontFamily: 'Suii'
		}
	})

	return (
		<div className='App'>
			<ThemeProvider theme={theme}>
				<BrowserRouter>
					<Routes>
						<Route path='/' element={<Home />} />
						<Route path='/about' element={<About />} />
						<Route path='/grid' element={<GridGame />} />
					</Routes>
				</BrowserRouter>
			</ThemeProvider>
		</div>
	);
}

export default App;

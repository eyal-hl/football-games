import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './Components/Home/Home';
import About from './Components/About/About';
import GridGame from './Components/GridGame/GridGame';

function App() {
	return (
		<div className='App'>
			<BrowserRouter>
				<Routes>
					<Route path='/' element={<Home />} />
					<Route path='/about' element={<About />} />
					<Route path='/grid' element={<GridGame />} />
				</Routes>
			</BrowserRouter>
		</div>
	);
}

export default App;

import SearchBox from '../SearchBox/SearchBox';
import css from './Home.module.css';

const Home = () => {
  return (
    <div className={css.home}>
      <h1>Home</h1>
      <p>This is the home page.</p>
      <SearchBox onSelect={(player) => console.log(player)} />
    </div>
  );
};

export default Home;

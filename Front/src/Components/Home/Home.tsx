import { useNavigate } from 'react-router-dom';
import css from './Home.module.css';
import GridViewIcon from '@mui/icons-material/GridView';
import AccountTreeIcon from '@mui/icons-material/AccountTree';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className={css.home}>
      <div className={css.hero}>
        <div className={css.heroTitle}>Football Explorer</div>
        <div className={css.heroSubtitle}>Discover football in different ways</div>
      </div>

      <div className={css.games}>
        <div className={css.gameCard} onClick={() => navigate('/grid')}>
          <div className={css.iconWrapper}>
            <GridViewIcon className={css.icon} />
          </div>
          <div className={css.gameTitle}>Grid Game</div>
          <div className={css.gameDescription}>Find players matching multiple criteria in a grid-based challenge</div>
        </div>

        <div className={css.gameCard} onClick={() => navigate('/connections')}>
          <div className={css.iconWrapper}>
            <AccountTreeIcon className={css.icon} />
          </div>
          <div className={css.gameTitle}>Connections</div>
          <div className={css.gameDescription}>Explore how players are connected through shared team history</div>
        </div>
      </div>
    </div>
  );
};

export default Home;

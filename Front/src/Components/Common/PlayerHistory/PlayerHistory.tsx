import { Modal, Tooltip } from '@mui/material';
import style from './PlayerHistory.module.css';
import classNames from 'classnames';
import { useEffect, useState } from 'react';
import { fetch_player_history } from '../../../utils/api';
import { playerTeamHistory } from '../../../utils/api.interfaces';

interface PlayerHistoryProps {
  player_id: string;
  open: boolean;
  onClose: () => void;
}

const PlayerHistory = ({ player_id, open, onClose }: PlayerHistoryProps) => {
  const [loading, setLoading] = useState(true);
  const [playerHistory, setPlayerHistory] = useState<playerTeamHistory[]>([]);

  useEffect(() => {
    (async () => {
      const history = await fetch_player_history(player_id);
      setPlayerHistory(history);
      setLoading(false);
    })();
  }, [player_id]);

  return (
    <Modal open={open} onClose={onClose}>
      <div className={classNames(style.Modal)}>
        <div className={style.Header}>Player History</div>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>League</th>
                <th>Team</th>
                <th>Years</th>
              </tr>
            </thead>
            <tbody>
              {playerHistory.map((history) => (
                <tr key={history.team_id} className={style.TeamRow}>
                  <td>
                    <Tooltip title={history.league}>
                      <img src={history.league_img} />
                    </Tooltip>
                  </td>
                  <td>
                    <Tooltip title={history.team}>
                      <img src={history.team_img.replace('tiny', 'big')} />
                    </Tooltip>
                  </td>
                  <td>{history.years}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </Modal>
  );
};

export default PlayerHistory;

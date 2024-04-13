import { useEffect, useState } from 'react';
import SearchBox from '../SearchBox/SearchBox';
import css from './ConnectionsGame.module.css';
import ConnectionsGraph, { graphData } from './ConnectionsGraph/ConnectionsGraph';
import { playerSchema } from '../../utils/api.interfaces';
import {
  fetch_all_players,
  fetch_all_players_from_league_year,
  fetch_all_players_from_team,
  fetch_connections,
  mass_fetch_connections,
} from '../../utils/api';
import { TEMP_DATA } from '../../utils/consts';

const ConnectionsGame = () => {
  const [nodes, setNodes] = useState<graphData['nodes']>([]);
  const [links, setLinks] = useState<graphData['links']>([]);
  const [nodesSize, setNodesSize] = useState<Map<string, number>>(new Map());
  const [isGraphDataUpdated, setIsGraphDataUpdated] = useState(true);
  const [render, setRender] = useState(false);

  useEffect(() => {
    setIsGraphDataUpdated(true);
  }, [links]);

  useEffect(() => {
    if (nodes.length < 2) return;
    const a = async () => {
      const player = nodes[nodes.length - 1];

      const newLinks: graphData['links'] = [];
      const connections = await mass_fetch_connections(
        player.id,
        nodes.map((node) => node.id).slice(0, nodes.length - 1)
      );
      connections.forEach((connection) => {
        if (connection.connections.length > 0) {
          setNodesSize((prev) => {
            const newMap = new Map(prev);
            newMap.set(player.id.toString(), (prev.get(player.id.toString()) || 5) + 1);
            newMap.set(connection.player_id.toString(), (prev.get(connection.player_id.toString()) || 5) + 1);
            return newMap;
          });

          connection.connections.forEach((connection_detail, index) => {
            newLinks.push({
              source: player.id,
              target: connection.player_id.toString(),
              label: connection_detail.team_name,
              years: connection_detail.years,
              timesMet: index,
            });
          });
        }
      });

      setLinks((prev) => [...prev, ...newLinks]);
      await new Promise((resolve) => {
        const intervalId = setInterval(() => {
          if (isGraphDataUpdated) {
            setIsGraphDataUpdated(false);
            clearInterval(intervalId);
            resolve();
          }
        }, 10); // Check every 10 milliseconds
      });
    };
    a();
  }, [nodes]);

  const addPlayer = async (player: playerSchema) => {
    setIsGraphDataUpdated(false);
    setNodes((prev) => [...prev, { id: player.player_id.toString(), img_ref: player.img_ref, name: player.name }]);

    await new Promise((resolve) => {
      const intervalId = setInterval(() => {
        if (isGraphDataUpdated) {
          clearInterval(intervalId);
          resolve();
        }
      }, 10); // Check every 10 milliseconds
    });
  };

  const addPlayers = async () => {
    // const a = await fetch_all_players_from_team('manchester_united', '2023');
    const a = await fetch_all_players_from_league_year('ligat_haal_ISR1', '2023');
    const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
    for (let i = 0; i < a.length; i++) {
      if (nodes.find((node) => node.id === a[i].player_id.toString())) continue;
      await addPlayer(a[i]);
      await delay(100 + 10 * i); // Delay increases with each iteration
      console.log(i);
    }
  };
  const downloadTxtFile = (data: string, name: string) => {
    const element = document.createElement('a');
    const file = new Blob([data], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = name;
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
  };

  const exportData = () => {
    downloadTxtFile(JSON.stringify(links), 'links.json');
    downloadTxtFile(JSON.stringify(nodes), 'nodes.json');
    downloadTxtFile(
      JSON.stringify(nodesSize, (key, value) => {
        if (value instanceof Map) {
          return {
            dataType: 'Map',
            value: Array.from(value.entries()), // or with spread: value: [...value]
          };
        } else {
          return value;
        }
      }),
      'nodesSize.json'
    );
  };
  return (
    <div className={css.connectionsGame}>
      <div className={css.connectionsGameHeader}>
        <h1>Connections Game</h1>
        <div className={css.top}>
          <SearchBox
            onSelectFullPlayer={(player) => {
              if (!nodes.find((node) => node.id === player.player_id.toString())) {
                addPlayer(player);
              }
            }}
          />
          <button onClick={addPlayers}>Add players</button>
          <button onClick={exportData}>Export data</button>
          <button onClick={() => setRender((prev) => !prev)}>Toggle render</button>
        </div>
      </div>
      <div className={css.connectionsGameBoard}>
        <ConnectionsGraph graphData={{ nodes, links }} nodesSize={nodesSize} render={render} />
      </div>
    </div>
  );
};

export default ConnectionsGame;

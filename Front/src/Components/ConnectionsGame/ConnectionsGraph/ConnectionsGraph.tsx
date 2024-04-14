import { useState } from 'react';
import { ForceGraph2D } from 'react-force-graph';
import data from '../../../utils/teamsColors.json';
const teamColors = JSON.parse(JSON.stringify(data));

export interface graphData {
  nodes: { id: string; img_ref: string; name: string }[];
  links: { source: string; target: string; label: string; years: string; timesMet: number }[];
}
interface ConnectionsGraphProps {
  graphData: graphData;
  nodesSize: Map<string, number>;
  render: boolean;
  freezeLayout: boolean;
}

const ConnectionsGraph = ({ graphData, nodesSize, render, freezeLayout }: ConnectionsGraphProps) => {
  const drawLineWithColors = (canvas, startPoint, endPoint, colors) => {
    const ctx = canvas.getContext('2d');
    const deltaX = endPoint.x - startPoint.x;
    const deltaY = endPoint.y - startPoint.y;
    const numSegments = 100; // You can adjust this for smoother or more detailed lines

    const segmentDeltaX = deltaX / numSegments;
    const segmentDeltaY = deltaY / numSegments;

    let currentX = startPoint.x;
    let currentY = startPoint.y;

    for (let i = 0; i < numSegments; i++) {
      const color = colors[i % colors.length]; // Cycle through colors
      ctx.beginPath();
      ctx.moveTo(currentX, currentY);
      ctx.lineTo(currentX + segmentDeltaX, currentY + segmentDeltaY);
      ctx.strokeStyle = color;
      ctx.stroke();

      currentX += segmentDeltaX;
      currentY += segmentDeltaY;
    }
  };

  const [otherTeamsColors, setOtherTeamsColors] = useState<Map<string, string>>(new Map());

  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  const getOtherTeamsColor = (teamName: string) => {
    if (otherTeamsColors.has(teamName)) return otherTeamsColors.get(teamName);
    const color = ['#' + Math.floor(Math.random() * 16777215).toString(16)];
    setOtherTeamsColors((prev) => {
      const newMap = new Map(prev);
      newMap.set(teamName, color);
      return newMap;
    });
    return color;
  };
  console.log(otherTeamsColors);

  return render ? (
    <ForceGraph2D
      graphData={graphData}
      width={1000}
      height={700}
      linkLabel={(link) => link.label + ' (' + link.years + ')'}
      linkAutoColorBy={(link) => link.label}
      linkCurvature={(link) => {
        return link.timesMet % 2 === 0 ? 0.2 * link.timesMet : -0.2 * (link.timesMet + 1);
      }}
      nodeCanvasObject={(node, ctx) => {
        const size = 5;

        const img = new Image(size, size);
        img.src = node.img_ref; // Path to your node image

        ctx.drawImage(img, (node.x || 0) - size / 2, (node.y || 0) - size / 2, size, size);
      }}
      nodePointerAreaPaint={(node, color, ctx) => {
        const size = 5;
        ctx.fillStyle = color;
        ctx.fillRect((node.x || 0) - size / 2, (node.y || 0) - size / 2, size, size); // draw square as pointer trap
      }}
      nodeLabel={(node) => node.name + ' (' + ((nodesSize.get(node.id) || 5) - 5) + ')'}
      onNodeClick={(node) => {
        if (selectedNode === node.id) {
          setSelectedNode(null);
          return;
        }
        setSelectedNode(node.id);
      }}
      linkVisibility={(link) => {
        return !selectedNode || link.source.id === selectedNode || link.target.id === selectedNode;
      }}
      cooldownTicks={freezeLayout ? 0 : Infinity}
      linkCanvasObject={(link, ctx) => {
        const colors = teamColors[link.label] ?? getOtherTeamsColor(link.label);

        drawLineWithColors(
          ctx.canvas,
          { x: link.source.x, y: link.source.y },
          { x: link.target.x, y: link.target.y },
          colors
        );
      }}
      onLinkClick={(link) => {
        navigator.clipboard.writeText(link.label);
      }}
    />
  ) : (
    <div style={{ width: '1000px', height: '700px' }}></div>
  );
};

export default ConnectionsGraph;

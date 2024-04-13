import { useState } from 'react';
import { ForceGraph2D } from 'react-force-graph';
export interface graphData {
  nodes: { id: string; img_ref: string; name: string }[];
  links: { source: string; target: string; label: string; years: string; timesMet: number }[];
}
interface ConnectionsGraphProps {
  graphData: graphData;
  nodesSize: Map<string, number>;
  render: boolean;
}

const ConnectionsGraph = ({ graphData, nodesSize, render }: ConnectionsGraphProps) => {
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
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
    />
  ) : (
    <div style={{ width: '1000px', height: '700px' }}></div>
  );
};

export default ConnectionsGraph;

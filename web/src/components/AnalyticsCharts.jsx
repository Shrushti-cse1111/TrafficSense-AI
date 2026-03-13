import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const AnalyticsCharts = ({ data }) => {
  if (!data || data.length === 0) return <p className="stat-label">Gathering trend data...</p>;

  // Format data for chart
  const chartData = data.map(item => ({
    hour: `${item.hour}:00`,
    speed: Math.round(item.speed_kmh)
  }));

  return (
    <div style={{ width: '100%', height: 200, marginTop: '1rem' }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis 
            dataKey="hour" 
            stroke="#94a3b8" 
            fontSize={10} 
            tick={{ fill: '#94a3b8' }}
          />
          <YAxis 
            stroke="#94a3b8" 
            fontSize={10} 
            tick={{ fill: '#94a3b8' }}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
            itemStyle={{ color: '#818cf8' }}
          />
          <Line 
            type="monotone" 
            dataKey="speed" 
            stroke="#818cf8" 
            strokeWidth={2} 
            dot={false}
            activeDot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AnalyticsCharts;

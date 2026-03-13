import React from 'react';
import { Navigation, Clock, AlertTriangle } from 'lucide-react';

const RouteSuggestions = ({ routes }) => {
  if (!routes || routes.length === 0) return null;

  return (
    <section className="routes-section" style={{ marginTop: '1.5rem' }}>
      <h3 className="stat-label" style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <Navigation size={16} /> Suggested Routes
      </h3>
      <div className="routes-list" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {routes.map((route, i) => (
          <div key={i} className="route-card" style={{ 
            background: 'var(--glass)', 
            padding: '1rem', 
            borderRadius: '0.75rem', 
            borderLeft: `4px solid ${route.color}`,
            border: '1px solid var(--glass-border)',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.5rem'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>{route.name}</span>
              <span className={`stat-value small`} style={{ color: route.color }}>{route.congestion}</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                <Clock size={12} /> {route.time_mins} mins
              </span>
              {route.congestion === 'High' && (
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: 'var(--danger)' }}>
                  <AlertTriangle size={12} /> Heavy Traffic
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default RouteSuggestions;

import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Map as MapIcon, BarChart3, Navigation as NavigationIcon, ShieldAlert, LogOut, Activity, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';

const Layout = ({ children, lastUpdated, hotspots = [], alerts = [] }) => {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    const navItems = [
        { path: '/', icon: <MapIcon size={18} />, label: 'Traffic Map' },
        { path: '/analytics', icon: <BarChart3 size={18} />, label: 'Analytics' },
        { path: '/routes', icon: <NavigationIcon size={18} />, label: 'Smart Routes' },
    ];

    return (
        <div className="layout-container vertical">
            <header className="navbar neon-glass">
                <div className="nav-left">
                    <div className="logo-section small">
                        <ShieldAlert size={28} className="neon-icon" />
                        <h1 className="neon-text">TrafficSense</h1>
                    </div>
                    <nav className="top-nav">
                        {navItems.map((item) => (
                            <NavLink 
                                key={item.path} 
                                to={item.path} 
                                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                            >
                                {item.icon}
                                <span>{item.label}</span>
                            </NavLink>
                        ))}
                    </nav>
                </div>

                <div className="live-data-ticker">
                    <div className="ticker-content">
                        {alerts.length > 0 ? alerts.map((alert, index) => (
                            <span key={index} className="ticker-item">
                                <span className={`neon-dot ${alert.severity === 'critical' ? 'red' : alert.severity === 'high' ? 'yellow' : ''}`}></span>
                                {alert.type.toUpperCase()}: {alert.location} - {alert.description}
                            </span>
                        )) : (
                            <>
                                <span className="ticker-item"><span className="neon-dot"></span> LIVE PUNE: MG Road - High Congestion (+12m)</span>
                                <span className="ticker-item"><span className="neon-dot green"></span> Hinjewadi Phase 3 - Clear Flow (42km/h)</span>
                                <span className="ticker-item"><span className="neon-dot yellow"></span> Baner Road - Moderate Traffic</span>
                                <span className="ticker-item"><span className="neon-dot"></span> Weather: 31°C Clear High Humidity</span>
                            </>
                        )}
                    </div>
                </div>
                
                <div className="nav-right">
                    <div className="status-pill neon-pill">
                        <Activity size={12} className="pulse" />
                        <span>Command Center</span>
                    </div>
                    <div className="v-divider"></div>
                    <button onClick={handleLogout} className="logout-icon-btn neon-hover" title="Logout">
                        <LogOut size={18} />
                    </button>
                    <div className="user-avatar-small neon-border">AD</div>
                </div>
            </header>

            <div className="main-wrapper">
                <aside className="info-sidebar glass-card">
                    <div className="info-section">
                        <h3>Traffic Index</h3>
                        <div className="heatmap-index">
                            <div className="index-item"><span className="dot critical"></span> Critical</div>
                            <div className="index-item"><span className="dot high"></span> High</div>
                            <div className="index-item"><span className="dot moderate"></span> Moderate</div>
                            <div className="index-item"><span className="dot clear"></span> Clear</div>
                        </div>
                    </div>

                    <div className="info-section">
                        <h3>Live Hotspots</h3>
                        <div className="hotspot-list">
                            {hotspots.length > 0 ? hotspots.map((spot, i) => (
                                <div key={i} className="hotspot-item-detailed">
                                    <div className="spot-header">
                                        <span className="spot-name">{spot.name}</span>
                                        <span className={`severity-tag ${spot.status.toLowerCase()}`}>{spot.status}</span>
                                    </div>
                                    <div className="spot-details">
                                        <span>Avg. {spot.speed || '24'}km/h</span>
                                        <span className="v-divider-small"></span>
                                        <span>{spot.condition || 'Clear'}</span>
                                    </div>
                                </div>
                            )) : (
                                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Monitoring city grid...</p>
                            )}
                        </div>
                    </div>

                    <div className="info-section alerts-section">
                        <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--danger)' }}>
                            <AlertCircle size={14} /> Active Alerts
                        </h3>
                        <div className="alerts-list">
                            {alerts.length > 0 ? alerts.map((alert, i) => (
                                <div key={i} className={`alert-card ${alert.severity}`} style={{
                                    padding: '0.75rem',
                                    borderRadius: '0.5rem',
                                    background: 'var(--background)',
                                    alignItems: 'flex-start',
                                    marginTop: '0.5rem',
                                    borderLeft: `3px solid ${alert.severity === 'critical' ? 'var(--danger)' : alert.severity === 'high' ? 'var(--warning)' : 'var(--primary)'}`
                                }}>
                                    <div style={{ fontWeight: 'bold', fontSize: '0.8rem', color: 'var(--text-main)', marginBottom: '0.2rem' }}>
                                        {alert.type} • {alert.location}
                                    </div>
                                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                                        {alert.description}
                                    </div>
                                    <div style={{ fontSize: '0.65rem', color: 'var(--primary)', marginTop: '0.3rem' }}>
                                        {alert.time}
                                    </div>
                                </div>
                            )) : (
                                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>No active alerts in Pune</p>
                            )}
                        </div>
                    </div>

                    <div className="sidebar-footer">
                        <p className="sync-time">Last Updated: {lastUpdated}</p>
                    </div>
                </aside>

                <main className="content-area">
                    <div className="page-content">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
};

export default Layout;

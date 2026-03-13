import React from 'react';
import AnalyticsCharts from '../components/AnalyticsCharts';
import { motion } from 'framer-motion';
import { TrendingUp, Clock, Activity } from 'lucide-react';

const AnalyticsPage = ({ trends, forecast = [] }) => {
    return (
        <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="page-container analytics-page"
        >
            <div className="analytics-header">
                <div>
                    <h2>Traffic Analytics & Forecast</h2>
                    <p>Insights for Pune Metropolitan Region</p>
                </div>
                <button className="export-btn" onClick={() => alert('Exporting Pune Traffic Data to CSV...')}>
                    Export Data (CSV)
                </button>
            </div>

            <div className="analytics-grid">
                <div className="chart-section glass-card">
                    <div className="card-title">
                        <TrendingUp size={18} />
                        <span>Hourly Traffic Intensity (Historical)</span>
                    </div>
                    <AnalyticsCharts data={trends} />
                </div>

                <div className="chart-section glass-card">
                    <div className="card-title">
                        <Clock size={18} />
                        <span>Traffic Forecast Timeline (Next 12 Hours)</span>
                    </div>
                    {/* Transform forecast data to match chart expectations */}
                    <AnalyticsCharts data={forecast.map(f => ({ hour: f.time.replace(' ', ''), speed_kmh: f.predicted_speed }))} />
                </div>

                <div className="stats-sidebar">
                    <div className="mini-card glass-card">
                        <Activity size={18} />
                        <div>
                            <span className="label">Forecast Severity</span>
                            <span className="value" style={{color: '#fbbf24'}}>Moderate Traffic</span>
                        </div>
                    </div>
                    <div className="mini-card glass-card">
                        <Clock size={18} />
                        <div>
                            <span className="label">Peak Hour Today</span>
                            <span className="value">6:00 PM - 8:00 PM</span>
                        </div>
                    </div>
                </div>
            </div>
        </motion.div>
    );
};

export default AnalyticsPage;

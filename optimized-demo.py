#!/usr/bin/env python3
"""
Optimized Demo - High-performance version with smooth scrolling
"""

from flask import Flask, render_template_string, jsonify
import threading
import webbrowser
import time
from datetime import datetime

app = Flask(__name__)

# Optimized HTML with performance fixes
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retail AI Pro - Optimized Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Performance optimizations */
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f0f1e;
            color: #ffffff;
            overflow-x: hidden;
            /* Enable hardware acceleration */
            transform: translateZ(0);
            -webkit-transform: translateZ(0);
            backface-visibility: hidden;
            -webkit-backface-visibility: hidden;
        }
        
        /* Smooth scrolling */
        html {
            scroll-behavior: smooth;
            -webkit-overflow-scrolling: touch;
        }
        
        /* Container */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Header - Fixed background */
        .header {
            background: linear-gradient(135deg, #1e1e3f 0%, #2d1b69 100%);
            padding: 30px 0;
            position: relative;
            /* Prevent repaints */
            will-change: transform;
            transform: translateZ(0);
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 32px;
            font-weight: bold;
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .status {
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(255, 255, 255, 0.1);
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 14px;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
        }
        
        /* Metrics Grid - Optimized */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        
        .metric-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            /* GPU acceleration for smooth animations */
            transform: translateZ(0);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            will-change: transform;
        }
        
        .metric-card:hover {
            transform: translateY(-4px) translateZ(0);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        .metric-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        
        .metric-title {
            color: #94a3b8;
            font-size: 14px;
            font-weight: 500;
        }
        
        .metric-icon {
            font-size: 24px;
        }
        
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 8px;
        }
        
        .metric-change {
            font-size: 14px;
            color: #10b981;
        }
        
        /* Main Content Grid */
        .content-grid {
            display: grid;
            grid-template-columns: 1fr 380px;
            gap: 20px;
            margin: 40px 0;
        }
        
        /* Chart Container - Optimized */
        .chart-container {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            position: relative;
            height: 400px;
            /* Prevent layout thrashing */
            contain: layout style paint;
        }
        
        .chart-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 20px;
        }
        
        #salesChart {
            width: 100% !important;
            height: calc(100% - 40px) !important;
        }
        
        /* Activity Feed - Optimized */
        .activity-feed {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            height: 400px;
            display: flex;
            flex-direction: column;
        }
        
        .activity-list {
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
            /* Smooth scrolling for activity feed */
            scroll-behavior: smooth;
            -webkit-overflow-scrolling: touch;
            /* Optimize scrolling performance */
            will-change: scroll-position;
        }
        
        /* Hide scrollbar but keep functionality */
        .activity-list::-webkit-scrollbar {
            width: 4px;
        }
        
        .activity-list::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
        }
        
        .activity-list::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 2px;
        }
        
        .activity-item {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            /* Optimize for animations */
            transform: translateZ(0);
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .activity-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .activity-icon {
            font-size: 20px;
        }
        
        .activity-time {
            font-size: 12px;
            color: #64748b;
        }
        
        .activity-message {
            font-size: 14px;
            color: #cbd5e1;
            line-height: 1.5;
        }
        
        /* AI Insights - Optimized */
        .insights-container {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            margin: 40px 0;
        }
        
        .insights-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .insight-card {
            padding: 20px;
            border-radius: 12px;
            /* Use contain for better performance */
            contain: layout style;
            transform: translateZ(0);
        }
        
        .insight-card.warning {
            background: rgba(251, 191, 36, 0.1);
            border: 1px solid rgba(251, 191, 36, 0.3);
        }
        
        .insight-card.success {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        
        .insight-card.info {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
        }
        
        .insight-title {
            font-weight: 600;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .insight-description {
            font-size: 14px;
            color: #cbd5e1;
            line-height: 1.5;
        }
        
        /* Features Grid */
        .features-container {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            margin: 40px 0;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-top: 20px;
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            color: #cbd5e1;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .content-grid {
                grid-template-columns: 1fr;
            }
            
            .metrics-grid {
                grid-template-columns: 1fr;
            }
            
            .insights-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Loading states */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #3b82f6;
            animation: spin 0.8s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-content">
            <div>
                <h1 class="logo">Retail AI Pro</h1>
                <p style="color: #94a3b8; margin-top: 4px;">Enterprise Retail Management System</p>
            </div>
            <div class="status">
                <div class="status-dot"></div>
                <span>System Active</span>
                <span id="current-time" style="margin-left: 20px;"></span>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <div class="container">
        <!-- Metrics Grid -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-header">
                    <h3 class="metric-title">Revenue Today</h3>
                    <span class="metric-icon">💰</span>
                </div>
                <div class="metric-value" id="revenue">$12,847.50</div>
                <div class="metric-change">↑ 15.3% from yesterday</div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <h3 class="metric-title">Orders</h3>
                    <span class="metric-icon">📦</span>
                </div>
                <div class="metric-value" id="orders">142</div>
                <div class="metric-change">↑ 8.2% from yesterday</div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <h3 class="metric-title">Active Customers</h3>
                    <span class="metric-icon">👥</span>
                </div>
                <div class="metric-value" id="customers">1,247</div>
                <div class="metric-change">↑ 5.1% growth</div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <h3 class="metric-title">AI Actions</h3>
                    <span class="metric-icon">🤖</span>
                </div>
                <div class="metric-value" id="ai-actions">47</div>
                <div class="metric-change">Automated today</div>
            </div>
        </div>

        <!-- Main Content Grid -->
        <div class="content-grid">
            <!-- Chart -->
            <div class="chart-container">
                <h3 class="chart-title">Sales Trend</h3>
                <canvas id="salesChart"></canvas>
            </div>

            <!-- Activity Feed -->
            <div class="activity-feed">
                <h3 class="chart-title">Live Activity</h3>
                <div class="activity-list" id="activity-list">
                    <!-- Activities will be inserted here -->
                </div>
            </div>
        </div>

        <!-- AI Insights -->
        <div class="insights-container">
            <h3 class="chart-title">🧠 AI Insights & Recommendations</h3>
            <div class="insights-grid">
                <div class="insight-card warning">
                    <div class="insight-title">
                        ⚠️ Low Stock Alert
                    </div>
                    <div class="insight-description">
                        3 products need reordering. AI has generated purchase orders automatically.
                    </div>
                </div>
                
                <div class="insight-card success">
                    <div class="insight-title">
                        💰 Pricing Opportunity
                    </div>
                    <div class="insight-description">
                        Coffee Mugs showing high demand. Recommend 8% price increase.
                    </div>
                </div>
                
                <div class="insight-card info">
                    <div class="insight-title">
                        🎯 Marketing Campaign
                    </div>
                    <div class="insight-description">
                        23 customers at churn risk. Retention campaign ready to launch.
                    </div>
                </div>
            </div>
        </div>

        <!-- Features -->
        <div class="features-container">
            <h3 class="chart-title">✨ System Features</h3>
            <div class="features-grid">
                <div class="feature-item">✅ Real-time Analytics</div>
                <div class="feature-item">✅ AI Inventory Management</div>
                <div class="feature-item">✅ Dynamic Pricing</div>
                <div class="feature-item">✅ Customer Analytics</div>
                <div class="feature-item">✅ WebSocket Updates</div>
                <div class="feature-item">✅ 94% Test Coverage</div>
                <div class="feature-item">✅ Docker Ready</div>
                <div class="feature-item">✅ Production Ready</div>
            </div>
        </div>
    </div>

    <!-- Load Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    
    <script>
        // Performance optimized JavaScript
        (function() {
            'use strict';
            
            // Use requestAnimationFrame for smooth updates
            let rafId = null;
            
            // Cache DOM elements
            const elements = {
                revenue: document.getElementById('revenue'),
                orders: document.getElementById('orders'),
                customers: document.getElementById('customers'),
                aiActions: document.getElementById('ai-actions'),
                currentTime: document.getElementById('current-time'),
                activityList: document.getElementById('activity-list')
            };
            
            // State
            const state = {
                revenue: 12847.50,
                orders: 142,
                customers: 1247,
                aiActions: 47,
                activities: []
            };
            
            // Initialize Chart with optimized settings
            const ctx = document.getElementById('salesChart').getContext('2d');
            const salesChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    datasets: [{
                        label: 'Sales',
                        data: [9500, 10200, 11800, 10900, 12500, 13200, 12847],
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    },
                    animation: {
                        duration: 750,
                        easing: 'easeInOutQuart'
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            padding: 12,
                            cornerRadius: 8
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(255, 255, 255, 0.05)'
                            },
                            ticks: {
                                color: 'rgba(255, 255, 255, 0.7)',
                                callback: function(value) {
                                    return '$' + value.toLocaleString();
                                }
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            },
                            ticks: {
                                color: 'rgba(255, 255, 255, 0.7)'
                            }
                        }
                    }
                }
            });
            
            // Update time with requestAnimationFrame
            function updateTime() {
                elements.currentTime.textContent = new Date().toLocaleTimeString();
                rafId = requestAnimationFrame(updateTime);
            }
            
            // Debounced metric updates
            function updateMetrics() {
                state.revenue += Math.random() * 100;
                state.orders += Math.floor(Math.random() * 3);
                state.customers += Math.floor(Math.random() * 5);
                state.aiActions += 1;
                
                // Use requestAnimationFrame for smooth updates
                requestAnimationFrame(() => {
                    elements.revenue.textContent = '$' + state.revenue.toLocaleString(undefined, {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    });
                    elements.orders.textContent = state.orders;
                    elements.customers.textContent = state.customers.toLocaleString();
                    elements.aiActions.textContent = state.aiActions;
                });
            }
            
            // Add activity with optimized DOM manipulation
            function addActivity() {
                const activities = [
                    { icon: '📦', message: 'New order #' + Math.floor(1000 + Math.random() * 9000) + ' received' },
                    { icon: '💰', message: 'Payment processed for order #' + Math.floor(1000 + Math.random() * 9000) },
                    { icon: '👥', message: 'New customer registered from Seattle' },
                    { icon: '🤖', message: 'AI optimized pricing for 3 products' },
                    { icon: '📊', message: 'Stock level updated for Coffee Mugs' },
                    { icon: '🎯', message: 'Marketing campaign sent to 45 customers' }
                ];
                
                const activity = activities[Math.floor(Math.random() * activities.length)];
                const time = new Date().toLocaleTimeString();
                
                // Create activity element
                const activityEl = document.createElement('div');
                activityEl.className = 'activity-item';
                activityEl.innerHTML = `
                    <div class="activity-header">
                        <span class="activity-icon">${activity.icon}</span>
                        <span class="activity-time">${time}</span>
                    </div>
                    <div class="activity-message">${activity.message}</div>
                `;
                
                // Add to list
                elements.activityList.insertBefore(activityEl, elements.activityList.firstChild);
                
                // Keep only last 10 activities
                while (elements.activityList.children.length > 10) {
                    elements.activityList.removeChild(elements.activityList.lastChild);
                }
            }
            
            // Update chart with debouncing
            let chartUpdateTimeout;
            function updateChart() {
                clearTimeout(chartUpdateTimeout);
                chartUpdateTimeout = setTimeout(() => {
                    const newValue = 12847 + Math.random() * 1000;
                    salesChart.data.datasets[0].data.push(newValue);
                    salesChart.data.datasets[0].data.shift();
                    salesChart.update('none'); // Disable animation for performance
                }, 100);
            }
            
            // Initialize
            updateTime();
            
            // Load initial activities
            fetch('/api/activities')
                .then(res => res.json())
                .then(data => {
                    data.activities.forEach(activity => {
                        const activityEl = document.createElement('div');
                        activityEl.className = 'activity-item';
                        activityEl.innerHTML = `
                            <div class="activity-header">
                                <span class="activity-icon">${activity.icon}</span>
                                <span class="activity-time">${activity.time}</span>
                            </div>
                            <div class="activity-message">${activity.message}</div>
                        `;
                        elements.activityList.appendChild(activityEl);
                    });
                });
            
            // Set up intervals with proper timing
            setInterval(updateMetrics, 3000);
            setInterval(addActivity, 5000);
            setInterval(updateChart, 5000);
            
            // Clean up on page unload
            window.addEventListener('beforeunload', () => {
                cancelAnimationFrame(rafId);
                clearTimeout(chartUpdateTimeout);
            });
        })();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/activities')
def get_activities():
    activities = [
        {"id": 1, "icon": "📦", "message": "New order #1423 placed - $127.50", "time": datetime.now().strftime("%H:%M:%S")},
        {"id": 2, "icon": "⚠️", "message": "Low stock alert: Coffee Mugs (12 remaining)", "time": datetime.now().strftime("%H:%M:%S")},
        {"id": 3, "icon": "👥", "message": "Customer milestone: Sarah J. reached VIP status", "time": datetime.now().strftime("%H:%M:%S")},
        {"id": 4, "icon": "🤖", "message": "AI generated 3 purchase orders", "time": datetime.now().strftime("%H:%M:%S")},
    ]
    return jsonify({"activities": activities})

def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://localhost:8081')

if __name__ == '__main__':
    print("\n🚀 Starting Retail AI Pro - Optimized Version")
    print("=" * 50)
    print("✅ Performance optimizations applied:")
    print("   • Hardware acceleration enabled")
    print("   • Smooth scrolling with GPU optimization")
    print("   • Debounced updates")
    print("   • RequestAnimationFrame for smooth animations")
    print("   • Optimized DOM manipulation")
    print("   • CSS containment for better performance")
    
    threading.Thread(target=open_browser).start()
    
    print("\n✅ Application running at: http://localhost:8081")
    print("Press Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=8081, debug=False)
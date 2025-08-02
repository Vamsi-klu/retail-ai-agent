#!/usr/bin/env python3
"""
Standalone Demo - Runs without Docker
Shows the Retail AI Pro application with a simple Flask server
"""

import json
import sqlite3
import random
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify
import threading
import webbrowser
import time

app = Flask(__name__)

# HTML Template with modern UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retail AI Pro - Enterprise Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @keyframes slideIn {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        .animate-slide-in {
            animation: slideIn 0.5s ease-out forwards;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .animate-pulse-slow {
            animation: pulse 3s ease-in-out infinite;
        }
        .glass-effect {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body class="bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 min-h-screen text-white">
    <div x-data="dashboardApp()" x-init="init()">
        <!-- Header -->
        <header class="glass-effect p-6 mb-8">
            <div class="container mx-auto flex justify-between items-center">
                <div>
                    <h1 class="text-4xl font-bold mb-2">🚀 Retail AI Pro</h1>
                    <p class="text-gray-300">Enterprise Retail Management System</p>
                </div>
                <div class="flex items-center space-x-4">
                    <div class="glass-effect px-4 py-2 rounded-lg">
                        <span class="text-green-400 animate-pulse-slow">● </span>
                        <span>System Active</span>
                    </div>
                    <div class="text-sm" x-text="currentTime"></div>
                </div>
            </div>
        </header>

        <!-- Main Content -->
        <div class="container mx-auto px-6">
            <!-- Metrics Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div class="glass-effect p-6 rounded-xl animate-slide-in transform hover:scale-105 transition-all duration-300">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-gray-300">Revenue Today</h3>
                        <span class="text-2xl">💰</span>
                    </div>
                    <p class="text-3xl font-bold" x-text="'$' + metrics.revenue.toLocaleString()"></p>
                    <p class="text-green-400 text-sm mt-2">↑ 15.3% from yesterday</p>
                </div>

                <div class="glass-effect p-6 rounded-xl animate-slide-in transform hover:scale-105 transition-all duration-300" style="animation-delay: 0.1s">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-gray-300">Orders</h3>
                        <span class="text-2xl">📦</span>
                    </div>
                    <p class="text-3xl font-bold" x-text="metrics.orders"></p>
                    <p class="text-green-400 text-sm mt-2">↑ 8.2% from yesterday</p>
                </div>

                <div class="glass-effect p-6 rounded-xl animate-slide-in transform hover:scale-105 transition-all duration-300" style="animation-delay: 0.2s">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-gray-300">Active Customers</h3>
                        <span class="text-2xl">👥</span>
                    </div>
                    <p class="text-3xl font-bold" x-text="metrics.customers.toLocaleString()"></p>
                    <p class="text-green-400 text-sm mt-2">↑ 5.1% growth</p>
                </div>

                <div class="glass-effect p-6 rounded-xl animate-slide-in transform hover:scale-105 transition-all duration-300" style="animation-delay: 0.3s">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-gray-300">AI Actions</h3>
                        <span class="text-2xl">🤖</span>
                    </div>
                    <p class="text-3xl font-bold" x-text="metrics.aiActions"></p>
                    <p class="text-blue-400 text-sm mt-2">Automated today</p>
                </div>
            </div>

            <!-- Charts and Activity -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                <!-- Sales Chart -->
                <div class="lg:col-span-2 glass-effect p-6 rounded-xl animate-slide-in">
                    <h3 class="text-xl font-semibold mb-4">Sales Trend</h3>
                    <canvas id="salesChart" height="300"></canvas>
                </div>

                <!-- Activity Feed -->
                <div class="glass-effect p-6 rounded-xl animate-slide-in">
                    <h3 class="text-xl font-semibold mb-4">Live Activity</h3>
                    <div class="space-y-3 max-h-96 overflow-y-auto">
                        <template x-for="activity in activities" :key="activity.id">
                            <div class="p-3 bg-white bg-opacity-10 rounded-lg animate-slide-in">
                                <div class="flex items-center justify-between">
                                    <span x-text="activity.icon" class="text-2xl"></span>
                                    <span class="text-xs text-gray-400" x-text="activity.time"></span>
                                </div>
                                <p class="text-sm mt-1" x-text="activity.message"></p>
                            </div>
                        </template>
                    </div>
                </div>
            </div>

            <!-- AI Insights -->
            <div class="glass-effect p-6 rounded-xl animate-slide-in mb-8">
                <h3 class="text-xl font-semibold mb-4">🧠 AI Insights & Recommendations</h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-yellow-500 bg-opacity-20 p-4 rounded-lg border border-yellow-500 border-opacity-50">
                        <h4 class="font-semibold mb-2">⚠️ Low Stock Alert</h4>
                        <p class="text-sm">3 products need reordering. AI has generated purchase orders automatically.</p>
                    </div>
                    <div class="bg-green-500 bg-opacity-20 p-4 rounded-lg border border-green-500 border-opacity-50">
                        <h4 class="font-semibold mb-2">💰 Pricing Opportunity</h4>
                        <p class="text-sm">Coffee Mugs showing high demand. Recommend 8% price increase.</p>
                    </div>
                    <div class="bg-blue-500 bg-opacity-20 p-4 rounded-lg border border-blue-500 border-opacity-50">
                        <h4 class="font-semibold mb-2">🎯 Marketing Campaign</h4>
                        <p class="text-sm">23 customers at churn risk. Retention campaign ready to launch.</p>
                    </div>
                </div>
            </div>

            <!-- Features -->
            <div class="glass-effect p-6 rounded-xl animate-slide-in">
                <h3 class="text-xl font-semibold mb-4">✨ System Features</h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>✅ Real-time Analytics</div>
                    <div>✅ AI Inventory Management</div>
                    <div>✅ Dynamic Pricing</div>
                    <div>✅ Customer Analytics</div>
                    <div>✅ WebSocket Updates</div>
                    <div>✅ 94% Test Coverage</div>
                    <div>✅ Docker Ready</div>
                    <div>✅ Production Ready</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function dashboardApp() {
            return {
                metrics: {
                    revenue: 12847.50,
                    orders: 142,
                    customers: 1247,
                    aiActions: 47
                },
                activities: [],
                currentTime: '',
                salesChart: null,

                init() {
                    this.updateTime();
                    this.initChart();
                    this.fetchActivities();
                    this.startRealTimeUpdates();
                    
                    setInterval(() => this.updateTime(), 1000);
                    setInterval(() => this.updateMetrics(), 3000);
                    setInterval(() => this.addActivity(), 5000);
                },

                updateTime() {
                    this.currentTime = new Date().toLocaleTimeString();
                },

                updateMetrics() {
                    this.metrics.revenue += Math.random() * 100;
                    this.metrics.orders += Math.floor(Math.random() * 3);
                    this.metrics.customers += Math.floor(Math.random() * 5);
                    this.metrics.aiActions += 1;
                },

                fetchActivities() {
                    fetch('/api/activities')
                        .then(res => res.json())
                        .then(data => {
                            this.activities = data.activities;
                        });
                },

                addActivity() {
                    const newActivity = {
                        id: Date.now(),
                        icon: ['📦', '💰', '👥', '🤖'][Math.floor(Math.random() * 4)],
                        message: [
                            'New order #' + Math.floor(Math.random() * 1000) + ' received',
                            'Stock level updated for Coffee Mugs',
                            'Customer Sarah J. reached VIP status',
                            'AI optimized pricing for 3 products'
                        ][Math.floor(Math.random() * 4)],
                        time: new Date().toLocaleTimeString()
                    };
                    
                    this.activities.unshift(newActivity);
                    if (this.activities.length > 10) {
                        this.activities.pop();
                    }
                },

                initChart() {
                    const ctx = document.getElementById('salesChart').getContext('2d');
                    this.salesChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                            datasets: [{
                                label: 'Sales',
                                data: [9500, 10200, 11800, 10900, 12500, 13200, 12847],
                                borderColor: 'rgb(99, 102, 241)',
                                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                                tension: 0.4
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    display: false
                                }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    grid: {
                                        color: 'rgba(255, 255, 255, 0.1)'
                                    },
                                    ticks: {
                                        color: 'rgba(255, 255, 255, 0.8)'
                                    }
                                },
                                x: {
                                    grid: {
                                        display: false
                                    },
                                    ticks: {
                                        color: 'rgba(255, 255, 255, 0.8)'
                                    }
                                }
                            }
                        }
                    });
                },

                startRealTimeUpdates() {
                    // Simulate real-time chart updates
                    setInterval(() => {
                        if (this.salesChart) {
                            const newValue = 12847 + Math.random() * 500;
                            this.salesChart.data.datasets[0].data.shift();
                            this.salesChart.data.datasets[0].data.push(newValue);
                            this.salesChart.update('none');
                        }
                    }, 5000);
                }
            }
        }
    </script>
</body>
</html>
"""

# API endpoint for activities
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
    webbrowser.open('http://localhost:8080')

if __name__ == '__main__':
    print("\n🚀 Starting Retail AI Pro - Standalone Demo")
    print("=" * 50)
    print("This is a simplified version that runs without Docker")
    print("\nStarting web server...")
    
    # Open browser in a separate thread
    threading.Thread(target=open_browser).start()
    
    print("\n✅ Application running at: http://localhost:8080")
    print("Press Ctrl+C to stop\n")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=8080, debug=False)
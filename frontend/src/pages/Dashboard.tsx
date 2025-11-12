/**
 * Dashboard Page
 */
import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '@/services/api';
import { TrendingUp, Package, Users, ShoppingCart, AlertTriangle } from 'lucide-react';
import type { DashboardMetrics } from '@/types';

export default function Dashboard() {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['dashboard-metrics'],
    queryFn: () => api.getDashboardMetrics(),
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  const stats = [
    {
      name: 'Total Revenue',
      value: `$${metrics?.total_revenue.toLocaleString() || 0}`,
      icon: TrendingUp,
      color: 'text-green-600',
    },
    {
      name: 'Total Orders',
      value: metrics?.total_orders || 0,
      icon: ShoppingCart,
      color: 'text-blue-600',
    },
    {
      name: 'Total Customers',
      value: metrics?.total_customers || 0,
      icon: Users,
      color: 'text-purple-600',
    },
    {
      name: 'Total Products',
      value: metrics?.total_products || 0,
      icon: Package,
      color: 'text-orange-600',
    },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.name} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold mt-1">{stat.value}</p>
                </div>
                <Icon className={`w-8 h-8 ${stat.color}`} />
              </div>
            </div>
          );
        })}
      </div>

      {/* Low Stock Alert */}
      {metrics && metrics.low_stock_products > 0 && (
        <div className="card bg-yellow-50 border border-yellow-200">
          <div className="flex items-center">
            <AlertTriangle className="w-6 h-6 text-yellow-600 mr-3" />
            <div>
              <h3 className="font-semibold text-yellow-900">Low Stock Alert</h3>
              <p className="text-sm text-yellow-700">
                {metrics.low_stock_products} products are running low on stock
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Today's Performance</h3>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Revenue</span>
              <span className="font-semibold">
                ${metrics?.today_revenue.toLocaleString() || 0}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Orders</span>
              <span className="font-semibold">{metrics?.today_orders || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Average Order Value</span>
              <span className="font-semibold">
                ${metrics?.average_order_value.toFixed(2) || 0}
              </span>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Inventory Status</h3>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Total Products</span>
              <span className="font-semibold">{metrics?.total_products || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Low Stock Items</span>
              <span className="font-semibold text-yellow-600">
                {metrics?.low_stock_products || 0}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * TypeScript type definitions for Retail AI Pro
 */

export interface Product {
  id: number;
  sku: string;
  name: string;
  description?: string;
  category_id?: number;
  supplier_id?: number;
  cost_price: number;
  selling_price: number;
  discount_price?: number;
  current_stock: number;
  reorder_point: number;
  reorder_quantity: number;
  is_active: boolean;
  is_featured: boolean;
  is_on_sale: boolean;
  created_at: string;
  updated_at: string;
}

export interface Customer {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  address?: string;
  city?: string;
  state?: string;
  zip_code?: string;
  total_purchases: number;
  total_orders: number;
  average_order_value: number;
  loyalty_tier: string;
  loyalty_points: number;
  churn_risk: number;
  lifetime_value: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Order {
  id: number;
  order_number: string;
  customer_id: number;
  subtotal: number;
  tax_amount: number;
  discount_amount: number;
  shipping_cost: number;
  total_amount: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled' | 'refunded';
  payment_method: string;
  payment_status: string;
  created_at: string;
  updated_at: string;
  items: OrderItem[];
}

export interface OrderItem {
  id: number;
  product_id: number;
  product_name: string;
  product_sku: string;
  quantity: number;
  unit_price: number;
  total: number;
}

export interface DashboardMetrics {
  total_revenue: number;
  total_orders: number;
  total_customers: number;
  total_products: number;
  low_stock_products: number;
  average_order_value: number;
  today_revenue: number;
  today_orders: number;
}

export interface RevenueData {
  date: string;
  revenue: number;
  orders: number;
}

export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  role: string;
  is_active: boolean;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  password: string;
}

export interface ApiError {
  detail: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

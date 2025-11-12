/**
 * API service for making HTTP requests to the backend
 */
import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  Product,
  Customer,
  Order,
  DashboardMetrics,
  RevenueData,
  User,
  AuthTokens,
  LoginCredentials,
  RegisterData,
  ApiError,
} from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor to handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ApiError>) => {
        if (error.response?.status === 401) {
          // Clear tokens and redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(credentials: LoginCredentials): Promise<AuthTokens> {
    const { data } = await this.client.post<AuthTokens>('/api/v1/auth/login', credentials);
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    return data;
  }

  async register(userData: RegisterData): Promise<User> {
    const { data } = await this.client.post<User>('/api/v1/auth/register', userData);
    return data;
  }

  async getCurrentUser(): Promise<User> {
    const { data } = await this.client.get<User>('/api/v1/auth/me');
    return data;
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // Product endpoints
  async getProducts(params?: {
    skip?: number;
    limit?: number;
    category_id?: number;
    is_active?: boolean;
    search?: string;
  }): Promise<Product[]> {
    const { data } = await this.client.get<Product[]>('/api/v1/products', { params });
    return data;
  }

  async getProduct(id: number): Promise<Product> {
    const { data } = await this.client.get<Product>(`/api/v1/products/${id}`);
    return data;
  }

  async createProduct(product: Partial<Product>): Promise<Product> {
    const { data } = await this.client.post<Product>('/api/v1/products', product);
    return data;
  }

  async updateProduct(id: number, product: Partial<Product>): Promise<Product> {
    const { data } = await this.client.put<Product>(`/api/v1/products/${id}`, product);
    return data;
  }

  async deleteProduct(id: number): Promise<void> {
    await this.client.delete(`/api/v1/products/${id}`);
  }

  async getLowStockProducts(): Promise<Product[]> {
    const { data} = await this.client.get<Product[]>('/api/v1/products/low-stock');
    return data;
  }

  // Customer endpoints
  async getCustomers(params?: {
    skip?: number;
    limit?: number;
    loyalty_tier?: string;
    search?: string;
  }): Promise<Customer[]> {
    const { data } = await this.client.get<Customer[]>('/api/v1/customers', { params });
    return data;
  }

  async getCustomer(id: number): Promise<Customer> {
    const { data } = await this.client.get<Customer>(`/api/v1/customers/${id}`);
    return data;
  }

  async createCustomer(customer: Partial<Customer>): Promise<Customer> {
    const { data } = await this.client.post<Customer>('/api/v1/customers', customer);
    return data;
  }

  async updateCustomer(id: number, customer: Partial<Customer>): Promise<Customer> {
    const { data } = await this.client.put<Customer>(`/api/v1/customers/${id}`, customer);
    return data;
  }

  async getHighValueCustomers(): Promise<Customer[]> {
    const { data } = await this.client.get<Customer[]>('/api/v1/customers/high-value');
    return data;
  }

  async getAtRiskCustomers(): Promise<Customer[]> {
    const { data } = await this.client.get<Customer[]>('/api/v1/customers/at-risk');
    return data;
  }

  // Order endpoints
  async getOrders(params?: {
    skip?: number;
    limit?: number;
    customer_id?: number;
    status?: string;
  }): Promise<Order[]> {
    const { data } = await this.client.get<Order[]>('/api/v1/orders', { params });
    return data;
  }

  async getOrder(id: number): Promise<Order> {
    const { data } = await this.client.get<Order>(`/api/v1/orders/${id}`);
    return data;
  }

  async createOrder(order: Partial<Order>): Promise<Order> {
    const { data } = await this.client.post<Order>('/api/v1/orders', order);
    return data;
  }

  async cancelOrder(id: number): Promise<Order> {
    const { data } = await this.client.post<Order>(`/api/v1/orders/${id}/cancel`);
    return data;
  }

  // Analytics endpoints
  async getDashboardMetrics(): Promise<DashboardMetrics> {
    const { data } = await this.client.get<DashboardMetrics>('/api/v1/analytics/dashboard');
    return data;
  }

  async getRevenue(days: number = 30): Promise<RevenueData[]> {
    const { data } = await this.client.get<RevenueData[]>('/api/v1/analytics/revenue', {
      params: { days },
    });
    return data;
  }

  async getTopProducts(limit: number = 10): Promise<any[]> {
    const { data } = await this.client.get('/api/v1/analytics/top-products', {
      params: { limit },
    });
    return data;
  }

  async getInventoryAlerts(): Promise<any> {
    const { data } = await this.client.get('/api/v1/analytics/inventory-alerts');
    return data;
  }
}

export const api = new ApiService();
export default api;

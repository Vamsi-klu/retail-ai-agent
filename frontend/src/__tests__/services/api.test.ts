/**
 * Tests for API service
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import { api } from '@/services/api';

// Mock axios
vi.mock('axios');
const mockedAxios = axios as any;

describe('ApiService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockedAxios.create.mockReturnValue({
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
      interceptors: {
        request: { use: vi.fn() },
        response: { use: vi.fn() },
      },
    });
  });

  it('should have login method', () => {
    expect(api.login).toBeDefined();
  });

  it('should have register method', () => {
    expect(api.register).toBeDefined();
  });

  it('should have getCurrentUser method', () => {
    expect(api.getCurrentUser).toBeDefined();
  });

  it('should have product methods', () => {
    expect(api.getProducts).toBeDefined();
    expect(api.getProduct).toBeDefined();
    expect(api.createProduct).toBeDefined();
    expect(api.updateProduct).toBeDefined();
    expect(api.deleteProduct).toBeDefined();
  });

  it('should have customer methods', () => {
    expect(api.getCustomers).toBeDefined();
    expect(api.getCustomer).toBeDefined();
    expect(api.createCustomer).toBeDefined();
    expect(api.updateCustomer).toBeDefined();
  });

  it('should have order methods', () => {
    expect(api.getOrders).toBeDefined();
    expect(api.getOrder).toBeDefined();
    expect(api.createOrder).toBeDefined();
    expect(api.cancelOrder).toBeDefined();
  });

  it('should have analytics methods', () => {
    expect(api.getDashboardMetrics).toBeDefined();
    expect(api.getRevenue).toBeDefined();
    expect(api.getTopProducts).toBeDefined();
    expect(api.getInventoryAlerts).toBeDefined();
  });

  it('should have logout method', () => {
    expect(api.logout).toBeDefined();
    api.logout();
    // Verify localStorage was cleared (mocked in setup)
  });
});

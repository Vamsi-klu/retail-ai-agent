/**
 * Tests for authSlice
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { configureStore } from '@reduxjs/toolkit';
import authReducer, { login, logout, clearError } from '@/store/slices/authSlice';
import api from '@/services/api';

// Mock the API
vi.mock('@/services/api', () => ({
  default: {
    login: vi.fn(),
    getCurrentUser: vi.fn(),
    logout: vi.fn(),
  },
}));

describe('authSlice', () => {
  let store: ReturnType<typeof configureStore>;

  beforeEach(() => {
    store = configureStore({
      reducer: {
        auth: authReducer,
      },
    });
    vi.clearAllMocks();
  });

  it('should handle initial state', () => {
    const state = store.getState().auth;
    expect(state.user).toBeNull();
    expect(state.isAuthenticated).toBe(false);
    expect(state.isLoading).toBe(false);
    expect(state.error).toBeNull();
  });

  it('should handle logout', () => {
    store.dispatch(logout());
    const state = store.getState().auth;
    expect(state.user).toBeNull();
    expect(state.isAuthenticated).toBe(false);
    expect(api.logout).toHaveBeenCalled();
  });

  it('should handle clearError', () => {
    store.dispatch(clearError());
    const state = store.getState().auth;
    expect(state.error).toBeNull();
  });

  it('should handle login.pending', () => {
    store.dispatch(login.pending('', { username: 'test', password: 'test' }));
    const state = store.getState().auth;
    expect(state.isLoading).toBe(true);
    expect(state.error).toBeNull();
  });

  it('should handle login.fulfilled', () => {
    const user = {
      id: 1,
      email: 'test@example.com',
      username: 'testuser',
      first_name: 'Test',
      last_name: 'User',
      role: 'staff',
      is_active: true,
    };

    store.dispatch(login.fulfilled(user, '', { username: 'test', password: 'test' }));
    const state = store.getState().auth;
    expect(state.isLoading).toBe(false);
    expect(state.user).toEqual(user);
    expect(state.isAuthenticated).toBe(true);
  });

  it('should handle login.rejected', () => {
    const error = new Error('Login failed');
    store.dispatch(login.rejected(error, '', { username: 'test', password: 'test' }));
    const state = store.getState().auth;
    expect(state.isLoading).toBe(false);
    expect(state.error).toBe('Login failed');
  });
});

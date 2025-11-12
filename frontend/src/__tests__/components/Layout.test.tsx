/**
 * Tests for Layout component
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import Layout from '@/components/layout/Layout';
import authReducer from '@/store/slices/authSlice';

const mockStore = configureStore({
  reducer: {
    auth: authReducer,
  },
  preloadedState: {
    auth: {
      user: {
        id: 1,
        email: 'test@example.com',
        username: 'testuser',
        first_name: 'Test',
        last_name: 'User',
        role: 'staff',
        is_active: true,
      },
      isAuthenticated: true,
      isLoading: false,
      error: null,
    },
  },
});

describe('Layout', () => {
  it('renders layout with sidebar and header', () => {
    render(
      <Provider store={mockStore}>
        <BrowserRouter>
          <Layout>
            <div>Test Content</div>
          </Layout>
        </BrowserRouter>
      </Provider>
    );

    expect(screen.getByText('Retail AI Pro')).toBeInTheDocument();
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Products')).toBeInTheDocument();
    expect(screen.getByText('Customers')).toBeInTheDocument();
    expect(screen.getByText('Orders')).toBeInTheDocument();
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('displays user name in header', () => {
    render(
      <Provider store={mockStore}>
        <BrowserRouter>
          <Layout>
            <div>Test Content</div>
          </Layout>
        </BrowserRouter>
      </Provider>
    );

    expect(screen.getByText(/Test User/)).toBeInTheDocument();
  });
});

/**
 * Customers slice for managing customer state
 */
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import api from '@/services/api';
import type { Customer } from '@/types';

interface CustomersState {
  items: Customer[];
  currentCustomer: Customer | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: CustomersState = {
  items: [],
  currentCustomer: null,
  isLoading: false,
  error: null,
};

export const fetchCustomers = createAsyncThunk(
  'customers/fetchCustomers',
  async (params?: { search?: string; loyalty_tier?: string }) => {
    return await api.getCustomers(params);
  }
);

export const fetchCustomer = createAsyncThunk(
  'customers/fetchCustomer',
  async (id: number) => {
    return await api.getCustomer(id);
  }
);

export const createCustomer = createAsyncThunk(
  'customers/createCustomer',
  async (customer: Partial<Customer>) => {
    return await api.createCustomer(customer);
  }
);

const customersSlice = createSlice({
  name: 'customers',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchCustomers.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchCustomers.fulfilled, (state, action: PayloadAction<Customer[]>) => {
        state.isLoading = false;
        state.items = action.payload;
      })
      .addCase(fetchCustomers.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch customers';
      })
      .addCase(fetchCustomer.fulfilled, (state, action: PayloadAction<Customer>) => {
        state.currentCustomer = action.payload;
      })
      .addCase(createCustomer.fulfilled, (state, action: PayloadAction<Customer>) => {
        state.items.push(action.payload);
      });
  },
});

export default customersSlice.reducer;

/**
 * Orders slice for managing order state
 */
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import api from '@/services/api';
import type { Order } from '@/types';

interface OrdersState {
  items: Order[];
  currentOrder: Order | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: OrdersState = {
  items: [],
  currentOrder: null,
  isLoading: false,
  error: null,
};

export const fetchOrders = createAsyncThunk(
  'orders/fetchOrders',
  async (params?: { customer_id?: number; status?: string }) => {
    return await api.getOrders(params);
  }
);

export const fetchOrder = createAsyncThunk(
  'orders/fetchOrder',
  async (id: number) => {
    return await api.getOrder(id);
  }
);

export const createOrder = createAsyncThunk(
  'orders/createOrder',
  async (order: Partial<Order>) => {
    return await api.createOrder(order);
  }
);

const ordersSlice = createSlice({
  name: 'orders',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchOrders.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchOrders.fulfilled, (state, action: PayloadAction<Order[]>) => {
        state.isLoading = false;
        state.items = action.payload;
      })
      .addCase(fetchOrders.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch orders';
      })
      .addCase(fetchOrder.fulfilled, (state, action: PayloadAction<Order>) => {
        state.currentOrder = action.payload;
      })
      .addCase(createOrder.fulfilled, (state, action: PayloadAction<Order>) => {
        state.items.unshift(action.payload);
      });
  },
});

export default ordersSlice.reducer;

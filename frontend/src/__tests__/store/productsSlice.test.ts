/**
 * Tests for productsSlice
 */
import { describe, it, expect, beforeEach } from 'vitest';
import { configureStore } from '@reduxjs/toolkit';
import productsReducer, {
  fetchProducts,
  createProduct,
  updateProduct,
  deleteProduct,
  clearCurrentProduct,
} from '@/store/slices/productsSlice';
import type { Product } from '@/types';

describe('productsSlice', () => {
  let store: ReturnType<typeof configureStore>;

  beforeEach(() => {
    store = configureStore({
      reducer: {
        products: productsReducer,
      },
    });
  });

  it('should handle initial state', () => {
    const state = store.getState().products;
    expect(state.items).toEqual([]);
    expect(state.currentProduct).toBeNull();
    expect(state.isLoading).toBe(false);
    expect(state.error).toBeNull();
  });

  it('should handle clearCurrentProduct', () => {
    store.dispatch(clearCurrentProduct());
    const state = store.getState().products;
    expect(state.currentProduct).toBeNull();
  });

  it('should handle fetchProducts.pending', () => {
    store.dispatch(fetchProducts.pending('', {}));
    const state = store.getState().products;
    expect(state.isLoading).toBe(true);
  });

  it('should handle fetchProducts.fulfilled', () => {
    const products: Product[] = [
      {
        id: 1,
        sku: 'TEST-001',
        name: 'Test Product',
        cost_price: 50,
        selling_price: 75,
        current_stock: 100,
        reorder_point: 20,
        reorder_quantity: 50,
        is_active: true,
        is_featured: false,
        is_on_sale: false,
        created_at: '2024-01-01',
        updated_at: '2024-01-01',
      },
    ];

    store.dispatch(fetchProducts.fulfilled(products, '', {}));
    const state = store.getState().products;
    expect(state.isLoading).toBe(false);
    expect(state.items).toEqual(products);
  });

  it('should handle fetchProducts.rejected', () => {
    const error = new Error('Failed to fetch');
    store.dispatch(fetchProducts.rejected(error, '', {}));
    const state = store.getState().products;
    expect(state.isLoading).toBe(false);
    expect(state.error).toBe('Failed to fetch');
  });

  it('should handle createProduct.fulfilled', () => {
    const product: Product = {
      id: 2,
      sku: 'TEST-002',
      name: 'New Product',
      cost_price: 30,
      selling_price: 50,
      current_stock: 50,
      reorder_point: 10,
      reorder_quantity: 25,
      is_active: true,
      is_featured: false,
      is_on_sale: false,
      created_at: '2024-01-01',
      updated_at: '2024-01-01',
    };

    store.dispatch(createProduct.fulfilled(product, '', {}));
    const state = store.getState().products;
    expect(state.items).toContainEqual(product);
  });

  it('should handle updateProduct.fulfilled', () => {
    const initialProduct: Product = {
      id: 1,
      sku: 'TEST-001',
      name: 'Test Product',
      cost_price: 50,
      selling_price: 75,
      current_stock: 100,
      reorder_point: 20,
      reorder_quantity: 50,
      is_active: true,
      is_featured: false,
      is_on_sale: false,
      created_at: '2024-01-01',
      updated_at: '2024-01-01',
    };

    // Set initial state
    store.dispatch(fetchProducts.fulfilled([initialProduct], '', {}));

    const updatedProduct = { ...initialProduct, name: 'Updated Product' };
    store.dispatch(updateProduct.fulfilled(updatedProduct, '', { id: 1, product: {} }));

    const state = store.getState().products;
    expect(state.items[0].name).toBe('Updated Product');
  });

  it('should handle deleteProduct.fulfilled', () => {
    const product: Product = {
      id: 1,
      sku: 'TEST-001',
      name: 'Test Product',
      cost_price: 50,
      selling_price: 75,
      current_stock: 100,
      reorder_point: 20,
      reorder_quantity: 50,
      is_active: true,
      is_featured: false,
      is_on_sale: false,
      created_at: '2024-01-01',
      updated_at: '2024-01-01',
    };

    // Set initial state
    store.dispatch(fetchProducts.fulfilled([product], '', {}));

    // Delete product
    store.dispatch(deleteProduct.fulfilled(1, '', 1));

    const state = store.getState().products;
    expect(state.items).toEqual([]);
  });
});

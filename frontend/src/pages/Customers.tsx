/**
 * Customers Page
 */
import { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '@/hooks/redux';
import { fetchCustomers } from '@/store/slices/customersSlice';
import { Users } from 'lucide-react';

export default function Customers() {
  const dispatch = useAppDispatch();
  const { items: customers, isLoading } = useAppSelector((state) => state.customers);

  useEffect(() => {
    dispatch(fetchCustomers());
  }, [dispatch]);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Customers</h1>

      <div className="card">
        {isLoading ? (
          <div className="text-center py-12">Loading customers...</div>
        ) : customers.length === 0 ? (
          <div className="text-center py-12">
            <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">No customers found</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Orders
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Total Spent
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Tier
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {customers.map((customer) => (
                  <tr key={customer.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">
                      {customer.first_name} {customer.last_name}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">{customer.email}</td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {customer.total_orders}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      ${customer.total_purchases.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <span
                        className={`px-2 py-1 rounded-full text-xs ${
                          customer.loyalty_tier === 'Platinum'
                            ? 'bg-purple-100 text-purple-800'
                            : customer.loyalty_tier === 'Gold'
                            ? 'bg-yellow-100 text-yellow-800'
                            : customer.loyalty_tier === 'Silver'
                            ? 'bg-gray-200 text-gray-800'
                            : 'bg-orange-100 text-orange-800'
                        }`}
                      >
                        {customer.loyalty_tier}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

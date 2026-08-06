'use client';

import { 
  ChartBarIcon, 
  UsersIcon, 
  ShoppingCartIcon, 
  CurrencyDollarIcon 
} from '@heroicons/react/24/outline';

const stats = [
  { name: 'Total Revenue', value: '$45,231.89', icon: CurrencyDollarIcon, change: '+20.1%' },
  { name: 'Users', value: '2,651', icon: UsersIcon, change: '+12.5%' },
  { name: 'Orders', value: '384', icon: ShoppingCartIcon, change: '+6.8%' },
  { name: 'Conversion', value: '23.4%', icon: ChartBarIcon, change: '+3.2%' },
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
        <p className="text-sm text-gray-500">Welcome back! Here's what's happening with your project.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <stat.icon className="h-6 w-6 text-gray-400" aria-hidden="true" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">{stat.name}</dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">{stat.value}</div>
                      <span className="ml-2 text-sm font-medium text-green-600">{stat.change}</span>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Content - Example Charts or tables */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
          <ul className="divide-y divide-gray-200">
            {[1, 2, 3, 4].map((item) => (
              <li key={item} className="py-3 flex justify-between">
                <span className="text-sm text-gray-600">User #{item} signed up</span>
                <span className="text-sm text-gray-400">2 min ago</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Top Products</h3>
          <ul className="divide-y divide-gray-200">
            {['Product A', 'Product B', 'Product C', 'Product D'].map((product) => (
              <li key={product} className="py-3 flex justify-between">
                <span className="text-sm text-gray-600">{product}</span>
                <span className="text-sm font-medium text-gray-900">$99.00</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
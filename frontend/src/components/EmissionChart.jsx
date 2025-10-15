import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingDown } from 'lucide-react';

export default function EmissionChart({ optimizedData, directData }) {
  if (!optimizedData) return null;

  const chartData = [
    {
      name: 'Direct Route',
      'CO₂ (kg)': directData?.co2 || optimizedData.estimated_co2_kg * 1.15,
      'Fuel (kg)': directData?.fuel || optimizedData.estimated_fuel_kg * 1.15
    },
    {
      name: 'Optimized Route',
      'CO₂ (kg)': optimizedData.estimated_co2_kg,
      'Fuel (kg)': optimizedData.estimated_fuel_kg
    }
  ];

  const savings = optimizedData.co2_savings_vs_direct || 0;

  return (
    <div className="bg-white rounded-3xl shadow-2xl p-8 border border-gray-100">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-2xl font-bold text-gray-900">Emission Comparison</h3>
        {savings > 0 && (
          <div className="flex items-center space-x-2 bg-green-100 text-green-700 px-4 py-2 rounded-full font-bold">
            <TrendingDown className="w-5 h-5" />
            <span>{savings}% Reduced</span>
          </div>
        )}
      </div>
      
      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="name" 
            tick={{ fill: '#6b7280', fontSize: 14, fontWeight: 600 }}
          />
          <YAxis 
            tick={{ fill: '#6b7280', fontSize: 12 }}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: '#ffffff',
              border: '2px solid #e5e7eb',
              borderRadius: '12px',
              padding: '12px'
            }}
          />
          <Legend 
            wrapperStyle={{
              paddingTop: '20px',
              fontSize: '14px',
              fontWeight: 600
            }}
          />
          <Bar 
            dataKey="CO₂ (kg)" 
            fill="url(#colorCO2)" 
            radius={[8, 8, 0, 0]}
          />
          <Bar 
            dataKey="Fuel (kg)" 
            fill="url(#colorFuel)" 
            radius={[8, 8, 0, 0]}
          />
          <defs>
            <linearGradient id="colorCO2" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#10b981" stopOpacity={1}/>
              <stop offset="100%" stopColor="#059669" stopOpacity={1}/>
            </linearGradient>
            <linearGradient id="colorFuel" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#f59e0b" stopOpacity={1}/>
              <stop offset="100%" stopColor="#d97706" stopOpacity={1}/>
            </linearGradient>
          </defs>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
import React from 'react';

interface WeatherProps {
  city: string;
  temperature: string;
  condition: string;
  humidity: string;
  wind: string;
  description: string;
}

const getWeatherIcon = (condition: string): string => {
  const conditionMap: Record<string, string> = {
    '晴天': '☀️',
    '多云': '⛅',
    '阴天': '☁️',
    '小雨': '🌧️',
    '大雨': '🌧️',
    '雪': '❄️',
    '雾': '🌫️'
  };
  return conditionMap[condition] || '🌤️';
};

const getBackgroundGradient = (condition: string): string => {
  const gradientMap: Record<string, string> = {
    '晴天': 'from-yellow-400 to-orange-500',
    '多云': 'from-gray-400 to-gray-600',
    '阴天': 'from-gray-500 to-gray-700',
    '小雨': 'from-blue-400 to-blue-600',
    '大雨': 'from-blue-600 to-blue-800',
    '雪': 'from-blue-200 to-white',
    '雾': 'from-gray-300 to-gray-500'
  };
  return gradientMap[condition] || 'from-blue-400 to-blue-600';
};

const WeatherComponent: React.FC<WeatherProps> = ({
  city,
  temperature,
  condition,
  humidity,
  wind,
  description
}) => {
  const weatherIcon = getWeatherIcon(condition);
  const gradientClass = getBackgroundGradient(condition);

  return (
    <div className={`max-w-sm mx-auto bg-gradient-to-br ${gradientClass} rounded-xl shadow-lg overflow-hidden text-white transition-transform hover:scale-105 duration-300`}>
      {/* Header */}
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">{city}</h2>
            <p className="text-sm opacity-90">{condition}</p>
          </div>
          <div className="text-5xl">
            {weatherIcon}
          </div>
        </div>
      </div>

      {/* Temperature */}
      <div className="px-6 py-2">
        <div className="text-6xl font-light text-center">
          {temperature}
        </div>
      </div>

      {/* Weather Details */}
      <div className="px-6 py-4 bg-black bg-opacity-20">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="flex items-center space-x-2">
            <span className="opacity-75">💧</span>
            <span>湿度: {humidity}</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="opacity-75">💨</span>
            <span>风速: {wind}</span>
          </div>
        </div>
      </div>

      {/* Description */}
      <div className="px-6 py-4 bg-black bg-opacity-10">
        <p className="text-sm leading-relaxed opacity-90">
          {description}
        </p>
      </div>
    </div>
  );
};

export default {
  weather: WeatherComponent,
};
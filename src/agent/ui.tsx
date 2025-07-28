import React, { useState, useEffect } from 'react';

// Mock weather data for different cities
const mockWeatherData = {
  '北京': {
    temperature: '22°C',
    condition: '晴天',
    humidity: '45%',
    windSpeed: '3km/h',
    icon: '☀️',
    gradient: 'linear-gradient(135deg, #fdcb6e 0%, #e17055 100%)',
    description: '今天北京天气晴朗，温度适宜，适合外出活动。'
  },
  '上海': {
    temperature: '18°C', 
    condition: '多云',
    humidity: '68%',
    windSpeed: '5km/h',
    icon: '⛅',
    gradient: 'linear-gradient(135deg, #74b9ff 0%, #0984e3 100%)',
    description: '上海今天多云转阴，温度稍凉，建议增添衣物。'
  },
  '深圳': {
    temperature: '26°C',
    condition: '小雨',
    humidity: '78%',
    windSpeed: '7km/h', 
    icon: '🌧️',
    gradient: 'linear-gradient(135deg, #636e72 0%, #2d3436 100%)',
    description: '深圳今天有小雨，湿度较高，出门记得带伞。'
  },
  '广州': {
    temperature: '24°C',
    condition: '阴天',
    humidity: '72%',
    windSpeed: '4km/h',
    icon: '☁️',
    gradient: 'linear-gradient(135deg, #636e72 0%, #2d3436 100%)',
    description: '广州今天阴天，温度舒适，适合室内活动。'
  },
  '杭州': {
    temperature: '20°C',
    condition: '晴天',
    humidity: '55%',
    windSpeed: '6km/h',
    icon: '☀️',
    gradient: 'linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%)',
    description: '杭州今天晴空万里，温度宜人，是游览的好天气。'
  }
};

const WeatherComponent = (props: { city: string }) => {
  const [isVisible, setIsVisible] = useState(false);
  const [weatherData, setWeatherData] = useState(mockWeatherData['北京']);

  useEffect(() => {
    console.log('🎯 WeatherComponent 正在渲染!', { city: props.city });
    
    // Trigger animation on mount
    setIsVisible(true);
    
    // Get weather data for the specified city
    const cityData = mockWeatherData[props.city as keyof typeof mockWeatherData];
    if (cityData) {
      setWeatherData(cityData);
    }
  }, [props.city]);

  return (
    <div className="weather-container">
      <div 
        className={`weather-card ${isVisible ? 'visible' : ''}`}
        style={{ background: weatherData.gradient }}
      >
        {/* Header */}
        <div className="weather-header">
          <h2 className="city-name">{props.city}</h2>
          <div className="weather-icon">{weatherData.icon}</div>
        </div>

        {/* Main Temperature */}
        <div className="temperature-section">
          <div className="temperature">{weatherData.temperature}</div>
          <div className="condition">{weatherData.condition}</div>
          <div className="description">{weatherData.description}</div>
        </div>

        {/* Weather Details */}
        <div className="weather-details">
          <div className="detail-item">
            <div className="detail-icon">💧</div>
            <div className="detail-info">
              <span className="detail-label">湿度</span>
              <span className="detail-value">{weatherData.humidity}</span>
            </div>
          </div>
          
          <div className="detail-item">
            <div className="detail-icon">💨</div>
            <div className="detail-info">
              <span className="detail-label">风速</span>
              <span className="detail-value">{weatherData.windSpeed}</span>
            </div>
          </div>
        </div>

        {/* Animated Background Elements */}
        <div className="bg-animation">
          <div className="cloud cloud-1">☁️</div>
          <div className="cloud cloud-2">☁️</div>
          <div className="sparkle sparkle-1">✨</div>
          <div className="sparkle sparkle-2">✨</div>
          <div className="sparkle sparkle-3">✨</div>
        </div>
      </div>

      <style jsx>{`
        .weather-container {
          display: flex;
          justify-content: center;
          padding: 20px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .weather-card {
          position: relative;
          width: 350px;
          height: 450px;
          border-radius: 25px;
          padding: 30px;
          color: white;
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
          overflow: hidden;
          transform: translateY(50px);
          opacity: 0;
          transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
          backdrop-filter: blur(10px);
        }

        .weather-card.visible {
          transform: translateY(0);
          opacity: 1;
        }

        .weather-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 25px;
          backdrop-filter: blur(10px);
        }

        .weather-header {
          position: relative;
          z-index: 2;
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 40px;
        }

        .city-name {
          font-size: 28px;
          font-weight: 300;
          margin: 0;
          letter-spacing: 1px;
          animation: slideInLeft 0.8s ease-out 0.3s both;
        }

        .weather-icon {
          font-size: 60px;
          animation: bounce 2s infinite, slideInRight 0.8s ease-out 0.3s both;
        }

        .temperature-section {
          position: relative;
          z-index: 2;
          text-align: center;
          margin: 60px 0;
        }

        .temperature {
          font-size: 72px;
          font-weight: 100;
          margin: 0;
          line-height: 1;
          animation: scaleIn 1s ease-out 0.6s both;
          text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }

        .condition {
          font-size: 22px;
          font-weight: 300;
          margin: 10px 0 5px 0;
          opacity: 0.9;
          animation: fadeInUp 0.8s ease-out 0.9s both;
        }

        .description {
          font-size: 16px;
          opacity: 0.8;
          font-weight: 300;
          animation: fadeInUp 0.8s ease-out 1.1s both;
        }

        .weather-details {
          position: relative;
          z-index: 2;
          display: flex;
          justify-content: space-around;
          margin-top: 50px;
        }

        .detail-item {
          display: flex;
          align-items: center;
          gap: 12px;
          animation: fadeInUp 0.8s ease-out 1.3s both;
        }

        .detail-icon {
          font-size: 24px;
          animation: pulse 2s infinite;
        }

        .detail-info {
          display: flex;
          flex-direction: column;
        }

        .detail-label {
          font-size: 14px;
          opacity: 0.8;
          font-weight: 300;
        }

        .detail-value {
          font-size: 18px;
          font-weight: 500;
        }

        /* Background Animations */
        .bg-animation {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          pointer-events: none;
          overflow: hidden;
        }

        .cloud {
          position: absolute;
          font-size: 30px;
          opacity: 0.3;
          animation: float 6s ease-in-out infinite;
        }

        .cloud-1 {
          top: 15%;
          left: 10%;
          animation-delay: 0s;
        }

        .cloud-2 {
          top: 25%;
          right: 15%;
          animation-delay: 3s;
        }

        .sparkle {
          position: absolute;
          font-size: 16px;
          opacity: 0.6;
          animation: twinkle 3s ease-in-out infinite;
        }

        .sparkle-1 {
          top: 30%;
          left: 20%;
          animation-delay: 0s;
        }

        .sparkle-2 {
          top: 60%;
          right: 25%;
          animation-delay: 1s;
        }

        .sparkle-3 {
          bottom: 25%;
          left: 15%;
          animation-delay: 2s;
        }

        /* Keyframe Animations */
        @keyframes slideInLeft {
          from {
            transform: translateX(-50px);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }

        @keyframes slideInRight {
          from {
            transform: translateX(50px);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }

        @keyframes scaleIn {
          from {
            transform: scale(0.5);
            opacity: 0;
          }
          to {
            transform: scale(1);
            opacity: 1;
          }
        }

        @keyframes fadeInUp {
          from {
            transform: translateY(30px);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }

        @keyframes bounce {
          0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
          }
          40% {
            transform: translateY(-10px);
          }
          60% {
            transform: translateY(-5px);
          }
        }

        @keyframes float {
          0%, 100% {
            transform: translateY(0px);
          }
          50% {
            transform: translateY(-20px);
          }
        }

        @keyframes twinkle {
          0%, 100% {
            opacity: 0.6;
            transform: scale(1);
          }
          50% {
            opacity: 1;
            transform: scale(1.2);
          }
        }

        @keyframes pulse {
          0%, 100% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.1);
          }
        }

        /* Responsive Design */
        @media (max-width: 480px) {
          .weather-card {
            width: 300px;
            height: 400px;
            padding: 25px;
          }

          .temperature {
            font-size: 60px;
          }

          .city-name {
            font-size: 24px;
          }

          .weather-icon {
            font-size: 50px;
          }
        }
      `}</style>
    </div>
  );
};

export default {
  weather: WeatherComponent,
};
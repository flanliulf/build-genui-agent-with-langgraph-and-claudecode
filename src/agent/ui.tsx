import React, { useState, useEffect } from 'react';

// Weather component props interface - matches backend WeatherOutput
interface WeatherProps {
  city: string;
  temperature: string;
  condition: string;
  humidity: string;
  windSpeed: string;
  description: string;
}

// Visual mapping functions - keep presentation logic in frontend
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
    '晴天': 'linear-gradient(135deg, #fdcb6e 0%, #e17055 100%)',
    '多云': 'linear-gradient(135deg, #74b9ff 0%, #0984e3 100%)',
    '阴天': 'linear-gradient(135deg, #636e72 0%, #2d3436 100%)',
    '小雨': 'linear-gradient(135deg, #636e72 0%, #2d3436 100%)',
    '大雨': 'linear-gradient(135deg, #2d3436 0%, #000000 100%)',
    '雪': 'linear-gradient(135deg, #74b9ff 0%, #ffffff 100%)',
    '雾': 'linear-gradient(135deg, #ddd6fe 0%, #8b5cf6 100%)'
  };
  return gradientMap[condition] || 'linear-gradient(135deg, #74b9ff 0%, #0984e3 100%)';
};

const WeatherComponent = (props: WeatherProps) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    console.log('🎯 WeatherComponent 正在渲染!', props);
    
    // Trigger animation on mount
    setIsVisible(true);
  }, [props]);

  // Use props data directly instead of mock data
  const weatherData = {
    temperature: props.temperature,
    condition: props.condition,
    humidity: props.humidity,
    windSpeed: props.windSpeed,
    description: props.description,
    icon: getWeatherIcon(props.condition),
    gradient: getBackgroundGradient(props.condition)
  };

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
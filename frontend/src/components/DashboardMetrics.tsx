import React, { useEffect, useState } from 'react';
import { Card, Typography, Space, Spin } from 'antd';
import axios from 'axios';

const { Title, Text } = Typography;

interface Summary {
  total_models: number;
  algorithms: Record<string, number>;
  functions: Record<string, number>;
  languages: Record<string, number>;
  model_types: Record<string, number>;
  tools: Record<string, number>;
}

const DashboardMetrics: React.FC = () => {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await axios.get('http://localhost:8000/models/summary/dashboard');
        setSummary(response.data);
      } catch (error) {
        console.error('Error fetching summary:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSummary();
  }, []);

  if (loading) {
    return <Spin size="large" />;
  }

  if (!summary) {
    return <Text>No hay datos disponibles</Text>;
  }

  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Title level={2}>Resumen de Modelos</Title>
      
      <Space wrap>
        <Card title="Total de Modelos" style={{ width: 300 }}>
          <Title level={2}>{summary.total_models}</Title>
        </Card>
        
        <Card title="Algoritmos Más Usados" style={{ width: 300 }}>
          {Object.entries(summary.algorithms || {}).map(([key, value]) => (
            <div key={key}>
              <Text>{key}: {value}</Text>
            </div>
          ))}
        </Card>
        
        <Card title="Lenguajes de Programación" style={{ width: 300 }}>
          {Object.entries(summary.languages || {}).map(([key, value]) => (
            <div key={key}>
              <Text>{key}: {value}</Text>
            </div>
          ))}
        </Card>
      </Space>
      
      <Space wrap>
        <Card title="Tipos de Modelos" style={{ width: 300 }}>
          {Object.entries(summary.model_types || {}).map(([key, value]) => (
            <div key={key}>
              <Text>{key}: {value}</Text>
            </div>
          ))}
        </Card>
        
        <Card title="Funciones" style={{ width: 300 }}>
          {Object.entries(summary.functions || {}).map(([key, value]) => (
            <div key={key}>
              <Text>{key}: {value}</Text>
            </div>
          ))}
        </Card>
        
        <Card title="Herramientas" style={{ width: 300 }}>
          {Object.entries(summary.tools || {}).map(([key, value]) => (
            <div key={key}>
              <Text>{key}: {value}</Text>
            </div>
          ))}
        </Card>
      </Space>
    </Space>
  );
};

export default DashboardMetrics;
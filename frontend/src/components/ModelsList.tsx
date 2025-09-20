import React, { useEffect, useState } from 'react';
import { Table, Tag, Space, Button, message } from 'antd';
import axios from 'axios';

interface Model {
  id: string;
  name: string;
  algorithm: string;
  function: string;
  modelVersionName: string;
  createdBy: string;
  modifiedTimeStamp: string;
}

const ModelsList: React.FC = () => {
  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchModels = async () => {
    try {
      const response = await axios.get('http://localhost:8000/models');
      setModels(response.data);
    } catch (error) {
      message.error('Error al cargar los modelos');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchModels();
  }, []);

  const columns = [
    {
      title: 'Nombre',
      dataIndex: 'name',
      key: 'name',
      sorter: (a: Model, b: Model) => a.name.localeCompare(b.name),
    },
    {
      title: 'Algoritmo',
      dataIndex: 'algorithm',
      key: 'algorithm',
      filters: [...new Set(models.map(m => m.algorithm))].map(alg => ({
        text: alg,
        value: alg,
      })),
      onFilter: (value: string, record: Model) => record.algorithm === value,
    },
    {
      title: 'Función',
      dataIndex: 'function',
      key: 'function',
      render: (text: string) => (
        <Tag color={
          text === 'classification' ? 'blue' :
          text === 'regression' ? 'green' :
          text === 'clustering' ? 'orange' :
          'purple'
        }>
          {text}
        </Tag>
      ),
    },
    {
      title: 'Versión',
      dataIndex: 'modelVersionName',
      key: 'modelVersionName',
    },
    {
      title: 'Creado por',
      dataIndex: 'createdBy',
      key: 'createdBy',
    },
    {
      title: 'Última modificación',
      dataIndex: 'modifiedTimeStamp',
      key: 'modifiedTimeStamp',
      render: (text: string) => new Date(text).toLocaleDateString(),
      sorter: (a: Model, b: Model) => new Date(a.modifiedTimeStamp).getTime() - new Date(b.modifiedTimeStamp).getTime(),
    },
    {
      title: 'Acciones',
      key: 'actions',
      render: (_: any, record: Model) => (
        <Space>
          <Button type="primary" onClick={() => message.info('Función de edición en desarrollo')}>
            Editar
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <Table
      columns={columns}
      dataSource={models}
      rowKey="id"
      loading={loading}
      pagination={{ pageSize: 10 }}
    />
  );
};

export default ModelsList;
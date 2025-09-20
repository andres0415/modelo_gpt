import React, { useState } from 'react';
import { Form, Input, Select, Upload, Button, message, Divider } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import axios from 'axios';

const { TextArea } = Input;

const ModelRegistrationForm: React.FC = () => {
  const [form] = Form.useForm();
  const [fileList, setFileList] = useState<any[]>([]);
  const [isJsonMode, setIsJsonMode] = useState(false);

  const onFinish = async (values: any) => {
    try {
      if (fileList.length > 0) {
        const formData = new FormData();
        formData.append('file', fileList[0]);
        await axios.post('http://localhost:8000/models/from-json-file', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        message.success('Modelo registrado exitosamente desde JSON');
      } else {
        const modelData = {
          ...values,
          creationTimeStamp: new Date().toISOString(),
          createdBy: values.modeler || 'anonymous',
          modifiedTimeStamp: new Date().toISOString(),
          modifiedBy: values.modeler || 'anonymous',
          id: '', // Se generará en el backend
          scoreCodeType: values.modelType,
          trainCodeType: values.modelType,
          tool: `${values.modelType.charAt(0).toUpperCase()}${values.modelType.slice(1)}`,
          toolVersion: '3.9',
          modelVersionName: '1.0',
          custom_properties: []
        };
        await axios.post('http://localhost:8000/models', modelData);
        message.success('Modelo registrado exitosamente desde formulario');
      }
      form.resetFields();
      setFileList([]);
      setIsJsonMode(false);
    } catch (error: any) {
      message.error(`Error al registrar el modelo: ${error.response?.data?.detail || error.message}`);
      console.error(error);
    }
  };

  const beforeUpload = (file: File) => {
    const isJSON = file.type === 'application/json' || file.name.endsWith('.json');
    if (!isJSON) {
      message.error('Solo se permiten archivos JSON!');
      return false;
    }
    setFileList([file]);
    setIsJsonMode(true);
    return false;
  };

  const onRemoveFile = () => {
    setFileList([]);
    setIsJsonMode(false);
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={onFinish}
      style={{ maxWidth: 800 }}
    >
      <Upload.Dragger
        beforeUpload={beforeUpload}
        fileList={fileList}
        onRemove={onRemoveFile}
        accept=".json"
        multiple={false}
      >
        <p className="ant-upload-drag-icon">
          <UploadOutlined />
        </p>
        <p className="ant-upload-text">Haz clic o arrastra un archivo JSON aquí</p>
        <p className="ant-upload-hint">
          El archivo JSON debe contener toda la información del modelo
        </p>
      </Upload.Dragger>

      {!isJsonMode && (
        <>
          <Divider>O registra manualmente</Divider>

          <Form.Item
            label="Nombre del Modelo"
            name="name"
            rules={[{ required: true, message: 'Por favor ingrese el nombre del modelo' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Descripción"
            name="description"
            rules={[{ required: true, message: 'Por favor ingrese una descripción' }]}
          >
            <TextArea rows={4} />
          </Form.Item>

          <Form.Item
            label="Algoritmo"
            name="algorithm"
            rules={[{ required: true, message: 'Por favor seleccione un algoritmo' }]}
          >
            <Select>
              <Select.Option value="XGBoost">XGBoost</Select.Option>
              <Select.Option value="RandomForest">Random Forest</Select.Option>
              <Select.Option value="Neural Network">Neural Network</Select.Option>
              <Select.Option value="LLM">LLM</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="Función"
            name="function"
            rules={[{ required: true, message: 'Por favor seleccione una función' }]}
          >
            <Select>
              <Select.Option value="classification">Clasificación</Select.Option>
              <Select.Option value="regression">Regresión</Select.Option>
              <Select.Option value="clustering">Clustering</Select.Option>
              <Select.Option value="generative">Generativo</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="Tipo de Modelo"
            name="modelType"
            rules={[{ required: true, message: 'Por favor seleccione el tipo de modelo' }]}
          >
            <Select>
              <Select.Option value="python">Python</Select.Option>
              <Select.Option value="r">R</Select.Option>
              <Select.Option value="java">Java</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="Nivel del Target"
            name="targetLevel"
            rules={[{ required: true, message: 'Por favor seleccione el nivel del target' }]}
          >
            <Select>
              <Select.Option value="nominal">Nominal</Select.Option>
              <Select.Option value="ordinal">Ordinal</Select.Option>
              <Select.Option value="interval">Interval</Select.Option>
              <Select.Option value="ratio">Ratio</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="Modelador"
            name="modeler"
            rules={[{ required: true, message: 'Por favor ingrese el nombre del modelador' }]}
          >
            <Input />
          </Form.Item>
        </>
      )}

      <Form.Item>
        <Button type="primary" htmlType="submit">
          {isJsonMode ? 'Registrar desde JSON' : 'Registrar Modelo'}
        </Button>
      </Form.Item>
    </Form>
  );
};

export default ModelRegistrationForm;

import { useState } from 'react';
import { Layout, Menu } from 'antd';
import { DashboardOutlined, FormOutlined, UnorderedListOutlined } from '@ant-design/icons';
import ModelRegistrationForm from './components/ModelRegistrationForm';
import ModelsList from './components/ModelsList';
import DashboardMetrics from './components/DashboardMetrics';

const { Header, Content, Footer } = Layout;

function App() {
  const [activeComponent, setActiveComponent] = useState('dashboard');

  const renderComponent = () => {
    switch (activeComponent) {
      case 'register':
        return <ModelRegistrationForm />;
      case 'list':
        return <ModelsList />;
      default:
        return <DashboardMetrics />;
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header>
        <div style={{ float: 'left', color: 'white', marginRight: '24px' }}>
          ML Models Registry
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['dashboard']}
          onSelect={({ key }) => setActiveComponent(key as string)}
          items={[
            {
              key: 'dashboard',
              icon: <DashboardOutlined />,
              label: 'Dashboard',
            },
            {
              key: 'register',
              icon: <FormOutlined />,
              label: 'Registrar Modelo',
            },
            {
              key: 'list',
              icon: <UnorderedListOutlined />,
              label: 'Lista de Modelos',
            },
          ]}
        />
      </Header>
      <Content style={{ padding: '24px', background: '#fff' }}>
        {renderComponent()}
      </Content>
      <Footer style={{ textAlign: 'center' }}>
        ML Models Registry ©2025
      </Footer>
    </Layout>
  );
}

export default App;

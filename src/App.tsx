import { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DonorDashboard from './pages/DonorDashboard';
import RecipientDashboard from './pages/RecipientDashboard';
import NGODashboard from './pages/NGODashboard';

function AppContent() {
  const [currentPage, setCurrentPage] = useState('home');
  const { user, isAuthenticated } = useAuth();

  const navigate = (page: string) => {
    setCurrentPage(page);
  };

  if (isAuthenticated && user) {
    if (user.role === 'donor' && currentPage !== 'home' && currentPage !== 'login' && currentPage !== 'register') {
      return <DonorDashboard onNavigate={navigate} />;
    }
    if (user.role === 'recipient' && currentPage !== 'home' && currentPage !== 'login' && currentPage !== 'register') {
      return <RecipientDashboard onNavigate={navigate} />;
    }
    if (user.role === 'ngo_admin' && currentPage !== 'home' && currentPage !== 'login' && currentPage !== 'register') {
      return <NGODashboard onNavigate={navigate} />;
    }
  }

  switch (currentPage) {
    case 'login':
      return <LoginPage onNavigate={navigate} />;
    case 'register':
      return <RegisterPage onNavigate={navigate} />;
    case 'donor-dashboard':
      return isAuthenticated && user?.role === 'donor' ? (
        <DonorDashboard onNavigate={navigate} />
      ) : (
        <LoginPage onNavigate={navigate} />
      );
    case 'recipient-dashboard':
      return isAuthenticated && user?.role === 'recipient' ? (
        <RecipientDashboard onNavigate={navigate} />
      ) : (
        <LoginPage onNavigate={navigate} />
      );
    case 'ngo-dashboard':
      return isAuthenticated && user?.role === 'ngo_admin' ? (
        <NGODashboard onNavigate={navigate} />
      ) : (
        <LoginPage onNavigate={navigate} />
      );
    default:
      return <HomePage onNavigate={navigate} />;
  }
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;


import React, { createContext, useContext, useState, useEffect } from 'react';
import apiService from '@/lib/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem('authToken');
      
      if (token) {
        try {
          // Verify token with backend and get current user
          const response = await apiService.getCurrentUser();
          if (response.data) {
            setUser(response.data);
          }
        } catch (error) {
          console.error('Token validation failed:', error);
          // Clear invalid token
          localStorage.removeItem('authToken');
          localStorage.removeItem('userData');
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (username, password) => {
    try {
      const response = await apiService.login(username, password);
      
      if (response.data && response.data.access_token) {
        const { access_token, user: userData } = response.data;
        
        // Store token and user data
        localStorage.setItem('authToken', access_token);
        localStorage.setItem('userData', JSON.stringify(userData));
        setUser(userData);
        
        return { success: true, user: userData };
      }
      
      return { success: false, error: response.message || 'Login failed' };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: error.message || 'Login failed' };
    }
  };

  const register = async (userData) => {
    try {
      const response = await apiService.register(userData);
      
      if (response.data && response.data.access_token) {
        const { access_token, user } = response.data;
        
        // Store token and user data
        localStorage.setItem('authToken', access_token);
        localStorage.setItem('userData', JSON.stringify(user));
        setUser(user);
        
        return { success: true, user };
      }
      
      return { success: false, error: response.message || 'Registration failed' };
    } catch (error) {
      console.error('Registration error:', error);
      return { success: false, error: error.message || 'Registration failed' };
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    setUser(null);
  };

  const refreshToken = async () => {
    try {
      const response = await apiService.refreshToken();
      if (response.data && response.data.access_token) {
        localStorage.setItem('authToken', response.data.access_token);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Token refresh failed:', error);
      logout();
      return false;
    }
  };

  const updateUser = (updatedUserData) => {
    const newUserData = { ...user, ...updatedUserData };
    setUser(newUserData);
    localStorage.setItem('userData', JSON.stringify(newUserData));
  };

  const value = {
    user,
    login,
    register,
    logout,
    refreshToken,
    updateUser,
    loading,
    isAdmin: user?.role === 'admin',
    isAgent: user?.role === 'agent',
    isClient: user?.role === 'client',
    canManageProperties: user?.role === 'admin' || user?.role === 'agent',
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

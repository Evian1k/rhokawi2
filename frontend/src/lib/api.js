/**
 * API Service Layer for Rhokawi Properties
 * Connects React frontend to Flask backend API
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Helper method to get auth headers
  getAuthHeaders() {
    const token = localStorage.getItem('authToken');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  // Helper method to handle API responses
  async handleResponse(response) {
    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'Network error' }));
      throw new Error(error.message || `HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  // Generic fetch method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getAuthHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      return await this.handleResponse(response);
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // Auth methods
  async login(username, password) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  async addAdmin(adminData) {
    return this.request('/auth/add-admin', {
      method: 'POST',
      body: JSON.stringify(adminData),
    });
  }

  async getAdmins() {
    return this.request('/auth/admins');
  }

  async deleteAdmin(adminId) {
    return this.request(`/auth/admins/${adminId}`, {
      method: 'DELETE',
    });
  }

  async refreshToken() {
    return this.request('/auth/refresh', {
      method: 'POST',
    });
  }

  async getCurrentUser() {
    return this.request('/auth/me');
  }

  // Property methods
  async getProperties(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/properties${queryString ? `?${queryString}` : ''}`);
  }

  async searchProperties(searchParams) {
    const queryString = new URLSearchParams(searchParams).toString();
    return this.request(`/properties/search?${queryString}`);
  }

  async getProperty(id) {
    return this.request(`/properties/${id}`);
  }

  async createProperty(propertyData) {
    return this.request('/properties', {
      method: 'POST',
      body: JSON.stringify(propertyData),
    });
  }

  async updateProperty(id, propertyData) {
    return this.request(`/properties/${id}`, {
      method: 'PUT',
      body: JSON.stringify(propertyData),
    });
  }

  async deleteProperty(id) {
    return this.request(`/properties/${id}`, {
      method: 'DELETE',
    });
  }

  async verifyProperty(id, isVerified, notes = '') {
    return this.request(`/properties/${id}/verify`, {
      method: 'PUT',
      body: JSON.stringify({ is_verified: isVerified, verification_notes: notes }),
    });
  }

  async addPropertyImages(propertyId, imageUrls) {
    return this.request(`/properties/${propertyId}/images`, {
      method: 'POST',
      body: JSON.stringify({ image_urls: imageUrls }),
    });
  }

  // Contact methods
  async sendContactMessage(messageData) {
    return this.request('/contact', {
      method: 'POST',
      body: JSON.stringify(messageData),
    });
  }

  async getContactMessages(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/contact${queryString ? `?${queryString}` : ''}`);
  }

  async getContactMessage(id) {
    return this.request(`/contact/${id}`);
  }

  async updateMessageStatus(id, status) {
    return this.request(`/contact/${id}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    });
  }

  async deleteContactMessage(id) {
    return this.request(`/contact/${id}`, {
      method: 'DELETE',
    });
  }

  // File upload methods
  async uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    const token = localStorage.getItem('authToken');
    const headers = {};
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(`${this.baseURL}/upload`, {
        method: 'POST',
        headers,
        body: formData,
      });

      return await this.handleResponse(response);
    } catch (error) {
      console.error('File upload failed:', error);
      throw error;
    }
  }

  async uploadMultipleFiles(files) {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    const token = localStorage.getItem('authToken');
    const headers = {};
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(`${this.baseURL}/upload/multiple`, {
        method: 'POST',
        headers,
        body: formData,
      });

      return await this.handleResponse(response);
    } catch (error) {
      console.error('Multiple file upload failed:', error);
      throw error;
    }
  }

  async deleteFile(fileData) {
    return this.request('/upload/delete', {
      method: 'POST',
      body: JSON.stringify(fileData),
    });
  }

  // Health check
  async healthCheck() {
    return this.request('/');
  }

  // API info
  async getApiInfo() {
    return this.request('');
  }
}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService;

// Export named functions for easier imports
export const {
  login,
  addAdmin,
  getAdmins,
  deleteAdmin,
  refreshToken,
  getCurrentUser,
  getProperties,
  searchProperties,
  getProperty,
  createProperty,
  updateProperty,
  deleteProperty,
  verifyProperty,
  addPropertyImages,
  sendContactMessage,
  getContactMessages,
  getContactMessage,
  updateMessageStatus,
  deleteContactMessage,
  uploadFile,
  uploadMultipleFiles,
  deleteFile,
  healthCheck,
  getApiInfo,
} = apiService;
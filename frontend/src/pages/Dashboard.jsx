import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { Plus, Home, Star, TrendingUp, Eye, Users, CheckCircle, XCircle, UserPlus, Settings, MessageSquare, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useAuth } from '@/contexts/AuthContext';
import PropertyForm from '@/components/dashboard/PropertyForm';
import PropertyList from '@/components/dashboard/PropertyList';
import ConfirmationDialog from '@/components/ConfirmationDialog';
import { useToast } from '@/components/ui/use-toast';
import apiService from '@/lib/api';

const Dashboard = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [properties, setProperties] = useState([]);
  const [admins, setAdmins] = useState([]);
  const [contacts, setContacts] = useState([]);
  const [contactsPage, setContactsPage] = useState(1);
  const [contactsTotalPages, setContactsTotalPages] = useState(1);
  const [unreadCount, setUnreadCount] = useState(0);
  const [showForm, setShowForm] = useState(false);
  const [showAdminForm, setShowAdminForm] = useState(false);
  const [editingProperty, setEditingProperty] = useState(null);
  const [deletingProperty, setDeletingProperty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('properties');
  const [adminForm, setAdminForm] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: ''
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  // Auto-refresh contact messages every 30 seconds when on contacts tab
  useEffect(() => {
    let interval;
    if (activeTab === 'contacts') {
      interval = setInterval(() => {
        loadContacts(contactsPage);
      }, 30000); // 30 seconds
    }
    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [activeTab, contactsPage]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      await Promise.all([
        loadProperties(),
        loadAdmins(),
        loadContacts()
      ]);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      toast({
        title: "Error loading dashboard",
        description: error.message,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const loadProperties = async () => {
    try {
      const response = await apiService.getProperties({ show_all: true });
      if (response.data) {
        setProperties(response.data.properties || []);
      }
    } catch (error) {
      console.error('Failed to load properties:', error);
    }
  };

  const loadAdmins = async () => {
    try {
      if (user?.is_main_admin) {
        const response = await apiService.getAdmins();
        if (response.data) {
          setAdmins(response.data || []);
        }
      }
    } catch (error) {
      console.error('Failed to load admins:', error);
    }
  };

  const loadContacts = async (page = 1) => {
    try {
      const response = await apiService.getContactMessages({ page, per_page: 10 });
      if (response.data) {
        const messages = response.data.messages || [];
        setContacts(messages);
        setContactsTotalPages(response.data.pagination?.pages || 1);
        setContactsPage(page);
        // Count unread messages
        const unread = messages.filter(msg => msg.status === 'unread').length;
        setUnreadCount(unread);
      }
    } catch (error) {
      console.error('Failed to load contacts:', error);
      toast({
        title: "Error loading messages",
        description: "Failed to load contact messages",
        variant: "destructive",
      });
    }
  };

  const handleUpdateContactStatus = async (contactId, status) => {
    try {
      await apiService.updateMessageStatus(contactId, status);
      // Reload contacts to reflect the status change
      await loadContacts();
      toast({
        title: "Status updated",
        description: `Contact message marked as ${status}.`,
      });
    } catch (error) {
      toast({
        title: "Error updating status",
        description: error.message,
        variant: "destructive",
      });
    }
  };

  const handleAddProperty = () => {
    setEditingProperty(null);
    setShowForm(true);
  };

  const handleEditProperty = (property) => {
    setEditingProperty(property);
    setShowForm(true);
  };

  const handleDeleteProperty = (property) => {
    setDeletingProperty(property);
  };

  const confirmDeleteProperty = async () => {
    try {
      await apiService.deleteProperty(deletingProperty.id);
      await loadProperties(); // Reload properties
      setDeletingProperty(null);
      toast({
        title: "Property deleted",
        description: "Property has been successfully deleted.",
      });
    } catch (error) {
      toast({
        title: "Error deleting property",
        description: error.message,
        variant: "destructive",
      });
    }
  };

  const handlePropertySubmit = async (propertyData) => {
    try {
      if (editingProperty) {
        await apiService.updateProperty(editingProperty.id, propertyData);
        toast({
          title: "Property updated",
          description: "Property has been successfully updated.",
        });
      } else {
        await apiService.createProperty(propertyData);
        toast({
          title: "Property created",
          description: "Property has been successfully created. Don't forget to verify it to make it public!",
        });
      }
      
      await loadProperties(); // Reload properties
      setShowForm(false);
      setEditingProperty(null);
    } catch (error) {
      toast({
        title: "Error saving property",
        description: error.message,
        variant: "destructive",
      });
    }
  };

  const handleVerifyProperty = async (propertyId, isVerified) => {
    try {
      await apiService.verifyProperty(propertyId, isVerified, isVerified ? 'Property verified for public display' : 'Property unverified');
      await loadProperties(); // Reload properties
      toast({
        title: isVerified ? "Property verified" : "Property unverified",
        description: isVerified ? "Property is now visible to public" : "Property is now hidden from public",
      });
    } catch (error) {
      toast({
        title: "Error updating property verification",
        description: error.message,
        variant: "destructive",
      });
    }
  };

  const handleAddAdmin = async (e) => {
    e.preventDefault();
    try {
      await apiService.addAdmin(adminForm);
      await loadAdmins(); // Reload admins
      setShowAdminForm(false);
      setAdminForm({
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: ''
      });
      toast({
        title: "Admin added",
        description: "New admin has been successfully added.",
      });
    } catch (error) {
      toast({
        title: "Error adding admin",
        description: error.message,
        variant: "destructive",
      });
    }
  };

  const handleDeleteAdmin = async (adminId) => {
    try {
      await apiService.deleteAdmin(adminId);
      await loadAdmins(); // Reload admins
      toast({
        title: "Admin deleted",
        description: "Admin has been successfully removed.",
      });
    } catch (error) {
      toast({
        title: "Error deleting admin",
        description: error.message,
        variant: "destructive",
      });
    }
  };

  const stats = {
    total: properties.length,
    verified: properties.filter(p => p.is_verified).length,
    unverified: properties.filter(p => !p.is_verified).length,
    contacts: contacts.length
  };

  if (loading) {
    return (
      <div className="pt-16 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-red-600"></div>
          <p className="mt-4 text-lg">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>Admin Dashboard - Rhokawi Properties</title>
      </Helmet>

      <div className="pt-16 min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
            <p className="text-gray-600">Welcome back, {user?.first_name || user?.username}</p>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <Home className="h-8 w-8 text-red-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Properties</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <CheckCircle className="h-8 w-8 text-green-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Verified (Public)</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.verified}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <XCircle className="h-8 w-8 text-yellow-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Pending Verification</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.unverified}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <div className="flex items-center">
                  <MessageSquare className="h-8 w-8 text-blue-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">New Inquiries</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.contacts}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Tabs */}
          <div className="mb-6">
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8">
                <button
                  onClick={() => setActiveTab('properties')}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'properties'
                      ? 'border-red-500 text-red-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Home className="w-4 h-4 inline mr-2" />
                  Properties
                </button>

                {user?.is_main_admin && (
                  <button
                    onClick={() => setActiveTab('admins')}
                    className={`py-2 px-1 border-b-2 font-medium text-sm ${
                      activeTab === 'admins'
                        ? 'border-red-500 text-red-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <Users className="w-4 h-4 inline mr-2" />
                    Admin Users
                  </button>
                )}

                <button
                  onClick={() => setActiveTab('contacts')}
                  className={`py-2 px-1 border-b-2 font-medium text-sm relative ${
                    activeTab === 'contacts'
                      ? 'border-red-500 text-red-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <MessageSquare className="w-4 h-4 inline mr-2" />
                  Contact Messages
                  {unreadCount > 0 && (
                    <Badge className="ml-2 bg-red-600 text-white text-xs px-2 py-1 min-w-[20px] h-5 flex items-center justify-center rounded-full">
                      {unreadCount}
                    </Badge>
                  )}
                </button>
              </nav>
            </div>
          </div>

          {/* Properties Tab */}
          {activeTab === 'properties' && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold">Properties Management</h2>
                <Button onClick={handleAddProperty} className="bg-red-600 hover:bg-red-700">
                  <Plus className="w-4 h-4 mr-2" />
                  Add Property
                </Button>
              </div>

              {properties.length === 0 ? (
                <Card>
                  <CardContent className="p-12 text-center">
                    <Home className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No properties yet</h3>
                    <p className="text-gray-600 mb-4">Get started by adding your first property</p>
                    <Button onClick={handleAddProperty} className="bg-red-600 hover:bg-red-700">
                      <Plus className="w-4 h-4 mr-2" />
                      Add Property
                    </Button>
                  </CardContent>
                </Card>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {properties.map((property) => (
                    <Card key={property.id} className="overflow-hidden">
                      <div className="relative h-48">
                        <img
                          src={property.images && property.images.length > 0 
                            ? (property.images[0].startsWith('http') 
                              ? property.images[0] 
                              : `${import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'}/uploads/images/${property.images[0]}`)
                            : "https://images.unsplash.com/photo-1595872018818-97555653a011"
                          }
                          alt={property.title}
                          className="w-full h-full object-cover"
                        />
                        <div className="absolute top-2 right-2">
                          <Badge variant={property.is_verified ? "default" : "secondary"}>
                            {property.is_verified ? "Public" : "Hidden"}
                          </Badge>
                        </div>
                      </div>
                      <CardContent className="p-4">
                        <h3 className="font-semibold mb-2 line-clamp-2">{property.title}</h3>
                        <p className="text-gray-600 mb-2">{property.location}</p>
                        <p className="text-lg font-bold text-red-600 mb-4">
                          KES {property.price?.toLocaleString()}
                        </p>
                        
                        <div className="flex gap-2 mb-3">
                          <Button
                            size="sm"
                            variant={property.is_verified ? "outline" : "default"}
                            onClick={() => handleVerifyProperty(property.id, !property.is_verified)}
                            className={property.is_verified ? "text-red-600" : "bg-green-600 hover:bg-green-700"}
                          >
                            {property.is_verified ? (
                              <>
                                <XCircle className="w-3 h-3 mr-1" />
                                Hide
                              </>
                            ) : (
                              <>
                                <CheckCircle className="w-3 h-3 mr-1" />
                                Verify
                              </>
                            )}
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleEditProperty(property)}
                          >
                            <Settings className="w-3 h-3 mr-1" />
                            Edit
                          </Button>
                        </div>
                        
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleDeleteProperty(property)}
                          className="w-full text-red-600"
                        >
                          Delete Property
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Admins Tab */}
          {activeTab === 'admins' && user?.is_main_admin && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold">Admin Users</h2>
                <Button onClick={() => setShowAdminForm(true)} className="bg-red-600 hover:bg-red-700">
                  <UserPlus className="w-4 h-4 mr-2" />
                  Add Admin
                </Button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {admins.map((admin) => (
                  <Card key={admin.id}>
                    <CardContent className="p-6">
                      <div className="flex items-center justify-between mb-4">
                        <div className="w-12 h-12 bg-red-600 text-white rounded-full flex items-center justify-center font-bold">
                          {admin.first_name ? admin.first_name.charAt(0) : admin.username.charAt(0)}
                        </div>
                        {admin.is_main_admin && (
                          <Badge>Main Admin</Badge>
                        )}
                      </div>
                      <h3 className="font-semibold">{admin.first_name} {admin.last_name}</h3>
                      <p className="text-gray-600">@{admin.username}</p>
                      <p className="text-gray-600">{admin.email}</p>
                      
                      {!admin.is_main_admin && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleDeleteAdmin(admin.id)}
                          className="w-full mt-4 text-red-600"
                        >
                          Remove Admin
                        </Button>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {/* Contacts Tab */}
          {activeTab === 'contacts' && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold">Contact Messages</h2>
                <Button
                  onClick={() => loadContacts()}
                  variant="outline"
                  size="sm"
                >
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Refresh
                </Button>
              </div>
              
              {contacts.length === 0 ? (
                <Card>
                  <CardContent className="p-12 text-center">
                    <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No messages yet</h3>
                    <p className="text-gray-600">Contact messages will appear here when customers send inquiries</p>
                  </CardContent>
                </Card>
              ) : (
                <div className="space-y-4">
                  {contacts.map((contact) => (
                    <Card key={contact.id} className={contact.status === 'unread' ? 'border-l-4 border-l-red-500' : ''}>
                      <CardContent className="p-6">
                        <div className="flex justify-between items-start mb-4">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                              <h3 className="font-semibold text-lg">{contact.name}</h3>
                              <Badge variant={contact.status === 'unread' ? 'destructive' : contact.status === 'read' ? 'secondary' : 'default'}>
                                {contact.status}
                              </Badge>
                            </div>
                            <div className="space-y-1 text-sm text-gray-600">
                              <p><strong>Email:</strong> {contact.email}</p>
                              {contact.phone && <p><strong>Phone:</strong> {contact.phone}</p>}
                              {contact.user_name && <p><strong>User:</strong> {contact.user_name}</p>}
                            </div>
                          </div>
                          <div className="text-right">
                            <Badge variant="secondary">
                              {new Date(contact.created_at).toLocaleDateString()}
                            </Badge>
                            <p className="text-xs text-gray-500 mt-1">
                              {new Date(contact.created_at).toLocaleTimeString()}
                            </p>
                          </div>
                        </div>
                        
                        <div className="bg-gray-50 p-4 rounded-lg mb-4">
                          <h4 className="font-medium mb-2">Message:</h4>
                          <p className="text-gray-700 whitespace-pre-wrap">{contact.message}</p>
                        </div>
                        
                        {contact.property_title && (
                          <div className="bg-blue-50 p-3 rounded-lg mb-4">
                            <p className="text-sm text-blue-800">
                              <strong>Regarding Property:</strong> {contact.property_title}
                            </p>
                          </div>
                        )}

                        <div className="flex gap-2 pt-4 border-t">
                          {contact.status === 'unread' && (
                            <Button
                              onClick={() => handleUpdateContactStatus(contact.id, 'read')}
                              variant="outline"
                              size="sm"
                            >
                              Mark as Read
                            </Button>
                          )}
                          <Button
                            onClick={() => handleUpdateContactStatus(contact.id, 'replied')}
                            variant="outline"
                            size="sm"
                          >
                            Mark as Replied
                          </Button>
                          <Button
                            onClick={() => window.open(`mailto:${contact.email}?subject=Re: Your inquiry&body=Hi ${contact.name},%0D%0A%0D%0AThank you for your inquiry...`)}
                            variant="default"
                            size="sm"
                          >
                            Reply via Email
                          </Button>
                          {contact.phone && (
                            <Button
                              onClick={() => window.open(`tel:${contact.phone}`)}
                              variant="outline"
                              size="sm"
                            >
                              Call
                            </Button>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Property Form Modal */}
          {showForm && (
            <PropertyForm
              property={editingProperty}
              onSubmit={handlePropertySubmit}
              onClose={() => {
                setShowForm(false);
                setEditingProperty(null);
              }}
            />
          )}

          {/* Add Admin Modal */}
          {showAdminForm && (
            <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
              <div className="bg-white rounded-lg p-6 w-full max-w-md">
                <h3 className="text-lg font-semibold mb-4">Add New Admin</h3>
                <form onSubmit={handleAddAdmin} className="space-y-4">
                  <div>
                    <input
                      type="text"
                      placeholder="Username"
                      value={adminForm.username}
                      onChange={(e) => setAdminForm({ ...adminForm, username: e.target.value })}
                      className="w-full p-3 border rounded-lg"
                      required
                    />
                  </div>
                  <div>
                    <input
                      type="email"
                      placeholder="Email"
                      value={adminForm.email}
                      onChange={(e) => setAdminForm({ ...adminForm, email: e.target.value })}
                      className="w-full p-3 border rounded-lg"
                      required
                    />
                  </div>
                  <div>
                    <input
                      type="password"
                      placeholder="Password"
                      value={adminForm.password}
                      onChange={(e) => setAdminForm({ ...adminForm, password: e.target.value })}
                      className="w-full p-3 border rounded-lg"
                      required
                    />
                  </div>
                  <div>
                    <input
                      type="text"
                      placeholder="First Name"
                      value={adminForm.first_name}
                      onChange={(e) => setAdminForm({ ...adminForm, first_name: e.target.value })}
                      className="w-full p-3 border rounded-lg"
                    />
                  </div>
                  <div>
                    <input
                      type="text"
                      placeholder="Last Name"
                      value={adminForm.last_name}
                      onChange={(e) => setAdminForm({ ...adminForm, last_name: e.target.value })}
                      className="w-full p-3 border rounded-lg"
                    />
                  </div>
                  <div className="flex gap-2">
                    <Button type="submit" className="flex-1 bg-red-600 hover:bg-red-700">
                      Add Admin
                    </Button>
                    <Button 
                      type="button" 
                      variant="outline" 
                      onClick={() => setShowAdminForm(false)}
                      className="flex-1"
                    >
                      Cancel
                    </Button>
                  </div>
                </form>
              </div>
            </div>
          )}

          {/* Delete Confirmation */}
          {deletingProperty && (
            <ConfirmationDialog
              isOpen={true}
              onClose={() => setDeletingProperty(null)}
              onConfirm={confirmDeleteProperty}
              title="Delete Property"
              description={`Are you sure you want to delete "${deletingProperty.title}"? This action cannot be undone.`}
            />
          )}
        </div>
      </div>
    </>
  );
};

export default Dashboard;
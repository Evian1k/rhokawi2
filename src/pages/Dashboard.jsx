import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { Plus, Home, Star, TrendingUp, Eye } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { useAuth } from '@/contexts/AuthContext';
import PropertyForm from '@/components/dashboard/PropertyForm';
import PropertyList from '@/components/dashboard/PropertyList';
import ConfirmationDialog from '@/components/ConfirmationDialog';
import { useToast } from '@/components/ui/use-toast';

const Dashboard = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [properties, setProperties] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingProperty, setEditingProperty] = useState(null);
  const [deletingProperty, setDeletingProperty] = useState(null);

  useEffect(() => {
    loadProperties();
  }, []);

  const loadProperties = () => {
    const savedProperties = localStorage.getItem('properties');
    if (savedProperties) {
      setProperties(JSON.parse(savedProperties));
    }
  };

  const saveProperties = (updatedProperties) => {
    localStorage.setItem('properties', JSON.stringify(updatedProperties));
    setProperties(updatedProperties);
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

  const confirmDelete = () => {
    const updatedProperties = properties.filter(prop => prop.id !== deletingProperty.id);
    saveProperties(updatedProperties);
    toast({
      title: "Property Deleted!",
      description: `"${deletingProperty.title}" has been successfully deleted.`,
    });
    setDeletingProperty(null);
  };

  const handleFormSubmit = (propertyData) => {
    let updatedProperties;
    if (editingProperty) {
      updatedProperties = properties.map(prop =>
        prop.id === editingProperty.id ? { ...prop, ...propertyData } : prop
      );
      toast({
        title: "Property Updated!",
        description: `"${propertyData.title}" has been successfully updated.`,
      });
    } else {
      updatedProperties = [...properties, { ...propertyData, id: Date.now(), images: [] }];
      toast({
        title: "Property Added!",
        description: `"${propertyData.title}" has been successfully added.`,
      });
    }
    saveProperties(updatedProperties);
    setShowForm(false);
    setEditingProperty(null);
  };

  const toggleFeatured = (propertyId) => {
    const updatedProperties = properties.map(prop =>
      prop.id === propertyId ? { ...prop, featured: !prop.featured } : prop
    );
    saveProperties(updatedProperties);
    toast({
      title: "Property Updated!",
      description: "Featured status has been updated.",
    });
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-KE', {
      style: 'currency',
      currency: 'KES',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  const stats = [
    {
      title: 'Total Properties',
      value: properties.length,
      icon: Home,
      color: 'bg-blue-500'
    },
    {
      title: 'Featured Properties',
      value: properties.filter(p => p.featured).length,
      icon: Star,
      color: 'bg-yellow-500'
    },
    {
      title: 'Total Value',
      value: formatPrice(properties.reduce((sum, p) => sum + (p.price || 0), 0)),
      icon: TrendingUp,
      color: 'bg-green-500'
    },
    {
      title: 'Property Types',
      value: new Set(properties.map(p => p.type)).size,
      icon: Eye,
      color: 'bg-purple-500'
    }
  ];

  return (
    <>
      <Helmet>
        <title>Admin Dashboard - Rhokawi Properties Ltd</title>
        <meta name="description" content="Admin dashboard for managing properties at Rhokawi Properties Ltd. Add, edit, and manage property listings." />
      </Helmet>

      <div className="pt-16 min-h-screen bg-background">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-8"
          >
            <h1 className="text-3xl font-bold mb-2">
              Welcome back, <span className="gradient-text">{user?.name}</span>
            </h1>
            <p className="text-muted-foreground">
              Manage your property listings and track performance
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-muted-foreground">{stat.title}</p>
                        <p className="text-2xl font-bold">{stat.value}</p>
                      </div>
                      <div className={`w-12 h-12 ${stat.color} rounded-lg flex items-center justify-center`}>
                        <stat.icon className="w-6 h-6 text-white" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="mb-8"
          >
            {!showForm && (
              <Button
                onClick={handleAddProperty}
                className="bg-red-600 hover:bg-red-700"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add New Property
              </Button>
            )}
          </motion.div>

          {showForm && (
            <PropertyForm
              property={editingProperty}
              onSubmit={handleFormSubmit}
              onCancel={() => { setShowForm(false); setEditingProperty(null); }}
            />
          )}

          <PropertyList
            properties={properties}
            onEdit={handleEditProperty}
            onDelete={handleDeleteProperty}
            onToggleFeatured={toggleFeatured}
            formatPrice={formatPrice}
          />

          <ConfirmationDialog
            open={!!deletingProperty}
            onOpenChange={() => setDeletingProperty(null)}
            onConfirm={confirmDelete}
            title="Are you sure you want to delete this property?"
            description="This action cannot be undone. This will permanently delete the property listing."
          />
        </div>
      </div>
    </>
  );
};

export default Dashboard;
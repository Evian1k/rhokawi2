import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import ImageUploader from '@/components/ImageUploader';
import { X } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';

const PropertyForm = ({ property, onSubmit, onCancel }) => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    title: '',
    price: '',
    location: '',
    type: '',
    bedrooms: '',
    bathrooms: '',
    area: '',
    description: '',
    featured: false,
    images: [],
  });

  const propertyTypes = [
    'Apartment', 'House', 'Villa', 'Townhouse', 'Penthouse',
    'Bungalow', 'Studio', 'Duplex', 'Mansion'
  ];

  useEffect(() => {
    if (property) {
      setFormData({
        title: property.title || '',
        price: property.price?.toString() || '',
        location: property.location || '',
        type: property.type || '',
        bedrooms: property.bedrooms?.toString() || '',
        bathrooms: property.bathrooms?.toString() || '',
        area: property.area?.toString() || '',
        description: property.description || '',
        featured: property.featured || false,
        images: property.images || [],
      });
    } else {
      setFormData({
        title: '', price: '', location: '', type: '', bedrooms: '',
        bathrooms: '', area: '', description: '', featured: false, images: [],
      });
    }
  }, [property]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (name, value) => {
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (checked) => {
    setFormData(prev => ({ ...prev, featured: checked }));
  };

  const handleFilesChange = (files) => {
    setFormData(prev => ({ ...prev, images: files }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.type) {
      toast({
        title: "Validation Error",
        description: "Please select a property type.",
        variant: "destructive",
      });
      return;
    }
    const submissionData = {
      ...formData,
      price: parseInt(formData.price) || 0,
      bedrooms: parseInt(formData.bedrooms) || 0,
      bathrooms: parseInt(formData.bathrooms) || 0,
      area: parseInt(formData.area) || 0,
    };
    onSubmit(submissionData);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="mb-8"
    >
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>
            {property ? 'Edit Property' : 'Add New Property'}
          </CardTitle>
          <Button variant="ghost" size="icon" onClick={onCancel}>
            <X className="w-4 h-4" />
          </Button>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="images">Property Images</Label>
              <ImageUploader onFilesChange={handleFilesChange} existingImages={formData.images} />
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="title">Property Title *</Label>
                <Input id="title" name="title" value={formData.title} onChange={handleInputChange} required placeholder="e.g., Modern Villa in Karen" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="price">Price (KSh) *</Label>
                <Input id="price" name="price" type="number" value={formData.price} onChange={handleInputChange} required placeholder="e.g., 25000000" />
              </div>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="location">Location *</Label>
                <Input id="location" name="location" value={formData.location} onChange={handleInputChange} required placeholder="e.g., Karen, Nairobi" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="type">Property Type *</Label>
                <Select value={formData.type} onValueChange={(value) => handleSelectChange('type', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select property type" />
                  </SelectTrigger>
                  <SelectContent>
                    {propertyTypes.map(type => (
                      <SelectItem key={type} value={type}>{type}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="bedrooms">Bedrooms *</Label>
                <Input id="bedrooms" name="bedrooms" type="number" value={formData.bedrooms} onChange={handleInputChange} required placeholder="e.g., 4" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="bathrooms">Bathrooms *</Label>
                <Input id="bathrooms" name="bathrooms" type="number" value={formData.bathrooms} onChange={handleInputChange} required placeholder="e.g., 3" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="area">Area (sqm) *</Label>
                <Input id="area" name="area" type="number" value={formData.area} onChange={handleInputChange} required placeholder="e.g., 350" />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="description">Description *</Label>
              <Textarea id="description" name="description" value={formData.description} onChange={handleInputChange} required placeholder="Describe the property features and amenities..." rows={4} />
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox id="featured" checked={formData.featured} onCheckedChange={handleCheckboxChange} />
              <Label htmlFor="featured">Mark as Featured Property</Label>
            </div>
            <div className="flex gap-4">
              <Button type="submit" className="bg-red-600 hover:bg-red-700">
                {property ? 'Update Property' : 'Add Property'}
              </Button>
              <Button type="button" variant="outline" onClick={onCancel}>
                Cancel
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default PropertyForm;
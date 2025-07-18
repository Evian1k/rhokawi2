import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { MapPin, Loader2, Grid, Map, Filter } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/components/ui/use-toast';
import { useNavigate } from 'react-router-dom';
import apiService from '@/lib/api';

const PropertyMap = () => {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('map'); // 'map' or 'grid'
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [mapCenter, setMapCenter] = useState({ lat: -1.2921, lng: 36.8219 }); // Nairobi center
  const { toast } = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    fetchProperties();
  }, []);

  const fetchProperties = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiService.searchProperties({
        status: 'available',
        per_page: 100 // Get all available properties
      });
      
      if (response.data) {
        const propertiesWithCoords = response.data.properties.map(property => ({
          ...property,
          // Add mock coordinates for demonstration - in real app, these would be stored in DB
          coordinates: generateMockCoordinates(property.location)
        }));
        setProperties(propertiesWithCoords);
      }
    } catch (err) {
      console.error('Failed to fetch properties:', err);
      setError(err.message || 'Failed to load properties');
    } finally {
      setLoading(false);
    }
  };

  // Generate mock coordinates based on location - in real app, use geocoding API
  const generateMockCoordinates = (location) => {
    const baseCoords = {
      'Nairobi': { lat: -1.2921, lng: 36.8219 },
      'Westlands': { lat: -1.2676, lng: 36.8108 },
      'Karen': { lat: -1.3197, lng: 36.6858 },
      'Kilimani': { lat: -1.2905, lng: 36.7866 },
      'Lavington': { lat: -1.2830, lng: 36.7677 },
      'Upperhill': { lat: -1.2968, lng: 36.8217 },
      'Runda': { lat: -1.2084, lng: 36.7616 },
      'Muthaiga': { lat: -1.2484, lng: 36.8108 },
      'Gigiri': { lat: -1.2294, lng: 36.7617 },
      'Spring Valley': { lat: -1.2630, lng: 36.7831 }
    };

    // Try to match location with known areas
    const locationKey = Object.keys(baseCoords).find(key => 
      location.toLowerCase().includes(key.toLowerCase())
    );
    
    if (locationKey) {
      const base = baseCoords[locationKey];
      return {
        lat: base.lat + (Math.random() - 0.5) * 0.02, // Add small random offset
        lng: base.lng + (Math.random() - 0.5) * 0.02
      };
    }
    
    // Default to Nairobi with random offset
    return {
      lat: -1.2921 + (Math.random() - 0.5) * 0.1,
      lng: 36.8219 + (Math.random() - 0.5) * 0.1
    };
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-KE', {
      style: 'currency',
      currency: 'KES',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  const handlePropertyClick = (property) => {
    setSelectedProperty(property);
    setMapCenter(property.coordinates);
  };

  const handleViewProperty = (propertyId) => {
    navigate(`/properties/${propertyId}`);
  };

  if (loading) {
    return (
      <div className="pt-16 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin text-red-600 mx-auto mb-4" />
          <p className="text-lg">Loading property map...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>Property Map - Rhokawi Properties Ltd</title>
        <meta name="description" content="Explore all our properties on an interactive map. Find properties by location across Nairobi and Kenya." />
      </Helmet>

      <div className="pt-16">
        {/* Header */}
        <section className="bg-gradient-to-r from-red-600 to-red-800 text-white py-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center"
            >
              <h1 className="text-3xl md:text-4xl font-bold mb-4">
                Property Map
              </h1>
              <p className="text-xl opacity-90 mb-6">
                Explore all our {properties.length} available properties on the map
              </p>
              
              {/* View Toggle */}
              <div className="flex justify-center space-x-2">
                <Button
                  variant={viewMode === 'map' ? 'secondary' : 'outline'}
                  onClick={() => setViewMode('map')}
                  className="text-white border-white hover:bg-white/20"
                >
                  <Map className="mr-2 h-4 w-4" />
                  Map View
                </Button>
                <Button
                  variant={viewMode === 'grid' ? 'secondary' : 'outline'}
                  onClick={() => setViewMode('grid')}
                  className="text-white border-white hover:bg-white/20"
                >
                  <Grid className="mr-2 h-4 w-4" />
                  Grid View
                </Button>
              </div>
            </motion.div>
          </div>
        </section>

        {error ? (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="text-center">
              <div className="text-red-600 text-lg mb-4">Failed to load properties</div>
              <div className="text-muted-foreground mb-6">{error}</div>
              <Button 
                onClick={fetchProperties}
                className="bg-red-600 hover:bg-red-700"
              >
                Try Again
              </Button>
            </div>
          </div>
        ) : (
          <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {viewMode === 'map' ? (
              <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[600px]">
                {/* Map Container */}
                <div className="lg:col-span-3">
                  <Card className="h-full">
                    <CardContent className="p-0 h-full">
                      <div className="w-full h-full bg-gray-100 rounded-lg flex items-center justify-center relative overflow-hidden">
                        {/* Simplified Map Representation */}
                        <div className="absolute inset-0 bg-gradient-to-br from-green-100 to-blue-100">
                          {/* Mock map roads */}
                          <div className="absolute top-1/2 left-0 right-0 h-1 bg-gray-400 opacity-50"></div>
                          <div className="absolute top-0 bottom-0 left-1/2 w-1 bg-gray-400 opacity-50"></div>
                          
                          {/* Property Markers */}
                          {properties.map((property, index) => (
                            <div
                              key={property.id}
                              className={`absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer transition-all duration-200 ${
                                selectedProperty?.id === property.id ? 'scale-125 z-10' : 'hover:scale-110'
                              }`}
                              style={{
                                left: `${((property.coordinates.lng - 36.6) / 0.4) * 100}%`,
                                top: `${((property.coordinates.lat + 1.4) / 0.3) * 100}%`,
                              }}
                              onClick={() => handlePropertyClick(property)}
                            >
                              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold shadow-lg ${
                                selectedProperty?.id === property.id ? 'bg-red-600' : 'bg-red-500'
                              }`}>
                                <MapPin className="w-4 h-4" />
                              </div>
                              {selectedProperty?.id === property.id && (
                                <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 bg-white rounded-lg shadow-lg p-2 whitespace-nowrap z-20">
                                  <div className="text-xs font-medium">{formatPrice(property.price)}</div>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                        
                        <div className="absolute bottom-4 right-4 bg-white/90 backdrop-blur-sm rounded-lg p-3">
                          <div className="text-sm font-medium mb-2">Map Legend</div>
                          <div className="flex items-center space-x-2 text-xs">
                            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                            <span>Available Property</span>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>

                {/* Property List Sidebar */}
                <div className="lg:col-span-1">
                  <Card className="h-full">
                    <CardContent className="p-4 h-full overflow-auto">
                      <h3 className="font-semibold mb-4">Properties ({properties.length})</h3>
                      <div className="space-y-3">
                        {properties.map((property) => (
                          <div
                            key={property.id}
                            className={`p-3 border rounded-lg cursor-pointer transition-all duration-200 ${
                              selectedProperty?.id === property.id 
                                ? 'border-red-500 bg-red-50' 
                                : 'border-gray-200 hover:border-red-300 hover:bg-gray-50'
                            }`}
                            onClick={() => handlePropertyClick(property)}
                          >
                            <div className="text-sm font-medium mb-1 line-clamp-2">{property.title}</div>
                            <div className="text-xs text-muted-foreground mb-2 flex items-center">
                              <MapPin className="w-3 h-3 mr-1" />
                              {property.location}
                            </div>
                            <div className="text-sm font-bold text-red-600 mb-2">
                              {formatPrice(property.price)}
                            </div>
                            <div className="flex justify-between items-center">
                              <Badge variant="secondary" className="text-xs">
                                {property.property_type}
                              </Badge>
                              <Button 
                                size="sm" 
                                variant="outline" 
                                className="text-xs h-6"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleViewProperty(property.id);
                                }}
                              >
                                View
                              </Button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
            ) : (
              /* Grid View */
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {properties.map((property, index) => (
                  <motion.div
                    key={property.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.1 }}
                  >
                    <Card className="overflow-hidden h-full flex flex-col">
                      <div className="relative h-48">
                        <img 
                          className="w-full h-full object-cover"
                          alt={property.title}
                          src={property.images && property.images.length > 0 
                            ? (property.images[0].startsWith('http') 
                              ? property.images[0] 
                              : `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/uploads/images/${property.images[0]}`)
                            : "https://images.unsplash.com/photo-1595872018818-97555653a011"
                          }
                        />
                        <div className="absolute top-2 right-2">
                          <Badge className="bg-red-600">
                            {formatPrice(property.price)}
                          </Badge>
                        </div>
                      </div>
                      <CardContent className="p-4 flex flex-col flex-grow">
                        <h3 className="font-semibold mb-2 line-clamp-2">{property.title}</h3>
                        <p className="text-muted-foreground text-sm mb-3 flex items-center">
                          <MapPin className="w-4 h-4 mr-1" />
                          {property.location}
                        </p>
                        <div className="flex justify-between items-center mb-3">
                          <Badge variant="secondary">{property.property_type}</Badge>
                          <div className="text-xs text-muted-foreground">
                            {property.bedrooms && `${property.bedrooms} bed`}
                            {property.bathrooms && ` • ${property.bathrooms} bath`}
                          </div>
                        </div>
                        <Button 
                          className="w-full mt-auto bg-red-600 hover:bg-red-700"
                          onClick={() => handleViewProperty(property.id)}
                        >
                          View Property
                        </Button>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </div>
            )}
          </section>
        )}
      </div>
    </>
  );
};

export default PropertyMap;
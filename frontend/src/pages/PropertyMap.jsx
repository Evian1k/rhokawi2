import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { MapPin, Loader2, Grid, Map, Filter, Navigation } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/components/ui/use-toast';
import { useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import apiService from '@/lib/api';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom property marker icon
const createPropertyIcon = (price, isSelected = false) => {
  const priceText = new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
    notation: 'compact'
  }).format(price);

  return L.divIcon({
    html: `
      <div class="property-marker ${isSelected ? 'selected' : ''}" style="
        background: ${isSelected ? '#dc2626' : '#ef4444'};
        color: white;
        border: 3px solid white;
        border-radius: 20px;
        padding: 4px 8px;
        font-size: 11px;
        font-weight: bold;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        white-space: nowrap;
        transform: translate(-50%, -100%);
        position: relative;
      ">
        ${priceText}
        <div style="
          position: absolute;
          bottom: -6px;
          left: 50%;
          transform: translateX(-50%);
          width: 0;
          height: 0;
          border-left: 6px solid transparent;
          border-right: 6px solid transparent;
          border-top: 6px solid ${isSelected ? '#dc2626' : '#ef4444'};
        "></div>
      </div>
    `,
    className: 'property-marker-icon',
    iconSize: [60, 40],
    iconAnchor: [30, 40]
  });
};

// Component to update map view
const MapUpdater = ({ center, zoom }) => {
  const map = useMap();
  
  useEffect(() => {
    if (center) {
      map.setView(center, zoom);
    }
  }, [center, zoom, map]);
  
  return null;
};

const PropertyMap = () => {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('map'); // 'map' or 'grid'
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [mapCenter, setMapCenter] = useState([-1.2921, 36.8219]); // Nairobi center
  const [mapZoom, setMapZoom] = useState(11);
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
          // Add coordinates - in real app, these would be stored in DB or geocoded
          coordinates: generateCoordinatesFromLocation(property.location)
        }));
        setProperties(propertiesWithCoords);
      }
    } catch (err) {
      console.error('Failed to fetch properties:', err);
      setError(err.message || 'Failed to load properties');
      toast({
        title: "Error loading properties",
        description: err.message || 'Failed to load properties',
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  // Generate coordinates based on location - in real app, use geocoding API
  const generateCoordinatesFromLocation = (location) => {
    const locationCoords = {
      'Nairobi': [-1.2921, 36.8219],
      'Westlands': [-1.2676, 36.8108],
      'Karen': [-1.3197, 36.6858],
      'Kilimani': [-1.2905, 36.7866],
      'Lavington': [-1.2830, 36.7677],
      'Upperhill': [-1.2968, 36.8217],
      'Runda': [-1.2084, 36.7616],
      'Muthaiga': [-1.2484, 36.8108],
      'Gigiri': [-1.2294, 36.7617],
      'Spring Valley': [-1.2630, 36.7831],
      'Kileleshwa': [-1.2768, 36.7879],
      'Riverside': [-1.2690, 36.8140],
      'Parklands': [-1.2647, 36.8581],
      'Kasarani': [-1.2215, 36.8968],
      'Embakasi': [-1.3167, 36.8926],
      'Langata': [-1.3515, 36.7512],
      'Kibera': [-1.3133, 36.7890],
      'Mathare': [-1.2598, 36.8581]
    };

    // Try to match location with known coordinates
    const locationKey = Object.keys(locationCoords).find(key => 
      location.toLowerCase().includes(key.toLowerCase())
    );
    
    if (locationKey) {
      const base = locationCoords[locationKey];
      return [
        base[0] + (Math.random() - 0.5) * 0.01, // Add small random offset
        base[1] + (Math.random() - 0.5) * 0.01
      ];
    }
    
    // Default to Nairobi with random offset
    return [
      -1.2921 + (Math.random() - 0.5) * 0.05,
      36.8219 + (Math.random() - 0.5) * 0.05
    ];
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
    setMapZoom(15);
  };

  const handleViewProperty = (propertyId) => {
    navigate(`/properties/${propertyId}`);
  };

  const centerOnUserLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setMapCenter([latitude, longitude]);
          setMapZoom(13);
          toast({
            title: "Location found",
            description: "Map centered on your location",
          });
        },
        (error) => {
          console.error('Error getting location:', error);
          toast({
            title: "Location error",
            description: "Could not get your location",
            variant: "destructive",
          });
        }
      );
    } else {
      toast({
        title: "Location not supported",
        description: "Geolocation is not supported by this browser",
        variant: "destructive",
      });
    }
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
        <link 
          rel="stylesheet" 
          href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
          crossOrigin=""
        />
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
                Explore all our {properties.length} available properties on the interactive map
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
                {viewMode === 'map' && (
                  <Button
                    variant="outline"
                    onClick={centerOnUserLocation}
                    className="text-white border-white hover:bg-white/20"
                  >
                    <Navigation className="mr-2 h-4 w-4" />
                    My Location
                  </Button>
                )}
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
                  <Card className="h-full overflow-hidden">
                    <CardContent className="p-0 h-full">
                      <MapContainer
                        center={mapCenter}
                        zoom={mapZoom}
                        style={{ height: '100%', width: '100%' }}
                        className="rounded-lg"
                      >
                        <TileLayer
                          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        />
                        <MapUpdater center={mapCenter} zoom={mapZoom} />
                        
                        {properties.map((property) => (
                          <Marker
                            key={property.id}
                            position={property.coordinates}
                            icon={createPropertyIcon(property.price, selectedProperty?.id === property.id)}
                            eventHandlers={{
                              click: () => handlePropertyClick(property),
                            }}
                          >
                            <Popup>
                              <div className="w-64">
                                <img
                                  src={property.images && property.images.length > 0 
                                    ? (property.images[0].startsWith('http') 
                                      ? property.images[0] 
                                      : `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/uploads/images/${property.images[0]}`)
                                    : "https://images.unsplash.com/photo-1595872018818-97555653a011"
                                  }
                                  alt={property.title}
                                  className="w-full h-32 object-cover rounded-lg mb-2"
                                />
                                <h3 className="font-semibold text-sm mb-1">{property.title}</h3>
                                <p className="text-xs text-gray-600 mb-2 flex items-center">
                                  <MapPin className="w-3 h-3 mr-1" />
                                  {property.location}
                                </p>
                                <div className="flex justify-between items-center mb-2">
                                  <span className="font-bold text-red-600 text-sm">
                                    {formatPrice(property.price)}
                                  </span>
                                  <Badge variant="secondary" className="text-xs">
                                    {property.property_type}
                                  </Badge>
                                </div>
                                <Button 
                                  size="sm" 
                                  className="w-full bg-red-600 hover:bg-red-700 text-xs"
                                  onClick={() => handleViewProperty(property.id)}
                                >
                                  View Property
                                </Button>
                              </div>
                            </Popup>
                          </Marker>
                        ))}
                      </MapContainer>
                    </CardContent>
                  </Card>
                </div>

                {/* Property List Sidebar */}
                <div className="lg:col-span-1">
                  <Card className="h-full">
                    <CardContent className="p-4 h-full overflow-auto">
                      <h3 className="font-semibold mb-4 flex items-center">
                        <Filter className="w-4 h-4 mr-2" />
                        Properties ({properties.length})
                      </h3>
                      <div className="space-y-3">
                        {properties.map((property) => (
                          <div
                            key={property.id}
                            className={`p-3 border rounded-lg cursor-pointer transition-all duration-200 hover:shadow-md ${
                              selectedProperty?.id === property.id 
                                ? 'border-red-500 bg-red-50 shadow-md' 
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
                                className="text-xs h-6 hover:bg-red-50"
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
                    transition={{ duration: 0.6, delay: index * 0.05 }}
                  >
                    <Card className="overflow-hidden h-full flex flex-col hover:shadow-lg transition-shadow duration-300">
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
                          <Badge className="bg-red-600 hover:bg-red-700">
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
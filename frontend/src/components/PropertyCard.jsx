import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { MapPin, Bed, Bath, Square, Star } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';

const PropertyCard = ({ property, index }) => {
  const { toast } = useToast();
  const navigate = useNavigate();

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-KE', {
      style: 'currency',
      currency: 'KES',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  const handleViewDetails = (propertyId) => {
    navigate(`/properties/${propertyId}`);
  };

  const handleContactAgent = () => {
    navigate(`/properties/${property.id}`, { state: { openContact: true } });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: index * 0.1 }}
      viewport={{ once: true }}
    >
      <Card className="property-card overflow-hidden h-full flex flex-col">
        <div className="relative h-64">
          <img 
            className="w-full h-full object-cover"
            alt={`${property.title} - ${property.location}`}
            src={property.images && property.images.length > 0 
              ? (property.images[0].startsWith('http') 
                ? property.images[0] 
                : `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/uploads/images/${property.images[0]}`)
              : "https://images.unsplash.com/photo-1595872018818-97555653a011"
            }
          />
          {property.featured && (
            <div className="absolute top-4 right-4 bg-red-600 text-white px-3 py-1 rounded-full text-sm font-semibold flex items-center">
              <Star className="w-3 h-3 mr-1" />
              Featured
            </div>
          )}
        </div>
        <CardContent className="p-6 flex flex-col flex-grow">
          <div className="flex-grow">
            <h3 className="text-xl font-semibold mb-2">{property.title}</h3>
            <p className="text-muted-foreground mb-3 flex items-center">
              <MapPin className="w-4 h-4 mr-1" />
              {property.location}
            </p>
            <p className="text-sm text-muted-foreground mb-4 line-clamp-2">{property.description}</p>
            <div className="flex justify-between items-center mb-4">
              <span className="text-2xl font-bold text-red-600">
                {formatPrice(property.price)}
              </span>
              <span className="text-sm bg-muted px-2 py-1 rounded">
                {property.property_type}
              </span>
            </div>
            <div className="flex justify-between text-sm text-muted-foreground mb-4">
              {property.bedrooms && (
                <span className="flex items-center">
                  <Bed className="w-4 h-4 mr-1" />
                  {property.bedrooms} Beds
                </span>
              )}
              {property.bathrooms && (
                <span className="flex items-center">
                  <Bath className="w-4 h-4 mr-1" />
                  {property.bathrooms} Baths
                </span>
              )}
              {property.square_feet && (
                <span className="flex items-center">
                  <Square className="w-4 h-4 mr-1" />
                  {property.square_feet} sqft
                </span>
              )}
            </div>
          </div>
          <div className="flex gap-2 mt-auto">
            <Button
              className="flex-1 bg-red-600 hover:bg-red-700"
              onClick={() => handleViewDetails(property.id)}
            >
              View Details
            </Button>
            <Button
              variant="outline"
              className="flex-1"
              onClick={() => handleContactAgent()}
            >
              Contact
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default PropertyCard;
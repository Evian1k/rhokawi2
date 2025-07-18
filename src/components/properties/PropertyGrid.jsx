import React from 'react';
import PropertyCard from '@/components/PropertyCard';

const PropertyGrid = ({ properties }) => {
  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
      {properties.map((property, index) => (
        <PropertyCard key={property.id} property={property} index={index} />
      ))}
    </div>
  );
};

export default PropertyGrid;
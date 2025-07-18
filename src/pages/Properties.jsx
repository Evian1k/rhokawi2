import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { Search } from 'lucide-react';
import PropertyFilters from '@/components/properties/PropertyFilters';
import PropertyGrid from '@/components/properties/PropertyGrid';
import Pagination from '@/components/properties/Pagination';
import NoPropertiesFound from '@/components/properties/NoPropertiesFound';

const Properties = () => {
  const [properties, setProperties] = useState([]);
  const [filteredProperties, setFilteredProperties] = useState([]);
  const [filters, setFilters] = useState({
    searchTerm: '',
    priceRange: '',
    propertyType: '',
    location: '',
  });
  const [currentPage, setCurrentPage] = useState(1);
  const propertiesPerPage = 9;

  const sampleProperties = [
    { id: 1, title: 'Modern Villa in Karen', price: 25000000, location: 'Karen, Nairobi', type: 'Villa', bedrooms: 4, bathrooms: 3, area: 350, featured: true, image: 'Modern luxury villa with swimming pool and garden', description: 'Stunning modern villa with premium finishes, swimming pool, and landscaped garden.' },
    { id: 2, title: 'Executive Apartment', price: 8500000, location: 'Westlands, Nairobi', type: 'Apartment', bedrooms: 3, bathrooms: 2, area: 180, featured: true, image: 'Executive apartment with city view and modern amenities', description: 'Luxurious apartment with panoramic city views and modern amenities.' },
    { id: 3, title: 'Family Home in Runda', price: 18000000, location: 'Runda, Nairobi', type: 'House', bedrooms: 5, bathrooms: 4, area: 280, featured: false, image: 'Spacious family home with large garden and garage', description: 'Perfect family home with spacious rooms and beautiful garden.' },
    { id: 4, title: 'Penthouse in Kilimani', price: 15000000, location: 'Kilimani, Nairobi', type: 'Penthouse', bedrooms: 3, bathrooms: 3, area: 220, featured: false, image: 'Luxury penthouse with rooftop terrace and city views', description: 'Exclusive penthouse with rooftop terrace and stunning city views.' },
    { id: 5, title: 'Townhouse in Lavington', price: 12000000, location: 'Lavington, Nairobi', type: 'Townhouse', bedrooms: 4, bathrooms: 3, area: 200, featured: false, image: 'Modern townhouse with private garden and parking', description: 'Contemporary townhouse in a secure gated community.' },
    { id: 6, title: 'Bungalow in Muthaiga', price: 35000000, location: 'Muthaiga, Nairobi', type: 'Bungalow', bedrooms: 6, bathrooms: 5, area: 400, featured: true, image: 'Elegant bungalow with mature gardens and swimming pool', description: 'Elegant bungalow on a large plot with mature gardens.' },
    { id: 7, title: 'Studio Apartment', price: 3500000, location: 'Kileleshwa, Nairobi', type: 'Studio', bedrooms: 1, bathrooms: 1, area: 45, featured: false, image: 'Compact studio apartment with modern design', description: 'Perfect starter home or investment property.' },
    { id: 8, title: 'Duplex in Riverside', price: 22000000, location: 'Riverside, Nairobi', type: 'Duplex', bedrooms: 4, bathrooms: 4, area: 300, featured: false, image: 'Spacious duplex with modern amenities and garden', description: 'Spacious duplex with contemporary design and amenities.' },
    { id: 9, title: 'Mansion in Gigiri', price: 45000000, location: 'Gigiri, Nairobi', type: 'Mansion', bedrooms: 7, bathrooms: 6, area: 500, featured: true, image: 'Luxury mansion with extensive grounds and facilities', description: 'Magnificent mansion with extensive grounds and luxury facilities.' }
  ];

  useEffect(() => {
    const savedProperties = localStorage.getItem('properties');
    const initialProperties = savedProperties ? JSON.parse(savedProperties) : sampleProperties;
    setProperties(initialProperties);
    setFilteredProperties(initialProperties);
    if (!savedProperties) {
      localStorage.setItem('properties', JSON.stringify(sampleProperties));
    }
  }, []);

  useEffect(() => {
    let filtered = properties;
    const { searchTerm, priceRange, propertyType, location } = filters;

    if (searchTerm) {
      filtered = filtered.filter(p =>
        p.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.type.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    if (priceRange) {
      const [min, max] = priceRange.split('-').map(Number);
      filtered = filtered.filter(p => {
        if (max) return p.price >= min && p.price <= max;
        return p.price >= min;
      });
    }
    if (propertyType) {
      filtered = filtered.filter(p => p.type === propertyType);
    }
    if (location) {
      filtered = filtered.filter(p => p.location.toLowerCase().includes(location.toLowerCase()));
    }

    setFilteredProperties(filtered);
    setCurrentPage(1);
  }, [filters, properties]);

  const indexOfLastProperty = currentPage * propertiesPerPage;
  const indexOfFirstProperty = indexOfLastProperty - propertiesPerPage;
  const currentProperties = filteredProperties.slice(indexOfFirstProperty, indexOfLastProperty);
  const totalPages = Math.ceil(filteredProperties.length / propertiesPerPage);

  return (
    <>
      <Helmet>
        <title>Properties - Rhokawi Properties Ltd</title>
        <meta name="description" content="Browse our extensive collection of premium properties for sale and rent in Nairobi, Kenya. Find your dream home with Rhokawi Properties Ltd." />
      </Helmet>

      <div className="pt-16">
        <section className="relative py-20 bg-gradient-to-r from-red-600 to-red-800 text-white overflow-hidden">
          <div className="absolute inset-0 bg-black/20"></div>
          <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-center"
            >
              <h1 className="text-4xl md:text-5xl font-bold mb-6">
                Find Your Perfect Property
              </h1>
              <p className="text-xl md:text-2xl max-w-3xl mx-auto opacity-90">
                Discover premium properties for sale and rent across Nairobi and beyond.
              </p>
            </motion.div>
          </div>
        </section>

        <PropertyFilters filters={filters} setFilters={setFilters} resultsCount={filteredProperties.length} />

        <section className="section-padding bg-background">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {currentProperties.length > 0 ? (
              <>
                <PropertyGrid properties={currentProperties} />
                {totalPages > 1 && (
                  <Pagination
                    currentPage={currentPage}
                    totalPages={totalPages}
                    onPageChange={setCurrentPage}
                  />
                )}
              </>
            ) : (
              <NoPropertiesFound onClearFilters={() => setFilters({ searchTerm: '', priceRange: '', propertyType: '', location: '' })} />
            )}
          </div>
        </section>
      </div>
    </>
  );
};

export default Properties;
import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { Search, Loader2 } from 'lucide-react';
import PropertyFilters from '@/components/properties/PropertyFilters';
import PropertyGrid from '@/components/properties/PropertyGrid';
import Pagination from '@/components/properties/Pagination';
import NoPropertiesFound from '@/components/properties/NoPropertiesFound';
import apiService from '@/lib/api';

const Properties = () => {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    searchTerm: '',
    priceRange: '',
    propertyType: '',
    location: '',
  });
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 9,
    total: 0,
    pages: 1,
    has_next: false,
    has_prev: false,
  });

  // Fetch properties from API
  const fetchProperties = async (searchParams = {}) => {
    try {
      setLoading(true);
      setError(null);
      
      const params = {
        page: pagination.page,
        per_page: pagination.per_page,
        status: 'available',
        ...searchParams,
      };

      const response = await apiService.searchProperties(params);
      
      if (response.data) {
        setProperties(response.data.properties || []);
        setPagination(response.data.pagination || pagination);
      }
    } catch (err) {
      console.error('Failed to fetch properties:', err);
      setError(err.message || 'Failed to load properties');
    } finally {
      setLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    fetchProperties();
  }, []);

  // Handle filter changes
  useEffect(() => {
    const searchParams = {};
    
    if (filters.searchTerm) {
      searchParams.location = filters.searchTerm;
    }
    if (filters.location) {
      searchParams.location = filters.location;
    }
    if (filters.propertyType) {
      searchParams.property_type = filters.propertyType;
    }
    if (filters.priceRange) {
      const [minPrice, maxPrice] = filters.priceRange.split('-').map(p => p.replace(/[^0-9]/g, ''));
      if (minPrice) searchParams.min_price = minPrice;
      if (maxPrice) searchParams.max_price = maxPrice;
    }

    fetchProperties(searchParams);
  }, [filters]);

  // Handle pagination
  const handlePageChange = (newPage) => {
    setPagination(prev => ({ ...prev, page: newPage }));
    fetchProperties();
  };

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

        <PropertyFilters filters={filters} setFilters={setFilters} resultsCount={pagination.total} />

        <section className="section-padding bg-background">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {loading ? (
              <div className="flex items-center justify-center py-20">
                <Loader2 className="h-8 w-8 animate-spin text-red-600" />
                <span className="ml-2 text-lg">Loading properties...</span>
              </div>
            ) : error ? (
              <div className="text-center py-20">
                <div className="text-red-600 text-lg mb-4">Failed to load properties</div>
                <div className="text-muted-foreground mb-6">{error}</div>
                <button 
                  onClick={() => fetchProperties()}
                  className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                  Try Again
                </button>
              </div>
            ) : properties.length > 0 ? (
              <>
                <PropertyGrid properties={properties} />
                {pagination.pages > 1 && (
                  <Pagination
                    currentPage={pagination.page}
                    totalPages={pagination.pages}
                    onPageChange={handlePageChange}
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
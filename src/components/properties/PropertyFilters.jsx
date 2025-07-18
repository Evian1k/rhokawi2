import React from 'react';
import { motion } from 'framer-motion';
import { Search, Filter } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const PropertyFilters = ({ filters, setFilters, resultsCount }) => {
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (name, value) => {
    // If the value is "all", treat it as an empty string for filtering purposes
    const filterValue = value === 'all' ? '' : value;
    setFilters(prev => ({ ...prev, [name]: filterValue }));
  };

  const clearFilters = () => {
    setFilters({
      searchTerm: '',
      priceRange: '',
      propertyType: '',
      location: '',
    });
  };

  return (
    <section className="py-8 bg-background border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="space-y-4"
        >
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-5 h-5" />
            <Input
              name="searchTerm"
              placeholder="Search properties by title, location, or type..."
              value={filters.searchTerm}
              onChange={handleInputChange}
              className="pl-10 h-12 text-lg"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Select value={filters.priceRange || 'all'} onValueChange={(value) => handleSelectChange('priceRange', value)}>
              <SelectTrigger>
                <SelectValue placeholder="Price Range" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Prices</SelectItem>
                <SelectItem value="0-5000000">Under KSh 5M</SelectItem>
                <SelectItem value="5000000-10000000">KSh 5M - 10M</SelectItem>
                <SelectItem value="10000000-20000000">KSh 10M - 20M</SelectItem>
                <SelectItem value="20000000-30000000">KSh 20M - 30M</SelectItem>
                <SelectItem value="30000000">Above KSh 30M</SelectItem>
              </SelectContent>
            </Select>

            <Select value={filters.propertyType || 'all'} onValueChange={(value) => handleSelectChange('propertyType', value)}>
              <SelectTrigger>
                <SelectValue placeholder="Property Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="Apartment">Apartment</SelectItem>
                <SelectItem value="House">House</SelectItem>
                <SelectItem value="Villa">Villa</SelectItem>
                <SelectItem value="Townhouse">Townhouse</SelectItem>
                <SelectItem value="Penthouse">Penthouse</SelectItem>
                <SelectItem value="Bungalow">Bungalow</SelectItem>
                <SelectItem value="Studio">Studio</SelectItem>
                <SelectItem value="Duplex">Duplex</SelectItem>
                <SelectItem value="Mansion">Mansion</SelectItem>
              </SelectContent>
            </Select>

            <Input
              name="location"
              placeholder="Location"
              value={filters.location}
              onChange={handleInputChange}
            />

            <Button onClick={clearFilters} variant="outline" className="w-full">
              <Filter className="w-4 h-4 mr-2" />
              Clear Filters
            </Button>
          </div>

          <div className="text-muted-foreground">
            Showing {resultsCount} properties
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default PropertyFilters;
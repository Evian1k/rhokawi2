import React from 'react';
import { motion } from 'framer-motion';
import { Search } from 'lucide-react';
import { Button } from '@/components/ui/button';

const NoPropertiesFound = ({ onClearFilters }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="text-center py-12"
    >
      <div className="w-24 h-24 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
        <Search className="w-12 h-12 text-muted-foreground" />
      </div>
      <h3 className="text-xl font-semibold mb-2">No Properties Found</h3>
      <p className="text-muted-foreground mb-4">
        Try adjusting your search criteria or clearing the filters.
      </p>
      <Button onClick={onClearFilters} variant="outline">
        Clear All Filters
      </Button>
    </motion.div>
  );
};

export default NoPropertiesFound;
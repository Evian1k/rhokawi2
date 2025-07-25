import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { Toaster } from '@/components/ui/toaster';
import { ThemeProvider } from '@/contexts/ThemeContext';
import { AuthProvider } from '@/contexts/AuthContext';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import Home from '@/pages/Home';
import Properties from '@/pages/Properties';
import PropertyDetail from '@/pages/PropertyDetail';
import PropertyMap from '@/pages/PropertyMap';
import Contact from '@/pages/Contact';
import Login from '@/pages/Login';
import Dashboard from '@/pages/Dashboard';
import WhatsAppFloat from '@/components/WhatsAppFloat';
import ProtectedRoute from '@/components/ProtectedRoute';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <div className="min-h-screen flex flex-col bg-background text-foreground">
            <Helmet>
              <title>Rhokawi Properties Ltd - Premier Real Estate in Kenya</title>
              <meta name="description" content="Discover premium properties in Kenya with Rhokawi Properties Ltd. Your trusted partner for buying, selling, and renting real estate in Nairobi and beyond." />
            </Helmet>
            
            <Navbar />
            
            <main className="flex-grow">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/properties" element={<Properties />} />
                <Route path="/properties/:id" element={<PropertyDetail />} />
                <Route path="/property-map" element={<PropertyMap />} />
                <Route path="/contact" element={<Contact />} />
                
                {/* Secret admin access route - not linked anywhere publicly */}
                <Route path="/rhokawi-admin-access-portal-2025" element={<Login />} />
                
                <Route 
                  path="/dashboard" 
                  element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  } 
                />
              </Routes>
            </main>
            
            <Footer />
            <WhatsAppFloat />
            <Toaster />
          </div>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
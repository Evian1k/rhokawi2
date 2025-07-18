import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { 
  ArrowLeft, 
  MapPin, 
  Bed, 
  Bath, 
  Square, 
  Calendar, 
  Star,
  Phone,
  Mail,
  MessageCircle,
  CheckCircle,
  Camera,
  Share2,
  Heart
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/components/ui/use-toast';
import apiService from '@/lib/api';

const PropertyDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const { toast } = useToast();
  const [property, setProperty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [showContactForm, setShowContactForm] = useState(false);
  const [contactForm, setContactForm] = useState({
    name: '',
    email: '',
    phone: '',
    message: 'I am interested in purchasing this property. Please contact me with more details.'
  });

  useEffect(() => {
    fetchProperty();
  }, [id]);

  useEffect(() => {
    // Open contact form if navigated from property card
    if (location.state?.openContact) {
      setShowContactForm(true);
    }
  }, [location.state]);

  const fetchProperty = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getProperty(id);
      
      if (response.data) {
        setProperty(response.data);
      } else {
        setError('Property not found');
      }
    } catch (err) {
      console.error('Failed to fetch property:', err);
      setError(err.message || 'Failed to load property details');
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-KE', {
      style: 'currency',
      currency: 'KES',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  const handleContactSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiService.sendContactMessage({
        name: contactForm.name,
        email: contactForm.email,
        phone: contactForm.phone,
        message: contactForm.message,
        property_id: property.id
      });
      
      toast({
        title: "Message Sent Successfully!",
        description: "We'll contact you within 24 hours to discuss this property.",
      });
      
      setShowContactForm(false);
      setContactForm({
        name: '',
        email: '',
        phone: '',
        message: 'I am interested in purchasing this property. Please contact me with more details.'
      });
    } catch (error) {
      toast({
        title: "Failed to Send Message",
        description: error.message || "Please try again later.",
        variant: "destructive",
      });
    }
  };

  const handleBuyProperty = () => {
    setShowContactForm(true);
    setContactForm(prev => ({
      ...prev,
      message: `I would like to purchase the property "${property.title}" listed at ${formatPrice(property.price)}. Please contact me to proceed with the buying process.`
    }));
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: property.title,
          text: `Check out this property: ${property.title} in ${property.location}`,
          url: window.location.href,
        });
      } catch (err) {
        console.log('Error sharing:', err);
      }
    } else {
      // Fallback to copying URL
      navigator.clipboard.writeText(window.location.href);
      toast({
        title: "Link Copied!",
        description: "Property link copied to clipboard.",
      });
    }
  };

  const getDefaultImage = () => {
    return "https://images.unsplash.com/photo-1595872018818-97555653a011?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80";
  };

  const getPropertyImages = () => {
    if (property?.images && property.images.length > 0) {
      return property.images.map(img => 
        img.startsWith('http') ? img : `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/uploads/images/${img}`
      );
    }
    return [getDefaultImage()];
  };

  if (loading) {
    return (
      <div className="pt-16 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-red-600"></div>
          <p className="mt-4 text-lg">Loading property details...</p>
        </div>
      </div>
    );
  }

  if (error || !property) {
    return (
      <div className="pt-16 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">Property Not Found</h2>
          <p className="text-muted-foreground mb-6">{error || 'This property may have been sold or removed.'}</p>
          <Button onClick={() => navigate('/properties')} className="bg-red-600 hover:bg-red-700">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Properties
          </Button>
        </div>
      </div>
    );
  }

  const images = getPropertyImages();

  return (
    <>
      <Helmet>
        <title>{property.title} - Rhokawi Properties Ltd</title>
        <meta name="description" content={`${property.description} Located in ${property.location}. Price: ${formatPrice(property.price)}`} />
      </Helmet>

      <div className="pt-16">
        {/* Navigation Bar */}
        <div className="bg-white border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <Button 
                variant="outline" 
                onClick={() => navigate('/properties')}
                className="flex items-center"
              >
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to Properties
              </Button>
              
              <div className="flex gap-2">
                <Button variant="outline" size="sm" onClick={handleShare}>
                  <Share2 className="h-4 w-4" />
                </Button>
                <Button variant="outline" size="sm">
                  <Heart className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Property Images */}
        <section className="relative">
          <div className="grid grid-cols-1 lg:grid-cols-4 lg:grid-rows-2 gap-2 h-[500px]">
            {/* Main Image */}
            <div className="lg:col-span-2 lg:row-span-2 relative">
              <img
                src={images[currentImageIndex]}
                alt={property.title}
                className="w-full h-full object-cover rounded-lg cursor-pointer"
                onClick={() => setCurrentImageIndex(0)}
              />
              <div className="absolute bottom-4 left-4 bg-black/50 text-white px-3 py-1 rounded-full flex items-center">
                <Camera className="w-4 h-4 mr-1" />
                {images.length} Photos
              </div>
            </div>
            
            {/* Thumbnail Images */}
            {images.slice(1, 5).map((image, index) => (
              <div key={index} className="relative">
                <img
                  src={image}
                  alt={`${property.title} - ${index + 2}`}
                  className="w-full h-full object-cover rounded-lg cursor-pointer hover:opacity-80 transition-opacity"
                  onClick={() => setCurrentImageIndex(index + 1)}
                />
              </div>
            ))}
          </div>
        </section>

        {/* Property Information */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
              >
                <div className="flex flex-wrap items-center gap-2 mb-4">
                  <Badge variant="secondary">{property.property_type}</Badge>
                  <Badge variant="secondary">{property.status}</Badge>
                  {property.is_verified && (
                    <Badge className="bg-green-100 text-green-800">
                      <CheckCircle className="w-3 h-3 mr-1" />
                      Verified
                    </Badge>
                  )}
                </div>

                <h1 className="text-3xl md:text-4xl font-bold mb-4">{property.title}</h1>
                
                <div className="flex items-center text-muted-foreground mb-6">
                  <MapPin className="w-5 h-5 mr-2" />
                  <span className="text-lg">{property.location}</span>
                  {property.address && (
                    <span className="ml-2">• {property.address}</span>
                  )}
                </div>

                <div className="text-4xl font-bold text-red-600 mb-8">
                  {formatPrice(property.price)}
                </div>

                {/* Property Stats */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                  {property.bedrooms && (
                    <div className="flex items-center space-x-2">
                      <Bed className="w-5 h-5 text-red-600" />
                      <span className="font-semibold">{property.bedrooms}</span>
                      <span className="text-muted-foreground">Bedrooms</span>
                    </div>
                  )}
                  {property.bathrooms && (
                    <div className="flex items-center space-x-2">
                      <Bath className="w-5 h-5 text-red-600" />
                      <span className="font-semibold">{property.bathrooms}</span>
                      <span className="text-muted-foreground">Bathrooms</span>
                    </div>
                  )}
                  {property.square_feet && (
                    <div className="flex items-center space-x-2">
                      <Square className="w-5 h-5 text-red-600" />
                      <span className="font-semibold">{property.square_feet}</span>
                      <span className="text-muted-foreground">Sq Ft</span>
                    </div>
                  )}
                  {property.year_built && (
                    <div className="flex items-center space-x-2">
                      <Calendar className="w-5 h-5 text-red-600" />
                      <span className="font-semibold">{property.year_built}</span>
                      <span className="text-muted-foreground">Built</span>
                    </div>
                  )}
                </div>

                {/* Description */}
                <div className="mb-8">
                  <h2 className="text-2xl font-bold mb-4">Description</h2>
                  <p className="text-muted-foreground leading-relaxed">
                    {property.description || "No description available for this property."}
                  </p>
                </div>

                {/* Features */}
                {property.features && property.features.length > 0 && (
                  <div className="mb-8">
                    <h2 className="text-2xl font-bold mb-4">Features</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {property.features.map((feature, index) => (
                        <div key={index} className="flex items-center">
                          <CheckCircle className="w-4 h-4 text-green-600 mr-2" />
                          <span>{feature}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Property Details */}
                <div className="mb-8">
                  <h2 className="text-2xl font-bold mb-4">Property Details</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {property.lot_size && (
                      <div className="flex justify-between py-2 border-b">
                        <span className="font-medium">Lot Size:</span>
                        <span>{property.lot_size}</span>
                      </div>
                    )}
                    <div className="flex justify-between py-2 border-b">
                      <span className="font-medium">Property Type:</span>
                      <span>{property.property_type}</span>
                    </div>
                    <div className="flex justify-between py-2 border-b">
                      <span className="font-medium">Status:</span>
                      <span className="capitalize">{property.status}</span>
                    </div>
                    <div className="flex justify-between py-2 border-b">
                      <span className="font-medium">Listed:</span>
                      <span>{new Date(property.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
              </motion.div>
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <Card className="sticky top-24">
                  <CardContent className="p-6">
                    <div className="text-center mb-6">
                      <div className="text-3xl font-bold text-red-600 mb-2">
                        {formatPrice(property.price)}
                      </div>
                      <p className="text-muted-foreground">Ready to Move In</p>
                    </div>

                    <div className="space-y-3 mb-6">
                      <Button 
                        className="w-full bg-red-600 hover:bg-red-700 text-lg py-6"
                        onClick={handleBuyProperty}
                      >
                        <Phone className="mr-2 h-5 w-5" />
                        Buy This Property
                      </Button>
                      
                      <Button 
                        variant="outline" 
                        className="w-full py-3"
                        onClick={() => setShowContactForm(true)}
                      >
                        <MessageCircle className="mr-2 h-4 w-4" />
                        Request Info
                      </Button>
                      
                      <Button 
                        variant="outline" 
                        className="w-full py-3"
                        onClick={() => window.open(`https://wa.me/254700000000?text=I'm interested in the property: ${property.title}`, '_blank')}
                      >
                        <MessageCircle className="mr-2 h-4 w-4" />
                        WhatsApp
                      </Button>
                    </div>

                    {/* Agent Info */}
                    {property.admin && (
                      <div className="border-t pt-6">
                        <h3 className="font-semibold mb-3">Listed by</h3>
                        <div className="flex items-center space-x-3">
                          <div className="w-12 h-12 bg-red-600 text-white rounded-full flex items-center justify-center font-bold">
                            {property.admin.name ? property.admin.name.charAt(0) : 'A'}
                          </div>
                          <div>
                            <p className="font-medium">{property.admin.name || 'Admin'}</p>
                            <p className="text-sm text-muted-foreground">Rhokawi Properties</p>
                          </div>
                        </div>
                        <div className="mt-4 space-y-2">
                          <Button variant="outline" size="sm" className="w-full">
                            <Phone className="mr-2 h-3 w-3" />
                            Call Agent
                          </Button>
                          <Button variant="outline" size="sm" className="w-full">
                            <Mail className="mr-2 h-3 w-3" />
                            Email Agent
                          </Button>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Contact Form Modal */}
        {showContactForm && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
              <h3 className="text-lg font-semibold mb-4">Contact Us About This Property</h3>
              <form onSubmit={handleContactSubmit} className="space-y-4">
                <div>
                  <input
                    type="text"
                    placeholder="Your Name"
                    value={contactForm.name}
                    onChange={(e) => setContactForm({ ...contactForm, name: e.target.value })}
                    className="w-full p-3 border rounded-lg"
                    required
                  />
                </div>
                <div>
                  <input
                    type="email"
                    placeholder="Your Email"
                    value={contactForm.email}
                    onChange={(e) => setContactForm({ ...contactForm, email: e.target.value })}
                    className="w-full p-3 border rounded-lg"
                    required
                  />
                </div>
                <div>
                  <input
                    type="tel"
                    placeholder="Your Phone Number"
                    value={contactForm.phone}
                    onChange={(e) => setContactForm({ ...contactForm, phone: e.target.value })}
                    className="w-full p-3 border rounded-lg"
                  />
                </div>
                <div>
                  <textarea
                    placeholder="Your message..."
                    value={contactForm.message}
                    onChange={(e) => setContactForm({ ...contactForm, message: e.target.value })}
                    className="w-full p-3 border rounded-lg h-24"
                    required
                  />
                </div>
                <div className="flex gap-2">
                  <Button type="submit" className="flex-1 bg-red-600 hover:bg-red-700">
                    Send Message
                  </Button>
                  <Button 
                    type="button" 
                    variant="outline" 
                    onClick={() => setShowContactForm(false)}
                    className="flex-1"
                  >
                    Cancel
                  </Button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default PropertyDetail;
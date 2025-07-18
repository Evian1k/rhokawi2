
    import React from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { ArrowRight, Star, Users, Home as HomeIcon, Award, MapPin } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import PropertyCard from '@/components/PropertyCard';

const Home = () => {
  const stats = [
    { number: '500+', label: 'Properties Listed', icon: HomeIcon },
    { number: '98%', label: 'Client Satisfaction', icon: Star },
    { number: '1000+', label: 'Happy Clients', icon: Users },
    { number: '15+', label: 'Years Experience', icon: Award },
  ];

  const featuredProperties = [
    {
      id: 1,
      title: 'Modern Villa in Karen',
      price: 25000000,
      location: 'Karen, Nairobi',
      bedrooms: 4,
      bathrooms: 3,
      area: 350,
      featured: true,
      images: ['https://images.unsplash.com/photo-1613490493576-7fde63acd811?q=80&w=2071&auto=format&fit=crop', 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?q=80&w=1974&auto=format&fit=crop'],
      description: 'Stunning modern villa with premium finishes, swimming pool, and landscaped garden.'
    },
    {
      id: 2,
      title: 'Executive Apartment',
      price: 8500000,
      location: 'Westlands, Nairobi',
      bedrooms: 3,
      bathrooms: 2,
      area: 180,
      featured: true,
      images: ['https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?q=80&w=2070&auto=format&fit=crop', 'https://images.unsplash.com/photo-1494203484021-3c454daf695d?q=80&w=2070&auto=format&fit=crop'],
      description: 'Luxurious apartment with panoramic city views and modern amenities.'
    },
    {
      id: 3,
      title: 'Family Home in Runda',
      price: 18000000,
      location: 'Runda, Nairobi',
      bedrooms: 5,
      bathrooms: 4,
      area: 280,
      featured: true,
      images: ['https://images.unsplash.com/photo-1570129477492-45c003edd2be?q=80&w=2070&auto=format&fit=crop', 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2070&auto=format&fit=crop'],
      description: 'Perfect family home with spacious rooms and beautiful garden.'
    }
  ];

  const testimonials = [
    {
      name: 'Sarah Wanjiku',
      role: 'Property Buyer',
      content: 'Rhokawi Properties made my dream of owning a home come true. Their professional service and attention to detail is unmatched.',
      rating: 5
    },
    {
      name: 'John Mwangi',
      role: 'Property Investor',
      content: 'I have worked with Rhokawi Properties on multiple investments. They consistently deliver excellent results and valuable insights.',
      rating: 5
    },
    {
      name: 'Grace Akinyi',
      role: 'First-time Buyer',
      content: 'The team guided me through every step of the buying process. I felt supported and confident throughout the entire journey.',
      rating: 5
    }
  ];

  return (
    <>
      <Helmet>
        <title>Rhokawi Properties Ltd - Premier Real Estate in Kenya</title>
        <meta name="description" content="Discover premium properties in Kenya with Rhokawi Properties Ltd. Your trusted partner for buying, selling, and renting real estate in Nairobi and beyond." />
      </Helmet>

      <div className="pt-16">
        <section className="relative min-h-[calc(100vh-4rem)] flex items-center justify-center overflow-hidden">
          <div className="absolute inset-0 hero-gradient"></div>
          <div className="absolute inset-0 bg-black/40"></div>
          
          <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="space-y-8"
            >
              <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold leading-tight">
                Find Your Dream
                <span className="block text-red-400">Property Today</span>
              </h1>
              
              <p className="text-xl md:text-2xl max-w-3xl mx-auto text-gray-200">
                Discover premium real estate opportunities in Kenya with Rhokawi Properties Ltd. 
                Your trusted partner for exceptional properties and professional service.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <Link to="/properties">
                  <Button size="lg" className="bg-red-600 hover:bg-red-700 text-white px-8 py-3 text-lg">
                    Browse Properties
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
                <Link to="/contact">
                  <Button variant="outline" size="lg" className="border-white text-white hover:bg-white hover:text-black px-8 py-3 text-lg">
                    Contact Us
                  </Button>
                </Link>
              </div>
            </motion.div>
          </div>

          <div className="absolute top-20 left-10 w-20 h-20 bg-red-500/20 rounded-full animate-float"></div>
          <div className="absolute bottom-20 right-10 w-16 h-16 bg-white/10 rounded-full animate-float" style={{ animationDelay: '2s' }}></div>
          <div className="absolute top-1/2 left-20 w-12 h-12 bg-red-400/30 rounded-full animate-float" style={{ animationDelay: '4s' }}></div>
        </section>

        <section className="section-padding bg-background">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="text-center"
                >
                  <div className="flex justify-center mb-4">
                    <div className="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center">
                      <stat.icon className="w-8 h-8 text-red-600" />
                    </div>
                  </div>
                  <div className="stats-counter">{stat.number}</div>
                  <p className="text-muted-foreground font-medium">{stat.label}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        <section className="section-padding bg-muted/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Why Choose <span className="gradient-text">Rhokawi Properties</span>
              </h2>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
                We combine years of experience with innovative technology to deliver exceptional real estate services
              </p>
            </motion.div>

            <div className="grid md:grid-cols-3 gap-8">
              {[
                { title: 'Expert Knowledge', description: 'Our team has deep understanding of the Kenyan real estate market with over 15 years of experience.', icon: Award },
                { title: 'Personalized Service', description: 'We provide tailored solutions that match your specific needs and budget requirements.', icon: Users },
                { title: 'Prime Locations', description: 'Access to the best properties in Nairobi and surrounding areas with verified ownership.', icon: MapPin }
              ].map((feature, index) => (
                <motion.div key={index} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, delay: index * 0.2 }} viewport={{ once: true }}>
                  <Card className="h-full hover:shadow-lg transition-shadow">
                    <CardContent className="p-6 text-center">
                      <div className="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                        <feature.icon className="w-8 h-8 text-red-600" />
                      </div>
                      <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                      <p className="text-muted-foreground">{feature.description}</p>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        <section className="section-padding bg-background">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }} viewport={{ once: true }} className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">Featured <span className="gradient-text">Properties</span></h2>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">Discover our handpicked selection of premium properties</p>
            </motion.div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {featuredProperties.map((property, index) => (
                <PropertyCard key={property.id} property={property} index={index} />
              ))}
            </div>
            <div className="text-center mt-12">
              <Link to="/properties">
                <Button size="lg" variant="outline" className="border-red-600 text-red-600 hover:bg-red-600 hover:text-white">
                  View All Properties <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
          </div>
        </section>

        <section className="section-padding bg-muted/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }} viewport={{ once: true }} className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">What Our <span className="gradient-text">Clients Say</span></h2>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">Don't just take our word for it - hear from our satisfied clients</p>
            </motion.div>
            <div className="grid md:grid-cols-3 gap-8">
              {testimonials.map((testimonial, index) => (
                <motion.div key={index} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, delay: index * 0.2 }} viewport={{ once: true }}>
                  <Card className="h-full">
                    <CardContent className="p-6">
                      <div className="flex mb-4">{[...Array(testimonial.rating)].map((_, i) => <Star key={i} className="w-5 h-5 fill-yellow-400 text-yellow-400" />)}</div>
                      <p className="text-muted-foreground mb-6 italic">"{testimonial.content}"</p>
                      <div>
                        <p className="font-semibold">{testimonial.name}</p>
                        <p className="text-sm text-muted-foreground">{testimonial.role}</p>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        <section className="section-padding bg-gradient-to-r from-red-600 to-red-800 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }} viewport={{ once: true }} className="space-y-8">
              <h2 className="text-3xl md:text-4xl font-bold">Ready to Find Your Dream Property?</h2>
              <p className="text-xl max-w-3xl mx-auto opacity-90">Let our experienced team help you navigate the real estate market and find the perfect property for your needs.</p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <Link to="/contact">
                  <Button size="lg" variant="secondary" className="px-8 py-3 text-lg">
                    Get Started Today <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
              </div>
            </motion.div>
          </div>
        </section>
      </div>
    </>
  );
};

export default Home;
  
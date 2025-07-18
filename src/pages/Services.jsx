
import React from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { Home, Key, TrendingUp, Users, Shield, Search, Calculator, FileText } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';

const Services = () => {
  const mainServices = [
    {
      icon: Home,
      title: 'Property Sales',
      description: 'Expert assistance in buying and selling residential and commercial properties with comprehensive market analysis and negotiation support.',
      features: ['Market Valuation', 'Property Marketing', 'Negotiation Support', 'Legal Assistance']
    },
    {
      icon: Key,
      title: 'Property Rentals',
      description: 'Complete rental services for landlords and tenants, including property listing, tenant screening, and lease management.',
      features: ['Tenant Screening', 'Lease Management', 'Property Listing', 'Rental Collection']
    },
    {
      icon: TrendingUp,
      title: 'Investment Advisory',
      description: 'Strategic real estate investment guidance to help you build a profitable property portfolio with expert market insights.',
      features: ['Market Analysis', 'ROI Calculations', 'Portfolio Planning', 'Risk Assessment']
    },
    {
      icon: Users,
      title: 'Property Management',
      description: 'Comprehensive property management services to maximize your investment returns while minimizing your involvement.',
      features: ['Maintenance Coordination', 'Tenant Relations', 'Financial Reporting', '24/7 Support']
    }
  ];

  const additionalServices = [
    {
      icon: Shield,
      title: 'Legal Services',
      description: 'Complete legal support for all property transactions including title verification and documentation.'
    },
    {
      icon: Search,
      title: 'Property Search',
      description: 'Personalized property search services to find properties that match your specific requirements.'
    },
    {
      icon: Calculator,
      title: 'Mortgage Advisory',
      description: 'Expert guidance on mortgage options and financing solutions for your property purchase.'
    },
    {
      icon: FileText,
      title: 'Documentation',
      description: 'Professional handling of all property-related documentation and paperwork.'
    }
  ];

  const process = [
    {
      step: '01',
      title: 'Initial Consultation',
      description: 'We start with understanding your needs, budget, and preferences through a detailed consultation.'
    },
    {
      step: '02',
      title: 'Property Search/Listing',
      description: 'Based on your requirements, we either search for suitable properties or list your property for sale/rent.'
    },
    {
      step: '03',
      title: 'Viewing & Evaluation',
      description: 'We arrange property viewings and provide professional evaluation and market analysis.'
    },
    {
      step: '04',
      title: 'Negotiation & Closing',
      description: 'We handle negotiations and guide you through the closing process with legal support.'
    }
  ];

  return (
    <>
      <Helmet>
        <title>Our Services - Rhokawi Properties Ltd</title>
        <meta name="description" content="Explore comprehensive real estate services offered by Rhokawi Properties Ltd including property sales, rentals, investment advisory, and property management in Kenya." />
      </Helmet>

      <div className="pt-16">
        {/* Hero Section */}
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
                Our Services
              </h1>
              <p className="text-xl md:text-2xl max-w-3xl mx-auto opacity-90">
                Comprehensive real estate solutions tailored to meet all your property needs in Kenya.
              </p>
            </motion.div>
          </div>
        </section>

        {/* Main Services Section */}
        <section className="section-padding bg-background">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Core <span className="gradient-text">Services</span>
              </h2>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
                Professional real estate services designed to deliver exceptional results
              </p>
            </motion.div>

            <div className="grid md:grid-cols-2 gap-8">
              {mainServices.map((service, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                >
                  <Card className="h-full hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center mb-4">
                        <service.icon className="w-8 h-8 text-red-600" />
                      </div>
                      <CardTitle className="text-xl">{service.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-muted-foreground mb-6">{service.description}</p>
                      <div className="space-y-2">
                        <h4 className="font-semibold text-sm">Key Features:</h4>
                        <ul className="space-y-1">
                          {service.features.map((feature, idx) => (
                            <li key={idx} className="text-sm text-muted-foreground flex items-center">
                              <div className="w-1.5 h-1.5 bg-red-600 rounded-full mr-2"></div>
                              {feature}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Additional Services Section */}
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
                Additional <span className="gradient-text">Services</span>
              </h2>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
                Supporting services to ensure a complete real estate experience
              </p>
            </motion.div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {additionalServices.map((service, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                >
                  <Card className="h-full text-center hover:shadow-lg transition-shadow">
                    <CardContent className="p-6">
                      <div className="w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                        <service.icon className="w-6 h-6 text-red-600" />
                      </div>
                      <h3 className="font-semibold mb-2">{service.title}</h3>
                      <p className="text-sm text-muted-foreground">{service.description}</p>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Process Section */}
        <section className="section-padding bg-background">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Our <span className="gradient-text">Process</span>
              </h2>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
                A streamlined approach to ensure smooth and successful transactions
              </p>
            </motion.div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {process.map((step, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.2 }}
                  viewport={{ once: true }}
                  className="text-center"
                >
                  <div className="relative mb-6">
                    <div className="w-20 h-20 bg-gradient-to-br from-red-600 to-red-800 rounded-full flex items-center justify-center mx-auto text-white text-xl font-bold">
                      {step.step}
                    </div>
                    {index < process.length - 1 && (
                      <div className="hidden lg:block absolute top-10 left-full w-full h-0.5 bg-red-200 dark:bg-red-800 -translate-x-10"></div>
                    )}
                  </div>
                  <h3 className="text-lg font-semibold mb-3">{step.title}</h3>
                  <p className="text-muted-foreground">{step.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Why Choose Our Services Section */}
        <section className="section-padding bg-muted/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <motion.div
                initial={{ opacity: 0, x: -30 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8 }}
                viewport={{ once: true }}
              >
                <h2 className="text-3xl md:text-4xl font-bold mb-6">
                  Why Choose Our <span className="gradient-text">Services</span>
                </h2>
                <div className="space-y-6">
                  <div className="flex items-start space-x-4">
                    <div className="w-6 h-6 bg-red-600 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <div className="w-2 h-2 bg-white rounded-full"></div>
                    </div>
                    <div>
                      <h3 className="font-semibold mb-2">Expert Knowledge</h3>
                      <p className="text-muted-foreground">15+ years of experience in the Kenyan real estate market with deep local insights.</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <div className="w-6 h-6 bg-red-600 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <div className="w-2 h-2 bg-white rounded-full"></div>
                    </div>
                    <div>
                      <h3 className="font-semibold mb-2">Personalized Approach</h3>
                      <p className="text-muted-foreground">Tailored solutions that match your specific needs, budget, and timeline.</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <div className="w-6 h-6 bg-red-600 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <div className="w-2 h-2 bg-white rounded-full"></div>
                    </div>
                    <div>
                      <h3 className="font-semibold mb-2">End-to-End Support</h3>
                      <p className="text-muted-foreground">Complete assistance from initial consultation to final transaction and beyond.</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-4">
                    <div className="w-6 h-6 bg-red-600 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <div className="w-2 h-2 bg-white rounded-full"></div>
                    </div>
                    <div>
                      <h3 className="font-semibold mb-2">Proven Track Record</h3>
                      <p className="text-muted-foreground">Over 1000 successful transactions with 98% client satisfaction rate.</p>
                    </div>
                  </div>
                </div>
              </motion.div>
              
              <motion.div
                initial={{ opacity: 0, x: 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8 }}
                viewport={{ once: true }}
                className="relative"
              >
                <img  
                  className="w-full h-96 object-cover rounded-lg shadow-lg"
                  alt="Professional real estate consultation meeting"
                 src="https://images.unsplash.com/photo-1675270714610-11a5cadcc7b3" />
              </motion.div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="section-padding bg-gradient-to-r from-red-600 to-red-800 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="space-y-8"
            >
              <h2 className="text-3xl md:text-4xl font-bold">
                Ready to Get Started?
              </h2>
              <p className="text-xl max-w-3xl mx-auto opacity-90">
                Let us help you achieve your real estate goals with our comprehensive services and expert guidance.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <Link to="/contact">
                  <Button size="lg" variant="secondary" className="px-8 py-3 text-lg">
                    Contact Us Today
                  </Button>
                </Link>
                <Link to="/properties">
                  <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-red-600 px-8 py-3 text-lg">
                    View Properties
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

export default Services;

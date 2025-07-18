
import React from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { Award, Users, Target, Heart, MapPin, Phone, Mail } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

const About = () => {
  const values = [
    {
      icon: Target,
      title: 'Excellence',
      description: 'We strive for excellence in every transaction, ensuring the highest standards of service and professionalism.'
    },
    {
      icon: Heart,
      title: 'Integrity',
      description: 'We conduct our business with honesty, transparency, and ethical practices that build lasting trust.'
    },
    {
      icon: Users,
      title: 'Client-Focused',
      description: 'Our clients are at the heart of everything we do. We listen, understand, and deliver personalized solutions.'
    },
    {
      icon: Award,
      title: 'Innovation',
      description: 'We embrace modern technology and innovative approaches to enhance the real estate experience.'
    }
  ];

  const team = [
    {
      name: 'David Rhokawi',
      role: 'Founder & CEO',
      description: 'With over 15 years in real estate, David leads our vision of transforming property experiences in Kenya.',
      image: 'Professional headshot of David Rhokawi, CEO of Rhokawi Properties'
    },
    {
      name: 'Sarah Wanjiku',
      role: 'Head of Sales',
      description: 'Sarah brings 10+ years of sales expertise, helping clients find their perfect properties with personalized service.',
      image: 'Professional headshot of Sarah Wanjiku, Head of Sales'
    },
    {
      name: 'John Mwangi',
      role: 'Property Manager',
      description: 'John oversees our property management services, ensuring optimal value and maintenance for all properties.',
      image: 'Professional headshot of John Mwangi, Property Manager'
    }
  ];

  return (
    <>
      <Helmet>
        <title>About Us - Rhokawi Properties Ltd</title>
        <meta name="description" content="Learn about Rhokawi Properties Ltd, Kenya's premier real estate company. Discover our mission, values, and experienced team dedicated to exceptional property services." />
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
                About Rhokawi Properties
              </h1>
              <p className="text-xl md:text-2xl max-w-3xl mx-auto opacity-90">
                Building dreams, creating communities, and transforming lives through exceptional real estate services in Kenya.
              </p>
            </motion.div>
          </div>
        </section>

        {/* Our Story Section */}
        <section className="section-padding bg-background">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <motion.div
                initial={{ opacity: 0, x: -30 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8 }}
                viewport={{ once: true }}
              >
                <h2 className="text-3xl md:text-4xl font-bold mb-6">
                  Our <span className="gradient-text">Story</span>
                </h2>
                <div className="space-y-4 text-muted-foreground">
                  <p>
                    Founded in 2009, Rhokawi Properties Ltd began with a simple yet powerful vision: to revolutionize the real estate experience in Kenya. What started as a small family business has grown into one of the most trusted names in Kenyan real estate.
                  </p>
                  <p>
                    Over the years, we have helped thousands of families find their dream homes, assisted investors in building profitable portfolios, and contributed to the development of thriving communities across Nairobi and beyond.
                  </p>
                  <p>
                    Our success is built on a foundation of trust, expertise, and an unwavering commitment to our clients. We understand that buying or selling property is one of life's most significant decisions, and we're honored to be part of that journey.
                  </p>
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
                  alt="Rhokawi Properties office building and team"
                 src="https://images.unsplash.com/photo-1658022136407-e5bc0433f053" />
                <div className="absolute -bottom-6 -left-6 w-24 h-24 bg-red-600 rounded-lg flex items-center justify-center text-white">
                  <div className="text-center">
                    <div className="text-2xl font-bold">15+</div>
                    <div className="text-xs">Years</div>
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Mission & Vision Section */}
        <section className="section-padding bg-muted/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid md:grid-cols-2 gap-12">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                viewport={{ once: true }}
              >
                <Card className="h-full">
                  <CardContent className="p-8">
                    <div className="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center mb-6">
                      <Target className="w-8 h-8 text-red-600" />
                    </div>
                    <h3 className="text-2xl font-bold mb-4">Our Mission</h3>
                    <p className="text-muted-foreground">
                      To provide exceptional real estate services that exceed client expectations while contributing to the sustainable development of Kenya's property market. We are committed to integrity, innovation, and creating lasting value for all stakeholders.
                    </p>
                  </CardContent>
                </Card>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                viewport={{ once: true }}
              >
                <Card className="h-full">
                  <CardContent className="p-8">
                    <div className="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center mb-6">
                      <Award className="w-8 h-8 text-red-600" />
                    </div>
                    <h3 className="text-2xl font-bold mb-4">Our Vision</h3>
                    <p className="text-muted-foreground">
                      To be Kenya's leading real estate company, recognized for our professionalism, innovation, and positive impact on communities. We envision a future where every Kenyan has access to quality housing and investment opportunities.
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Values Section */}
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
                Our <span className="gradient-text">Values</span>
              </h2>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
                The principles that guide everything we do
              </p>
            </motion.div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {values.map((value, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                >
                  <Card className="h-full text-center hover:shadow-lg transition-shadow">
                    <CardContent className="p-6">
                      <div className="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                        <value.icon className="w-8 h-8 text-red-600" />
                      </div>
                      <h3 className="text-xl font-semibold mb-3">{value.title}</h3>
                      <p className="text-muted-foreground">{value.description}</p>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Team Section */}
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
                Meet Our <span className="gradient-text">Team</span>
              </h2>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
                Experienced professionals dedicated to your success
              </p>
            </motion.div>

            <div className="grid md:grid-cols-3 gap-8">
              {team.map((member, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.2 }}
                  viewport={{ once: true }}
                >
                  <Card className="overflow-hidden hover:shadow-lg transition-shadow">
                    <div className="relative h-64">
                      <img  
                        className="w-full h-full object-cover"
                        alt={member.name}
                       src="https://images.unsplash.com/photo-1644424235476-295f24d503d9" />
                    </div>
                    <CardContent className="p-6 text-center">
                      <h3 className="text-xl font-semibold mb-2">{member.name}</h3>
                      <p className="text-red-600 font-medium mb-3">{member.role}</p>
                      <p className="text-muted-foreground">{member.description}</p>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Contact CTA Section */}
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
                Ready to Work With Us?
              </h2>
              <p className="text-xl max-w-3xl mx-auto opacity-90">
                Experience the difference that expertise, integrity, and personalized service can make in your real estate journey.
              </p>
              <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
                <div className="flex flex-col items-center space-y-2">
                  <Phone className="w-8 h-8" />
                  <span className="font-semibold">Call Us</span>
                  <span>+254 713 663 866</span>
                </div>
                <div className="flex flex-col items-center space-y-2">
                  <Mail className="w-8 h-8" />
                  <span className="font-semibold">Email Us</span>
                  <span>info@rhokawiproperties.com</span>
                </div>
                <div className="flex flex-col items-center space-y-2">
                  <MapPin className="w-8 h-8" />
                  <span className="font-semibold">Visit Us</span>
                  <span>Imara Daima, Nairobi</span>
                </div>
              </div>
            </motion.div>
          </div>
        </section>
      </div>
    </>
  );
};

export default About;

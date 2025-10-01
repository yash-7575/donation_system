import { useState, useEffect } from 'react';
import { Heart, TrendingUp, Users, Gift, ChevronRight, Star, ArrowRight, Check } from 'lucide-react';
import Button from '../components/Button';
import Card from '../components/Card';
import { mockStatistics, mockFeedback } from '../data/mockData';

interface HomePageProps {
  onNavigate: (page: string) => void;
}

export default function HomePage({ onNavigate }: HomePageProps) {
  const [stats, setStats] = useState({ totalDonations: 0, totalRequests: 0, successfulMatches: 0, activeDonors: 0, familiesHelped: 0 });

  useEffect(() => {
    const animateNumbers = () => {
      const duration = 2000;
      const steps = 60;
      const increment = {
        totalDonations: mockStatistics.totalDonations / steps,
        totalRequests: mockStatistics.totalRequests / steps,
        successfulMatches: mockStatistics.successfulMatches / steps,
        activeDonors: mockStatistics.activeDonors / steps,
        familiesHelped: mockStatistics.familiesHelped / steps,
      };

      let currentStep = 0;
      const timer = setInterval(() => {
        currentStep++;
        if (currentStep >= steps) {
          setStats(mockStatistics);
          clearInterval(timer);
        } else {
          setStats({
            totalDonations: Math.floor(increment.totalDonations * currentStep),
            totalRequests: Math.floor(increment.totalRequests * currentStep),
            successfulMatches: Math.floor(increment.successfulMatches * currentStep),
            activeDonors: Math.floor(increment.activeDonors * currentStep),
            familiesHelped: Math.floor(increment.familiesHelped * currentStep),
          });
        }
      }, duration / steps);
    };

    animateNumbers();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-purple-50 to-cyan-50">
      <header className="fixed top-0 left-0 right-0 z-40 glass-effect">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 gradient-primary rounded-xl flex items-center justify-center">
              <Heart className="w-7 h-7 text-white" fill="white" />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-orange-600 to-purple-600 bg-clip-text text-transparent">
              GiveHope
            </span>
          </div>
          <nav className="hidden md:flex items-center space-x-8">
            <a href="#how-it-works" className="text-gray-700 hover:text-orange-600 font-medium transition-colors">How It Works</a>
            <a href="#impact" className="text-gray-700 hover:text-orange-600 font-medium transition-colors">Our Impact</a>
            <a href="#stories" className="text-gray-700 hover:text-orange-600 font-medium transition-colors">Success Stories</a>
            <a href="#feedback" className="text-gray-700 hover:text-orange-600 font-medium transition-colors">Testimonials</a>
          </nav>
          <Button onClick={() => onNavigate('login')} size="md">
            Get Started
          </Button>
        </div>
      </header>

      <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
        <div className="absolute inset-0 gradient-hero opacity-20" />
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-72 h-72 bg-orange-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float" />
          <div className="absolute top-40 right-10 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float" style={{ animationDelay: '1s' }} />
          <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-cyan-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float" style={{ animationDelay: '2s' }} />
        </div>

        <div className="relative container mx-auto px-6 text-center">
          <div className="animate-fade-in-up">
            <h1 className="text-5xl md:text-7xl font-extrabold text-gray-900 mb-6 leading-tight">
              Connecting Hearts,
              <br />
              <span className="bg-gradient-to-r from-orange-600 via-purple-600 to-cyan-600 bg-clip-text text-transparent">
                Changing Lives
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
              A revolutionary platform that bridges the gap between generous donors and families in need,
              facilitated by trusted NGOs making real impact in communities.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
              <Button size="lg" onClick={() => onNavigate('register')} className="group">
                Start Giving Today
                <ArrowRight className="inline-block ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button variant="outline" size="lg" onClick={() => onNavigate('register')}>
                I Need Help
              </Button>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 animate-fade-in" style={{ animationDelay: '0.2s' }}>
            <Card className="text-center">
              <Gift className="w-12 h-12 mx-auto mb-3 text-orange-600" />
              <div className="text-3xl font-bold text-gray-900 mb-1">{stats.totalDonations.toLocaleString()}</div>
              <div className="text-gray-600">Items Donated</div>
            </Card>
            <Card className="text-center">
              <Users className="w-12 h-12 mx-auto mb-3 text-purple-600" />
              <div className="text-3xl font-bold text-gray-900 mb-1">{stats.familiesHelped.toLocaleString()}</div>
              <div className="text-gray-600">Families Helped</div>
            </Card>
            <Card className="text-center">
              <TrendingUp className="w-12 h-12 mx-auto mb-3 text-cyan-600" />
              <div className="text-3xl font-bold text-gray-900 mb-1">{stats.successfulMatches.toLocaleString()}</div>
              <div className="text-gray-600">Successful Matches</div>
            </Card>
            <Card className="text-center">
              <Heart className="w-12 h-12 mx-auto mb-3 text-rose-600" />
              <div className="text-3xl font-bold text-gray-900 mb-1">{stats.activeDonors.toLocaleString()}</div>
              <div className="text-gray-600">Active Donors</div>
            </Card>
          </div>
        </div>
      </section>

      <section id="how-it-works" className="py-24 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16 animate-fade-in-up">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">How It Works</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              A simple, transparent process that ensures your donations reach those who need them most
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 relative">
            <div className="hidden md:block absolute top-1/2 left-1/3 right-1/3 h-1 bg-gradient-to-r from-orange-500 via-purple-500 to-cyan-500 -translate-y-1/2" style={{ width: 'calc(66.666% - 4rem)', left: 'calc(16.666% + 2rem)' }} />

            <div className="relative animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
              <Card className="text-center relative z-10">
                <div className="w-20 h-20 gradient-primary rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse-glow">
                  <Gift className="w-10 h-10 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">1. Donate</h3>
                <p className="text-gray-600 leading-relaxed">
                  Donors register and list items they want to give away. Upload photos, describe the item, and choose delivery options.
                </p>
              </Card>
            </div>

            <div className="relative animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <Card className="text-center relative z-10">
                <div className="w-20 h-20 gradient-secondary rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse-glow" style={{ animationDelay: '0.5s' }}>
                  <Users className="w-10 h-10 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">2. Match</h3>
                <p className="text-gray-600 leading-relaxed">
                  NGO administrators review donations and requests, then intelligently match items with families in need.
                </p>
              </Card>
            </div>

            <div className="relative animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
              <Card className="text-center relative z-10">
                <div className="w-20 h-20 gradient-accent rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse-glow" style={{ animationDelay: '1s' }}>
                  <Heart className="w-10 h-10 text-white" fill="white" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">3. Impact</h3>
                <p className="text-gray-600 leading-relaxed">
                  Items are delivered to recipients, creating real impact. Track your donation journey and receive heartfelt thanks.
                </p>
              </Card>
            </div>
          </div>
        </div>
      </section>

      <section id="impact" className="py-24 gradient-hero">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16 text-white animate-fade-in-up">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">Real-Time Impact Dashboard</h2>
            <p className="text-xl opacity-90 max-w-2xl mx-auto">
              Watch the difference we're making together, updated live across our community
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { label: 'Donations This Month', value: '156', icon: Gift, color: 'orange' },
              { label: 'Pending Matches', value: '23', icon: TrendingUp, color: 'purple' },
              { label: 'Families Helped This Week', value: '47', icon: Users, color: 'cyan' },
              { label: 'Active Volunteers', value: '89', icon: Heart, color: 'rose' },
              { label: 'Cities Reached', value: '34', icon: TrendingUp, color: 'green' },
              { label: 'Thank You Messages', value: '312', icon: Star, color: 'amber' },
            ].map((stat, index) => (
              <Card key={index} className="text-center animate-scale-in" style={{ animationDelay: `${index * 0.1}s` }}>
                <stat.icon className={`w-12 h-12 mx-auto mb-3 text-${stat.color}-600`} />
                <div className="text-4xl font-bold text-gray-900 mb-1">{stat.value}</div>
                <div className="text-gray-600">{stat.label}</div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section id="stories" className="py-24 bg-gradient-to-br from-purple-50 to-cyan-50">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16 animate-fade-in-up">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">Success Stories</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Real stories from real people whose lives have been transformed
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                image: 'https://images.pexels.com/photos/1416530/pexels-photo-1416530.jpeg?auto=compress&cs=tinysrgb&w=800',
                quote: "Thanks to GiveHope, my children have warm clothes for winter. The process was respectful and dignified. I'm forever grateful.",
                name: 'Maria Rodriguez',
                role: 'Recipient',
              },
              {
                image: 'https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=800',
                quote: "I've donated through many platforms, but GiveHope shows me exactly where my donations go. The impact is real and measurable.",
                name: 'David Chen',
                role: 'Donor',
              },
              {
                image: 'https://images.pexels.com/photos/3184405/pexels-photo-3184405.jpeg?auto=compress&cs=tinysrgb&w=800',
                quote: "This platform revolutionized how our NGO operates. We can now help more families efficiently and transparently.",
                name: 'Jennifer Smith',
                role: 'NGO Director',
              },
            ].map((story, index) => (
              <Card key={index} hover className="animate-fade-in-up" style={{ animationDelay: `${index * 0.1}s` }}>
                <div className="relative h-48 -m-6 mb-6 rounded-t-xl overflow-hidden">
                  <img src={story.image} alt={story.name} className="w-full h-full object-cover" />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
                </div>
                <div className="flex mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-amber-400 fill-amber-400" />
                  ))}
                </div>
                <p className="text-gray-700 mb-4 italic leading-relaxed">"{story.quote}"</p>
                <div className="flex items-center">
                  <div>
                    <div className="font-semibold text-gray-900">{story.name}</div>
                    <div className="text-sm text-gray-600">{story.role}</div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section id="feedback" className="py-24 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16 animate-fade-in-up">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">What People Say</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Hear from our community of donors, recipients, and NGO partners
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {mockFeedback.map((item, index) => (
              <Card key={item.id} hover className="animate-scale-in" style={{ animationDelay: `${index * 0.1}s` }}>
                <div className="flex items-center mb-3">
                  <div className="w-12 h-12 gradient-primary rounded-full flex items-center justify-center text-white font-bold text-lg mr-3">
                    {item.userName.charAt(0)}
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900">{item.userName}</div>
                    <div className="text-sm text-gray-600 capitalize">{item.userRole.replace('_', ' ')}</div>
                  </div>
                </div>
                <div className="flex mb-3">
                  {[...Array(item.rating)].map((_, i) => (
                    <Star key={i} className="w-4 h-4 text-amber-400 fill-amber-400" />
                  ))}
                </div>
                <p className="text-gray-700 text-sm leading-relaxed">{item.comment}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section className="py-24 gradient-hero">
        <div className="container mx-auto px-6 text-center">
          <div className="animate-fade-in-up">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">Ready to Make a Difference?</h2>
            <p className="text-xl text-white opacity-90 mb-8 max-w-2xl mx-auto">
              Join thousands of people already creating positive change in their communities
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Button size="lg" variant="accent" onClick={() => onNavigate('register')} className="bg-white text-purple-600 hover:bg-gray-100">
                Register as Donor
              </Button>
              <Button size="lg" variant="outline" onClick={() => onNavigate('register')} className="border-white text-white hover:bg-white hover:text-purple-600">
                Register as Recipient
              </Button>
            </div>
          </div>
        </div>
      </section>

      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 gradient-primary rounded-lg flex items-center justify-center">
                  <Heart className="w-6 h-6 text-white" fill="white" />
                </div>
                <span className="text-xl font-bold">GiveHope</span>
              </div>
              <p className="text-gray-400 leading-relaxed">
                Connecting generous donors with families in need through trusted NGO partnerships.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Quick Links</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-white transition-colors">How It Works</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Success Stories</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">For Users</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Donor Resources</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Recipient Support</a></li>
                <li><a href="#" className="hover:text-white transition-colors">NGO Partners</a></li>
                <li><a href="#" className="hover:text-white transition-colors">FAQ</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Cookie Policy</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-gray-400">
            <p>&copy; 2024 GiveHope. All rights reserved. Made with love for communities in need.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

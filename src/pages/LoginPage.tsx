import { useState } from 'react';
import { Heart, Mail, Lock, ArrowLeft } from 'lucide-react';
import Button from '../components/Button';
import { useAuth } from '../context/AuthContext';
import { UserRole } from '../types';

interface LoginPageProps {
  onNavigate: (page: string) => void;
}

export default function LoginPage({ onNavigate }: LoginPageProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<UserRole>('donor');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const success = await login(email, password, role);
      if (success) {
        if (role === 'donor') onNavigate('donor-dashboard');
        else if (role === 'recipient') onNavigate('recipient-dashboard');
        else onNavigate('ngo-dashboard');
      } else {
        setError('Invalid credentials. Try: john@donor.com, sarah@recipient.com, or admin@ngo.org');
      }
    } catch (err) {
      setError('Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      <div className="hidden lg:flex lg:w-1/2 gradient-hero items-center justify-center p-12 relative overflow-hidden">
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-20 left-10 w-72 h-72 bg-white rounded-full mix-blend-overlay filter blur-3xl animate-float" />
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-white rounded-full mix-blend-overlay filter blur-3xl animate-float" style={{ animationDelay: '1s' }} />
        </div>
        <div className="relative text-white text-center max-w-md animate-fade-in-up">
          <div className="w-24 h-24 bg-white/20 backdrop-blur-sm rounded-3xl flex items-center justify-center mx-auto mb-8">
            <Heart className="w-14 h-14 text-white" fill="white" />
          </div>
          <h2 className="text-4xl font-bold mb-4">Welcome Back!</h2>
          <p className="text-xl opacity-90 leading-relaxed">
            Continue your journey of making a difference in people's lives. Every login brings you closer to creating real impact.
          </p>
          <div className="mt-12 space-y-4">
            <div className="flex items-center justify-center space-x-3 text-white/90">
              <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">✓</div>
              <span>Track your donation impact</span>
            </div>
            <div className="flex items-center justify-center space-x-3 text-white/90">
              <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">✓</div>
              <span>Connect with recipients</span>
            </div>
            <div className="flex items-center justify-center space-x-3 text-white/90">
              <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">✓</div>
              <span>Manage your contributions</span>
            </div>
          </div>
        </div>
      </div>

      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-gradient-to-br from-orange-50 via-purple-50 to-cyan-50">
        <div className="w-full max-w-md animate-fade-in">
          <button
            onClick={() => onNavigate('home')}
            className="flex items-center text-gray-600 hover:text-gray-900 mb-8 transition-colors"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Home
          </button>

          <div className="bg-white rounded-2xl shadow-xl p-8">
            <div className="text-center mb-8">
              <div className="w-16 h-16 gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Heart className="w-9 h-9 text-white" fill="white" />
              </div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Sign In</h1>
              <p className="text-gray-600">Access your GiveHope account</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  I am a
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { value: 'donor', label: 'Donor' },
                    { value: 'recipient', label: 'Recipient' },
                    { value: 'ngo_admin', label: 'NGO Admin' },
                  ].map((option) => (
                    <button
                      key={option.value}
                      type="button"
                      onClick={() => setRole(option.value as UserRole)}
                      className={`py-3 px-4 rounded-lg font-medium transition-all ${
                        role === option.value
                          ? 'gradient-primary text-white shadow-lg'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {option.label}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-11 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 focus:ring-2 focus:ring-orange-200 transition-all"
                    placeholder="you@example.com"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full pl-11 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 focus:ring-2 focus:ring-orange-200 transition-all"
                    placeholder="••••••••"
                    required
                  />
                </div>
              </div>

              {error && (
                <div className="bg-red-50 border-2 border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                  {error}
                </div>
              )}

              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center">
                  <input type="checkbox" className="w-4 h-4 text-orange-600 rounded" />
                  <span className="ml-2 text-gray-600">Remember me</span>
                </label>
                <a href="#" className="text-orange-600 hover:text-orange-700 font-medium">
                  Forgot password?
                </a>
              </div>

              <Button type="submit" fullWidth size="lg" disabled={loading}>
                {loading ? 'Signing in...' : 'Sign In'}
              </Button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-gray-600">
                Don't have an account?{' '}
                <button
                  onClick={() => onNavigate('register')}
                  className="text-orange-600 hover:text-orange-700 font-semibold"
                >
                  Create Account
                </button>
              </p>
            </div>
          </div>

          <div className="mt-6 text-center text-sm text-gray-600">
            <p>Demo accounts: john@donor.com | sarah@recipient.com | admin@ngo.org</p>
          </div>
        </div>
      </div>
    </div>
  );
}

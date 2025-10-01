import { useState } from 'react';
import { Heart, User, Mail, Lock, Phone, MapPin, ArrowLeft, ArrowRight } from 'lucide-react';
import Button from '../components/Button';
import { useAuth } from '../context/AuthContext';
import { UserRole } from '../types';

interface RegisterPageProps {
  onNavigate: (page: string) => void;
}

export default function RegisterPage({ onNavigate }: RegisterPageProps) {
  const [step, setStep] = useState(1);
  const [role, setRole] = useState<UserRole>('donor');
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    country: '',
  });
  const [error, setError] = useState('');
  const { register } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    const success = await register({ ...formData, role }, formData.password);
    if (success) {
      if (role === 'donor') onNavigate('donor-dashboard');
      else if (role === 'recipient') onNavigate('recipient-dashboard');
      else onNavigate('ngo-dashboard');
    }
  };

  const updateFormData = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-orange-50 via-purple-50 to-cyan-50">
      <div className="hidden lg:flex lg:w-1/2 gradient-hero items-center justify-center p-12 relative overflow-hidden">
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-20 left-10 w-72 h-72 bg-white rounded-full mix-blend-overlay filter blur-3xl animate-float" />
        </div>
        <div className="relative text-white text-center max-w-md animate-fade-in">
          <Heart className="w-24 h-24 mx-auto mb-6 animate-bounce-subtle" fill="white" />
          <h2 className="text-4xl font-bold mb-4">Join Our Community</h2>
          <p className="text-xl opacity-90 leading-relaxed mb-8">
            Become part of a movement that's changing lives, one donation at a time.
          </p>
          <div className="space-y-4 text-left">
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 bg-white/30 rounded-full flex items-center justify-center mt-1">✓</div>
              <div>
                <div className="font-semibold">Make Real Impact</div>
                <div className="text-sm opacity-80">See exactly where your donations go</div>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 bg-white/30 rounded-full flex items-center justify-center mt-1">✓</div>
              <div>
                <div className="font-semibold">Transparent Process</div>
                <div className="text-sm opacity-80">Track every step of your contribution</div>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 bg-white/30 rounded-full flex items-center justify-center mt-1">✓</div>
              <div>
                <div className="font-semibold">Trusted Network</div>
                <div className="text-sm opacity-80">Verified NGOs and secure platform</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-2xl animate-fade-in">
          <button
            onClick={() => step === 1 ? onNavigate('home') : setStep(step - 1)}
            className="flex items-center text-gray-600 hover:text-gray-900 mb-8 transition-colors"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            {step === 1 ? 'Back to Home' : 'Previous Step'}
          </button>

          <div className="bg-white rounded-2xl shadow-xl p-8">
            <div className="text-center mb-8">
              <div className="w-16 h-16 gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Heart className="w-9 h-9 text-white" fill="white" />
              </div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Create Account</h1>
              <p className="text-gray-600">Step {step} of 3</p>
            </div>

            <div className="flex items-center mb-8">
              {[1, 2, 3].map((s) => (
                <div key={s} className="flex items-center flex-1">
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center font-bold transition-all ${
                      s <= step ? 'gradient-primary text-white' : 'bg-gray-200 text-gray-400'
                    }`}
                  >
                    {s}
                  </div>
                  {s < 3 && <div className={`flex-1 h-1 mx-2 ${s < step ? 'gradient-primary' : 'bg-gray-200'}`} />}
                </div>
              ))}
            </div>

            <form onSubmit={handleSubmit}>
              {step === 1 && (
                <div className="space-y-6 animate-fade-in">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-3">
                      Choose Your Role
                    </label>
                    <div className="grid gap-4">
                      {[
                        { value: 'donor', label: 'Donor', desc: 'I want to donate items to help others' },
                        { value: 'recipient', label: 'Recipient', desc: 'I need assistance with essential items' },
                        { value: 'ngo_admin', label: 'NGO Administrator', desc: 'I represent an organization' },
                      ].map((option) => (
                        <button
                          key={option.value}
                          type="button"
                          onClick={() => setRole(option.value as UserRole)}
                          className={`p-4 rounded-xl border-2 text-left transition-all ${
                            role === option.value
                              ? 'border-orange-500 bg-orange-50'
                              : 'border-gray-200 hover:border-gray-300'
                          }`}
                        >
                          <div className="font-semibold text-gray-900">{option.label}</div>
                          <div className="text-sm text-gray-600 mt-1">{option.desc}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                  <Button type="button" fullWidth size="lg" onClick={() => setStep(2)}>
                    Continue <ArrowRight className="inline ml-2 w-5 h-5" />
                  </Button>
                </div>
              )}

              {step === 2 && (
                <div className="space-y-4 animate-fade-in">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <input
                        type="text"
                        value={formData.fullName}
                        onChange={(e) => updateFormData('fullName', e.target.value)}
                        className="w-full pl-11 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 transition-all"
                        required
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Email Address</label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <input
                        type="email"
                        value={formData.email}
                        onChange={(e) => updateFormData('email', e.target.value)}
                        className="w-full pl-11 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 transition-all"
                        required
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Password</label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <input
                        type="password"
                        value={formData.password}
                        onChange={(e) => updateFormData('password', e.target.value)}
                        className="w-full pl-11 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 transition-all"
                        required
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Confirm Password</label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <input
                        type="password"
                        value={formData.confirmPassword}
                        onChange={(e) => updateFormData('confirmPassword', e.target.value)}
                        className="w-full pl-11 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 transition-all"
                        required
                      />
                    </div>
                  </div>
                  <Button type="button" fullWidth size="lg" onClick={() => setStep(3)}>
                    Continue <ArrowRight className="inline ml-2 w-5 h-5" />
                  </Button>
                </div>
              )}

              {step === 3 && (
                <div className="space-y-4 animate-fade-in">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Phone Number</label>
                    <div className="relative">
                      <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <input
                        type="tel"
                        value={formData.phone}
                        onChange={(e) => updateFormData('phone', e.target.value)}
                        className="w-full pl-11 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 transition-all"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Address</label>
                    <div className="relative">
                      <MapPin className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                      <input
                        type="text"
                        value={formData.address}
                        onChange={(e) => updateFormData('address', e.target.value)}
                        className="w-full pl-11 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 transition-all"
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">City</label>
                      <input
                        type="text"
                        value={formData.city}
                        onChange={(e) => updateFormData('city', e.target.value)}
                        className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 transition-all"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">State</label>
                      <input
                        type="text"
                        value={formData.state}
                        onChange={(e) => updateFormData('state', e.target.value)}
                        className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 transition-all"
                      />
                    </div>
                  </div>
                  {error && (
                    <div className="bg-red-50 border-2 border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                      {error}
                    </div>
                  )}
                  <Button type="submit" fullWidth size="lg">
                    Create Account
                  </Button>
                </div>
              )}
            </form>

            <div className="mt-6 text-center text-sm text-gray-600">
              Already have an account?{' '}
              <button
                onClick={() => onNavigate('login')}
                className="text-orange-600 hover:text-orange-700 font-semibold"
              >
                Sign In
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

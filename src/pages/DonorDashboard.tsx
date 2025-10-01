import { useState } from 'react';
import { Heart, Gift, TrendingUp, MessageSquare, User, LogOut, Plus, Upload, Package, CheckCircle, Clock, Truck } from 'lucide-react';
import Button from '../components/Button';
import Card from '../components/Card';
import Modal from '../components/Modal';
import { useAuth } from '../context/AuthContext';
import { mockDonations, mockMessages } from '../data/mockData';
import { ItemCategory, ItemCondition } from '../types';

interface DonorDashboardProps {
  onNavigate: (page: string) => void;
}

export default function DonorDashboard({ onNavigate }: DonorDashboardProps) {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [showDonateModal, setShowDonateModal] = useState(false);
  const [donationForm, setDonationForm] = useState({
    title: '',
    description: '',
    category: 'clothing' as ItemCategory,
    quantity: 1,
    condition: 'good' as ItemCondition,
    pickupAvailable: false,
    deliveryAvailable: false,
  });

  const handleLogout = () => {
    logout();
    onNavigate('home');
  };

  const userDonations = mockDonations.filter(d => d.donorId === user?.id);
  const userMessages = mockMessages.filter(m => m.recipientId === user?.id);

  const stats = {
    totalDonations: userDonations.length,
    itemsDelivered: userDonations.filter(d => d.status === 'delivered').length,
    impactScore: userDonations.length * 15,
    thankYouMessages: userMessages.length,
  };

  const statusColors = {
    pending: 'bg-yellow-100 text-yellow-800',
    approved: 'bg-blue-100 text-blue-800',
    matched: 'bg-purple-100 text-purple-800',
    in_transit: 'bg-cyan-100 text-cyan-800',
    delivered: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-purple-50 to-cyan-50 flex">
      <aside className="w-64 bg-white shadow-lg fixed h-full">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 gradient-primary rounded-xl flex items-center justify-center">
              <Heart className="w-7 h-7 text-white" fill="white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-orange-600 to-purple-600 bg-clip-text text-transparent">
              GiveHope
            </span>
          </div>
          <div className="flex items-center space-x-3 mt-4">
            <div className="w-10 h-10 gradient-secondary rounded-full flex items-center justify-center text-white font-bold">
              {user?.fullName.charAt(0)}
            </div>
            <div className="flex-1 min-w-0">
              <div className="font-semibold text-gray-900 truncate">{user?.fullName}</div>
              <div className="text-xs text-gray-500 truncate">Donor</div>
            </div>
          </div>
        </div>

        <nav className="p-4 space-y-2">
          {[
            { id: 'dashboard', icon: TrendingUp, label: 'Dashboard' },
            { id: 'donations', icon: Gift, label: 'My Donations' },
            { id: 'messages', icon: MessageSquare, label: 'Messages', badge: userMessages.filter(m => !m.read).length },
            { id: 'profile', icon: User, label: 'Profile' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                activeTab === item.id
                  ? 'gradient-primary text-white shadow-lg'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <item.icon className="w-5 h-5" />
              <span className="flex-1 text-left font-medium">{item.label}</span>
              {item.badge > 0 && (
                <span className="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">
                  {item.badge}
                </span>
              )}
            </button>
          ))}
        </nav>

        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
          <button
            onClick={handleLogout}
            className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-red-600 hover:bg-red-50 transition-all"
          >
            <LogOut className="w-5 h-5" />
            <span className="font-medium">Logout</span>
          </button>
        </div>
      </aside>

      <main className="flex-1 ml-64 p-8">
        {activeTab === 'dashboard' && (
          <div className="animate-fade-in">
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome back, {user?.fullName}!</h1>
              <p className="text-gray-600">Track your donations and see the impact you're making</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <Card className="animate-scale-in">
                <div className="flex items-center justify-between mb-2">
                  <Gift className="w-10 h-10 text-orange-600" />
                  <div className="text-right">
                    <div className="text-3xl font-bold text-gray-900">{stats.totalDonations}</div>
                    <div className="text-sm text-gray-600">Total Donations</div>
                  </div>
                </div>
              </Card>
              <Card className="animate-scale-in" style={{ animationDelay: '0.1s' }}>
                <div className="flex items-center justify-between mb-2">
                  <CheckCircle className="w-10 h-10 text-green-600" />
                  <div className="text-right">
                    <div className="text-3xl font-bold text-gray-900">{stats.itemsDelivered}</div>
                    <div className="text-sm text-gray-600">Items Delivered</div>
                  </div>
                </div>
              </Card>
              <Card className="animate-scale-in" style={{ animationDelay: '0.2s' }}>
                <div className="flex items-center justify-between mb-2">
                  <TrendingUp className="w-10 h-10 text-purple-600" />
                  <div className="text-right">
                    <div className="text-3xl font-bold text-gray-900">{stats.impactScore}</div>
                    <div className="text-sm text-gray-600">Impact Score</div>
                  </div>
                </div>
              </Card>
              <Card className="animate-scale-in" style={{ animationDelay: '0.3s' }}>
                <div className="flex items-center justify-between mb-2">
                  <Heart className="w-10 h-10 text-rose-600" />
                  <div className="text-right">
                    <div className="text-3xl font-bold text-gray-900">{stats.thankYouMessages}</div>
                    <div className="text-sm text-gray-600">Thank You Notes</div>
                  </div>
                </div>
              </Card>
            </div>

            <div className="mb-8">
              <Card className="gradient-hero text-white p-8">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-2xl font-bold mb-2">Ready to make a difference?</h2>
                    <p className="opacity-90 mb-4">Share items you no longer need with families who need them</p>
                    <Button variant="accent" size="lg" onClick={() => setShowDonateModal(true)} className="bg-white text-purple-600 hover:bg-gray-100">
                      <Plus className="inline mr-2 w-5 h-5" />
                      Donate New Item
                    </Button>
                  </div>
                  <Gift className="w-32 h-32 opacity-20 hidden md:block" />
                </div>
              </Card>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  <Package className="w-6 h-6 mr-2 text-orange-600" />
                  Recent Donations
                </h3>
                <div className="space-y-3">
                  {userDonations.slice(0, 3).map((donation) => (
                    <div key={donation.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                      <div className="flex-1">
                        <div className="font-semibold text-gray-900">{donation.title}</div>
                        <div className="text-sm text-gray-600">{donation.category} • {donation.quantity} items</div>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColors[donation.status]}`}>
                        {donation.status}
                      </span>
                    </div>
                  ))}
                </div>
              </Card>

              <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  <MessageSquare className="w-6 h-6 mr-2 text-purple-600" />
                  Recent Messages
                </h3>
                <div className="space-y-3">
                  {userMessages.slice(0, 3).map((message) => (
                    <div key={message.id} className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                      <div className="flex items-start justify-between mb-1">
                        <div className="font-semibold text-gray-900">{message.senderName}</div>
                        {!message.read && <div className="w-2 h-2 bg-orange-500 rounded-full" />}
                      </div>
                      <div className="text-sm text-gray-600">{message.subject}</div>
                      <div className="text-xs text-gray-500 mt-1">{new Date(message.createdAt).toLocaleDateString()}</div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          </div>
        )}

        {activeTab === 'donations' && (
          <div className="animate-fade-in">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">My Donations</h1>
                <p className="text-gray-600">Manage and track all your donations</p>
              </div>
              <Button onClick={() => setShowDonateModal(true)}>
                <Plus className="inline mr-2 w-5 h-5" />
                New Donation
              </Button>
            </div>

            <div className="grid gap-6">
              {userDonations.map((donation) => (
                <Card key={donation.id} hover>
                  <div className="flex flex-col md:flex-row gap-6">
                    <div className="w-full md:w-48 h-48 bg-gray-200 rounded-lg overflow-hidden flex-shrink-0">
                      {donation.imageUrl ? (
                        <img src={donation.imageUrl} alt={donation.title} className="w-full h-full object-cover" />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center">
                          <Package className="w-16 h-16 text-gray-400" />
                        </div>
                      )}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="text-xl font-bold text-gray-900">{donation.title}</h3>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColors[donation.status]}`}>
                          {donation.status}
                        </span>
                      </div>
                      <p className="text-gray-600 mb-4">{donation.description}</p>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <div className="text-gray-500">Category</div>
                          <div className="font-semibold text-gray-900 capitalize">{donation.category}</div>
                        </div>
                        <div>
                          <div className="text-gray-500">Quantity</div>
                          <div className="font-semibold text-gray-900">{donation.quantity}</div>
                        </div>
                        <div>
                          <div className="text-gray-500">Condition</div>
                          <div className="font-semibold text-gray-900 capitalize">{donation.condition.replace('_', ' ')}</div>
                        </div>
                        <div>
                          <div className="text-gray-500">Created</div>
                          <div className="font-semibold text-gray-900">{new Date(donation.createdAt).toLocaleDateString()}</div>
                        </div>
                      </div>
                      <div className="flex items-center gap-4 mt-4 text-sm">
                        {donation.pickupAvailable && (
                          <div className="flex items-center text-green-600">
                            <CheckCircle className="w-4 h-4 mr-1" />
                            Pickup Available
                          </div>
                        )}
                        {donation.deliveryAvailable && (
                          <div className="flex items-center text-blue-600">
                            <Truck className="w-4 h-4 mr-1" />
                            Delivery Available
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'messages' && (
          <div className="animate-fade-in">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Messages</h1>
            <div className="grid gap-4">
              {userMessages.map((message) => (
                <Card key={message.id} hover>
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 gradient-primary rounded-full flex items-center justify-center text-white font-bold flex-shrink-0">
                      {message.senderName.charAt(0)}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <div className="font-bold text-gray-900">{message.senderName}</div>
                          <div className="text-sm text-gray-500">{new Date(message.createdAt).toLocaleString()}</div>
                        </div>
                        {!message.read && (
                          <span className="bg-orange-500 text-white text-xs font-semibold px-2 py-1 rounded-full">New</span>
                        )}
                      </div>
                      <h3 className="font-semibold text-gray-900 mb-2">{message.subject}</h3>
                      <p className="text-gray-700">{message.content}</p>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'profile' && (
          <div className="animate-fade-in max-w-2xl">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Profile Settings</h1>
            <Card>
              <div className="space-y-6">
                <div className="flex items-center space-x-4">
                  <div className="w-20 h-20 gradient-primary rounded-full flex items-center justify-center text-white font-bold text-2xl">
                    {user?.fullName.charAt(0)}
                  </div>
                  <div>
                    <div className="text-xl font-bold text-gray-900">{user?.fullName}</div>
                    <div className="text-gray-600">{user?.email}</div>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
                  <div>
                    <div className="text-sm text-gray-500 mb-1">Phone</div>
                    <div className="font-semibold text-gray-900">{user?.phone || 'Not provided'}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500 mb-1">Location</div>
                    <div className="font-semibold text-gray-900">{user?.city ? `${user.city}, ${user.state}` : 'Not provided'}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500 mb-1">Member Since</div>
                    <div className="font-semibold text-gray-900">{new Date(user?.createdAt || '').toLocaleDateString()}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500 mb-1">Account Status</div>
                    <div className={`inline-flex items-center px-2 py-1 rounded-full text-sm font-semibold ${user?.verified ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                      {user?.verified ? 'Verified' : 'Pending'}
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        )}
      </main>

      <Modal isOpen={showDonateModal} onClose={() => setShowDonateModal(false)} title="Donate New Item" size="lg">
        <form className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Item Title</label>
            <input
              type="text"
              value={donationForm.title}
              onChange={(e) => setDonationForm({ ...donationForm, title: e.target.value })}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 transition-all"
              placeholder="e.g., Winter Coat"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Description</label>
            <textarea
              value={donationForm.description}
              onChange={(e) => setDonationForm({ ...donationForm, description: e.target.value })}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 transition-all"
              rows={4}
              placeholder="Describe the item condition, size, features, etc."
              required
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Category</label>
              <select
                value={donationForm.category}
                onChange={(e) => setDonationForm({ ...donationForm, category: e.target.value as ItemCategory })}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 transition-all"
              >
                <option value="clothing">Clothing</option>
                <option value="food">Food</option>
                <option value="electronics">Electronics</option>
                <option value="furniture">Furniture</option>
                <option value="education">Education</option>
                <option value="medical">Medical</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Condition</label>
              <select
                value={donationForm.condition}
                onChange={(e) => setDonationForm({ ...donationForm, condition: e.target.value as ItemCondition })}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 transition-all"
              >
                <option value="new">New</option>
                <option value="like_new">Like New</option>
                <option value="good">Good</option>
                <option value="fair">Fair</option>
                <option value="acceptable">Acceptable</option>
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Quantity</label>
            <input
              type="number"
              value={donationForm.quantity}
              onChange={(e) => setDonationForm({ ...donationForm, quantity: parseInt(e.target.value) })}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-orange-500 transition-all"
              min="1"
              required
            />
          </div>
          <div className="space-y-3">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={donationForm.pickupAvailable}
                onChange={(e) => setDonationForm({ ...donationForm, pickupAvailable: e.target.checked })}
                className="w-5 h-5 text-orange-600 rounded"
              />
              <span className="ml-3 text-gray-700">Pickup available at my location</span>
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={donationForm.deliveryAvailable}
                onChange={(e) => setDonationForm({ ...donationForm, deliveryAvailable: e.target.checked })}
                className="w-5 h-5 text-orange-600 rounded"
              />
              <span className="ml-3 text-gray-700">I can deliver the item</span>
            </label>
          </div>
          <div className="flex gap-4">
            <Button type="button" variant="outline" onClick={() => setShowDonateModal(false)} fullWidth>
              Cancel
            </Button>
            <Button type="submit" fullWidth>
              Submit Donation
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}

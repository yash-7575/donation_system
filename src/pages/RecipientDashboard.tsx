import { useState } from 'react';
import { Heart, Package, MessageSquare, User, LogOut, Plus, AlertCircle } from 'lucide-react';
import Button from '../components/Button';
import Card from '../components/Card';
import Modal from '../components/Modal';
import { useAuth } from '../context/AuthContext';
import { mockRequests, mockDonations } from '../data/mockData';
import { ItemCategory, UrgencyLevel } from '../types';

interface RecipientDashboardProps {
  onNavigate: (page: string) => void;
}

export default function RecipientDashboard({ onNavigate }: RecipientDashboardProps) {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [showRequestModal, setShowRequestModal] = useState(false);

  const handleLogout = () => {
    logout();
    onNavigate('home');
  };

  const userRequests = mockRequests.filter(r => r.recipientId === user?.id);
  const approvedDonations = mockDonations.filter(d => d.status === 'approved');

  const urgencyColors = {
    low: 'bg-gray-100 text-gray-800',
    medium: 'bg-blue-100 text-blue-800',
    high: 'bg-orange-100 text-orange-800',
    critical: 'bg-red-100 text-red-800',
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-cyan-50 via-purple-50 to-orange-50 flex">
      <aside className="w-64 bg-white shadow-lg fixed h-full">
        <div className="p-6 border-b">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 gradient-accent rounded-xl flex items-center justify-center">
              <Heart className="w-7 h-7 text-white" fill="white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-cyan-600 to-purple-600 bg-clip-text text-transparent">
              GiveHope
            </span>
          </div>
          <div className="flex items-center space-x-3 mt-4">
            <div className="w-10 h-10 gradient-accent rounded-full flex items-center justify-center text-white font-bold">
              {user?.fullName.charAt(0)}
            </div>
            <div className="flex-1 min-w-0">
              <div className="font-semibold text-gray-900 truncate">{user?.fullName}</div>
              <div className="text-xs text-gray-500 truncate">Recipient</div>
            </div>
          </div>
        </div>

        <nav className="p-4 space-y-2">
          {[
            { id: 'dashboard', icon: Package, label: 'Dashboard' },
            { id: 'requests', icon: AlertCircle, label: 'My Requests' },
            { id: 'browse', icon: Package, label: 'Browse Donations' },
            { id: 'profile', icon: User, label: 'Profile' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                activeTab === item.id
                  ? 'gradient-accent text-white shadow-lg'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <item.icon className="w-5 h-5" />
              <span className="flex-1 text-left font-medium">{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="absolute bottom-0 left-0 right-0 p-4 border-t">
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
            <h1 className="text-3xl font-bold text-gray-900 mb-8">My Dashboard</h1>

            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <Card>
                <div className="text-center">
                  <Package className="w-12 h-12 mx-auto mb-3 text-cyan-600" />
                  <div className="text-3xl font-bold text-gray-900">{userRequests.length}</div>
                  <div className="text-gray-600">Total Requests</div>
                </div>
              </Card>
              <Card>
                <div className="text-center">
                  <AlertCircle className="w-12 h-12 mx-auto mb-3 text-orange-600" />
                  <div className="text-3xl font-bold text-gray-900">{userRequests.filter(r => r.status === 'pending').length}</div>
                  <div className="text-gray-600">Pending Requests</div>
                </div>
              </Card>
              <Card>
                <div className="text-center">
                  <Heart className="w-12 h-12 mx-auto mb-3 text-rose-600" />
                  <div className="text-3xl font-bold text-gray-900">{userRequests.filter(r => r.status === 'fulfilled').length}</div>
                  <div className="text-gray-600">Fulfilled</div>
                </div>
              </Card>
            </div>

            <Card className="gradient-accent text-white p-8 mb-8">
              <h2 className="text-2xl font-bold mb-2">Need assistance?</h2>
              <p className="opacity-90 mb-4">Submit a request and our NGO partners will help match you with donors</p>
              <Button variant="accent" size="lg" onClick={() => setShowRequestModal(true)} className="bg-white text-cyan-600">
                <Plus className="inline mr-2 w-5 h-5" />
                New Request
              </Button>
            </Card>

            <div className="grid md:grid-cols-2 gap-6">
              <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-4">Recent Requests</h3>
                <div className="space-y-3">
                  {userRequests.slice(0, 3).map((request) => (
                    <div key={request.id} className="p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <div className="font-semibold text-gray-900">{request.title}</div>
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${urgencyColors[request.urgency]}`}>
                          {request.urgency}
                        </span>
                      </div>
                      <div className="text-sm text-gray-600">{request.category} • {request.quantity} needed</div>
                    </div>
                  ))}
                </div>
              </Card>

              <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-4">Available Donations</h3>
                <div className="space-y-3">
                  {approvedDonations.slice(0, 3).map((donation) => (
                    <div key={donation.id} className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors">
                      <div className="font-semibold text-gray-900">{donation.title}</div>
                      <div className="text-sm text-gray-600">{donation.category} • {donation.quantity} available</div>
                      <div className="text-xs text-gray-500 mt-1">by {donation.donorName}</div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          </div>
        )}

        {activeTab === 'requests' && (
          <div className="animate-fade-in">
            <div className="flex items-center justify-between mb-8">
              <h1 className="text-3xl font-bold text-gray-900">My Requests</h1>
              <Button onClick={() => setShowRequestModal(true)}>
                <Plus className="inline mr-2 w-5 h-5" />
                New Request
              </Button>
            </div>

            <div className="grid gap-6">
              {userRequests.map((request) => (
                <Card key={request.id} hover>
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="text-xl font-bold text-gray-900">{request.title}</h3>
                    <div className="flex gap-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${urgencyColors[request.urgency]}`}>
                        {request.urgency}
                      </span>
                      <span className="px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-800">
                        {request.status}
                      </span>
                    </div>
                  </div>
                  <p className="text-gray-600 mb-4">{request.description}</p>
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <div className="text-gray-500">Category</div>
                      <div className="font-semibold text-gray-900 capitalize">{request.category}</div>
                    </div>
                    <div>
                      <div className="text-gray-500">Quantity</div>
                      <div className="font-semibold text-gray-900">{request.quantity}</div>
                    </div>
                    <div>
                      <div className="text-gray-500">Created</div>
                      <div className="font-semibold text-gray-900">{new Date(request.createdAt).toLocaleDateString()}</div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'browse' && (
          <div className="animate-fade-in">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Browse Available Donations</h1>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {approvedDonations.map((donation) => (
                <Card key={donation.id} hover>
                  <div className="h-48 bg-gray-200 rounded-lg overflow-hidden mb-4">
                    {donation.imageUrl ? (
                      <img src={donation.imageUrl} alt={donation.title} className="w-full h-full object-cover" />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center">
                        <Package className="w-16 h-16 text-gray-400" />
                      </div>
                    )}
                  </div>
                  <h3 className="font-bold text-gray-900 mb-2">{donation.title}</h3>
                  <p className="text-sm text-gray-600 mb-3 line-clamp-2">{donation.description}</p>
                  <div className="text-sm text-gray-500 mb-4">
                    <div className="capitalize">{donation.category} • {donation.condition.replace('_', ' ')}</div>
                    <div>{donation.quantity} available</div>
                  </div>
                  <Button variant="outline" fullWidth size="sm">Request This Item</Button>
                </Card>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'profile' && (
          <div className="animate-fade-in max-w-2xl">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Profile</h1>
            <Card>
              <div className="space-y-6">
                <div className="flex items-center space-x-4">
                  <div className="w-20 h-20 gradient-accent rounded-full flex items-center justify-center text-white font-bold text-2xl">
                    {user?.fullName.charAt(0)}
                  </div>
                  <div>
                    <div className="text-xl font-bold text-gray-900">{user?.fullName}</div>
                    <div className="text-gray-600">{user?.email}</div>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        )}
      </main>

      <Modal isOpen={showRequestModal} onClose={() => setShowRequestModal(false)} title="Submit New Request" size="lg">
        <form className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">What do you need?</label>
            <input type="text" className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg" placeholder="e.g., Winter clothing for children" required />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Description</label>
            <textarea className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg" rows={4} placeholder="Please describe your situation and why you need this assistance" required />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Category</label>
              <select className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg">
                <option value="clothing">Clothing</option>
                <option value="food">Food</option>
                <option value="electronics">Electronics</option>
                <option value="furniture">Furniture</option>
                <option value="education">Education</option>
                <option value="medical">Medical</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Urgency</label>
              <select className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg">
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>
          </div>
          <div className="flex gap-4">
            <Button type="button" variant="outline" onClick={() => setShowRequestModal(false)} fullWidth>Cancel</Button>
            <Button type="submit" fullWidth>Submit Request</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}

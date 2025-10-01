import { useState } from 'react';
import { Heart, BarChart3, Package, Users, GitMerge, LogOut, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import Button from '../components/Button';
import Card from '../components/Card';
import { useAuth } from '../context/AuthContext';
import { mockDonations, mockRequests, mockMatches, mockStatistics } from '../data/mockData';

interface NGODashboardProps {
  onNavigate: (page: string) => void;
}

export default function NGODashboard({ onNavigate }: NGODashboardProps) {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedDonation, setSelectedDonation] = useState<string | null>(null);
  const [selectedRequest, setSelectedRequest] = useState<string | null>(null);

  const handleLogout = () => {
    logout();
    onNavigate('home');
  };

  const pendingDonations = mockDonations.filter(d => d.status === 'pending');
  const pendingRequests = mockRequests.filter(r => r.status === 'pending');
  const approvedDonations = mockDonations.filter(d => d.status === 'approved');
  const approvedRequests = mockRequests.filter(r => r.status === 'approved');

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-cyan-50 to-orange-50 flex">
      <aside className="w-64 bg-white shadow-lg fixed h-full">
        <div className="p-6 border-b">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 gradient-secondary rounded-xl flex items-center justify-center">
              <Heart className="w-7 h-7 text-white" fill="white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-purple-600 to-cyan-600 bg-clip-text text-transparent">
              GiveHope
            </span>
          </div>
          <div className="flex items-center space-x-3 mt-4">
            <div className="w-10 h-10 gradient-secondary rounded-full flex items-center justify-center text-white font-bold">
              {user?.fullName.charAt(0)}
            </div>
            <div className="flex-1 min-w-0">
              <div className="font-semibold text-gray-900 truncate">{user?.fullName}</div>
              <div className="text-xs text-gray-500 truncate">NGO Admin</div>
            </div>
          </div>
        </div>

        <nav className="p-4 space-y-2">
          {[
            { id: 'dashboard', icon: BarChart3, label: 'Dashboard' },
            { id: 'approvals', icon: AlertCircle, label: 'Approvals', badge: pendingDonations.length + pendingRequests.length },
            { id: 'matching', icon: GitMerge, label: 'Match Center' },
            { id: 'users', icon: Users, label: 'Users' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                activeTab === item.id
                  ? 'gradient-secondary text-white shadow-lg'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <item.icon className="w-5 h-5" />
              <span className="flex-1 text-left font-medium">{item.label}</span>
              {item.badge && item.badge > 0 && (
                <span className="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">
                  {item.badge}
                </span>
              )}
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
            <h1 className="text-3xl font-bold text-gray-900 mb-8">NGO Dashboard</h1>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
              <Card className="text-center">
                <Package className="w-12 h-12 mx-auto mb-3 text-orange-600" />
                <div className="text-3xl font-bold text-gray-900">{mockStatistics.totalDonations}</div>
                <div className="text-gray-600">Total Donations</div>
              </Card>
              <Card className="text-center">
                <AlertCircle className="w-12 h-12 mx-auto mb-3 text-purple-600" />
                <div className="text-3xl font-bold text-gray-900">{mockStatistics.totalRequests}</div>
                <div className="text-gray-600">Total Requests</div>
              </Card>
              <Card className="text-center">
                <CheckCircle className="w-12 h-12 mx-auto mb-3 text-green-600" />
                <div className="text-3xl font-bold text-gray-900">{mockStatistics.successfulMatches}</div>
                <div className="text-gray-600">Successful Matches</div>
              </Card>
              <Card className="text-center">
                <Users className="w-12 h-12 mx-auto mb-3 text-cyan-600" />
                <div className="text-3xl font-bold text-gray-900">{mockStatistics.familiesHelped}</div>
                <div className="text-gray-600">Families Helped</div>
              </Card>
            </div>

            <div className="grid md:grid-cols-2 gap-6 mb-8">
              <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  <AlertCircle className="w-6 h-6 mr-2 text-orange-600" />
                  Pending Approvals
                </h3>
                <div className="space-y-3">
                  {pendingDonations.slice(0, 2).map((donation) => (
                    <div key={donation.id} className="p-3 bg-orange-50 rounded-lg">
                      <div className="font-semibold text-gray-900">Donation: {donation.title}</div>
                      <div className="text-sm text-gray-600">by {donation.donorName}</div>
                    </div>
                  ))}
                  {pendingRequests.slice(0, 2).map((request) => (
                    <div key={request.id} className="p-3 bg-purple-50 rounded-lg">
                      <div className="font-semibold text-gray-900">Request: {request.title}</div>
                      <div className="text-sm text-gray-600">by {request.recipientName}</div>
                    </div>
                  ))}
                </div>
              </Card>

              <Card>
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  <GitMerge className="w-6 h-6 mr-2 text-purple-600" />
                  Recent Matches
                </h3>
                <div className="space-y-3">
                  {mockMatches.map((match) => {
                    const donation = mockDonations.find(d => d.id === match.donationId);
                    const request = mockRequests.find(r => r.id === match.requestId);
                    return (
                      <div key={match.id} className="p-3 bg-green-50 rounded-lg">
                        <div className="font-semibold text-gray-900 text-sm">{donation?.title} → {request?.recipientName}</div>
                        <div className="text-xs text-gray-600 capitalize">{match.status}</div>
                      </div>
                    );
                  })}
                </div>
              </Card>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              <Card>
                <h4 className="font-semibold text-gray-900 mb-3">This Month</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">New Donations</span>
                    <span className="font-bold">156</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">New Requests</span>
                    <span className="font-bold">89</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Matches Made</span>
                    <span className="font-bold">124</span>
                  </div>
                </div>
              </Card>
              <Card>
                <h4 className="font-semibold text-gray-900 mb-3">By Category</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Clothing</span>
                    <span className="font-bold">42%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Food</span>
                    <span className="font-bold">28%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Electronics</span>
                    <span className="font-bold">18%</span>
                  </div>
                </div>
              </Card>
              <Card>
                <h4 className="font-semibold text-gray-900 mb-3">Success Rate</h4>
                <div className="text-center">
                  <div className="text-4xl font-bold text-green-600 mb-2">85%</div>
                  <div className="text-sm text-gray-600">Match success rate</div>
                </div>
              </Card>
            </div>
          </div>
        )}

        {activeTab === 'approvals' && (
          <div className="animate-fade-in">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Pending Approvals</h1>

            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Donations</h2>
              <div className="grid gap-4">
                {pendingDonations.map((donation) => (
                  <Card key={donation.id}>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-gray-900 mb-2">{donation.title}</h3>
                        <p className="text-gray-600 mb-4">{donation.description}</p>
                        <div className="grid grid-cols-4 gap-4 text-sm mb-4">
                          <div>
                            <div className="text-gray-500">Donor</div>
                            <div className="font-semibold">{donation.donorName}</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Category</div>
                            <div className="font-semibold capitalize">{donation.category}</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Quantity</div>
                            <div className="font-semibold">{donation.quantity}</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Condition</div>
                            <div className="font-semibold capitalize">{donation.condition.replace('_', ' ')}</div>
                          </div>
                        </div>
                        <div className="flex gap-3">
                          <Button size="sm" variant="primary">
                            <CheckCircle className="w-4 h-4 mr-1" />
                            Approve
                          </Button>
                          <Button size="sm" variant="outline">
                            <XCircle className="w-4 h-4 mr-1" />
                            Reject
                          </Button>
                        </div>
                      </div>
                      {donation.imageUrl && (
                        <div className="w-32 h-32 ml-4 bg-gray-200 rounded-lg overflow-hidden flex-shrink-0">
                          <img src={donation.imageUrl} alt={donation.title} className="w-full h-full object-cover" />
                        </div>
                      )}
                    </div>
                  </Card>
                ))}
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Requests</h2>
              <div className="grid gap-4">
                {pendingRequests.map((request) => (
                  <Card key={request.id}>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-start justify-between mb-2">
                          <h3 className="text-xl font-bold text-gray-900">{request.title}</h3>
                          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            request.urgency === 'critical' ? 'bg-red-100 text-red-800' :
                            request.urgency === 'high' ? 'bg-orange-100 text-orange-800' :
                            'bg-blue-100 text-blue-800'
                          }`}>
                            {request.urgency}
                          </span>
                        </div>
                        <p className="text-gray-600 mb-4">{request.description}</p>
                        <div className="grid grid-cols-4 gap-4 text-sm mb-4">
                          <div>
                            <div className="text-gray-500">Recipient</div>
                            <div className="font-semibold">{request.recipientName}</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Category</div>
                            <div className="font-semibold capitalize">{request.category}</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Quantity</div>
                            <div className="font-semibold">{request.quantity}</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Family Size</div>
                            <div className="font-semibold">{request.familySize}</div>
                          </div>
                        </div>
                        <div className="flex gap-3">
                          <Button size="sm" variant="primary">
                            <CheckCircle className="w-4 h-4 mr-1" />
                            Approve
                          </Button>
                          <Button size="sm" variant="outline">
                            <XCircle className="w-4 h-4 mr-1" />
                            Reject
                          </Button>
                        </div>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'matching' && (
          <div className="animate-fade-in">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Matching Center</h1>
            <p className="text-gray-600 mb-6">Select a donation and a request to create a match</p>

            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  <Package className="w-6 h-6 mr-2 text-orange-600" />
                  Available Donations
                </h2>
                <div className="space-y-3">
                  {approvedDonations.map((donation) => (
                    <Card
                      key={donation.id}
                      hover
                      onClick={() => setSelectedDonation(donation.id)}
                      className={`cursor-pointer ${selectedDonation === donation.id ? 'ring-4 ring-orange-500' : ''}`}
                    >
                      <div className="font-semibold text-gray-900">{donation.title}</div>
                      <div className="text-sm text-gray-600 capitalize">{donation.category} • {donation.quantity} items</div>
                      <div className="text-xs text-gray-500 mt-1">by {donation.donorName}</div>
                    </Card>
                  ))}
                </div>
              </div>

              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  <AlertCircle className="w-6 h-6 mr-2 text-purple-600" />
                  Pending Requests
                </h2>
                <div className="space-y-3">
                  {approvedRequests.map((request) => (
                    <Card
                      key={request.id}
                      hover
                      onClick={() => setSelectedRequest(request.id)}
                      className={`cursor-pointer ${selectedRequest === request.id ? 'ring-4 ring-purple-500' : ''}`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="font-semibold text-gray-900">{request.title}</div>
                          <div className="text-sm text-gray-600 capitalize">{request.category} • {request.quantity} needed</div>
                          <div className="text-xs text-gray-500 mt-1">by {request.recipientName}</div>
                        </div>
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                          request.urgency === 'critical' ? 'bg-red-100 text-red-800' :
                          request.urgency === 'high' ? 'bg-orange-100 text-orange-800' :
                          'bg-blue-100 text-blue-800'
                        }`}>
                          {request.urgency}
                        </span>
                      </div>
                    </Card>
                  ))}
                </div>
              </div>
            </div>

            {selectedDonation && selectedRequest && (
              <div className="mt-8 animate-scale-in">
                <Card className="gradient-secondary text-white p-8">
                  <h3 className="text-2xl font-bold mb-4 flex items-center">
                    <GitMerge className="w-8 h-8 mr-3" />
                    Create Match
                  </h3>
                  <p className="mb-6 opacity-90">You've selected a donation and a request. Click below to create a match.</p>
                  <Button variant="accent" size="lg" className="bg-white text-purple-600 hover:bg-gray-100">
                    <CheckCircle className="inline mr-2 w-5 h-5" />
                    Confirm Match
                  </Button>
                </Card>
              </div>
            )}
          </div>
        )}

        {activeTab === 'users' && (
          <div className="animate-fade-in">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">User Management</h1>
            <Card>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="border-b-2 border-gray-200">
                    <tr>
                      <th className="text-left py-3 px-4 font-semibold text-gray-900">Name</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-900">Email</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-900">Role</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-900">Status</th>
                      <th className="text-left py-3 px-4 font-semibold text-gray-900">Joined</th>
                    </tr>
                  </thead>
                  <tbody>
                    {[...mockDonations.map(d => ({ name: d.donorName, role: 'donor' })), ...mockRequests.map(r => ({ name: r.recipientName, role: 'recipient' }))].slice(0, 10).map((user, index) => (
                      <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                        <td className="py-3 px-4">{user.name}</td>
                        <td className="py-3 px-4 text-gray-600">{user.name.toLowerCase().replace(' ', '.')}@example.com</td>
                        <td className="py-3 px-4">
                          <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                            user.role === 'donor' ? 'bg-orange-100 text-orange-800' : 'bg-cyan-100 text-cyan-800'
                          }`}>
                            {user.role}
                          </span>
                        </td>
                        <td className="py-3 px-4">
                          <span className="px-2 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-800">
                            Active
                          </span>
                        </td>
                        <td className="py-3 px-4 text-gray-600">2024-09-{String(index + 1).padStart(2, '0')}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          </div>
        )}
      </main>
    </div>
  );
}

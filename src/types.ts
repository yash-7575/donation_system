export type UserRole = 'donor' | 'recipient' | 'ngo_admin';

export type DonationStatus = 'pending' | 'approved' | 'matched' | 'in_transit' | 'delivered' | 'rejected';
export type RequestStatus = 'pending' | 'approved' | 'matched' | 'fulfilled' | 'rejected';
export type MatchStatus = 'pending' | 'confirmed' | 'in_progress' | 'completed' | 'cancelled';
export type DeliveryStatus = 'pending' | 'scheduled' | 'in_transit' | 'delivered';

export type ItemCategory = 'clothing' | 'food' | 'electronics' | 'furniture' | 'education' | 'medical' | 'other';
export type ItemCondition = 'new' | 'like_new' | 'good' | 'fair' | 'acceptable';
export type UrgencyLevel = 'low' | 'medium' | 'high' | 'critical';

export interface User {
  id: string;
  email: string;
  fullName: string;
  role: UserRole;
  phone?: string;
  address?: string;
  city?: string;
  state?: string;
  country?: string;
  avatarUrl?: string;
  bio?: string;
  verified: boolean;
  createdAt: Date;
}

export interface Donation {
  id: string;
  donorId: string;
  donorName: string;
  title: string;
  description: string;
  category: ItemCategory;
  quantity: number;
  condition: ItemCondition;
  imageUrl?: string;
  pickupAvailable: boolean;
  deliveryAvailable: boolean;
  status: DonationStatus;
  approvedBy?: string;
  approvedAt?: Date;
  createdAt: Date;
}

export interface Request {
  id: string;
  recipientId: string;
  recipientName: string;
  title: string;
  description: string;
  category: ItemCategory;
  quantity: number;
  urgency: UrgencyLevel;
  familySize: number;
  situation?: string;
  imageUrl?: string;
  status: RequestStatus;
  approvedBy?: string;
  approvedAt?: Date;
  createdAt: Date;
}

export interface Match {
  id: string;
  donationId: string;
  requestId: string;
  matchedBy: string;
  status: MatchStatus;
  notes?: string;
  deliveryStatus: DeliveryStatus;
  completedAt?: Date;
  createdAt: Date;
}

export interface Message {
  id: string;
  senderId: string;
  senderName: string;
  recipientId: string;
  recipientName: string;
  subject: string;
  content: string;
  read: boolean;
  createdAt: Date;
}

export interface Feedback {
  id: string;
  userId: string;
  userName: string;
  userRole: UserRole;
  matchId?: string;
  rating: number;
  comment: string;
  isPublic: boolean;
  createdAt: Date;
}

export interface Statistics {
  totalDonations: number;
  totalRequests: number;
  successfulMatches: number;
  activeDonors: number;
  familiesHelped: number;
}

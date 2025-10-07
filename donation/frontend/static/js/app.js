// Simple navigation helpers to mimic SPA routes
document.addEventListener('click', function (e) {
  const target = e.target.closest('[data-nav]');
  if (!target) return;
  const href = target.getAttribute('data-nav');
  if (href) {
    window.location.href = href;
  }
});

// Basic tab switcher pattern used on dashboards
window.activateTab = function (tabGroupId, tabId) {
  const group = document.getElementById(tabGroupId);
  if (!group) return;
  group.querySelectorAll('[data-tab-panel]').forEach(el => { el.classList.add('hidden'); });
  const panel = group.querySelector(`[data-tab-panel="${tabId}"]`);
  if (panel) panel.classList.remove('hidden');
  group.querySelectorAll('[data-tab-btn]').forEach(btn => {
    const active = btn.getAttribute('data-tab-btn') === tabId;
    btn.classList.toggle('gradient-primary', active);
    btn.classList.toggle('text-white', active);
    btn.classList.toggle('hover:bg-gray-100', !active);
  });
};

// Role selection for auth pages (register/login)
document.addEventListener('DOMContentLoaded', function () {
  const roleGroup = document.querySelector('[data-role-group]');
  if (!roleGroup) return;
  const form = document.querySelector('[data-role-form]');
  const hiddenRole = document.querySelector('input[name="role"]');
  const roleToPath = { donor: '/donor/', recipient: '/recipient/', ngo_admin: '/ngo/' };

  function setActive(role) {
    if (hiddenRole) hiddenRole.value = role;
    // Only change form action for recipient and NGO, keep donor submitting to register page
    if (form && roleToPath[role] && role !== 'donor') {
      form.setAttribute('action', roleToPath[role]);
    }
    document.querySelectorAll('[data-role-section]')
      .forEach(sec => { sec.style.display = (sec.getAttribute('data-role-section') === role) ? '' : 'none'; });
    roleGroup.querySelectorAll('[data-role-btn]').forEach(btn => {
      const isActive = btn.getAttribute('data-role-btn') === role;
      btn.classList.toggle('gradient-primary', isActive);
      btn.classList.toggle('text-white', isActive);
      btn.classList.toggle('bg-gray-100', !isActive);
      btn.classList.toggle('text-gray-700', !isActive);
    });
  }

  roleGroup.addEventListener('click', function (e) {
    const btn = e.target.closest('[data-role-btn]');
    if (!btn) return;
    const role = btn.getAttribute('data-role-btn');
    setActive(role);
  });

  // Initialize to current or default donor
  const initial = (hiddenRole && hiddenRole.value) || 'donor';
  setActive(initial);

  // API submission: create row in respective table via backend
  if (form) {
    form.addEventListener('submit', async function (e) {
      // Only use AJAX for recipient and NGO registrations
      // Donor registration will use standard form submission to Django view
      const role = hiddenRole ? hiddenRole.value : 'donor';
      if (role === 'donor') {
        // Let the form submit normally to Django view
        console.log("Donor form submission - allowing normal submission");
        return true;
      }
      
      // For recipient and NGO, use AJAX
      console.log("Non-donor form submission - using AJAX");
      e.preventDefault();
      const formData = new FormData(form);
      const payload = Object.fromEntries(formData.entries());
      try {
        let url = '/api/recipients/';
        if (role === 'ngo_admin') url = '/api/ngos/';
        if (role === 'ngo_admin') {
          payload['ngo_name'] = payload['ngo_name'] || payload['name'] || '';
        }
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (!res.ok) {
          const msg = await res.text();
          throw new Error(msg || 'Failed');
        }
        const data = await res.json();
        localStorage.setItem('gh_user', JSON.stringify({ role, ...payload, id: data.recipient_id || data.ngo_id }));
        window.location.href = roleToPath[role];
      } catch (err) {
        alert('Registration failed: ' + (err && err.message ? err.message : 'Unknown error'));
      }
    });
  }
  
  // Handle donation form submission
  const donationForm = document.getElementById('donation-form');
  if (donationForm) {
    donationForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      console.log("Donation form submission");
      
      // Show loading state
      const submitButton = donationForm.querySelector('button[type="submit"]');
      const originalText = submitButton.textContent;
      submitButton.textContent = 'Submitting...';
      submitButton.disabled = true;
      
      const formData = new FormData(donationForm);
      const payload = Object.fromEntries(formData.entries());
      
      try {
        const res = await fetch('/donor/', {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify(payload)
        });
        
        if (!res.ok) {
          const msg = await res.text();
          throw new Error(msg || 'Failed');
        }
        
        const data = await res.json();
        if (data.success) {
          showToast('Donation submitted successfully!');
          // Close the modal
          const modal = document.getElementById('donation-modal');
          if (modal) modal.classList.add('hidden');
          // Reset the form
          donationForm.reset();
          // Refresh donations list
          loadDonations();
        } else {
          showToast('Donation submission failed: ' + (data.error || 'Unknown error'), 'error');
        }
      } catch (err) {
        showToast('Donation submission failed: ' + (err && err.message ? err.message : 'Unknown error'), 'error');
      } finally {
        // Reset button state
        submitButton.textContent = originalText;
        submitButton.disabled = false;
      }
    });
  }
  
  // Handle profile form submission
  const profileForm = document.getElementById('profile-form');
  if (profileForm) {
    profileForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      
      console.log('💾 Saving profile changes...');
      
      // Show loading state
      const submitButton = profileForm.querySelector('button[type="submit"]');
      const originalText = submitButton.textContent;
      submitButton.textContent = 'Saving...';
      submitButton.disabled = true;
      
      // Validate all fields
      const inputs = profileForm.querySelectorAll('input');
      let isValid = true;
      
      inputs.forEach(input => {
        if (!validateField(input)) {
          isValid = false;
        }
      });
      
      if (!isValid) {
        showToast('Please fix the errors in the form', 'error');
        submitButton.textContent = originalText;
        submitButton.disabled = false;
        return;
      }
      
      try {
        // Collect form data
        const formData = new FormData(profileForm);
        const profileData = {};
        
        inputs.forEach(input => {
          const fieldName = input.getAttribute('data-user');
          if (fieldName && input.value.trim()) {
            profileData[fieldName] = input.value.trim();
          }
        });
        
        console.log('📊 Profile data to save:', profileData);
        
        // In a real implementation, this would make an API call to update profile
        // For now, we'll simulate the API call
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Simulate success
        showToast('✅ Profile updated successfully!');
        
        // Update the profile display
        updateProfileDisplay(profileData);
        
      } catch (error) {
        console.error('Error saving profile:', error);
        showToast('❌ Failed to update profile: ' + error.message, 'error');
      } finally {
        // Reset button state
        submitButton.textContent = originalText;
        submitButton.disabled = false;
      }
    });
  }
  
  // Load donations when donations tab is activated
  const donationsTabBtn = document.querySelector('[data-tab-btn="donations"]');
  if (donationsTabBtn) {
    donationsTabBtn.addEventListener('click', function () {
      loadDonations();
    });
  }
  
  // Load messages when messages tab is activated
  const messagesTabBtn = document.querySelector('[data-tab-btn="messages"]');
  if (messagesTabBtn) {
    messagesTabBtn.addEventListener('click', function () {
      loadMessages();
    });
  }
  
  // Load profile when profile tab is activated
  const profileTabBtn = document.querySelector('[data-tab-btn="profile"]');
  if (profileTabBtn) {
    profileTabBtn.addEventListener('click', function () {
      loadProfile();
    });
  }
  
  // Load initial dashboard data
  loadDashboardData();
});

// Helper function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Function to show toast notifications
function showToast(message, type = 'success') {
  const toast = document.getElementById('success-toast');
  const messageElement = document.getElementById('success-message');
  
  if (toast && messageElement) {
    messageElement.textContent = message;
    toast.classList.remove('hidden');
    
    // Change color based on type
    if (type === 'error') {
      toast.classList.remove('bg-green-500');
      toast.classList.add('bg-red-500');
    } else {
      toast.classList.remove('bg-red-500');
      toast.classList.add('bg-green-500');
    }
    
    // Hide after 3 seconds
    setTimeout(() => {
      toast.classList.add('hidden');
    }, 3000);
  }
}

// Function to load dashboard data
function loadDashboardData() {
  // In a real implementation, this would fetch data from the API
  // For now, we'll use mock data
  const totalDonationsEl = document.getElementById('total-donations');
  const deliveredDonationsEl = document.getElementById('delivered-donations');
  const impactScoreEl = document.getElementById('impact-score');
  const thankYouNotesEl = document.getElementById('thank-you-notes');
  
  // Only update if elements exist
  if (totalDonationsEl) totalDonationsEl.textContent = '8';
  if (deliveredDonationsEl) deliveredDonationsEl.textContent = '5';
  if (impactScoreEl) impactScoreEl.textContent = '120';
  if (thankYouNotesEl) thankYouNotesEl.textContent = '3';
}

// Function to load messages
async function loadMessages() {
  const messagesList = document.getElementById('messages-list');
  if (!messagesList) {
    console.error('❌ messages-list element not found');
    return;
  }
  
  // Show loading state
  messagesList.innerHTML = '<div class="bg-white rounded-xl shadow-md p-6 text-center text-gray-500">Loading messages...</div>';
  
  try {
    const currentUserId = getCurrentUserId();
    
    if (!currentUserId) {
      throw new Error('User not logged in - no user ID found');
    }
    
    // For now, we'll show mock messages since there's no messages API
    // In a real implementation, this would fetch from /api/donors/{id}/messages/
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
    
    const mockMessages = [
      {
        id: 1,
        from: 'GiveHope Team',
        subject: 'Thank you for your donation!',
        message: 'Your winter clothing donation has been successfully delivered to families in need.',
        timestamp: '2025-10-07T08:30:00Z',
        type: 'success'
      },
      {
        id: 2,
        from: 'Local NGO',
        subject: 'Pickup scheduled',
        message: 'We will be picking up your food donation on October 8th between 2-4 PM.',
        timestamp: '2025-10-06T14:20:00Z',
        type: 'info'
      },
      {
        id: 3,
        from: 'Recipient Family',
        subject: 'Heartfelt thanks',
        message: 'Thank you so much for the books! My children are so happy and excited to read them.',
        timestamp: '2025-10-05T19:45:00Z',
        type: 'heart'
      }
    ];
    
    // Clear loading state
    messagesList.innerHTML = '';
    
    if (mockMessages.length === 0) {
      messagesList.innerHTML = `
        <div class="bg-white rounded-xl shadow-md p-6 text-center text-gray-500">
          <p>📭 No messages yet.</p>
          <p class="mt-2 text-sm">Messages from NGOs and recipients will appear here.</p>
        </div>
      `;
      return;
    }
    
    // Display messages
    mockMessages.forEach(message => {
      const messageElement = document.createElement('div');
      messageElement.className = 'bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow';
      
      const typeIcons = {
        'success': '✅',
        'info': 'ℹ️',
        'heart': '💝',
        'warning': '⚠️'
      };
      
      const typeColors = {
        'success': 'border-l-green-500 bg-green-50',
        'info': 'border-l-blue-500 bg-blue-50',
        'heart': 'border-l-pink-500 bg-pink-50',
        'warning': 'border-l-yellow-500 bg-yellow-50'
      };
      
      const formattedDate = new Date(message.timestamp).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
      
      messageElement.innerHTML = `
        <div class="border-l-4 ${typeColors[message.type] || typeColors['info']} p-4 rounded-r-lg">
          <div class="flex items-start justify-between mb-2">
            <div class="flex items-center gap-2">
              <span class="text-lg">${typeIcons[message.type] || typeIcons['info']}</span>
              <h3 class="font-bold text-gray-900">${message.subject}</h3>
            </div>
            <span class="text-xs text-gray-500">${formattedDate}</span>
          </div>
          
          <p class="text-sm text-gray-600 mb-2">From: <span class="font-medium">${message.from}</span></p>
          <p class="text-gray-700">${message.message}</p>
          
          <div class="mt-4 flex gap-2">
            <button class="text-blue-600 hover:text-blue-800 text-sm font-medium" onclick="markAsRead(${message.id})">
              Mark as Read
            </button>
            <button class="text-gray-600 hover:text-gray-800 text-sm font-medium" onclick="deleteMessage(${message.id})">
              Delete
            </button>
          </div>
        </div>
      `;
      
      messagesList.appendChild(messageElement);
    });
    
    console.log('✅ Messages loaded successfully:', mockMessages.length, 'messages');
    
  } catch (error) {
    console.error('❌ Error loading messages:', error);
    messagesList.innerHTML = `
      <div class="bg-white rounded-xl shadow-md p-6 text-center">
        <div class="text-red-500 mb-4">
          <h3 class="text-lg font-semibold">❌ Failed to load messages</h3>
          <p class="mt-2">${error.message}</p>
        </div>
        
        <button onclick="loadMessages()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 font-medium">
          🔄 Try Again
        </button>
      </div>
    `;
  }
}

// Function to load and initialize profile
function loadProfile() {
  console.log('🔄 Loading profile data...');
  
  // Profile is already loaded via Django template context
  // Just ensure form validation and interactivity
  const profileForm = document.getElementById('profile-form');
  if (profileForm) {
    // Add real-time validation
    const inputs = profileForm.querySelectorAll('input');
    inputs.forEach(input => {
      input.addEventListener('input', function() {
        validateField(this);
      });
    });
    
    console.log('✅ Profile form initialized with validation');
  }
}

// Helper functions for messages
function markAsRead(messageId) {
  showToast(`Message ${messageId} marked as read`);
  // In a real implementation, this would make an API call
}

function deleteMessage(messageId) {
  if (confirm('Are you sure you want to delete this message?')) {
    showToast(`Message ${messageId} deleted`);
    // In a real implementation, this would make an API call and refresh messages
    loadMessages();
  }
}

// Form validation helper
function validateField(field) {
  const value = field.value.trim();
  const fieldName = field.getAttribute('data-user') || field.name;
  
  // Remove existing validation messages
  const existingError = field.parentNode.querySelector('.error-message');
  if (existingError) existingError.remove();
  
  field.classList.remove('border-red-500', 'border-green-500');
  
  // Email validation
  if (field.type === 'email' && value) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      showFieldError(field, 'Please enter a valid email address');
      return false;
    }
  }
  
  // Phone validation
  if (field.type === 'tel' && value) {
    const phoneRegex = /^[\d\s\-\+\(\)]+$/;
    if (!phoneRegex.test(value) || value.length < 10) {
      showFieldError(field, 'Please enter a valid phone number');
      return false;
    }
  }
  
  // Required field validation
  if (field.required && !value) {
    showFieldError(field, `${fieldName} is required`);
    return false;
  }
  
  // Success state
  if (value) {
    field.classList.add('border-green-500');
  }
  
  return true;
}

function showFieldError(field, message) {
  field.classList.add('border-red-500');
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-message text-red-500 text-xs mt-1';
  errorDiv.textContent = message;
  field.parentNode.appendChild(errorDiv);
}

// Function to update profile display after save
function updateProfileDisplay(profileData) {
  // Update profile card display
  Object.keys(profileData).forEach(key => {
    const displayElement = document.querySelector(`.profile-${key}`);
    if (displayElement) {
      displayElement.textContent = profileData[key];
    }
    
    // Update field values in the display
    const fieldElement = document.querySelector(`.field-value`);
    const fieldElements = document.querySelectorAll('[data-user]');
    fieldElements.forEach(element => {
      if (element.getAttribute('data-user') === key) {
        if (element.tagName === 'INPUT') {
          element.value = profileData[key];
        } else {
          element.textContent = profileData[key];
        }
      }
    });
  });
  
  console.log('✅ Profile display updated');
}

// Function to handle any errors in JOIN operations
function handleJoinError(joinType, error) {
  console.error(`❌ Error in ${joinType}:`, error);
  
  const resultsTable = document.getElementById('results-table');
  if (resultsTable) {
    resultsTable.innerHTML = `
      <div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
        <div class="flex items-center gap-2 mb-2">
          <span class="text-xl">❌</span>
          <strong>Error loading ${joinType.replace('-', ' ')} results</strong>
        </div>
        <p class="text-sm mb-3">${error.message}</p>
        <div class="flex gap-2">
          <button onclick="showJoin('${joinType}')" class="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700">
            🔄 Try Again
          </button>
          <button onclick="testJoinConnectivity()" class="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
            🔍 Test Connection
          </button>
        </div>
      </div>
    `;
  }
}

// Function to test JOIN connectivity
async function testJoinConnectivity() {
  try {
    console.log('🔍 Testing JOIN API connectivity...');
    const response = await fetch('/api/health/');
    
    if (response.ok) {
      const data = await response.json();
      showToast('✅ Server connection OK - ' + JSON.stringify(data));
    } else {
      showToast('❌ Server returned status: ' + response.status, 'error');
    }
  } catch (error) {
    showToast('❌ Cannot connect to server: ' + error.message, 'error');
  }
}

// Function to load donations
async function loadDonations() {
  const donationsList = document.getElementById('donations-list');
  if (!donationsList) {
    console.error('❌ donations-list element not found');
    return;
  }
  
  // Show loading state
  donationsList.innerHTML = '<div class="bg-white rounded-xl shadow-md p-6 text-center text-gray-500">Loading donations...</div>';
  
  try {
    // Get the current user ID
    const currentUserId = getCurrentUserId();
    console.log('🔍 Current user ID:', currentUserId);
    
    if (!currentUserId) {
      throw new Error('User not logged in - no user ID found');
    }
    
    // Fetch donations for current donor
    console.log('🚀 Fetching donations for donor:', currentUserId);
    const donationsResponse = await fetch(`/api/donors/${currentUserId}/donations/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    console.log('📊 API Response status:', donationsResponse.status);
    
    if (!donationsResponse.ok) {
      const errorText = await donationsResponse.text();
      throw new Error(`Failed to fetch donations: ${donationsResponse.status} - ${errorText}`);
    }
    
    const donations = await donationsResponse.json();
    console.log('✅ Donations fetched successfully:', donations.length, 'donations');
    
    // Clear the loading state
    donationsList.innerHTML = '';
    
    if (donations.length === 0) {
      donationsList.innerHTML = `
        <div class="bg-white rounded-xl shadow-md p-6 text-center text-gray-500" id="no-donations-message">
          <p>You haven't made any donations yet.</p>
          <p class="mt-2">Click "Quick Donation" to get started!</p>
        </div>
      `;
      console.log('📝 No donations found for this donor');
      return;
    }
    
    // Display donations
    donations.forEach(donation => {
      const donationElement = document.createElement('div');
      donationElement.className = 'bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow';
      
      const statusColors = {
        'pending': 'bg-yellow-100 text-yellow-800',
        'matched': 'bg-blue-100 text-blue-800',
        'delivered': 'bg-green-100 text-green-800',
        'cancelled': 'bg-red-100 text-red-800'
      };
      
      const statusColor = statusColors[donation.status] || 'bg-gray-100 text-gray-800';
      
      // Format the date
      const createdDate = new Date(donation.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
      
      donationElement.innerHTML = `
        <div class="flex items-start justify-between mb-4">
          <div class="flex-1">
            <h3 class="text-xl font-bold text-gray-900 mb-2">${donation.title}</h3>
            <div class="flex items-center gap-4 text-sm text-gray-600 mb-2">
              <span class="font-medium">${donation.category}</span>
              <span>Qty: ${donation.quantity}</span>
              <span>${createdDate}</span>
            </div>
          </div>
          <span class="px-3 py-1 rounded-full text-xs font-semibold ${statusColor}">
            ${donation.status.charAt(0).toUpperCase() + donation.status.slice(1)}
          </span>
        </div>
        
        ${donation.description ? `<p class="text-gray-600 mb-4">${donation.description}</p>` : ''}
        
        <div class="flex items-center justify-between pt-4 border-t border-gray-100">
          <div class="text-sm text-gray-500">
            ${donation.ngo ? `Assigned to: <span class="font-medium text-gray-700">${donation.ngo.ngo_name}</span>` : 'Not yet assigned to an NGO'}
          </div>
          <div class="flex gap-2">
            <button class="text-blue-600 hover:text-blue-800 text-sm font-medium" onclick="viewDonationDetails(${donation.donation_id})">
              View Details
            </button>
          </div>
        </div>
      `;
      
      donationsList.appendChild(donationElement);
    });
    
  } catch (error) {
    console.error('❌ Error loading donations:', error);
    
    // Provide specific error messages based on the error type
    let errorMessage = error.message;
    let troubleshootingTips = '';
    
    if (error.message.includes('User not logged in')) {
      errorMessage = 'Please log in to view your donations';
      troubleshootingTips = `
        <div class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h4 class="font-semibold text-blue-900 mb-2">🔍 Troubleshooting:</h4>
          <ul class="text-sm text-blue-800 space-y-1">
            <li>• Make sure you're logged in as a donor</li>
            <li>• Try refreshing the page</li>
            <li>• Check if your session has expired</li>
          </ul>
        </div>
      `;
    } else if (error.message.includes('Failed to fetch donations')) {
      errorMessage = 'Unable to load donations from server';
      troubleshootingTips = `
        <div class="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <h4 class="font-semibold text-yellow-900 mb-2">🔍 Debug Info:</h4>
          <ul class="text-sm text-yellow-800 space-y-1">
            <li>• User ID: ${getCurrentUserId() || 'Not found'}</li>
            <li>• API endpoint working: Check network tab</li>
            <li>• Server status: ${error.message}</li>
          </ul>
        </div>
      `;
    }
    
    donationsList.innerHTML = `
      <div class="bg-white rounded-xl shadow-md p-6 text-center">
        <div class="text-red-500 mb-4">
          <h3 class="text-lg font-semibold">❌ Failed to load donations</h3>
          <p class="mt-2">${errorMessage}</p>
        </div>
        
        <div class="flex justify-center gap-3">
          <button onclick="loadDonations()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 font-medium">
            🔄 Try Again
          </button>
          <a href="/login/" class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 font-medium">
            🔑 Login
          </a>
        </div>
        
        ${troubleshootingTips}
      </div>
    `;
  }
}

// Helper function to get current user ID
function getCurrentUserId() {
  // First, try to get from the global variable set by Django template
  if (window.CURRENT_USER_ID && window.CURRENT_USER_ID !== 'null') {
    console.log('✅ Found user ID from window.CURRENT_USER_ID:', window.CURRENT_USER_ID);
    return window.CURRENT_USER_ID;
  }
  
  // Alternative: try to extract from page context elements
  const userElements = document.querySelectorAll('[data-user]');
  for (let element of userElements) {
    if (element.dataset.userId) {
      console.log('✅ Found user ID from data-user-id:', element.dataset.userId);
      return element.dataset.userId;
    }
  }
  
  // Debug: log what we found
  console.warn('⚠️ No user ID found. Available sources:');
  console.warn('- window.CURRENT_USER_ID:', window.CURRENT_USER_ID);
  console.warn('- data-user elements:', userElements.length);
  
  return null;
}

// Function to view donation details (placeholder)
function viewDonationDetails(donationId) {
  showToast(`Viewing details for donation ${donationId}`);
  // In a real app, this would open a modal or navigate to a details page
}

// Store SQL queries for each join type
const joinQueries = {
  'equijoin': `
SELECT 
    api_donor.name AS donor_name,
    api_donor.city,
    api_donation.title,
    api_donation.category,
    api_donation.status
FROM api_donor
INNER JOIN api_donation 
ON api_donor.donor_id = api_donation.donor_id
ORDER BY api_donor.name`,

  'non-equijoin': `
SELECT 
    d1.name AS donor1,
    d1.city AS city1,
    d2.name AS donor2,
    d2.city AS city2
FROM api_donor d1
JOIN api_donor d2 
ON d1.donor_id < d2.donor_id
LIMIT 20`,

  'self-join': `
SELECT 
    d1.name AS donor1,
    d2.name AS donor2,
    d1.city AS common_city
FROM api_donor d1
INNER JOIN api_donor d2 
ON d1.city = d2.city 
WHERE d1.donor_id < d2.donor_id
ORDER BY d1.city`,

  'natural-join': `
SELECT 
    api_donor.name,
    api_donor.city,
    api_donation.title,
    api_donation.quantity
FROM api_donor
INNER JOIN api_donation 
ON api_donor.donor_id = api_donation.donor_id
ORDER BY api_donor.name`,

  'left-join': `
SELECT 
    api_donor.donor_id,
    api_donor.name,
    api_donor.city,
    COUNT(api_donation.donation_id) AS donation_count,
    COALESCE(SUM(api_donation.quantity), 0) AS total_items
FROM api_donor
LEFT OUTER JOIN api_donation 
ON api_donor.donor_id = api_donation.donor_id
GROUP BY api_donor.donor_id, api_donor.name, api_donor.city
ORDER BY api_donor.name`,

  'right-join': `
SELECT 
    api_donation.title,
    api_donation.category,
    api_donor.name AS donor_name,
    api_donor.city
FROM api_donor
RIGHT OUTER JOIN api_donation 
ON api_donor.donor_id = api_donation.donor_id
ORDER BY api_donation.title`,

  'full-join': `
SELECT 
    api_donor.name AS donor_name,
    api_donation.title AS donation_title,
    api_donation.category,
    'Left Join' AS join_source
FROM api_donor
LEFT JOIN api_donation ON api_donor.donor_id = api_donation.donor_id
UNION
SELECT 
    api_donor.name AS donor_name,
    api_donation.title AS donation_title,
    api_donation.category,
    'Right Join' AS join_source
FROM api_donor
RIGHT JOIN api_donation ON api_donor.donor_id = api_donation.donor_id
WHERE api_donor.donor_id IS NULL
ORDER BY donor_name, donation_title`
};

// Function to show selected join
async function showJoin(joinType) {
  // Show SQL query
  document.getElementById('sql-query').style.display = 'block';
  document.getElementById('query-text').textContent = joinQueries[joinType];
  
  // Update title
  document.getElementById('result-title').textContent = 
    joinType.charAt(0).toUpperCase() + joinType.slice(1).replace('-', ' ') + ' Results';
  
  // Show loading state
  document.getElementById('results-table').innerHTML = 
    '<div class="bg-blue-50 border border-blue-200 rounded-lg p-4 text-blue-800">Loading results...</div>';
  
  // Fetch results from backend
  try {
    const response = await fetch(`/api/joins/${joinType}/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    
    if (data.success) {
      displayTable(data.results);
      displayStats(data.count, joinType);
    } else {
      throw new Error(data.error || 'Unknown error occurred');
    }
  } catch (error) {
    console.error('Error fetching join results:', error);
    handleJoinError(joinType, error);
  }
}

// Function to display results in HTML table
function displayTable(results) {
  const container = document.getElementById('results-table');
  
  if (!results || results.length === 0) {
    container.innerHTML = '<div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-yellow-800">No results found.</div>';
    return;
  }
  
  // Create table HTML
  let html = '<table class="w-full border-collapse bg-white rounded-lg overflow-hidden shadow-md"><thead class="bg-gradient-to-r from-blue-600 to-purple-600 text-white"><tr>';
  
  // Add headers
  Object.keys(results[0]).forEach(key => {
    html += `<th class="px-4 py-3 text-left font-semibold">${key.replace(/_/g, ' ').toUpperCase()}</th>`;
  });
  html += '</tr></thead><tbody>';
  
  // Add rows
  results.forEach((row, index) => {
    const rowClass = index % 2 === 0 ? 'bg-gray-50' : 'bg-white';
    html += `<tr class="${rowClass} hover:bg-blue-50 transition-colors">`;
    Object.values(row).forEach(value => {
      html += `<td class="px-4 py-3 border-b border-gray-200">${value !== null ? value : '<span class="text-gray-400">N/A</span>'}</td>`;
    });
    html += '</tr>';
  });
  
  html += '</tbody></table>';
  container.innerHTML = html;
}

// Function to display statistics
function displayStats(count, joinType) {
  const statsContainer = document.getElementById('results-stats');
  if (statsContainer) {
    statsContainer.style.display = 'block';
    statsContainer.innerHTML = `
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
        <strong>Results:</strong> ${count} rows returned for ${joinType.replace('-', ' ')} operation
      </div>
    `;
  }
}

// Simple modal open/close handling
document.addEventListener('click', function (e) {
  const openBtn = e.target.closest('[data-open-modal]');
  if (openBtn) {
    const id = openBtn.getAttribute('data-open-modal');
    const modal = document.getElementById(id + '-modal');
    if (modal) modal.classList.remove('hidden');
  }
  const closeBtn = e.target.closest('[data-close-modal]');
  if (closeBtn) {
    const modal = closeBtn.closest('[data-modal]');
    if (modal) modal.classList.add('hidden');
  }
});
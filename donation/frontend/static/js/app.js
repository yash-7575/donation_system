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
      showToast('Profile updated successfully!');
    });
  }
  
  // Load donations when donations tab is activated
  const donationsTabBtn = document.querySelector('[data-tab-btn="donations"]');
  if (donationsTabBtn) {
    donationsTabBtn.addEventListener('click', function () {
      loadDonations();
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
  document.getElementById('total-donations').textContent = '8';
  document.getElementById('delivered-donations').textContent = '5';
  document.getElementById('impact-score').textContent = '120';
  document.getElementById('thank-you-notes').textContent = '3';
}

// Function to load donations
function loadDonations() {
  // In a real implementation, this would fetch data from the API
  // For now, we'll use mock data
  const donationsList = document.getElementById('donations-list');
  if (!donationsList) return;
  
  // Remove the "no donations" message
  const noDonationsMessage = document.getElementById('no-donations-message');
  if (noDonationsMessage) {
    noDonationsMessage.remove();
  }
  
  // Add mock donations
  const mockDonations = [
    { title: 'Winter Coat', status: 'delivered', description: 'Warm coat suitable for cold weather.' },
    { title: 'Children\'s Books', status: 'pending', description: 'Set of 10 children\'s books in good condition.' },
    { title: 'Kitchen Utensils', status: 'matched', description: 'Various kitchen utensils including pots and pans.' }
  ];
  
  // Clear existing donations except the first one (which is the no donations message)
  donationsList.innerHTML = '';
  
  mockDonations.forEach(donation => {
    const donationElement = document.createElement('div');
    donationElement.className = 'bg-white rounded-xl shadow-md p-6';
    donationElement.innerHTML = `
      <div class="flex items-start justify-between">
        <h3 class="text-xl font-bold text-gray-900">${donation.title}</h3>
        <span class="px-3 py-1 rounded-full text-xs font-semibold ${
          donation.status === 'delivered' ? 'bg-green-100 text-green-800' :
          donation.status === 'matched' ? 'bg-blue-100 text-blue-800' :
          'bg-yellow-100 text-yellow-800'
        }">${donation.status}</span>
      </div>
      <p class="text-gray-600 mt-2">${donation.description}</p>
    `;
    donationsList.appendChild(donationElement);
  });
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
// Tab activation function - defined globally to match HTML onclick calls
window.activateTab = function (scopeId, tabId) {
    try {
        // Hide all tab panels
        document.querySelectorAll('[data-tab-panel]').forEach(panel => {
            panel.classList.add('hidden');
        });
        
        // Show the selected tab panel
        const activePanel = document.querySelector(`[data-tab-panel="${tabId}"]`);
        if (activePanel) {
            activePanel.classList.remove('hidden');
        }
        
        // Update active state for tab buttons
        document.querySelectorAll('[data-tab-btn]').forEach(btn => {
            const isActive = btn.getAttribute('data-tab-btn') === tabId;
            if (isActive) {
                btn.classList.add('gradient-primary', 'text-white');
                btn.classList.remove('hover:bg-gray-100', 'text-gray-700', 'bg-white');
            } else {
                btn.classList.remove('gradient-primary', 'text-white');
                btn.classList.add('hover:bg-gray-100', 'text-gray-700', 'bg-white');
            }
        });
    } catch (error) {
        console.error('Error activating tab:', error);
    }
};

document.addEventListener("DOMContentLoaded", () => {
    // Add event listeners to all tab buttons as backup to onclick
    document.querySelectorAll('[data-tab-btn]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const scopeId = this.closest('[id]').id;
            const tabId = this.getAttribute('data-tab-btn');
            activateTab(scopeId, tabId);
        });
    });
    
    // Modal open/close handling
    document.addEventListener('click', function (e) {
        const openBtn = e.target.closest('[data-open-modal]');
        if (openBtn) {
            e.preventDefault();
            const id = openBtn.getAttribute('data-open-modal');
            const modal = document.getElementById(id + '-modal');
            if (modal) {
                modal.classList.remove('hidden');
            }
        }
        
        const closeBtn = e.target.closest('[data-close-modal]');
        if (closeBtn) {
            const modal = closeBtn.closest('[data-modal]');
            if (modal) {
                modal.classList.add('hidden');
            }
        }
    });

    // Activate the dashboard tab by default
    activateTab('ngo-scope', 'dashboard');

    // Handle donation form submission
    const donationForm = document.getElementById("donation-form");
    if (donationForm) {
        donationForm.addEventListener("submit", function (e) {
            console.log('Submitting donation form...');
        });
    }

    // Handle profile form submission
    const profileForm = document.getElementById("profile-form");
    if (profileForm) {
        profileForm.addEventListener("submit", function (e) {
            console.log('Submitting profile form...');
        });
    }
});
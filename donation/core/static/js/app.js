// Tab and Modal Management Script

// Activate tab panels by scope and tab ID
window.activateTab = function (scopeId, tabId) {
    try {
        // Hide all tab panels in the given scope
        document.querySelectorAll(`#${scopeId} [data-tab-panel]`).forEach(panel => {
            panel.classList.add('hidden');
        });

        // Show the selected tab panel
        const activePanel = document.querySelector(`#${scopeId} [data-tab-panel="${tabId}"]`);
        if (activePanel) {
            activePanel.classList.remove('hidden');
        }

        // Update tab button states
        document.querySelectorAll(`#${scopeId} [data-tab-btn]`).forEach(btn => {
            const isActive = btn.getAttribute('data-tab-btn') === tabId;
            btn.classList.toggle('gradient-primary', isActive);
            btn.classList.toggle('text-white', isActive);
            btn.classList.toggle('shadow-lg', isActive);
            btn.classList.toggle('hover:bg-gray-100', !isActive);
            btn.classList.toggle('text-gray-700', !isActive);
        });
    } catch (error) {
        console.error('Error activating tab:', error);
    }
};

// On DOMContentLoaded, set up all interactive handlers
document.addEventListener("DOMContentLoaded", () => {
    // Tab button click handlers (backup for inline onclick)
    document.querySelectorAll('[data-tab-btn]').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const scopeId = this.closest('[id]').id;
            const tabId = this.getAttribute('data-tab-btn');
            activateTab(scopeId, tabId);
        });
    });

    // Modal open/close handling
    document.addEventListener('click', function (e) {
        // Open modal
        const openBtn = e.target.closest('[data-open-modal]');
        if (openBtn) {
            e.preventDefault();
            const modalId = openBtn.getAttribute('data-open-modal');
            const modal = document.getElementById(`${modalId}-modal`);
            if (modal) modal.classList.remove('hidden');
        }

        // Close modal
        const closeBtn = e.target.closest('[data-close-modal]');
        if (closeBtn) {
            const modal = closeBtn.closest('[data-modal]');
            if (modal) modal.classList.add('hidden');
        }
    });

    // Activate default dashboard tab in recipient-scope
    const recipientScope = document.getElementById('recipient-scope');
    if (recipientScope) {
        activateTab('recipient-scope', 'dashboard');
    }

    // Donation form submission handler
    const donationForm = document.getElementById("donation-form");
    if (donationForm) {
        donationForm.addEventListener("submit", function () {
            console.log('Submitting donation form...');
        });
    }

    // Profile form submission handler
    const profileForm = document.getElementById("profile-form");
    if (profileForm) {
        profileForm.addEventListener("submit", function () {
            console.log('Submitting profile form...');
        });
    }

    // Request update button: pre-fill and set action for update form
    document.querySelectorAll('.update-request-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            document.getElementById('update-request-title').value = btn.getAttribute('data-request-title');
            document.getElementById('update-request-description').value = btn.getAttribute('data-request-description');
            document.getElementById('update-request-category').value = btn.getAttribute('data-request-category');
            document.getElementById('update-request-urgency').value = btn.getAttribute('data-request-urgency');
            const updateForm = document.getElementById('update-request-form');
            updateForm.action = `/recipient/update/${btn.getAttribute('data-request-id')}/`;
        });
    });

    // Delete request button: modal confirmation and set delete form action
    document.addEventListener('click', function (e) {
        const deleteBtn = e.target.closest('.delete-request-btn');
        if (deleteBtn) {
            e.preventDefault();
            document.getElementById('delete-request-title').textContent = deleteBtn.getAttribute('data-request-title');
            const deleteForm = document.getElementById('delete-request-form');
            deleteForm.action = `/recipient/delete/${deleteBtn.getAttribute('data-request-id')}/`;
            document.getElementById('delete-request-modal').classList.remove('hidden');
        }
    });
});

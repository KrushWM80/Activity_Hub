// ┌─────────────────────────────────────────────────────────────────────┐
// │                   WIDGET MANAGEMENT (ADMIN FUNCTIONS)               │
// │                                                                       │
// │ Admin dashboard functions for managing widgets                       │
// │ - Widget table display and updates                                   │
// │ - Widget requests review                                             │
// │ - Widget editing and customization                                   │
// │                                                                       │
// │ Last Updated: April 16, 2026                                        │
// └─────────────────────────────────────────────────────────────────────┘

// ─── UTILITY FUNCTIONS ──────────────────────────────────────────────

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// ─── WIDGETS TABLE MANAGEMENT ──────────────────────────────────────

function loadWidgetsTable() {
    const tbody = document.getElementById('widgets-table-body');
    if (!tbody) return;

    const allWidgets = getAllWidgets();
    
    tbody.innerHTML = allWidgets.map(w => {
        const display = getWidgetDisplay(w);
        const isActive = isWidgetActive(w.id);
        const activeAreas = getAreasForWidget(w.id);

        const areasHtml = PLATFORM_AREAS.map(area => {
            const selected = activeAreas.includes(area);
            return '<span onclick="toggleWidgetArea(\'' + w.id + '\', \'' + area + '\')" ' +
                'style="display: inline-block; padding: 3px 10px; margin: 2px 4px 2px 0; border-radius: 14px; font-size: 0.78rem; font-weight: 500; cursor: pointer; transition: all 0.2s; ' +
                (selected
                    ? 'background: var(--walmart-blue); color: white; border: 1px solid var(--walmart-blue);'
                    : 'background: var(--gray-100); color: var(--gray-600); border: 1px solid var(--gray-300);') +
                '">' + escapeHtml(area) + '</span>';
        }).join('');

        return '<tr style="border-bottom: 1px solid var(--gray-300);">' +
            '<td style="padding: 12px 16px; font-family: monospace; font-weight: 500; color: var(--walmart-blue);">' + escapeHtml(w.id) + '</td>' +
            '<td style="padding: 12px 16px; font-weight: 500;">' + escapeHtml(display.name) + '</td>' +
            '<td style="padding: 12px 16px; color: var(--gray-600); font-size: 0.9rem;">' + escapeHtml(display.description) + '</td>' +
            '<td style="padding: 12px 16px; font-size: 0.9rem;">' + display.defaultSize + '</td>' +
            '<td style="padding: 12px 16px;">' + areasHtml + '</td>' +
            '<td style="padding: 12px 16px; text-align: center;">' +
                '<label style="position: relative; display: inline-block; width: 44px; height: 24px;">' +
                    '<input type="checkbox" ' + (isActive ? 'checked' : '') + ' onchange="toggleWidgetActive(\'' + w.id + '\', this.checked)" style="opacity: 0; width: 0; height: 0;">' +
                    '<span style="position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background: ' + (isActive ? 'var(--success)' : 'var(--gray-300)') + '; border-radius: 24px; transition: 0.3s;"></span>' +
                    '<span style="position: absolute; height: 18px; width: 18px; left: ' + (isActive ? '23px' : '3px') + '; bottom: 3px; background: white; border-radius: 50%; transition: 0.3s;"></span>' +
                '</label>' +
            '</td>' +
            '<td style="padding: 12px 16px; text-align: center;">' +
                '<button onclick="openEditWidgetModal(\'' + w.id + '\')" style="padding: 6px 12px; background: var(--walmart-blue); color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.85rem; font-weight: 500; transition: all 0.2s;" onmouseover="this.style.background=\'var(--walmart-blue-dark)\'" onmouseout="this.style.background=\'var(--walmart-blue)\'">✏️ Edit</button>' +
            '</td>' +
            '</tr>';
    }).join('');
}

function toggleWidgetActive(widgetId, isActive) {
    setWidgetActive(widgetId, isActive);
    loadWidgetsTable();
}

// ─── WIDGET EDIT MODAL ──────────────────────────────────────────────

function openEditWidgetModal(widgetId) {
    const widget = getWidgetById(widgetId);
    if (!widget) return;

    const display = getWidgetDisplay(widget);

    document.getElementById('edit-widget-id').value = widgetId;
    document.getElementById('edit-widget-name').value = display.name;
    document.getElementById('edit-widget-description').value = display.description;
    document.getElementById('edit-widget-size').value = display.defaultSize;

    // Set available areas checkboxes
    const activeAreas = getAreasForWidget(widgetId);
    PLATFORM_AREAS.forEach(area => {
        const checkbox = document.getElementById('edit-area-' + area.replace(/\s+/g, '-').toLowerCase());
        if (checkbox) checkbox.checked = activeAreas.includes(area);
    });

    showModal('editWidgetModal');
}

function saveWidgetChanges() {
    const widgetId = document.getElementById('edit-widget-id').value;
    const name = document.getElementById('edit-widget-name').value.trim();
    const description = document.getElementById('edit-widget-description').value.trim();
    const size = document.getElementById('edit-widget-size').value;

    if (!name || !description) {
        alert('Please fill in all required fields');
        return;
    }

    // Get selected areas
    const selectedAreas = [];
    PLATFORM_AREAS.forEach(area => {
        const checkbox = document.getElementById('edit-area-' + area.replace(/\s+/g, '-').toLowerCase());
        if (checkbox && checkbox.checked) selectedAreas.push(area);
    });

    if (selectedAreas.length === 0) {
        alert('Please select at least one available area');
        return;
    }

    // Update widget areas
    setAreasForWidget(widgetId, selectedAreas);

    // Update widget customizations
    setWidgetCustomization(widgetId, {
        name: name,
        description: description,
        defaultSize: size
    });

    // Reload table to show changes
    loadWidgetsTable();
    hideModal('editWidgetModal');
}

// ─── WIDGET REQUESTS MANAGEMENT ────────────────────────────────────

function loadWidgetRequests() {
    const requests = getWidgetRequests();
    const filter = document.getElementById('request-status-filter')?.value || 'all';
    const filtered = filter === 'all' ? requests : requests.filter(r => r.status === filter);

    // Update stats
    const stats = getWidgetRequestStats();
    const elements = {
        'pending-requests-count': stats.pending,
        'approved-requests-count': stats.approved,
        'denied-requests-count': stats.denied,
        'total-requests-count': stats.total
    };

    Object.entries(elements).forEach(([id, value]) => {
        const elem = document.getElementById(id);
        if (elem) elem.textContent = value;
    });

    const list = document.getElementById('widget-requests-list');
    if (!list) return;

    if (filtered.length === 0) {
        list.innerHTML = '<div style="padding: var(--space-4); text-align: center; color: var(--gray-600);">No ' +
            (filter === 'all' ? '' : filter + ' ') + 'widget requests found.</div>';
        return;
    }

    list.innerHTML = filtered.map((req, idx) => {
        const originalIdx = requests.indexOf(req);
        const statusColors = { pending: '#f59e0b', approved: '#38A169', denied: '#E53E3E' };
        const statusColor = statusColors[req.status] || '#718096';
        const dateStr = new Date(req.submittedAt).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
        const isUpdate = req.type === 'update';
        const typeBadge = isUpdate
            ? '<span style="padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 600; background: #DBEAFE; color: #1D4ED8; margin-left: 6px;">Update</span>'
            : '<span style="padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 600; background: #D1FAE5; color: #059669; margin-left: 6px;">New</span>';

        return '<div style="padding: var(--space-4); border-bottom: 1px solid var(--gray-300); display: flex; justify-content: space-between; align-items: center;">' +
            '<div>' +
                '<strong>' + escapeHtml(req.name) + '</strong>' + typeBadge +
                '<div style="font-size: 0.85rem; color: var(--gray-600); margin-top: 4px;">' + escapeHtml(req.description || 'No description') + '</div>' +
                '<div style="font-size: 0.75rem; color: var(--gray-600); margin-top: 4px;">Submitted: ' + dateStr + (req.submittedBy ? ' by ' + escapeHtml(req.submittedBy) : '') + '</div>' +
            '</div>' +
            '<div style="display: flex; align-items: center; gap: var(--space-2);">' +
                '<span style="padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; background: ' + statusColor + '22; color: ' + statusColor + ';">' + req.status.charAt(0).toUpperCase() + req.status.slice(1) + '</span>' +
                (req.status === 'pending' ?
                    '<button onclick="updateRequestStatus(' + originalIdx + ', \'approved\')" style="padding: 6px 12px; background: var(--success); color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.8rem;">✓ Approve</button>' +
                    '<button onclick="updateRequestStatus(' + originalIdx + ', \'denied\')" style="padding: 6px 12px; background: var(--error); color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.8rem;">✕ Deny</button>'
                : '') +
            '</div>' +
            '</div>';
    }).join('');
}

function filterWidgetRequests() {
    loadWidgetRequests();
}

function updateRequestStatus(idx, newStatus) {
    const requests = getWidgetRequests();
    if (requests[idx]) {
        requests[idx].status = newStatus;
        requests[idx].reviewedAt = new Date().toISOString();
        saveWidgetRequests(requests);
        loadWidgetRequests();
    }
}

// ─── CREATE NEW WIDGET ─────────────────────────────────────────────

function showCreateWidgetModal() {
    // Clear form fields
    document.getElementById('widget-id').value = '';
    document.getElementById('widget-name').value = '';
    document.getElementById('widget-description').value = '';
    document.getElementById('widget-default-size').value = '';
    document.getElementById('area-for-you').checked = false;
    document.getElementById('area-reporting').checked = false;
    
    showModal('createWidgetModal');
}

function createNewWidget() {
    const id = document.getElementById('widget-id').value.trim();
    const name = document.getElementById('widget-name').value.trim();
    const description = document.getElementById('widget-description').value.trim();
    const defaultSize = document.getElementById('widget-default-size').value;
    
    // Validate required fields
    if (!id || !name || !description || !defaultSize) {
        alert('Please fill in all required fields');
        return;
    }
    
    // Check if ID already exists (in base or custom)
    const allWidgets = getAllWidgets();
    if (allWidgets.some(w => w.id === id)) {
        alert('Widget ID already exists. Please use a different ID.');
        return;
    }
    
    // Get selected areas
    const areas = [];
    if (document.getElementById('area-for-you').checked) areas.push('For You');
    if (document.getElementById('area-reporting').checked) areas.push('Reporting');
    
    if (areas.length === 0) {
        alert('Please select at least one area');
        return;
    }
    
    // Create new widget object
    const newWidget = {
        id: id,
        name: name,
        description: description,
        defaultSize: defaultSize,
        defaultAreas: areas
    };
    
    // Save to custom widgets localStorage
    saveCustomWidget(newWidget);
    
    // Set widget as active
    setWidgetActive(id, true);
    
    // Set the areas for the widget
    setAreasForWidget(id, areas);
    
    // Refresh the widgets table
    loadWidgetsTable();
    
    // Close modal and show success message
    hideModal('createWidgetModal');
    alert('Widget "' + name + '" created successfully!');
}

// ─── INITIALIZATION ────────────────────────────────────────────────

function initializeWidgetManagement() {
    initializeWidgetStorage();
    loadWidgetsTable();
    loadWidgetRequests();
}

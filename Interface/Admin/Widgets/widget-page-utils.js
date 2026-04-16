// ┌─────────────────────────────────────────────────────────────────────┐
// │                   WIDGET PAGE UTILITIES                              │
// │                                                                       │
// │ Functions for pages (For You, Reporting) to display and manage       │
// │ widgets configured by Admin                                           │
// │                                                                       │
// │ Last Updated: April 16, 2026                                        │
// └─────────────────────────────────────────────────────────────────────┘

// ─── WIDGET DISPLAY ─────────────────────────────────────────────────

function getPageWidgets(pageArea) {
    return getActiveWidgetsForArea(pageArea);
}

function renderWidgetContainer(widget) {
    const display = getWidgetDisplay(widget);
    return `
        <div class="widget" id="widget-${widget.id}" data-widget-id="${widget.id}" data-size="${display.defaultSize}">
            <div class="widget-header">
                <h3 class="widget-title">${escapeHtml(display.name)}</h3>
                <div class="widget-actions">
                    <button class="widget-action-btn" onclick="editWidget('${widget.id}')">⚙️</button>
                    <button class="widget-action-btn" onclick="removeWidget('${widget.id}')">✕</button>
                </div>
            </div>
            <div class="widget-content">
                <!-- Widget content will be loaded here -->
            </div>
        </div>
    `;
}

// ─── EDIT MODE FUNCTIONS ───────────────────────────────────────────

function enterEditMode(pageArea) {
    const container = document.getElementById(`${pageArea.toLowerCase().replace(/\s+/g, '-')}-widgets-container`);
    if (!container) return;

    container.classList.add('edit-mode');
    document.body.classList.add('widget-edit-mode');

    // Show edit controls for each widget
    document.querySelectorAll('.widget').forEach(widget => {
        widget.classList.add('edit-enabled');
    });

    // Show the "Add Widget" button
    const addBtn = document.getElementById('add-widget-btn-' + pageArea.toLowerCase().replace(/\s+/g, '-'));
    if (addBtn) addBtn.style.display = 'block';
}

function exitEditMode(pageArea) {
    const container = document.getElementById(`${pageArea.toLowerCase().replace(/\s+/g, '-')}-widgets-container`);
    if (!container) return;

    container.classList.remove('edit-mode');
    document.body.classList.remove('widget-edit-mode');

    // Hide edit controls for each widget
    document.querySelectorAll('.widget').forEach(widget => {
        widget.classList.remove('edit-enabled');
    });

    // Hide the "Add Widget" button
    const addBtn = document.getElementById('add-widget-btn-' + pageArea.toLowerCase().replace(/\s+/g, '-'));
    if (addBtn) addBtn.style.display = 'none';
}

function toggleEditMode(pageArea) {
    if (document.body.classList.contains('widget-edit-mode')) {
        exitEditMode(pageArea);
    } else {
        enterEditMode(pageArea);
    }
}

// ─── WIDGET ACTIONS ────────────────────────────────────────────────

function editWidget(widgetId) {
    const widget = getWidgetById(widgetId);
    if (!widget) return;

    const display = getWidgetDisplay(widget);

    // Populate edit modal
    document.getElementById('edit-widget-id').value = widgetId;
    document.getElementById('edit-widget-name').value = display.name;
    document.getElementById('edit-widget-description').value = display.description;
    document.getElementById('edit-widget-size').value = display.defaultSize;

    // Show modal (assumes showModal function exists in parent page)
    if (typeof showModal !== 'undefined') {
        showModal('editWidgetModal');
    }
}

function removeWidget(widgetId) {
    if (!confirm('Remove this widget from this page?')) {
        return;
    }

    const currentAreas = getAreasForWidget(widgetId);
    const pageArea = document.body.getAttribute('data-page-area') || 'For You';
    const newAreas = currentAreas.filter(area => area !== pageArea);

    if (newAreas.length === 0) {
        alert('Widget must appear on at least one page. You can deactivate it via Admin panel.');
        return;
    }

    setAreasForWidget(widgetId, newAreas);

    // Remove widget element from DOM
    const widget = document.getElementById(`widget-${widgetId}`);
    if (widget) {
        widget.classList.add('removing');
        setTimeout(() => {
            widget.remove();
        }, 300);
    }
}

function addWidgetToPage(widgetId, pageArea) {
    const widget = getWidgetById(widgetId);
    if (!widget) return;

    const currentAreas = getAreasForWidget(widgetId);
    if (!currentAreas.includes(pageArea)) {
        setAreasForWidget(widgetId, [...currentAreas, pageArea]);
    }

    // Add widget to page
    const container = document.getElementById(`${pageArea.toLowerCase().replace(/\s+/g, '-')}-widgets-container`);
    if (container) {
        const widgetElement = document.createElement('div');
        widgetElement.innerHTML = renderWidgetContainer(widget);
        container.appendChild(widgetElement.firstElementChild);
    }
}

// ─── ADD WIDGET MODAL ───────────────────────────────────────────────

function getAvailableWidgetsForPage(pageArea) {
    // Get widgets that are:
    // 1. Active
    // 2. Configured for this page area
    // 3. Not already visible on this page
    const activeWidgets = getActiveWidgetsForArea(pageArea);
    const onPage = document.querySelectorAll('.widget[data-widget-id]');
    const onPageIds = new Set(Array.from(onPage).map(w => w.getAttribute('data-widget-id')));

    return activeWidgets.filter(w => !onPageIds.has(w.id));
}

function populateAddWidgetModal(pageArea) {
    const available = getAvailableWidgetsForPage(pageArea);
    const select = document.getElementById('add-widget-select');

    if (!select) return;

    select.innerHTML = '<option value="">-- Select a Widget --</option>';

    if (available.length === 0) {
        select.innerHTML = '<option value="" disabled>All widgets currently on dashboard</option>';
        return;
    }

    available.forEach(widget => {
        const display = getWidgetDisplay(widget);
        const option = document.createElement('option');
        option.value = widget.id;
        option.textContent = display.name;
        select.appendChild(option);
    });

    // Store the page area for later use
    select.setAttribute('data-page-area', pageArea);
}

function openAddWidgetModal(pageArea) {
    // CRITICAL: Show modal FIRST, then populate
    // Prevents early returns from blocking modal display
    const modal = document.getElementById('addWidgetModal');
    if (!modal) {
        console.error('addWidgetModal element not found');
        return;
    }
    
    // Show the modal immediately
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
    
    // THEN populate the content
    populateAddWidgetModal(pageArea);
}

function confirmAddWidget() {
    const select = document.getElementById('add-widget-select');
    if (!select) return;

    const widgetId = select.value;
    const pageArea = select.getAttribute('data-page-area') || 'For You';

    if (!widgetId) {
        alert('Please select a widget');
        return;
    }

    addWidgetToPage(widgetId, pageArea);

    if (typeof hideModal !== 'undefined') {
        hideModal('addWidgetModal');
    }

    select.value = '';
}

// ─── WIDGET PERSISTENCE ────────────────────────────────────────────

function savePageWidgetState(pageArea) {
    // This is handled by localStorage automatically
    // But you can add additional validation or logging here
    console.log(`Widget state saved for ${pageArea}`);
}

function loadPageWidgetState(pageArea) {
    const widgets = getPageWidgets(pageArea);
    return widgets;
}

// ─── PAGE INITIALIZATION ────────────────────────────────────────────

function initializePageWidgets(pageArea) {
    // Initialize storage
    initializeWidgetStorage();

    // Load and display widgets for this page area
    const widgets = loadPageWidgetState(pageArea);
    const container = document.getElementById(`${pageArea.toLowerCase().replace(/\s+/g, '-')}-widgets-container`);

    if (!container) {
        console.warn(`Widget container not found for ${pageArea}`);
        return;
    }

    container.innerHTML = widgets
        .map(widget => renderWidgetContainer(widget))
        .join('');

    console.log(`Initialized ${widgets.length} widgets for ${pageArea} page`);
}

// ─── UTILITIES ──────────────────────────────────────────────────────

function getWidgetCountForPage(pageArea) {
    return getPageWidgets(pageArea).length;
}

function hasWidgetOnPage(widgetId, pageArea) {
    const areas = getAreasForWidget(widgetId);
    return areas.includes(pageArea);
}

function getPageAreaFromElement(element) {
    // Try to determine the page area from the element or its parents
    if (element.hasAttribute('data-page-area')) {
        return element.getAttribute('data-page-area');
    }

    let current = element;
    while (current) {
        if (current.id && current.id.includes('container')) {
            if (current.id.includes('for-you')) return 'For You';
            if (current.id.includes('reporting')) return 'Reporting';
        }
        current = current.parentElement;
    }

    return 'For You'; // default
}

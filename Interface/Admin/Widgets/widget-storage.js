// ┌─────────────────────────────────────────────────────────────────────┐
// │                   WIDGET STORAGE UTILITIES                           │
// │                                                                       │
// │ Handles all localStorage operations for widgets across all pages     │
// │ - Widget active/inactive state                                       │
// │ - Widget area assignments (For You vs Reporting)                     │
// │ - Widget customizations (name, description, size)                    │
// │ - Widget requests from users                                         │
// │                                                                       │
// │ Last Updated: April 16, 2026                                        │
// └─────────────────────────────────────────────────────────────────────┘

// ─── LOCAL STORAGE KEYS ─────────────────────────────────────────────
const WIDGET_STORAGE_KEYS = {
    ACTIVE_STATE: 'activity-hub-widget-active',
    AREA_ASSIGNMENTS: 'activity-hub-widget-areas',
    CUSTOMIZATIONS: 'activity-hub-widget-customizations',
    WIDGET_REQUESTS: 'activity-hub-widget-requests',
    CUSTOM_WIDGETS: 'activity-hub-custom-widgets'
};

// ─── WIDGET ACTIVE STATE ────────────────────────────────────────────
// Tracks which widgets are enabled/disabled (true = enabled, false or missing = disabled)

function getWidgetActiveState() {
    try {
        return JSON.parse(localStorage.getItem(WIDGET_STORAGE_KEYS.ACTIVE_STATE) || '{}');
    } catch (e) {
        console.error('Error parsing widget active state:', e);
        return {};
    }
}

function isWidgetActive(widgetId) {
    const state = getWidgetActiveState();
    return state[widgetId] !== false;
}

function setWidgetActive(widgetId, isActive) {
    const state = getWidgetActiveState();
    state[widgetId] = isActive;
    localStorage.setItem(WIDGET_STORAGE_KEYS.ACTIVE_STATE, JSON.stringify(state));
}

// ─── WIDGET AREA ASSIGNMENTS ────────────────────────────────────────
// Tracks which areas each widget appears in (For You, Reporting, etc.)

function getWidgetAreas() {
    try {
        return JSON.parse(localStorage.getItem(WIDGET_STORAGE_KEYS.AREA_ASSIGNMENTS) || '{}');
    } catch (e) {
        console.error('Error parsing widget areas:', e);
        return {};
    }
}

function getAreasForWidget(widgetId) {
    const saved = getWidgetAreas();
    if (saved[widgetId]) {
        return saved[widgetId];
    }
    // Fall back to widget's default areas
    const widget = getWidgetById(widgetId);
    return widget ? widget.defaultAreas : [];
}

function setAreasForWidget(widgetId, areas) {
    const allAreas = getWidgetAreas();
    allAreas[widgetId] = areas;
    localStorage.setItem(WIDGET_STORAGE_KEYS.AREA_ASSIGNMENTS, JSON.stringify(allAreas));
}

function toggleWidgetArea(widgetId, area) {
    const current = getAreasForWidget(widgetId).slice();
    const idx = current.indexOf(area);
    if (idx >= 0) {
        current.splice(idx, 1);
    } else {
        current.push(area);
    }
    setAreasForWidget(widgetId, current);
}

// Get active widgets for a specific area
function getActiveWidgetsForArea(area) {
    const allWidgets = getAllWidgets();
    return allWidgets.filter(widget => {
        const isActive = isWidgetActive(widget.id);
        const areas = getAreasForWidget(widget.id);
        return isActive && areas.includes(area);
    });
}

// ─── WIDGET CUSTOMIZATIONS ──────────────────────────────────────────
// Tracks custom names, descriptions, and sizes

function getWidgetCustomizations() {
    try {
        return JSON.parse(localStorage.getItem(WIDGET_STORAGE_KEYS.CUSTOMIZATIONS) || '{}');
    } catch (e) {
        console.error('Error parsing widget customizations:', e);
        return {};
    }
}

function getWidgetCustomization(widgetId) {
    const customizations = getWidgetCustomizations();
    return customizations[widgetId] || null;
}

function setWidgetCustomization(widgetId, customization) {
    const customizations = getWidgetCustomizations();
    customizations[widgetId] = customization;
    localStorage.setItem(WIDGET_STORAGE_KEYS.CUSTOMIZATIONS, JSON.stringify(customizations));
}

function getWidgetDisplay(widget) {
    const custom = getWidgetCustomization(widget.id);
    return {
        name: custom?.name || widget.name,
        description: custom?.description || widget.description,
        defaultSize: custom?.defaultSize || widget.defaultSize
    };
}

// ─── WIDGET REQUESTS ────────────────────────────────────────────────
// Tracks user requests for new widgets or widgets updates

function getWidgetRequests() {
    try {
        return JSON.parse(localStorage.getItem(WIDGET_STORAGE_KEYS.WIDGET_REQUESTS) || '[]');
    } catch (e) {
        console.error('Error parsing widget requests:', e);
        return [];
    }
}

function saveWidgetRequests(requests) {
    localStorage.setItem(WIDGET_STORAGE_KEYS.WIDGET_REQUESTS, JSON.stringify(requests));
}

function addWidgetRequest(request) {
    const requests = getWidgetRequests();
    requests.push({
        ...request,
        submittedAt: new Date().toISOString()
    });
    saveWidgetRequests(requests);
}

function updateWidgetRequest(index, updates) {
    const requests = getWidgetRequests();
    if (requests[index]) {
        requests[index] = {
            ...requests[index],
            ...updates
        };
        saveWidgetRequests(requests);
    }
}

function getWidgetRequestStats() {
    const requests = getWidgetRequests();
    return {
        total: requests.length,
        pending: requests.filter(r => r.status === 'pending').length,
        approved: requests.filter(r => r.status === 'approved').length,
        denied: requests.filter(r => r.status === 'denied').length
    };
}

// ─── RESET & INITIALIZATION ────────────────────────────────────────

function resetWidgetStorage() {
    localStorage.removeItem(WIDGET_STORAGE_KEYS.ACTIVE_STATE);
    localStorage.removeItem(WIDGET_STORAGE_KEYS.AREA_ASSIGNMENTS);
    localStorage.removeItem(WIDGET_STORAGE_KEYS.CUSTOMIZATIONS);
    localStorage.removeItem(WIDGET_STORAGE_KEYS.WIDGET_REQUESTS);
    console.log('Widget storage reset to defaults');
}


// ─── CUSTOM WIDGETS (PERSISTED) ────────────────────────────────────
// Stores user/admin-created widgets that are saved between sessions

function getCustomWidgets() {
    try {
        return JSON.parse(localStorage.getItem(WIDGET_STORAGE_KEYS.CUSTOM_WIDGETS) || '[]');
    } catch (e) {
        console.error('Error parsing custom widgets:', e);
        return [];
    }
}

function saveCustomWidget(widget) {
    const custom = getCustomWidgets();
    // Remove if exists
    const idx = custom.findIndex(w => w.id === widget.id);
    if (idx >= 0) {
        custom[idx] = widget;
    } else {
        custom.push(widget);
    }
    localStorage.setItem(WIDGET_STORAGE_KEYS.CUSTOM_WIDGETS, JSON.stringify(custom));
}

function getAllWidgets() {
    // Merge base registry with custom widgets
    const custom = getCustomWidgets();
    const allWidgets = [...WIDGET_REGISTRY];
    
    // Add or update with custom widgets
    custom.forEach(customWidget => {
        const idx = allWidgets.findIndex(w => w.id === customWidget.id);
        if (idx >= 0) {
            allWidgets[idx] = customWidget;
        } else {
            allWidgets.push(customWidget);
        }
    });
    
    return allWidgets;
}

// ─── WIDGET INITIALIZATION ─────────────────────────────────────────

function initializeWidgetStorage() {
    // Merge custom widgets into the active state
    const allWidgets = getAllWidgets();
    
    // Initialize active state - all widgets are active by default
    if (!localStorage.getItem(WIDGET_STORAGE_KEYS.ACTIVE_STATE)) {
        const state = {};
        allWidgets.forEach(w => {
            state[w.id] = true;
        });
        localStorage.setItem(WIDGET_STORAGE_KEYS.ACTIVE_STATE, JSON.stringify(state));
    }
    
    // Initialize area assignments with defaults
    if (!localStorage.getItem(WIDGET_STORAGE_KEYS.AREA_ASSIGNMENTS)) {
        const areas = {};
        allWidgets.forEach(w => {
            areas[w.id] = w.defaultAreas;
        });
        localStorage.setItem(WIDGET_STORAGE_KEYS.AREA_ASSIGNMENTS, JSON.stringify(areas));
    }

    // Initialize area assignments - use default areas
    if (!localStorage.getItem(WIDGET_STORAGE_KEYS.AREA_ASSIGNMENTS)) {
        const areas = {};
        WIDGET_REGISTRY.forEach(w => {
            areas[w.id] = w.defaultAreas;
        });
        localStorage.setItem(WIDGET_STORAGE_KEYS.AREA_ASSIGNMENTS, JSON.stringify(areas));
    }
}

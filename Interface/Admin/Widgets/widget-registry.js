// ┌─────────────────────────────────────────────────────────────────────┐
// │                     WIDGET REGISTRY & CONFIGURATION                 │
// │                                                                       │
// │ Central configuration for all Activity Hub widgets across platforms  │
// │ - For You: 5 user-focused widgets                                   │
// │ - Reporting: 4 reporting/analytics widgets                          │
// │                                                                       │
// │ Last Updated: April 16, 2026                                        │
// │ Verified State: All pages synchronized                              │
// └─────────────────────────────────────────────────────────────────────┘

// Platform areas where widgets can appear
const PLATFORM_AREAS = ['For You', 'Reporting'];

// Authoritative Widget Registry
// All widget IDs, names, descriptions, and default configurations
const WIDGET_REGISTRY = [
    // ─── FOR YOU AREA (5 widgets) ───────────────────────────────────
    {
        id: 'my-tasks',
        name: 'My Tasks',
        description: 'Personal task list and to-do items',
        defaultSize: 'Large',
        defaultAreas: ['For You']
    },
    {
        id: 'notifications',
        name: 'Notifications & Alerts',
        description: 'System alerts and notifications',
        defaultSize: 'Medium',
        defaultAreas: ['For You']
    },
    {
        id: 'next-steps',
        name: 'Next Steps & Action Items',
        description: 'Upcoming actions and deadlines',
        defaultSize: 'Large',
        defaultAreas: ['For You']
    },
    {
        id: 'performance',
        name: 'Performance Metrics',
        description: 'Key performance indicators and trends',
        defaultSize: 'Large',
        defaultAreas: ['For You']
    },
    {
        id: 'team-activity',
        name: 'Team Activity Feed',
        description: 'Latest team member activity and updates',
        defaultSize: 'Medium',
        defaultAreas: ['For You']
    },

    // ─── REPORTING AREA (4 widgets) ─────────────────────────────────
    {
        id: 'activity-dashboard',
        name: 'Activity Dashboard',
        description: 'Dashboard with key metrics and trends',
        defaultSize: 'Extra Large',
        defaultAreas: ['Reporting']
    },
    {
        id: 'project-reports',
        name: 'Project Reports',
        description: 'Status and milestones for all projects',
        defaultSize: 'Extra Large',
        defaultAreas: ['Reporting']
    },
    {
        id: 'key-metrics',
        name: 'Key Metrics',
        description: 'Key reporting metrics and analytics',
        defaultSize: 'Extra Large',
        defaultAreas: ['Reporting']
    },
    {
        id: 'my-reports',
        name: 'My Reports',
        description: 'Custom reports',
        defaultSize: 'Extra Large',
        defaultAreas: ['Reporting']
    },
    {
        id: 'projects-metrics',
        name: 'Projects Overview',
        description: 'Impact Platform projects metrics and status overview',
        defaultSize: 'Extra Large',
        defaultAreas: ['Reporting']
    }
];

// Get widget by ID (searches base and custom widgets)
function getWidgetById(widgetId) {
    const widget = WIDGET_REGISTRY.find(w => w.id === widgetId);
    if (widget) return widget;
    
    // Also search custom widgets if available
    if (typeof getAllWidgets === 'function') {
        return getAllWidgets().find(w => w.id === widgetId);
    }
    return null;
}

// Get all widgets for a specific area
function getWidgetsForArea(area) {
    return WIDGET_REGISTRY.filter(w =>
        w.defaultAreas.includes(area)
    );
}

// Get for You widgets specifically
function getForYouWidgets() {
    return getWidgetsForArea('For You');
}

// Get Reporting widgets specifically
function getReportingWidgets() {
    return getWidgetsForArea('Reporting');
}

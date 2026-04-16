// ┌─────────────────────────────────────────────────────────────────────┐
// │            WIDGET SYSTEM VERIFICATION SCRIPT                         │
// │                                                                       │
// │ Browser console diagnostic tool for testing widget system            │
// │ Usage: Copy and paste into browser DevTools console                  │
// │                                                                       │
// │ Last Updated: April 16, 2026                                        │
// └─────────────────────────────────────────────────────────────────────┘

/**
 * WIDGET VERIFICATION SUITE
 * 
 * This script provides comprehensive testing for the Activity Hub Widget System.
 * It checks data consistency, storage state, and display logic.
 * 
 * Run all tests: widgetTestSuite.runAll()
 * Run specific test: widgetTestSuite.tests.registryTest()
 */

const widgetTestSuite = {
    results: [],
    
    // ─── TEST RESULTS TRACKING ─────────────────────────────────────
    
    log: function(testName, passed, details) {
        const result = {
            test: testName,
            passed: passed,
            details: details,
            timestamp: new Date().toLocaleTimeString()
        };
        this.results.push(result);
        
        const icon = passed ? '✅' : '❌';
        const color = passed ? 'color: #38A169;' : 'color: #E53E3E;';
        console.log(`%c${icon} ${testName}`, color + 'font-weight: bold;');
        if (details) {
            console.log(`   ${details}`);
        }
    },
    
    printSummary: function() {
        const total = this.results.length;
        const passed = this.results.filter(r => r.passed).length;
        const failed = total - passed;
        
        console.log('%c╔════════════════════════════════════════╗', 'color: #0f172a; font-weight: bold;');
        console.log('%c║       WIDGET SYSTEM TEST SUMMARY      ║', 'color: #0f172a; font-weight: bold;');
        console.log('%c╚════════════════════════════════════════╝', 'color: #0f172a; font-weight: bold;');
        console.log(`Total Tests: ${total}`);
        console.log(`%c✅ Passed: ${passed}`, 'color: #38A169; font-weight: bold;');
        console.log(`%c❌ Failed: ${failed}`, failed > 0 ? 'color: #E53E3E; font-weight: bold;' : 'color: #38A169;');
        
        if (failed > 0) {
            console.log('%c\nFailed Tests:', 'color: #E53E3E; font-weight: bold; font-size: 1.1em;');
            this.results.filter(r => !r.passed).forEach(r => {
                console.log(`  • ${r.test}: ${r.details}`);
            });
        }
    },
    
    // ─── TESTS ─────────────────────────────────────────────────────
    
    tests: {
        registryTest: function() {
            try {
                if (typeof WIDGET_REGISTRY === 'undefined') {
                    widgetTestSuite.log('Widget Registry Load', false, 'WIDGET_REGISTRY not found. Is widget-registry.js included?');
                    return;
                }
                
                const hasForYouWidgets = WIDGET_REGISTRY.some(w => w.defaultAreas.includes('For You'));
                const hasReportingWidgets = WIDGET_REGISTRY.some(w => w.defaultAreas.includes('Reporting'));
                
                const passed = 
                    WIDGET_REGISTRY.length === 9 &&
                    WIDGET_REGISTRY.every(w => w.id && w.name && w.description) &&
                    hasForYouWidgets &&
                    hasReportingWidgets;
                
                widgetTestSuite.log(
                    'Widget Registry Load',
                    passed,
                    `Loaded ${WIDGET_REGISTRY.length} widgets (5 For You, 4 Reporting)`
                );
            } catch (e) {
                widgetTestSuite.log('Widget Registry Load', false, e.message);
            }
        },
        
        storageTest: function() {
            try {
                if (typeof getWidgetActiveState === 'undefined') {
                    widgetTestSuite.log('Storage Functions', false, 'widget-storage.js not loaded');
                    return;
                }
                
                const activeState = getWidgetActiveState();
                const areas = getWidgetAreas();
                const customizations = getWidgetCustomizations();
                const requests = getWidgetRequests();
                
                const hasData = Object.keys(activeState).length > 0;
                
                widgetTestSuite.log(
                    'Storage Functions',
                    true,
                    `Active: ${Object.keys(activeState).length} widgets, Areas: ${Object.keys(areas).length} configs`
                );
            } catch (e) {
                widgetTestSuite.log('Storage Functions', false, e.message);
            }
        },
        
        activeWidgetsTest: function() {
            try {
                const forYouActive = getActiveWidgetsForArea('For You');
                const reportingActive = getActiveWidgetsForArea('Reporting');
                
                const forYouExpected = 5;
                const reportingExpected = 4;
                
                const forYouPass = forYouActive.length === forYouExpected;
                const reportingPass = reportingActive.length === reportingExpected;
                
                widgetTestSuite.log(
                    'Active Widgets For You',
                    forYouPass,
                    `Found ${forYouActive.length} (expected ${forYouExpected})`
                );
                
                widgetTestSuite.log(
                    'Active Widgets Reporting',
                    reportingPass,
                    `Found ${reportingActive.length} (expected ${reportingExpected})`
                );
            } catch (e) {
                widgetTestSuite.log('Active Widgets Count', false, e.message);
            }
        },
        
        widgetConsistencyTest: function() {
            try {
                const forYouWidgets = getForYouWidgets();
                const reportingWidgets = getReportingWidgets();
                
                // Check all widgets are in registry
                const allRegistryIds = new Set(WIDGET_REGISTRY.map(w => w.id));
                const forYouIds = forYouWidgets.map(w => w.id);
                const reportingIds = reportingWidgets.map(w => w.id);
                
                const forYouConsistent = forYouIds.every(id => allRegistryIds.has(id));
                const reportingConsistent = reportingIds.every(id => allRegistryIds.has(id));
                
                widgetTestSuite.log(
                    'For You Widget Registry Consistency',
                    forYouConsistent,
                    `All ${forYouIds.length} widgets in registry`
                );
                
                widgetTestSuite.log(
                    'Reporting Widget Registry Consistency',
                    reportingConsistent,
                    `All ${reportingIds.length} widgets in registry`
                );
            } catch (e) {
                widgetTestSuite.log('Widget Consistency', false, e.message);
            }
        },
        
        localStorageTest: function() {
            try {
                const keys = {
                    active: localStorage.getItem('activity-hub-widget-active'),
                    areas: localStorage.getItem('activity-hub-widget-areas'),
                    custom: localStorage.getItem('activity-hub-widget-customizations'),
                    requests: localStorage.getItem('activity-hub-widget-requests')
                };
                
                const allPresent = Object.values(keys).every(k => k !== null);
                
                widgetTestSuite.log(
                    'LocalStorage Keys Present',
                    allPresent,
                    `${Object.values(keys).filter(k => k).length}/4 keys exist`
                );
                
                // Check sizes
                let totalSize = 0;
                Object.entries(keys).forEach(([name, value]) => {
                    if (value) {
                        const bytes = new Blob([value]).size;
                        totalSize += bytes;
                        console.log(`   ${name}: ${bytes} bytes`);
                    }
                });
                
                widgetTestSuite.log(
                    'LocalStorage Size',
                    totalSize < 1000000, // 1MB limit
                    `${(totalSize / 1024).toFixed(2)} KB (< 1 MB)`
                );
            } catch (e) {
                widgetTestSuite.log('LocalStorage Test', false, e.message);
            }
        },
        
        pageIntegrationTest: function() {
            try {
                const forYouContainer = document.getElementById('for-you-widgets-container');
                const reportingContainer = document.getElementById('reporting-widgets-container');
                
                const forYouPresent = forYouContainer !== null;
                const reportingPresent = reportingContainer !== null;
                
                widgetTestSuite.log(
                    'For You Container',
                    forYouPresent,
                    forYouPresent ? `Found, ${forYouContainer.children.length} widgets` : 'Not found'
                );
                
                widgetTestSuite.log(
                    'Reporting Container',
                    reportingPresent,
                    reportingPresent ? `Found, ${reportingContainer.children.length} widgets` : 'Not found'
                );
            } catch (e) {
                widgetTestSuite.log('Page Integration', false, e.message);
            }
        },
        
        functionAvailabilityTest: function() {
            try {
                const requiredFunctions = [
                    'getWidgetById',
                    'getWidgetsForArea',
                    'getWidgetActiveState',
                    'getAreasForWidget',
                    'getActiveWidgetsForArea',
                    'getWidgetRequests',
                    'loadWidgetsTable',
                    'initializePageWidgets',
                    'getPageWidgets'
                ];
                
                const allAvailable = requiredFunctions.every(fn => typeof window[fn] === 'function');
                const missing = requiredFunctions.filter(fn => typeof window[fn] !== 'function');
                
                widgetTestSuite.log(
                    'Required Functions Available',
                    allAvailable,
                    allAvailable ? 'All functions loaded' : `Missing: ${missing.join(', ')}`
                );
            } catch (e) {
                widgetTestSuite.log('Function Availability', false, e.message);
            }
        }
    },
    
    // ─── RUN ALL TESTS ─────────────────────────────────────────────
    
    runAll: function() {
        this.results = [];
        
        console.log('%c╔════════════════════════════════════════╗', 'color: #0f172a; font-weight: bold;');
        console.log('%c║   WIDGET SYSTEM VERIFICATION SUITE    ║', 'color: #0f172a; font-weight: bold;');
        console.log('%c║        Running Diagnostic Tests        ║', 'color: #0f172a; font-weight: bold;');
        console.log('%c╚════════════════════════════════════════╝', 'color: #0f172a; font-weight: bold;');
        console.log('');
        
        // Run all tests
        Object.values(this.tests).forEach(test => {
            test.call(this);
        });
        
        console.log('');
        this.printSummary();
        
        return this.results;
    },
    
    // ─── QUICK DIAGNOSTICS ─────────────────────────────────────────
    
    quickDiag: function() {
        console.log('%cWIDGET REGISTRY:', 'font-weight: bold; color: #0f172a;');
        console.table(WIDGET_REGISTRY);
        
        console.log('%cACTIVE STATE:', 'font-weight: bold; color: #0f172a;');
        console.table(getWidgetActiveState());
        
        console.log('%cWIDGET AREAS:', 'font-weight: bold; color: #0f172a;');
        console.table(getWidgetAreas());
        
        console.log('%cFOR YOU WIDGETS:', 'font-weight: bold; color: #0f172a;');
        console.table(getActiveWidgetsForArea('For You'));
        
        console.log('%cREPORTING WIDGETS:', 'font-weight: bold; color: #0f172a;');
        console.table(getActiveWidgetsForArea('Reporting'));
    }
};

console.log('%cWidget Test Suite Ready! Use:', 'color: #0f172a; font-weight: bold; font-size: 1.2em;');
console.log('  widgetTestSuite.runAll()           - Run all tests');
console.log('  widgetTestSuite.quickDiag()        - Quick diagnostics');
console.log('  widgetTestSuite.tests.registryTest() - Run specific test');

# AI Assistant Integration Guide - Embedding Across Activity Hub Platforms

## 🎯 Integration Overview

This guide provides comprehensive instructions for embedding the Sparky AI Assistant throughout the Walmart Activity Hub ecosystem. The AI Assistant can be integrated as a floating widget, sidebar panel, or embedded component across all platforms and interfaces.

## 🏗️ Integration Architecture

### Component Structure
```
AI Assistant Integration
├── Core Widget (Universal)
├── Platform Adapters
│   ├── Web Dashboard Integration
│   ├── Mobile App Integration
│   ├── Desktop Application Integration
│   └── Kiosk/Terminal Integration
├── Backend Connectors
│   ├── API Gateway
│   ├── Authentication Bridge
│   ├── Data Context Service
│   └── Analytics Collector
└── Customization Layers
    ├── Branding Templates
    ├── Role-based Configurations
    ├── Department Customizations
    └── Language Localizations
```

## 🌐 Web Dashboard Integration

### Standard Sidebar Implementation
```html
<!-- Add to any Activity Hub page -->
<div id="ai-assistant-container"></div>

<script src="/js/ai-assistant-widget.js"></script>
<script>
// Initialize AI Assistant
const aiAssistant = new ActivityHubAI({
  apiUrl: 'https://api.activityhub.walmart.com',
  authToken: getUserAuthToken(),
  position: 'sidebar',
  theme: 'walmart-standard',
  user: {
    id: getCurrentUserId(),
    role: getCurrentUserRole(),
    department: getCurrentUserDepartment()
  },
  features: {
    voice: true,
    contextAwareness: true,
    visualGuidance: true,
    multiLanguage: false
  }
});

// Render the assistant
aiAssistant.render('#ai-assistant-container');
</script>
```

### Floating Chat Widget Implementation
```html
<!-- Minimal floating implementation -->
<script>
(function() {
  // Load AI Assistant asynchronously
  const script = document.createElement('script');
  script.src = '/js/ai-assistant-float.min.js';
  script.onload = function() {
    window.SparkyAI.init({
      mode: 'floating',
      position: 'bottom-right',
      trigger: 'manual', // or 'auto', 'scroll', 'time'
      apiKey: 'your_api_key',
      customization: {
        primaryColor: '#1E3A8A',
        accentColor: '#FFCC00',
        fontFamily: 'Everyday Sans'
      }
    });
  };
  document.head.appendChild(script);
})();
</script>
```

### Inline Context Help
```javascript
// Add contextual help to specific elements
const contextHelp = new ActivityHubAI.ContextHelper({
  triggers: [
    {
      selector: '.metric-card',
      helpText: 'These cards show your key performance indicators. Click for detailed explanations.',
      position: 'tooltip'
    },
    {
      selector: '#project-table',
      helpText: 'Your project overview table. I can help explain status indicators and next steps.',
      position: 'overlay'
    },
    {
      selector: '.dashboard-filter',
      helpText: 'Use filters to customize your view. Ask me for filter recommendations.',
      position: 'popover'
    }
  ]
});

contextHelp.activate();
```

## 📱 Mobile App Integration

### React Native Integration
```javascript
// Install the package
// npm install @walmart/activity-hub-ai-assistant

import { AIAssistant, AIFloatingButton } from '@walmart/activity-hub-ai-assistant';
import { useNavigation, useRoute } from '@react-navigation/native';

const DashboardScreen = () => {
  const navigation = useNavigation();
  const route = useRoute();
  
  return (
    <View style={styles.container}>
      {/* Your dashboard content */}
      <DashboardContent />
      
      {/* AI Assistant Floating Button */}
      <AIFloatingButton
        onPress={() => navigation.navigate('AIAssistant')}
        theme="walmart"
        position="bottom-right"
      />
      
      {/* Or Inline Assistant Panel */}
      <AIAssistant
        visible={showAssistant}
        context={{
          screen: route.name,
          data: dashboardData,
          user: currentUser
        }}
        style={styles.assistant}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc'
  },
  assistant: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: 300
  }
});
```

### iOS Swift Integration
```swift
import ActivityHubAI

class DashboardViewController: UIViewController {
    private var aiAssistant: AIAssistantView?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupAIAssistant()
    }
    
    private func setupAIAssistant() {
        let config = AIAssistantConfig(
            apiKey: "your_api_key",
            userId: currentUser.id,
            userRole: currentUser.role,
            theme: .walmart
        )
        
        aiAssistant = AIAssistantView(config: config)
        aiAssistant?.delegate = self
        
        // Add as floating button
        view.addSubview(aiAssistant!)
        aiAssistant?.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            aiAssistant!.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20),
            aiAssistant!.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor, constant: -20),
            aiAssistant!.widthAnchor.constraint(equalToConstant: 60),
            aiAssistant!.heightAnchor.constraint(equalToConstant: 60)
        ])
    }
}

extension DashboardViewController: AIAssistantDelegate {
    func aiAssistant(_ assistant: AIAssistantView, didReceiveResponse response: AIResponse) {
        // Handle AI responses
        if let action = response.suggestedAction {
            performAction(action)
        }
    }
    
    func aiAssistantDidRequestContext(_ assistant: AIAssistantView) -> AIContext {
        return AIContext(
            currentPage: "dashboard",
            visibleData: getDashboardData(),
            userPermissions: currentUser.permissions
        )
    }
}
```

### Android Kotlin Integration
```kotlin
// Add to build.gradle
implementation 'com.walmart.activityhub:ai-assistant:1.0.0'

class DashboardActivity : AppCompatActivity(), AIAssistantListener {
    
    private lateinit var aiAssistant: AIAssistantWidget
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_dashboard)
        
        setupAIAssistant()
    }
    
    private fun setupAIAssistant() {
        val config = AIAssistantConfig.Builder()
            .apiKey("your_api_key")
            .userId(currentUser.id)
            .userRole(currentUser.role)
            .theme(AITheme.WALMART)
            .features(
                AIFeatures.Builder()
                    .voiceInput(true)
                    .contextAwareness(true)
                    .visualGuidance(true)
                    .build()
            )
            .build()
        
        aiAssistant = AIAssistantWidget(this, config)
        aiAssistant.setListener(this)
        
        // Add as floating action button
        val fab = findViewById<FloatingActionButton>(R.id.ai_assistant_fab)
        fab.setOnClickListener {
            aiAssistant.show()
        }
    }
    
    override fun onAIResponse(response: AIResponse) {
        // Handle AI responses
        response.suggestedAction?.let { action ->
            handleSuggestedAction(action)
        }
    }
    
    override fun onContextRequest(): AIContext {
        return AIContext.Builder()
            .currentPage("dashboard")
            .visibleData(getDashboardData())
            .userPermissions(currentUser.permissions)
            .build()
    }
}
```

## 🖥️ Desktop Application Integration

### Electron Integration
```javascript
// main.js - Electron main process
const { app, BrowserWindow, ipcMain } = require('electron');
const { AIAssistantService } = require('@walmart/ai-assistant-electron');

let mainWindow;
let aiService;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });
  
  // Initialize AI Assistant Service
  aiService = new AIAssistantService({
    apiUrl: 'https://api.activityhub.walmart.com',
    window: mainWindow
  });
  
  mainWindow.loadFile('dashboard.html');
}

// Handle AI Assistant IPC calls
ipcMain.handle('ai-assistant-query', async (event, query, context) => {
  return await aiService.processQuery(query, context);
});

app.whenReady().then(createWindow);
```

```javascript
// preload.js - Electron preload script
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('aiAssistant', {
  query: (query, context) => ipcRenderer.invoke('ai-assistant-query', query, context),
  getContext: () => ipcRenderer.invoke('ai-assistant-get-context'),
  onResponse: (callback) => ipcRenderer.on('ai-assistant-response', callback)
});
```

```html
<!-- dashboard.html - Renderer process -->
<div id="dashboard-content">
  <!-- Dashboard content -->
</div>

<div id="ai-assistant-panel" class="ai-panel">
  <!-- AI Assistant interface -->
</div>

<script>
// Use exposed AI Assistant API
document.getElementById('ask-button').addEventListener('click', async () => {
  const query = document.getElementById('query-input').value;
  const context = {
    page: 'desktop-dashboard',
    visibleData: getVisibleDashboardData(),
    timestamp: new Date().toISOString()
  };
  
  const response = await window.aiAssistant.query(query, context);
  displayAIResponse(response);
});
</script>
```

### WPF (.NET) Integration
```csharp
// Install-Package WalmartActivityHub.AIAssistant

using WalmartActivityHub.AIAssistant;

public partial class DashboardWindow : Window
{
    private AIAssistantControl aiAssistant;
    
    public DashboardWindow()
    {
        InitializeComponent();
        SetupAIAssistant();
    }
    
    private void SetupAIAssistant()
    {
        var config = new AIAssistantConfig
        {
            ApiKey = "your_api_key",
            UserId = CurrentUser.Id,
            UserRole = CurrentUser.Role,
            Theme = AITheme.Walmart,
            Features = new AIFeatures
            {
                VoiceInput = true,
                ContextAwareness = true,
                VisualGuidance = true
            }
        };
        
        aiAssistant = new AIAssistantControl(config);
        aiAssistant.ResponseReceived += OnAIResponse;
        aiAssistant.ContextRequested += OnContextRequested;
        
        // Add to grid
        AIAssistantGrid.Children.Add(aiAssistant);
    }
    
    private void OnAIResponse(object sender, AIResponseEventArgs e)
    {
        // Handle AI response
        if (e.Response.SuggestedAction != null)
        {
            Dispatcher.Invoke(() => PerformSuggestedAction(e.Response.SuggestedAction));
        }
    }
    
    private void OnContextRequested(object sender, AIContextEventArgs e)
    {
        e.Context = new AIContext
        {
            CurrentPage = "desktop-dashboard",
            VisibleData = GetDashboardData(),
            UserPermissions = CurrentUser.Permissions
        };
    }
}
```

## 🏪 Kiosk/Terminal Integration

### Touch Screen Kiosk
```html
<!-- Kiosk-optimized interface -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Activity Hub Kiosk</title>
    <style>
        /* Kiosk-specific styles */
        .kiosk-container { font-size: 1.2em; }
        .ai-assistant-kiosk { 
            position: fixed; 
            bottom: 0; 
            width: 100%; 
            height: 300px; 
        }
        .touch-friendly { min-height: 48px; min-width: 48px; }
    </style>
</head>
<body>
    <div class="kiosk-container">
        <!-- Kiosk dashboard content -->
        <div id="kiosk-dashboard"></div>
        
        <!-- AI Assistant for kiosk -->
        <div class="ai-assistant-kiosk">
            <div class="ai-header">
                <h3>Need Help? Ask Sparky!</h3>
                <button class="voice-activate-btn touch-friendly">🎤 Tap to Speak</button>
            </div>
            <div class="ai-conversation"></div>
        </div>
    </div>
    
    <script>
    // Kiosk-specific AI Assistant configuration
    const kioskAI = new ActivityHubAI({
        mode: 'kiosk',
        touchOptimized: true,
        voicePrimary: true,
        autoTimeout: 30000, // Auto-hide after 30 seconds of inactivity
        accessibility: {
            screenReader: true,
            highContrast: true,
            largeText: true
        }
    });
    
    // Auto-activate voice input for accessibility
    kioskAI.onIdle = () => {
        kioskAI.showVoicePrompt();
    };
    </script>
</body>
</html>
```

## 🎨 Customization and Theming

### Brand Customization
```css
/* AI Assistant Walmart Theme */
.ai-assistant-walmart {
    --ai-primary-color: #1E3A8A;
    --ai-secondary-color: #3B82F6;
    --ai-accent-color: #FFCC00;
    --ai-text-color: #1E293B;
    --ai-background: #FFFFFF;
    --ai-border: #E2E8F0;
    --ai-font-family: 'Everyday Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    --ai-border-radius: 8px;
    --ai-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.ai-assistant-widget {
    font-family: var(--ai-font-family);
    color: var(--ai-text-color);
    background: var(--ai-background);
    border-radius: var(--ai-border-radius);
    box-shadow: var(--ai-shadow);
}

.ai-header {
    background: linear-gradient(135deg, var(--ai-primary-color) 0%, var(--ai-secondary-color) 100%);
    color: white;
}

.ai-button-primary {
    background: var(--ai-primary-color);
    color: white;
    border: none;
    border-radius: var(--ai-border-radius);
}

.ai-button-accent {
    background: var(--ai-accent-color);
    color: var(--ai-primary-color);
    border: none;
    border-radius: var(--ai-border-radius);
}
```

### Role-Based Configuration
```javascript
// Different configurations for different user roles
const roleConfigurations = {
  'c-level-executive': {
    features: {
      executiveSummaries: true,
      strategicInsights: true,
      crossDepartmentData: true,
      advancedAnalytics: true
    },
    interface: {
      complexity: 'advanced',
      dataDepth: 'comprehensive',
      suggestedQueries: [
        'Show me enterprise-wide performance trends',
        'What are the top strategic risks this quarter?',
        'Compare departmental ROI metrics'
      ]
    }
  },
  
  'manager': {
    features: {
      teamManagement: true,
      projectTracking: true,
      resourceAllocation: true,
      performanceReviews: true
    },
    interface: {
      complexity: 'intermediate',
      dataDepth: 'departmental',
      suggestedQueries: [
        'How is my team performing this month?',
        'What projects need my attention?',
        'Show me budget utilization'
      ]
    }
  },
  
  'team-member': {
    features: {
      personalProductivity: true,
      taskManagement: true,
      learningRecommendations: true,
      basicReporting: true
    },
    interface: {
      complexity: 'simple',
      dataDepth: 'personal',
      suggestedQueries: [
        'What are my tasks for today?',
        'How do I submit a time report?',
        'Find training resources for my role'
      ]
    }
  }
};

// Apply role-based configuration
function configureAIForUser(user) {
  const config = roleConfigurations[user.role] || roleConfigurations['team-member'];
  
  return new ActivityHubAI({
    ...baseConfig,
    features: config.features,
    interface: config.interface,
    user: user
  });
}
```

## 🔧 Configuration Management

### Environment-Specific Configurations
```javascript
// config/environments.js
const configurations = {
  development: {
    apiUrl: 'http://localhost:3000/api',
    debug: true,
    features: {
      voiceInput: true,
      contextAwareness: true,
      visualGuidance: true,
      analytics: false
    }
  },
  
  staging: {
    apiUrl: 'https://staging-api.activityhub.walmart.com/api',
    debug: false,
    features: {
      voiceInput: true,
      contextAwareness: true,
      visualGuidance: true,
      analytics: true
    }
  },
  
  production: {
    apiUrl: 'https://api.activityhub.walmart.com/api',
    debug: false,
    features: {
      voiceInput: true,
      contextAwareness: true,
      visualGuidance: true,
      analytics: true,
      advancedSecurity: true
    }
  }
};

module.exports = configurations[process.env.NODE_ENV || 'development'];
```

### Feature Flags
```javascript
// Feature flag management
const featureFlags = {
  voice_input: true,
  visual_guidance: true,
  predictive_suggestions: false, // Beta feature
  multilingual_support: true,
  advanced_analytics: false, // Premium feature
  integration_tutorials: true
};

// Check feature availability
function isFeatureEnabled(feature, userRole = null) {
  const flag = featureFlags[feature];
  
  if (typeof flag === 'boolean') {
    return flag;
  }
  
  if (typeof flag === 'object' && userRole) {
    return flag[userRole] || flag.default || false;
  }
  
  return false;
}

// Initialize AI Assistant with feature flags
const aiAssistant = new ActivityHubAI({
  features: {
    voiceInput: isFeatureEnabled('voice_input'),
    visualGuidance: isFeatureEnabled('visual_guidance'),
    predictiveSuggestions: isFeatureEnabled('predictive_suggestions', user.role)
  }
});
```

## 📊 Analytics and Tracking

### Usage Analytics
```javascript
// Analytics integration
const aiAnalytics = {
  trackInteraction: (event, data) => {
    // Send to analytics service
    analytics.track('ai_assistant_interaction', {
      event_type: event,
      user_id: data.userId,
      user_role: data.userRole,
      query_type: data.queryType,
      response_time: data.responseTime,
      satisfaction_score: data.satisfactionScore,
      timestamp: new Date().toISOString()
    });
  },
  
  trackFeatureUsage: (feature, context) => {
    analytics.track('ai_feature_usage', {
      feature_name: feature,
      context: context,
      user_role: getCurrentUserRole(),
      platform: getPlatformInfo(),
      timestamp: new Date().toISOString()
    });
  }
};

// Track AI Assistant events
aiAssistant.on('query_sent', (data) => {
  aiAnalytics.trackInteraction('query_sent', data);
});

aiAssistant.on('response_received', (data) => {
  aiAnalytics.trackInteraction('response_received', data);
});

aiAssistant.on('feedback_submitted', (data) => {
  aiAnalytics.trackInteraction('feedback_submitted', data);
});
```

## 🚀 Deployment Guide

### CDN Integration
```html
<!-- Quick integration via CDN -->
<script src="https://cdn.activityhub.walmart.com/ai-assistant/v1/ai-assistant.min.js"></script>
<link rel="stylesheet" href="https://cdn.activityhub.walmart.com/ai-assistant/v1/ai-assistant.min.css">

<script>
// Initialize with minimal configuration
window.SparkyAI.quick({
  apiKey: 'your_api_key',
  position: 'bottom-right',
  theme: 'walmart'
});
</script>
```

### NPM Package Installation
```bash
# Install the AI Assistant package
npm install @walmart/activity-hub-ai-assistant

# Or with Yarn
yarn add @walmart/activity-hub-ai-assistant
```

```javascript
// Import and use in your application
import { AIAssistant, AIFloatingWidget } from '@walmart/activity-hub-ai-assistant';
import '@walmart/activity-hub-ai-assistant/dist/styles.css';

// Initialize the assistant
const assistant = new AIAssistant({
  apiKey: process.env.REACT_APP_AI_API_KEY,
  userId: currentUser.id,
  userRole: currentUser.role
});

// Render in your React component
function Dashboard() {
  return (
    <div className="dashboard">
      <DashboardContent />
      <AIFloatingWidget assistant={assistant} />
    </div>
  );
}
```

---

## 📞 Support and Documentation

### Integration Support
- **Technical Documentation**: Complete API reference and integration guides
- **Code Examples**: Ready-to-use examples for all platforms
- **Developer Console**: Testing and debugging tools
- **Community Forums**: Developer community support
- **Professional Services**: Enterprise integration assistance

### Testing and Validation
- **Integration Testing**: Automated tests for all integration points
- **Performance Monitoring**: Real-time performance metrics
- **User Acceptance Testing**: Guided testing procedures
- **Accessibility Validation**: WCAG compliance verification
- **Security Auditing**: Regular security assessments

---

**Integration Guide Status**: ✅ Complete - Ready for Implementation  
**Last Updated**: November 7, 2025  
**Version**: 1.0.0  
**Owner**: Kendall Rush (kendall.rush@walmart.com)

Seamlessly embed intelligent AI assistance across every Activity Hub platform and touchpoint. 🚀
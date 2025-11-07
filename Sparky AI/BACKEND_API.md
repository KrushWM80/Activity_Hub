# AI Assistant Backend API - Technical Implementation

## 🏗️ Architecture Overview

The AI Assistant backend provides a robust, scalable API that powers intelligent, context-aware assistance throughout the Activity Hub. Built with microservices architecture, it seamlessly integrates with Sparky's AI capabilities and enterprise systems.

## 🔧 Technology Stack

### Core Services
- **Node.js + Express**: Primary API server with TypeScript
- **Python + FastAPI**: AI/ML processing service
- **Redis**: Session management and caching
- **PostgreSQL**: Conversation history and analytics
- **Elasticsearch**: Full-text search and indexing
- **RabbitMQ**: Asynchronous task processing

### AI/ML Integration
- **Sparky API**: Walmart's primary AI service
- **OpenAI GPT**: Backup NLP processing
- **Hugging Face Transformers**: Local model deployment
- **NLTK/spaCy**: Text processing and analysis
- **TensorFlow**: Custom model inference

### Infrastructure
- **Docker**: Containerized deployment
- **Kubernetes**: Orchestration and scaling
- **AWS/Azure**: Cloud infrastructure
- **API Gateway**: Request routing and security
- **Load Balancer**: High availability and performance

## 📡 API Endpoints

### Core Assistant API

#### **POST /api/v1/assistant/query**
Process user queries with context awareness
```javascript
// Request
{
  "query": "Why is Warehouse Automation delayed?",
  "context": {
    "page": "/dashboard/operations",
    "user_id": "kendall.rush@walmart.com",
    "user_role": "operations_manager",
    "visible_data": {
      "projects": [
        {
          "name": "Warehouse Automation",
          "status": "delayed",
          "completion": 45,
          "due_date": "2025-12-01"
        }
      ]
    },
    "session_id": "sess_abc123",
    "timestamp": "2025-11-07T14:30:00Z"
  }
}

// Response
{
  "response": {
    "text": "Based on the project data visible on your dashboard...",
    "type": "contextual_analysis",
    "confidence": 0.95,
    "sources": [
      {
        "type": "dashboard_data",
        "reference": "operations_dashboard.projects.warehouse_automation"
      }
    ]
  },
  "suggestions": [
    "Show detailed project timeline",
    "Find similar delayed projects",
    "Get vendor contact information"
  ],
  "actions": [
    {
      "type": "highlight_element",
      "target": "#warehouse-automation-row"
    }
  ],
  "metadata": {
    "processing_time_ms": 340,
    "ai_model": "sparky-enterprise-v2",
    "session_id": "sess_abc123"
  }
}
```

#### **GET /api/v1/assistant/context**
Retrieve current user context and page information
```javascript
// Response
{
  "context": {
    "user": {
      "id": "kendall.rush@walmart.com",
      "role": "operations_manager",
      "department": "Operations",
      "permissions": ["view_operations_data", "manage_team_projects"]
    },
    "page": {
      "url": "/dashboard/operations",
      "title": "Operations Dashboard",
      "elements": [
        {
          "id": "metrics-grid",
          "type": "metrics_display",
          "data_source": "operations_kpis"
        }
      ]
    },
    "data": {
      "visible_projects": 23,
      "accessible_systems": ["sap", "workday", "wms"],
      "recent_activity": [
        {
          "action": "viewed_project",
          "target": "warehouse_automation",
          "timestamp": "2025-11-07T14:25:00Z"
        }
      ]
    }
  }
}
```

#### **POST /api/v1/assistant/feedback**
Submit user feedback for response improvement
```javascript
// Request
{
  "query_id": "q_abc123",
  "feedback": {
    "helpful": true,
    "accuracy": 5,
    "completeness": 4,
    "comments": "Perfect explanation of the delay causes"
  }
}

// Response
{
  "success": true,
  "message": "Feedback recorded successfully"
}
```

### Search and Data API

#### **POST /api/v1/search/unified**
Search across all connected systems and data sources
```javascript
// Request
{
  "query": "supply chain optimization project budget",
  "scope": {
    "systems": ["activity_hub", "sap", "sharepoint"],
    "data_types": ["projects", "documents", "reports"],
    "user_permissions": ["operations_data", "financial_summary"]
  },
  "filters": {
    "date_range": {
      "start": "2025-01-01",
      "end": "2025-12-31"
    },
    "departments": ["Operations", "Finance"]
  }
}

// Response
{
  "results": [
    {
      "id": "proj_supply_chain_opt",
      "title": "Supply Chain Optimization Project",
      "type": "project",
      "source": "activity_hub",
      "relevance_score": 0.95,
      "summary": "Major initiative to optimize supply chain processes...",
      "data": {
        "budget": 850000,
        "status": "at_risk",
        "completion": 62
      },
      "access_url": "/projects/supply-chain-optimization"
    }
  ],
  "metadata": {
    "total_results": 12,
    "search_time_ms": 180,
    "systems_searched": ["activity_hub", "sap", "sharepoint"]
  }
}
```

#### **GET /api/v1/data/context-aware**
Get contextually relevant data for current user and page
```javascript
// Response
{
  "contextual_data": {
    "related_projects": [
      {
        "id": "proj_warehouse_auto",
        "name": "Warehouse Automation",
        "relevance": "current_dashboard_focus",
        "key_metrics": {
          "completion": 45,
          "budget_used": 1200000,
          "team_size": 12
        }
      }
    ],
    "suggested_actions": [
      {
        "type": "schedule_meeting",
        "title": "Review Warehouse Automation Progress",
        "priority": "high"
      }
    ],
    "related_documents": [
      {
        "title": "Warehouse Automation Project Plan",
        "url": "/documents/warehouse-auto-plan.pdf",
        "last_updated": "2025-11-01"
      }
    ]
  }
}
```

### Voice and Conversation API

#### **POST /api/v1/voice/speech-to-text**
Convert voice input to text for processing
```javascript
// Request (multipart/form-data)
{
  "audio": "[audio_blob]",
  "format": "webm",
  "language": "en-US",
  "context": {
    "user_id": "kendall.rush@walmart.com",
    "session_id": "sess_abc123"
  }
}

// Response
{
  "transcript": "Why is warehouse automation delayed?",
  "confidence": 0.92,
  "language_detected": "en-US",
  "processing_time_ms": 850
}
```

#### **POST /api/v1/voice/text-to-speech**
Convert AI responses to audio for voice interaction
```javascript
// Request
{
  "text": "Based on the project data visible on your dashboard...",
  "voice": "walmart_female_professional",
  "speed": 1.0,
  "format": "mp3"
}

// Response
{
  "audio_url": "/api/v1/voice/audio/resp_abc123.mp3",
  "duration_seconds": 12.5,
  "expires_at": "2025-11-07T15:30:00Z"
}
```

## 🔍 Context Analysis Engine

### Page Context Detection
```python
class ContextAnalyzer:
    def analyze_page_context(self, url, dom_data, user_role):
        """
        Analyze current page context for AI assistance
        """
        context = {
            'page_type': self.classify_page(url),
            'visible_data': self.extract_data_elements(dom_data),
            'user_capabilities': self.get_role_capabilities(user_role),
            'suggested_queries': self.generate_suggestions(url, dom_data)
        }
        return context
    
    def extract_data_elements(self, dom_data):
        """
        Extract meaningful data from page DOM
        """
        data_elements = []
        
        # Find metrics and KPI displays
        metrics = self.find_metrics(dom_data)
        
        # Identify data tables and lists
        tables = self.find_data_tables(dom_data)
        
        # Detect charts and visualizations
        charts = self.find_visualizations(dom_data)
        
        return {
            'metrics': metrics,
            'tables': tables,
            'visualizations': charts
        }
```

### Intent Recognition
```python
class IntentClassifier:
    def classify_intent(self, query, context):
        """
        Classify user intent for appropriate response generation
        """
        intents = {
            'data_explanation': self.is_asking_about_data(query, context),
            'process_guidance': self.is_asking_for_guidance(query),
            'search_request': self.is_search_query(query),
            'action_request': self.is_action_request(query),
            'comparison_request': self.is_comparison_query(query)
        }
        
        # Return highest confidence intent
        return max(intents.items(), key=lambda x: x[1])
```

## 🔐 Security and Authentication

### API Security
```javascript
// JWT Token Validation Middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }
  
  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ error: 'Invalid token' });
    req.user = user;
    next();
  });
};

// Role-based access control
const requireRole = (allowedRoles) => {
  return (req, res, next) => {
    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
};
```

### Data Privacy
```javascript
// Data anonymization for analytics
const anonymizeUserData = (data) => {
  return {
    ...data,
    user_id: hashUserId(data.user_id),
    email: undefined,
    personal_info: undefined
  };
};

// Audit logging
const auditLog = {
  logInteraction: (userId, query, response, metadata) => {
    const logEntry = {
      timestamp: new Date().toISOString(),
      user_id_hash: hashUserId(userId),
      query_hash: hashQuery(query),
      response_type: response.type,
      confidence: response.confidence,
      processing_time: metadata.processing_time_ms
    };
    
    database.auditLogs.insert(logEntry);
  }
};
```

## 📊 Analytics and Monitoring

### Performance Metrics
```python
class AIAssistantMetrics:
    def track_query_performance(self, query_id, metrics):
        """
        Track performance metrics for AI responses
        """
        self.metrics_db.insert({
            'query_id': query_id,
            'response_time_ms': metrics['response_time'],
            'ai_confidence': metrics['confidence'],
            'user_satisfaction': metrics.get('user_rating'),
            'resolution_rate': metrics.get('resolved', False),
            'timestamp': datetime.utcnow()
        })
    
    def generate_performance_report(self, date_range):
        """
        Generate comprehensive performance analytics
        """
        return {
            'avg_response_time': self.get_avg_response_time(date_range),
            'user_satisfaction': self.get_satisfaction_score(date_range),
            'query_volume': self.get_query_volume(date_range),
            'top_queries': self.get_popular_queries(date_range),
            'resolution_rate': self.get_resolution_rate(date_range)
        }
```

### Real-time Monitoring
```javascript
// Health check endpoint
app.get('/health', (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    services: {
      database: checkDatabaseConnection(),
      ai_service: checkAIServiceConnection(),
      search_engine: checkSearchEngine(),
      cache: checkRedisConnection()
    },
    metrics: {
      avg_response_time: getAverageResponseTime(),
      active_sessions: getActiveSessionCount(),
      queries_per_minute: getQueryRate()
    }
  };
  
  const isHealthy = Object.values(health.services).every(status => status === 'healthy');
  res.status(isHealthy ? 200 : 503).json(health);
});
```

## 🚀 Deployment Configuration

### Docker Configuration
```dockerfile
# AI Assistant API Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

EXPOSE 3000

CMD ["npm", "start"]
```

### Kubernetes Deployment
```yaml
# ai-assistant-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-assistant-api
  namespace: activity-hub
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-assistant-api
  template:
    metadata:
      labels:
        app: ai-assistant-api
    spec:
      containers:
      - name: ai-assistant
        image: walmart/ai-assistant-api:latest
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ai-assistant-secrets
              key: database-url
        - name: SPARKY_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-assistant-secrets
              key: sparky-api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: ai-assistant-service
  namespace: activity-hub
spec:
  selector:
    app: ai-assistant-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: ClusterIP
```

## 🔄 Integration Examples

### Frontend Integration
```javascript
// AI Assistant SDK for frontend integration
class ActivityHubAI {
  constructor(config) {
    this.apiUrl = config.apiUrl;
    this.authToken = config.authToken;
    this.sessionId = this.generateSessionId();
  }
  
  async askQuestion(query) {
    const context = await this.getPageContext();
    
    const response = await fetch(`${this.apiUrl}/api/v1/assistant/query`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.authToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query,
        context,
        session_id: this.sessionId
      })
    });
    
    return response.json();
  }
  
  async getPageContext() {
    return {
      page: window.location.pathname,
      visible_data: this.extractVisibleData(),
      user_role: this.getUserRole(),
      timestamp: new Date().toISOString()
    };
  }
}
```

### Enterprise System Integration
```python
# SAP integration for project data
class SAPIntegration:
    def __init__(self, config):
        self.sap_client = SAPClient(config)
    
    def get_project_details(self, project_id, user_permissions):
        """
        Fetch project details from SAP with permission filtering
        """
        if not self.check_user_permissions(user_permissions, 'project_data'):
            return None
            
        project_data = self.sap_client.query_project(project_id)
        
        # Filter sensitive data based on user role
        return self.filter_by_permissions(project_data, user_permissions)
    
    def search_projects(self, query, filters, user_permissions):
        """
        Search projects across SAP with contextual relevance
        """
        sap_results = self.sap_client.search(query, filters)
        
        # Enhance with contextual relevance scoring
        for result in sap_results:
            result['relevance_score'] = self.calculate_relevance(
                result, query, user_permissions
            )
        
        return sorted(sap_results, key=lambda x: x['relevance_score'], reverse=True)
```

---

## 📞 Development and Support

### Getting Started
```bash
# Clone the repository
git clone https://github.com/walmart/activity-hub-ai-assistant.git

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env

# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

### Environment Variables
```bash
# Required environment variables
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_assistant
REDIS_URL=redis://localhost:6379
SPARKY_API_KEY=your_sparky_api_key
JWT_SECRET=your_jwt_secret
ELASTICSEARCH_URL=http://localhost:9200

# Optional configuration
LOG_LEVEL=info
RATE_LIMIT_MAX=100
RATE_LIMIT_WINDOW=900000
```

---

**AI Assistant Backend Status**: ✅ Implementation Ready - Production Architecture Complete  
**Last Updated**: November 7, 2025  
**Version**: 1.0.0  
**Owner**: Kendall Rush (kendall.rush@walmart.com)

Power intelligent, context-aware assistance with enterprise-grade backend infrastructure. 🚀
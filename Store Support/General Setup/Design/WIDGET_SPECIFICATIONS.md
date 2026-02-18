# Activity Hub Widget Component Specifications
## Aligned with Walmart Brand Standards

## Core Widget Components

### 1. Notifications & Alerts Widget

#### Visual Specifications
```scss
.notification-widget {
  background: var(--white);
  border-radius: 12px;
  border: 1px solid var(--gray-200);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  
  .widget-header {
    background: linear-gradient(135deg, var(--walmart-blue) 0%, var(--walmart-blue-dark) 100%);
    color: var(--white);
    padding: var(--space-4) var(--space-6);
    border-radius: 12px 12px 0 0;
    
    .header-title {
      font-family: var(--font-primary);
      font-size: var(--text-lg);
      font-weight: var(--font-semibold);
      margin: 0;
    }
    
    .notification-count {
      background: var(--walmart-yellow);
      color: var(--gray-900);
      border-radius: 20px;
      padding: var(--space-1) var(--space-3);
      font-size: var(--text-xs);
      font-weight: var(--font-bold);
    }
  }
  
  .notification-list {
    max-height: 300px;
    overflow-y: auto;
    
    .notification-item {
      padding: var(--space-4) var(--space-6);
      border-bottom: 1px solid var(--gray-100);
      transition: background-color var(--duration-normal) var(--ease-in-out);
      
      &:hover {
        background-color: var(--gray-50);
      }
      
      &.priority-high {
        border-left: 4px solid var(--error);
        background-color: var(--error-background);
      }
      
      &.priority-medium {
        border-left: 4px solid var(--warning);
      }
      
      &.priority-low {
        border-left: 4px solid var(--info);
      }
      
      .notification-icon {
        width: 20px;
        height: 20px;
        margin-right: var(--space-3);
        color: var(--walmart-blue);
      }
      
      .notification-content {
        .notification-title {
          font-weight: var(--font-medium);
          color: var(--gray-900);
          margin-bottom: var(--space-1);
        }
        
        .notification-message {
          font-size: var(--text-sm);
          color: var(--gray-600);
          line-height: 1.4;
        }
        
        .notification-time {
          font-size: var(--text-xs);
          color: var(--gray-500);
          margin-top: var(--space-2);
        }
      }
    }
  }
}
```

### 2. My Tasks Widget

#### Visual Specifications
```scss
.tasks-widget {
  background: var(--white);
  border-radius: 12px;
  border: 1px solid var(--gray-200);
  
  .widget-header {
    background: var(--gray-50);
    padding: var(--space-4) var(--space-6);
    border-bottom: 1px solid var(--gray-200);
    border-radius: 12px 12px 0 0;
    
    .header-controls {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .add-task-btn {
        background: var(--walmart-blue);
        color: var(--white);
        border: none;
        border-radius: 6px;
        padding: var(--space-2) var(--space-4);
        font-size: var(--text-sm);
        font-weight: var(--font-medium);
        cursor: pointer;
        
        &:hover {
          background: var(--walmart-blue-dark);
        }
      }
    }
  }
  
  .task-list {
    padding: var(--space-4) var(--space-6);
    
    .task-item {
      display: flex;
      align-items: flex-start;
      padding: var(--space-3) 0;
      border-bottom: 1px solid var(--gray-100);
      
      &:last-child {
        border-bottom: none;
      }
      
      .task-checkbox {
        margin-right: var(--space-3);
        margin-top: var(--space-1);
        
        input[type="checkbox"] {
          width: 18px;
          height: 18px;
          accent-color: var(--walmart-blue);
        }
      }
      
      .task-content {
        flex: 1;
        
        .task-title {
          font-weight: var(--font-medium);
          color: var(--gray-900);
          margin-bottom: var(--space-1);
          
          &.completed {
            text-decoration: line-through;
            color: var(--gray-500);
          }
        }
        
        .task-meta {
          display: flex;
          align-items: center;
          gap: var(--space-4);
          font-size: var(--text-xs);
          color: var(--gray-600);
          
          .due-date {
            &.overdue {
              color: var(--error);
              font-weight: var(--font-medium);
            }
            
            &.due-soon {
              color: var(--warning);
              font-weight: var(--font-medium);
            }
          }
          
          .priority-badge {
            padding: var(--space-1) var(--space-2);
            border-radius: 4px;
            font-weight: var(--font-medium);
            text-transform: uppercase;
            
            &.high {
              background: var(--error-background);
              color: var(--error);
            }
            
            &.medium {
              background: var(--warning-background);
              color: var(--warning);
            }
            
            &.low {
              background: var(--info-background);
              color: var(--info);
            }
          }
        }
      }
    }
  }
}
```

### 3. Project Status Dashboard Widget

#### Visual Specifications
```scss
.project-dashboard-widget {
  background: var(--white);
  border-radius: 12px;
  border: 1px solid var(--gray-200);
  
  .widget-header {
    background: linear-gradient(135deg, var(--walmart-navy) 0%, var(--walmart-blue) 100%);
    color: var(--white);
    padding: var(--space-6);
    border-radius: 12px 12px 0 0;
    
    .project-title {
      font-size: var(--text-2xl);
      font-weight: var(--font-bold);
      margin-bottom: var(--space-2);
    }
    
    .project-meta {
      display: flex;
      gap: var(--space-6);
      font-size: var(--text-sm);
      opacity: 0.9;
    }
  }
  
  .project-metrics {
    padding: var(--space-6);
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--space-4);
    
    .metric-card {
      text-align: center;
      padding: var(--space-4);
      border-radius: 8px;
      background: var(--gray-50);
      
      .metric-value {
        font-size: var(--text-3xl);
        font-weight: var(--font-bold);
        color: var(--walmart-blue);
        margin-bottom: var(--space-1);
      }
      
      .metric-label {
        font-size: var(--text-sm);
        color: var(--gray-600);
        text-transform: uppercase;
        letter-spacing: 0.05em;
      }
      
      .metric-trend {
        margin-top: var(--space-2);
        font-size: var(--text-xs);
        
        &.positive {
          color: var(--success);
        }
        
        &.negative {
          color: var(--error);
        }
      }
    }
  }
  
  .progress-section {
    padding: 0 var(--space-6) var(--space-6);
    
    .progress-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: var(--space-4);
      
      .progress-title {
        font-weight: var(--font-semibold);
        color: var(--gray-900);
      }
      
      .progress-percentage {
        font-size: var(--text-lg);
        font-weight: var(--font-bold);
        color: var(--walmart-blue);
      }
    }
    
    .progress-bar {
      width: 100%;
      height: 8px;
      background: var(--gray-200);
      border-radius: 4px;
      overflow: hidden;
      
      .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--walmart-blue) 0%, var(--walmart-blue-light) 100%);
        border-radius: 4px;
        transition: width var(--duration-slow) var(--ease-out);
      }
    }
  }
  
  .health-indicators {
    padding: 0 var(--space-6) var(--space-6);
    display: flex;
    gap: var(--space-4);
    
    .health-indicator {
      flex: 1;
      padding: var(--space-3);
      border-radius: 6px;
      text-align: center;
      font-size: var(--text-sm);
      font-weight: var(--font-medium);
      
      &.healthy {
        background: var(--success-background);
        color: var(--success);
      }
      
      &.at-risk {
        background: var(--warning-background);
        color: var(--warning);
      }
      
      &.critical {
        background: var(--error-background);
        color: var(--error);
      }
    }
  }
}
```

### 4. Next Steps & Action Items Widget

#### Visual Specifications
```scss
.next-steps-widget {
  background: var(--white);
  border-radius: 12px;
  border: 1px solid var(--gray-200);
  
  .widget-header {
    background: linear-gradient(135deg, var(--walmart-yellow) 0%, var(--walmart-yellow-dark) 100%);
    color: var(--gray-900);
    padding: var(--space-4) var(--space-6);
    border-radius: 12px 12px 0 0;
    
    .header-title {
      font-weight: var(--font-bold);
      display: flex;
      align-items: center;
      gap: var(--space-2);
      
      .ai-badge {
        background: var(--white);
        color: var(--walmart-yellow-dark);
        padding: var(--space-1) var(--space-2);
        border-radius: 4px;
        font-size: var(--text-xs);
        font-weight: var(--font-bold);
        text-transform: uppercase;
      }
    }
  }
  
  .action-items {
    padding: var(--space-6);
    
    .action-item {
      display: flex;
      align-items: flex-start;
      padding: var(--space-4);
      margin-bottom: var(--space-3);
      border-radius: 8px;
      border-left: 4px solid var(--walmart-blue);
      background: var(--gray-50);
      transition: all var(--duration-normal) var(--ease-in-out);
      
      &:hover {
        background: var(--white);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      }
      
      &.urgent {
        border-left-color: var(--error);
        background: var(--error-background);
      }
      
      &.important {
        border-left-color: var(--warning);
        background: var(--warning-background);
      }
      
      .action-icon {
        width: 24px;
        height: 24px;
        margin-right: var(--space-3);
        color: var(--walmart-blue);
        flex-shrink: 0;
      }
      
      .action-content {
        flex: 1;
        
        .action-title {
          font-weight: var(--font-medium);
          color: var(--gray-900);
          margin-bottom: var(--space-1);
        }
        
        .action-description {
          font-size: var(--text-sm);
          color: var(--gray-600);
          line-height: 1.4;
          margin-bottom: var(--space-2);
        }
        
        .action-meta {
          display: flex;
          align-items: center;
          gap: var(--space-3);
          font-size: var(--text-xs);
          color: var(--gray-500);
          
          .estimated-time {
            background: var(--walmart-blue);
            color: var(--white);
            padding: var(--space-1) var(--space-2);
            border-radius: 4px;
            font-weight: var(--font-medium);
          }
        }
      }
    }
  }
}
```

## Widget Customization System

### Theme Variations
```scss
// Executive Theme - Darker, more professional
.theme-executive {
  .widget-header {
    background: linear-gradient(135deg, var(--gray-900) 0%, var(--gray-800) 100%);
  }
  
  .metric-value {
    color: var(--gray-900);
  }
}

// Team Member Theme - Brighter, more energetic
.theme-team {
  .widget-header {
    background: linear-gradient(135deg, var(--walmart-teal) 0%, var(--walmart-blue) 100%);
  }
}

// Project Manager Theme - Balanced and functional
.theme-project-manager {
  .widget-header {
    background: linear-gradient(135deg, var(--walmart-green) 0%, var(--walmart-teal) 100%);
  }
}
```

### Size Variations
```scss
// Small Widget (3x2)
.widget-small {
  .widget-header {
    padding: var(--space-3) var(--space-4);
    
    .header-title {
      font-size: var(--text-base);
    }
  }
  
  .widget-content {
    padding: var(--space-4);
    font-size: var(--text-sm);
  }
}

// Medium Widget (4x3)
.widget-medium {
  .widget-header {
    padding: var(--space-4) var(--space-5);
  }
  
  .widget-content {
    padding: var(--space-5);
  }
}

// Large Widget (6x4)
.widget-large {
  .widget-header {
    padding: var(--space-6);
  }
  
  .widget-content {
    padding: var(--space-6);
  }
}
```

## Interactive States

### Drag and Drop States
```scss
.widget-dragging {
  opacity: 0.7;
  transform: rotate(3deg);
  z-index: 1000;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.widget-drop-zone {
  border: 2px dashed var(--walmart-blue);
  background: rgba(0, 113, 206, 0.05);
  border-radius: 12px;
}

.widget-placeholder {
  border: 2px dashed var(--gray-300);
  background: var(--gray-50);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gray-500);
  font-weight: var(--font-medium);
}
```

### Loading States
```scss
.widget-loading {
  .widget-content {
    position: relative;
    overflow: hidden;
    
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.6),
        transparent
      );
      animation: shimmer 1.5s infinite;
    }
  }
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}
```

## Responsive Adaptations

### Mobile Optimizations
```scss
@media (max-width: 767px) {
  .widget-card {
    border-radius: 8px;
    margin-bottom: var(--space-4);
    
    .widget-header {
      padding: var(--space-4);
      border-radius: 8px 8px 0 0;
      
      .header-title {
        font-size: var(--text-lg);
      }
    }
    
    .widget-content {
      padding: var(--space-4);
    }
    
    // Stack metrics vertically on mobile
    .project-metrics {
      grid-template-columns: 1fr;
      gap: var(--space-3);
    }
    
    // Simplify action items on mobile
    .action-item {
      padding: var(--space-3);
      
      .action-icon {
        display: none;
      }
    }
  }
}
```

## Accessibility Enhancements

### Focus Management
```scss
.widget-card:focus-within {
  outline: 2px solid var(--walmart-blue);
  outline-offset: 2px;
}

.keyboard-user .widget-card:focus {
  box-shadow: 0 0 0 3px rgba(0, 113, 206, 0.3);
}

// High contrast mode support
@media (prefers-contrast: high) {
  .widget-card {
    border: 2px solid var(--gray-900);
  }
  
  .notification-item.priority-high {
    border-left-width: 6px;
  }
  
  .progress-bar {
    border: 1px solid var(--gray-900);
  }
}

// Reduced motion support
@media (prefers-reduced-motion: reduce) {
  .widget-card,
  .action-item,
  .task-item {
    transition: none;
  }
  
  .shimmer-animation {
    animation: none;
  }
}
```

---

**Next Steps:**
1. Extract exact brand colors from the Walmart PPT template
2. Confirm font specifications and licensing
3. Create React/Vue component implementations
4. Build interactive prototypes for user testing
5. Develop theme switching functionality
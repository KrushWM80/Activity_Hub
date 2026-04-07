# Multi-Select Dropdown Filter Pattern

**Created:** April 7, 2026
**Origin:** TDA Insights Dashboard (`Store Support/Projects/TDA Insights/dashboard.html`)
**Purpose:** Reusable pattern for adding multi-select dropdown filters to any dashboard

---

## Overview

Custom multi-select dropdown built with pure HTML/CSS/JS (no libraries). Features:
- Checkbox list with "All" toggle
- Smart button label ("All Selected", "3 of 5 selected", etc.)
- Optional type-to-search for long lists
- Event delegation (survives DOM rebuilds after data refresh)
- Click-outside-to-close behavior

---

## 1. HTML Structure

Each dropdown follows this naming convention — `{name}-dropdown`, `{name}-dropdown-btn`, `{name}-dropdown-panel`:

```html
<div class="filters-section">
    <div class="filters-header">Filter by</div>
    <div class="filters-grid">

        <!-- Repeat this block per filter -->
        <div class="filter-group">
            <label class="filter-label">Phase</label>
            <div class="dropdown-multi" id="phase-dropdown">
                <button type="button" class="dropdown-multi-btn" id="phase-dropdown-btn">All Selected</button>
                <div class="dropdown-multi-panel" id="phase-dropdown-panel">
                    <!-- Populated dynamically by JS -->
                </div>
            </div>
        </div>

        <!-- Example: second filter -->
        <div class="filter-group">
            <label class="filter-label">Status</label>
            <div class="dropdown-multi" id="status-dropdown">
                <button type="button" class="dropdown-multi-btn" id="status-dropdown-btn">All Selected</button>
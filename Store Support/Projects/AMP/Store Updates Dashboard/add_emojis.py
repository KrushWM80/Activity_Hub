# -*- coding: utf-8 -*-
# Add proper UTF-8 emojis back to the dashboard

with open('amp_analysis_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add emojis back where appropriate
replacements = [
    # Header section
    ('Send Feedback\n </button>', '💬 Send Feedback\n </button>'),
    ('ADMIN MODE', '👤 ADMIN MODE'),
    ('<h3>Filters</h3>', '<h3>📋 Filters</h3>'),
    ('<strong>Pre-Filter Configuration:</strong>', '<strong>⚙️ Pre-Filter Configuration:</strong>'),
    ('These pre-filters apply globally.', '⚠️ These pre-filters apply globally.'),
    # Feedback form
    ('<h2>Send Feedback</h2>', '<h2>💬 Send Feedback</h2>'),
    ('<label>Filters & Search</label>', '<label>🔍 Filters & Search</label>'),
    ('<label>Other</label>', '<label>💡 Other</label>'),
    ('>Next </', '>Next → </'),
    ('< Back</', '← Back</'),
    ('Submit Feedback </', 'Submit Feedback ✓ </'),
    # Console logs
    ("console.log('Exporting", "console.log('🔥 Exporting"),
    ("console.log('Clearing filters", "console.log('🔄 Clearing filters"),
    # Other
    ('Your Comments & Suggestions', '📝 Your Comments & Suggestions'),
    ("title.textContent = 'X Stores Incomplete'", "title.textContent = '❌ Stores Incomplete'"),
    ("console.error('X Feedback error:", "console.error('❌ Feedback error:"),
    ('>...</', '>⏳</'),
]

for old, new in replacements:
    content = content.replace(old, new)

# Save with UTF-8 BOM for Windows compatibility
with open('amp_analysis_dashboard.html', 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("Added proper UTF-8 emojis")

#!/usr/bin/env node
/**
 * Fix corrupted emoji characters in the dashboard HTML file
 * Replace broken UTF-8 sequences with HTML numeric entities
 */

const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'business-overview-dashboard.html');

console.log(`Reading ${filePath}...`);

// Read the file
let content = fs.readFileSync(filePath, 'utf8');

const originalSize = content.length;
console.log(`Original file size: ${originalSize} bytes`);

// Define the replacements
const replacements = {
  'ðŸ"‹': '&#x1F4CB;',  // Clipboard emoji (broken) -> HTML entity
  'ðŸ"ˆ': '&#x1F4C8;',  // Chart up emoji (broken) -> HTML entity
  'ðŸ"Š': '&#x1F4CA;',  // Bar chart emoji (broken) -> HTML entity
  'ðŸª': '&#x1F4CA;',   // Planet/Pie emoji (broken) -> HTML entity (using bar chart)
  'â–¼': '&#x25BC;',    // Down arrow (broken) -> HTML entity
};

// Apply replacements
for (const [broken, fixed] of Object.entries(replacements)) {
  const count = (content.match(new RegExp(broken, 'g')) || []).length;
  if (count > 0) {
    console.log(`✓ Found ${count} occurrences of broken pattern - replacing with HTML entity`);
    content = content.split(broken).join(fixed);
  }
}

const newSize = content.length;
console.log(`New file size: ${newSize} bytes (changed by ${newSize - originalSize} bytes)`);

// Write back
fs.writeFileSync(filePath, content, 'utf8');

console.log('✅ Fixed emoji characters successfully!');
console.log('The dashboard now uses HTML numeric entities for all icons.');

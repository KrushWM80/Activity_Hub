const fs = require('fs');

const filePath = './business-overview-dashboard.html';
let content = fs.readFileSync(filePath, 'utf-8');

console.log('Original size:', content.length, 'bytes');

// These are the exact Unicode sequences found in the file
// Each represents a broken emoji
const fixes = [
  {
    // U+00F0 U+0178 U+201C U+2039  (ð Ÿ " ‹)
    broken: String.fromCharCode(0xF0, 0x178, 0x201C, 0x2039),
    fixed: '📋',
    name: 'Clipboard'
  },
  {
    // U+00F0 U+0178 U+201C U+2018  (ð Ÿ " ')  
    broken: String.fromCharCode(0xF0, 0x178, 0x201C, 0x2018),
    fixed: '📈',
    name: 'Chart Up'
  },
  {
    // U+00F0 U+0178 U+201C U+201A  (ð Ÿ " ‚)
    broken: String.fromCharCode(0xF0, 0x178, 0x201C, 0x201A),
    fixed: '📊',
    name: 'Bar Chart'
  },
  {
    // U+00F0 U+0178 U+00AA  (ð Ÿ ª)
    broken: String.fromCharCode(0xF0, 0x178, 0xAA),
    fixed: '🪐',
    name: 'Planet'
  },
  {
    // U+00E2 U+2013 U+00BC  (â – ¼)
    broken: String.fromCharCode(0xE2, 0x2013, 0xBC),
    fixed: '▼',
    name: 'Down Arrow'
  }
];

console.log('\nReplacing broken patterns:\n');

for (const fix of fixes) {
  const regex = new RegExp(fix.broken, 'g');
  const matches = content.match(regex);
  const count = matches ? matches.length : 0;
  
  if (count > 0) {
    console.log(`  ✓ ${count}x ${fix.name}`);
    content = content.replaceAll(fix.broken, fix.fixed);
  }
}

fs.writeFileSync(filePath, content, 'utf-8');
const newSize = fs.readFileSync(filePath, 'utf-8').length;

console.log(`\n✅ Fixed! New size: ${newSize} bytes`);
console.log(`   Changed by: ${newSize - 2621921} bytes`);

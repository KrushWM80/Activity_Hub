# Code Puppy Pages - Quick Reference

## Platform Essentials

**URL**: https://puppy.walmart.com/code-puppy-pages/
**Deployment**: Single HTML file with embedded data
**Max File Size**: 10 MB (2.7 MB tested successfully)

## File Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard Name</title>
    <style>/* All CSS here */</style>
</head>
<body>
    <!-- HTML -->
    <script>
        window.EMBEDDED_DATA = {/* Data */};
        // JavaScript
    </script>
</body>
</html>
```

## Key Patterns

### 1. Data Structure
```javascript
window.EMBEDDED_DATA = {
    summary: {
        divisionStats: [{
            divisionId: "NHM BU",
            assignedCount: 58054,
            maxPossibleCount: 137820
        }]
    },
    stores: {
        data: [/* individual records */]
    }
};
```

### 2. Filtering Pattern
```javascript
// Filter stores, then filter stats
const divisionIds = [...new Set(stores.map(s => s.divisionId))];
const totalAssigned = divisionStats
    .filter(d => divisionIds.includes(d.divisionId))
    .reduce((sum, d) => sum + d.assignedCount, 0);
```

### 3. Global Context for Percentages
```javascript
function recalculateMetrics(stores, globalMaxPossible) {
    const totalMaxPossible = globalMaxPossible || filteredMax;
    const pct = (assigned / totalMaxPossible) * 100;
}
```

## Common Bugs & Fixes

### Bug: Wrong Assigned Count
 `sum + (s.maxQuestions || 0)` - Uses max possible
 `sum + (d.assignedCount || 0)` - Uses actual assigned from divisionStats

### Bug: 100% When Filtering
 Missing globalMaxPossible parameter
 Pass global max to maintain system-wide context

### Bug: Division Cards Don''t Filter
 Using all divisionStats
 Filter divisionStats by selected divisions

### Bug: Broken Emoji
 String operations on UTF-8
 Use Python binary operations (see fix_emoji.py)

## Emoji Hex Codes

| Emoji | Hex Code |
|-------|----------|
|  | f09f938b |
|  | f09f9388 |
|  | f09f948a |
|  | e29c85 |
|  | f09f8fa2 |
|  | e296bc |

## Python Emoji Fix
```python
with open(''file.html'', ''rb'') as f:
    content = f.read()
content = content.replace(
    bytes.fromhex(''c3b0c5b8e2809cc5a1''),  # broken
    bytes.fromhex(''f09f938b'')             # fixed
)
with open(''file.html'', ''wb'') as f:
    f.write(content)
```

## Testing Checklist

- [ ] No filters  Shows all data
- [ ] Single division  Shows correct assigned count
- [ ] Multiple filters  Metrics sum correctly
- [ ] Emoji display properly in browser
- [ ] File size < 10 MB
- [ ] No console errors

## When Things Go Wrong

**Assigned count is wrong**
 Check if using maxQuestions instead of divisionStats.assignedCount

**Percentages show 100%**
 Verify globalMaxPossible parameter is passed

**Emoji garbled**
 Run fix_emoji.py with binary operations

**Division cards show all divisions**
 Filter divisionStats before rendering

**Metrics don''t match backend**
 Use pre-calculated stats, don''t recalculate from stores

## Files in This Folder

- **CODE_PUPPY_GUIDE.md** - Complete development guide
- **EMOJI_FIX_GUIDE.md** - UTF-8 troubleshooting
- **DATA_ARCHITECTURE.md** - Filtering patterns
- **fix_emoji.py** - Binary emoji fix utility
- **fix-unicode.js** - JavaScript unicode fixes

**Last Updated**: January 13, 2026

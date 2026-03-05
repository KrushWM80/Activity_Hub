# PPT Generation Issues - Status Report

## Current Status: REGRESSION 🔴
- **Issue**: PPT files are now BLANK after latest update
- **Previous**: PPT working, 1 repair warning (acceptable)
- **Current**: PPT blank, 2+ repair warnings (broken)
- **Root Cause**: Unknown - likely XML structure or relationship mapping issue

## Symptoms
1. ✓ PPT file generates (correct file size: 4-36KB)
2. ✗ PPT opens with repair warnings (multiple)
3. ✗ PPT content is BLANK after repair
4. ✗ No slides visible after opening

## Changes Made in Latest Update
### backend_simple.py - generate_pptx_from_screenshots()
1. Added `presProps.xml` file
2. Added `viewProps.xml` file
3. Added `tableStyles.xml` file
4. Changed [Content_Types].xml to include above files
5. Updated ppt/_rels/presentation.xml.rels with:
   - rId1 → presProps.xml
   - rId2 → viewProps.xml
   - rId3 → tableStyles.xml
   - rId4+ → slide files
6. Added p:sldSz (slide size) to presentation.xml
7. Changed Walmart color to #0063B1
8. Added header bars to content slides

### dashboard.html - generatePPT()
1. Implemented `packRowsIntoPages()` for dynamic pagination
2. Changed from fixed 10 rows/page to content-aware packing
3. Added zoom=1.5 temporarily for better capture quality
4. Added `header` field to screenshot objects

## Likely Root Causes (Theories)

### Theory 1: Relationship ID Mismatch ⚠️
**Problem**: Relationship IDs in ppt/_rels/presentation.xml.rels don't match references in presentation.xml
- presProps/viewProps/tableStyles have rId1-3 but presentation.xml doesn't reference them
- Slide references use rId4+ but might be misparsed
- **Test**: Compare old working version with new version side-by-side

### Theory 2: presentation.xml Structure Issues ⚠️
**Problem**: p:sldSz or other new elements breaking parsing
- Added `<p:sldSz cx="9144000" cy="6858000"/>` without proper namespace
- Added `<p:notesSz .../>` which might conflict
- Namespace declarations might be incomplete
- **Test**: Remove these elements, test if PPT renders

### Theory 3: Missing/Incorrect XML Elements ⚠️
**Problem**: presProps/viewProps/tableStyles too minimal
- These files might need more content for PowerPoint to recognize them
- tableStyles empty might cause rendering issues
- viewProps structure might be wrong
- **Test**: Use valid presProps/viewProps from python-pptx generated file

### Theory 4: Image Encoding or Positioning 🔴
**Problem**: Header bar + image positioning in slide XML incorrect
- Header positioned at y=0 might overlap with slide background
- Image positioned at y=457200 might be off-screen
- Image dimensions (cx/cy) might be wrong
- **Test**: Remove header bar, test if image renders

## Files to Check
- [backend_simple.py](backend_simple.py) - Lines 335-550 (PPT generation)
- [dashboard.html](dashboard.html) - Lines 906-1100 (PPT capture + packing)
- test_output.pptx - Latest test file (4436 bytes)

## Validation Needed

### Test 1: Rollback to Previous Working Version
```powershell
# Revert backend_simple.py ppt function to previous version
# Re-test with old code to confirm it still works
# This establishes baseline
```

### Test 2: Use python-pptx Library Instead
```python
# Instead of raw XML, use official library:
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)
# Add slides programmatically
# Much safer than raw XML manipulation
```

### Test 3: Validate XML Structure
```powershell
# Use ZipFile to extract and inspect PPTX structure:
# - Check [Content_Types].xml validity
# - Check all .rels files
# - Check presentation.xml references are correct
# - Compare with known-good PPTX
```

### Test 4: Minimal Test Case
```python
# Build PPTX with ONLY:
# 1. Title slide (no header)
# 2. One image slide (no header, full-size image)
# 3. No presProps/viewProps/tableStyles initially
# Test if this works
```

## Next Steps for Next Session

### Priority 1: Identify Root Cause
- [ ] Extract and inspect generated PPT structure
- [ ] Compare with old working code
- [ ] Use python-pptx to validate structure
- [ ] Test minimal PPTX generation

### Priority 2: Fix or Revert
- [ ] If fix found: Apply and continue
- [ ] If not found: Revert to previous working version
- [ ] Document which changes caused regression

### Priority 3: Implement Better Solution
- [ ] Switch to python-pptx library (cleaner, safer)
- [ ] Keep dynamic row packing (works well)
- [ ] Keep header functionality (just fix rendering)
- [ ] Validate output with error handling

## Code References

**Current Working Version** (before latest update):
- Status: 1 repair warning, PPT displays correctly
- File size: Similar (3-4KB range)
- Code: Previous git state

**Current Broken Version** (after latest update):
- Status: 2+ repair warnings, blank PPT
- File size: Slightly larger (4-36KB)
- Code: Lines 335-550 in backend_simple.py

## Decision for Next Session
**Option A**: Debug XML structure (if time permits)
**Option B**: Revert to previous code + keep dynamic packing (fastest)
**Option C**: Implement python-pptx library (most robust)

**Recommendation**: Option B (revert) → then Option C (robust)
- Keep what works (basic PPT, dynamic packing)
- Add proper library-based approach
- Avoid raw XML manipulation issues

---
**Status**: BLOCKED - PPT generation broken
**Action**: Investigate before next session
**Estimated fix time**: 1-2 hours

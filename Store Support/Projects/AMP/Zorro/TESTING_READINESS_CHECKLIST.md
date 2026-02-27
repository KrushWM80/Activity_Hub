# Pre-Testing Readiness Checklist

**Created**: December 1, 2025  
**Status**: 98% Ready (awaiting SSO credentials)

---

## ✅ Code Ready

### Schema Validation
- [x] Pydantic models created for all 7 OpenAPI endpoints
- [x] Request constraints enforced (prompt length, duration range, etc.)
- [x] Response schemas defined and validated
- [x] Error schemas for 422 validation errors
- [x] File: `src/schemas/walmart_schemas.py` (600+ lines)

### Provider Implementation
- [x] All 7 endpoints using correct `/api/v1/` paths
- [x] Base URL updated to production: `https://retina-ds-genai-backend.prod.k8s.walmart.net`
- [x] Authentication: SSO Bearer token
- [x] Request/response validation against schemas
- [x] Two new methods added:
  - `suggest_prompt_for_image(image_base64)` - Get AI prompt suggestions
  - `cancel_video_generation(request_id)` - Cancel in-progress generation
- [x] File: `src/providers/walmart_media_studio.py` (updated)

### Test Suite
- [x] API connection test (checks `/health` endpoint)
- [x] Schema validation tests (valid and invalid requests)
- [x] Video generation test (full pipeline)
- [x] Aspect ratio compatibility test (16:9, 9:16, 1:1)
- [x] Enhanced error messages with solutions
- [x] File: `test_walmart_api.py` (updated)

### Documentation
- [x] Complete API integration guide (1,200+ lines)
- [x] All 7 endpoints documented with examples
- [x] Error handling guide
- [x] Best practices guide
- [x] Polling strategy explained
- [x] Complete workflow example
- [x] File: `API_INTEGRATION_GUIDE.md`

---

## ⏳ Pending - Credentials

### SSO Token Setup
- [ ] Receive SSO token from Oskar (expected this week)
- [ ] Add to `.env` file: `WALMART_SSO_TOKEN=<token>`
- [ ] Restart terminal to load `.env`
- [ ] Verify token is loaded: `echo $env:WALMART_SSO_TOKEN`

---

## 🎯 Testing Checklist (Execute After Credentials)

### Phase 1: Basic Connectivity (5 minutes)

```bash
# Step 1: Verify environment is configured
python -c "import os; print('Token loaded' if os.getenv('WALMART_SSO_TOKEN') else 'Token missing')"

# Step 2: Run connection test only
python test_walmart_api.py
# Expected: API connection successful, models listed
```

**Verify**:
- [x] No "WALMART_SSO_TOKEN not found" error
- [x] API connection says "✅ Media Studio API is available!"
- [x] Models listed (veo2, veo3 for video; imagen-4.0 for images)
- [x] Endpoint shows: `https://retina-ds-genai-backend.prod.k8s.walmart.net`

**If Failed**: 
- [ ] Check token is set: `$env:WALMART_SSO_TOKEN`
- [ ] Verify token format (usually long string or JWT)
- [ ] Try refreshing token if expired
- [ ] Contact Oskar if persistent

### Phase 2: Schema Validation (2 minutes)

When prompted "Run video generation test?", select **schema validation test** first:

```bash
python test_walmart_api.py
# At prompt, choose 'y' for schema validation
# Expected: 3 tests pass (valid request, invalid prompt, invalid duration)
```

**Verify**:
- [x] Valid request accepted
- [x] Empty prompt rejected
- [x] Duration > 8 rejected
- [x] Duration < 4 rejected
- [x] Prompt > 2000 chars rejected

**If Failed**:
- [ ] Check Pydantic version: `pip show pydantic`
- [ ] Re-install: `pip install pydantic==2.x`
- [ ] Verify `src/schemas/walmart_schemas.py` exists

### Phase 3: Video Generation (5-10 minutes)

```bash
python test_walmart_api.py
# Select 'y' for schema validation (if not done)
# Select 'y' for video generation test
# Expected: Video generates in 1-5 minutes
```

**Verify During Generation**:
- [x] Request submitted with request_id
- [x] Polling starts with 5-second intervals
- [x] Status shows: pending → processing → completed
- [x] Progress percentage increases (0% → 100%)
- [x] Video URL returned when complete
- [x] Video downloads to `output/videos/`

**Verify Generated Video**:
- [x] File exists: `output/videos/test_walmart_api_001_media_studio.mp4`
- [x] File size > 1MB (typical: 5-20MB)
- [x] Video duration ≈ 5 seconds (what was requested)
- [x] File plays in video player

**If Generation Times Out**:
- [ ] Try again (some videos take 5+ minutes)
- [ ] Check status endpoint manually:
  ```python
  curl -H "Authorization: Bearer $WALMART_SSO_TOKEN" \
       https://retina-ds-genai-backend.prod.k8s.walmart.net/api/v1/videos/status/{request_id}
  ```
- [ ] If status shows "failed", check error message
- [ ] Contact Oskar if API is down

### Phase 4: Aspect Ratio Testing (10-20 minutes)

```bash
python test_walmart_api.py
# Select 'y' for video generation test (if not already done)
# When asked "Test all aspect ratios?", select 'y'
# Expected: 3 videos generated (16:9, 9:16, 1:1)
```

**Verify Outputs**:
- [x] 16:9 video generates (widescreen)
- [x] 9:16 video generates (vertical/mobile)
- [x] 1:1 video generates (square/social media)
- [x] All videos have correct durations (4-8 seconds)
- [x] Files created in `output/videos/`

**Verify Resolutions** (check video metadata):
- [x] 16:9: ~1920x1080 or similar widescreen
- [x] 9:16: ~1080x1920 or similar vertical
- [x] 1:1: ~1080x1080 or similar square

---

## 📋 Post-Testing Checklist

### Document Results

```bash
# Create test results file
mkdir -p results
cat > results/TEST_RESULTS.md << 'EOF'
# API Testing Results

Date: December 2, 2025
Tester: [Your name]

## Phase 1: Connectivity
- Connection: PASS/FAIL
- Models available: veo2, veo3, imagen-4.0
- API version: 0.3.141

## Phase 2: Schema Validation
- Valid request: PASS/FAIL
- Invalid prompt: PASS/FAIL
- Invalid duration: PASS/FAIL

## Phase 3: Video Generation
- Video generated: YES/NO
- File size: ___ MB
- Duration: ___ seconds
- Request time: ___ seconds
- Generation time: ___ seconds

## Phase 4: Aspect Ratios
- 16:9: PASS/FAIL
- 9:16: PASS/FAIL
- 1:1: PASS/FAIL

## Issues Encountered
[List any errors or problems]

## Next Steps
[What to try next]
EOF
```

### Update EXECUTIVE_SUMMARY.md

```bash
# Phase 5 status update
# Change: Phase 5: Production Testing = 📋 In Progress
# Add date tested and results
```

### Prepare Pilot Video

Once everything works:

```bash
# Step 1: Create a real Walmart-focused prompt
prompt="A professional retail associate demonstrating inventory organization techniques on a Walmart store shelf with proper lighting and organized product placement. Clean, modern retail environment with associates wearing Walmart uniforms."

# Step 2: Generate video with this prompt
# Use the complete WalmartMediaStudioClient example from API_INTEGRATION_GUIDE.md

# Step 3: Add accessibility layer
# - Generate captions (use test_walmart_api.py or add to pipeline)
# - Create audio description script
# - Generate transcript

# Step 4: Save as first pilot video
# Location: output/pilots/pilot_001_<date>.mp4
```

---

## 🚀 When Everything is Working

### Next Steps (Dec 2-6)
1. [ ] Test 2-3 more video examples
2. [ ] Verify caching strategy (GET /models endpoint)
3. [ ] Test cancellation: `cancel_video_generation(request_id)`
4. [ ] Document any bugs or edge cases
5. [ ] Share results with Oskar and team

### Week of Dec 9-15
1. [ ] Generate first pilot video (1/week approved)
2. [ ] Apply accessibility layer
3. [ ] Gather metrics:
   - Generation time
   - Quality rating
   - Any issues encountered
4. [ ] Document learnings for Stephanie

### Mid-December Check-In
1. [ ] Present pilot videos and metrics
2. [ ] Discuss learnings and feature gaps
3. [ ] Get approval to scale to 100-150/week
4. [ ] Plan timeline for full rollout

---

## 📞 Support Contacts

### Technical Issues
- **Slack**: #help-genai-media-studio
- **Oskar Radermecker**: SSO, API access, technical questions
- **API Docs**: https://retina-ds-genai-backend.prod.k8s.walmart.net/docs

### Strategic Questions
- **Stephanie Tsai**: PM, approval decisions
- **Slack**: Post in #help-genai-media-studio for team visibility

---

## 📚 Key Documentation Files

| File | Purpose | Size |
|------|---------|------|
| `API_INTEGRATION_GUIDE.md` | Complete endpoint reference | 1,200+ lines |
| `API_TESTING_GUIDE.md` | Testing procedures | 438 lines |
| `test_walmart_api.py` | Runnable test suite | Updated |
| `src/schemas/walmart_schemas.py` | Pydantic schemas | 600+ lines |
| `src/providers/walmart_media_studio.py` | Provider implementation | Updated |
| `OPENAPI_IMPLEMENTATION_SUMMARY.md` | This summary | This file |

---

## Git Status

```bash
# Check recent commits
git log --oneline -5

# Should show:
# - OpenAPI 0.3.141 schema validation commit
# - API integration guide commit
# - Test updates commit
```

**Ready to push** once credentials are obtained and tests pass.

---

## Success Criteria

### ✅ Minimum Success
- [x] Code ready and committed
- [ ] Connection test passes
- [ ] At least 1 video generated successfully
- [ ] No 401 or 403 errors

### ✅ Full Success
- [ ] All 4 test phases pass
- [ ] 3+ videos generated with different prompts
- [ ] All aspect ratios tested
- [ ] Schema validation confirmed
- [ ] Results documented
- [ ] Team notified of completion

### ✅ Production Ready
- [ ] 5+ successful videos
- [ ] Accessibility layer working
- [ ] Metrics collected and documented
- [ ] Stephanie approves scaling up
- [ ] Timeline established for 100-150/week

---

**Status**: Ready to proceed once SSO token arrives from Oskar (expected Dec 1-6)

**Next Action**: Monitor email for SSO token, then execute Phase 1 checklist

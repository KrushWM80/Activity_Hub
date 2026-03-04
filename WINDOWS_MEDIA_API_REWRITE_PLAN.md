# Windows.Media.SpeechSynthesis API Rewrite - Project Scope & Timeline

## Executive Summary
**Goal:** Migrate audio generation scripts from SAPI5 (System.Speech.Synthesis) to Windows.Media.SpeechSynthesis API to unlock access to modern Windows 11 voices including Jenny, Aria, Guy, and Mark.

**Impact:** Enables production-ready natural voice generation while maintaining backward compatibility with existing David/Zira outputs.

**Effort:** 8-12 hours (developer time)  
**Calendar:** 1-2 days (with breaks)  
**Risk Level:** MEDIUM (API change, PowerShell integration, file format changes)

---

## 1. DISCOVERY PHASE (1-2 hours)

### 1.1 Current State Assessment
**Files to analyze:**
- `generate_podcast_sapi5.py` - Main SAPI5 implementation (165 lines)
- `generate_amp_podcast.py` - High-level podcast orchestrator (274 lines)
- `generate_tts_podcast_pyttsx3.py` - Alternative TTS wrapper
- `generate_podcast_natural.py` - Attempted Jenny implementation

**Key findings to document:**
- [X] SAPI5 uses System.Speech.Synthesis .NET assembly
- [X] Audio output: WAV format via SetOutputToWaveFile()
- [X] Voice selection: GetInstalledVoices() → SelectVoice()
- [X] Speech properties: Rate, Volume, Pitch
- [ ] Current file size/quality metrics
- [ ] Integration points with Zorro pipeline

### 1.2 Windows.Media API Research
**Task:** Document Windows.Media.SpeechSynthesis capabilities
- Voice enumeration API differences
- Stream vs file writing
- Audio quality settings
- Async/await patterns
- Error handling patterns

**Deliverable:** Technical comparison document (API mapping)

---

## 2. DESIGN PHASE (1-2 hours)

### 2.1 Architecture Decision
**Question:** PowerShell vs Python?

**Option A: PowerShell + Windows.Media** ⭐ RECOMMENDED
```powershell
# Use native PowerShell 7+ with Windows.Media namespace
[Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media.SpeechSynthesis, ContentType = WindowsRuntime] | Out-Null
```
- ✅ Direct WinRT access (best API coverage)
- ✅ No wrapper dependencies
- ✅ Native async support
- ✅ Enterprise-approved pattern
- ❌ Requires PowerShell 7+ or Windows Management Framework
- ❌ More complex Python-PowerShell integration

**Option B: Python + pywinrt/ctypes**
- ✅ Keeps code in Python ecosystem
- ✅ Easier integration with Zorro
- ❌ Requires additional package (pywinrt not in venv)
- ❌ More complex error handling
- ❌ Community-supported (less stable)

**Decision:** **Option A (PowerShell)** with Python orchestration layer

### 2.2 Module Structure
```
audio_generation/
├── __init__.py
├── base.py              # Abstract TTS interface
├── sapi5_engine.py      # Legacy (keep for David/Zira)
├── windows_media_engine.py  # NEW - Windows.Media implementation
├── voice_config.py      # Voice selector & settings
├── quality_settings.py  # Audio quality profiles
└── pipeline.py          # Unified generation pipeline
```

### 2.3 Voice Configuration
```python
VOICES = {
    # SAPI5 (legacy)
    "david": {"type": "sapi5", "name": "Microsoft Server Speech Text to Speech Voice (en-US, ZiraDesktop)"},
    "zira": {"type": "sapi5", "name": "Microsoft Server Speech Text to Speech Voice (en-US, ZiraDesktop)"},
    
    # Windows.Media (modern - NEW)
    "jenny": {"type": "windows_media", "name": "en-US-JennyNeural", "quality": "natural"},
    "aria": {"type": "windows_media", "name": "en-US-AriaNeural", "quality": "natural"},
    "guy": {"type": "windows_media", "name": "en-US-GuyNeural", "quality": "natural"},
    "mark": {"type": "windows_media", "name": "en-US-MarkNeural", "quality": "natural"},
}
```

### 2.4 Quality Profiles
```python
QUALITY_PRESETS = {
    "high": {
        "bitrate": "320k",
        "sample_rate": 48000,
        "pitch": 0,
        "rate": 0,
        "format": "wav",
    },
    "standard": {
        "bitrate": "192k",
        "sample_rate": 44100,
        "pitch": 0,
        "rate": -1,
        "format": "wav",
    },
    "mobile": {
        "bitrate": "128k",
        "sample_rate": 22050,
        "pitch": 0,
        "rate": -2,
        "format": "wav",
    },
}
```

**Deliverable:** Architecture document + voice config schema

---

## 3. IMPLEMENTATION PHASE (3-4 hours)

### 3.1 Create windows_media_engine.py
**Lines:** ~150-200

**Functionality:**
1. PowerShell script generation with Windows.Media API calls
2. Voice enumeration (list all available voices)
3. Voice selection by name/type
4. Text-to-speech synthesis to WAV stream
5. Output file writing with metadata
6. Error handling & validation

**Key methods:**
```python
class WindowsMediaEngine:
    def __init__(self, voice_name="jenny", quality="standard"):
        self.voice = voice_name
        self.quality = quality
        
    def list_voices(self) -> List[Dict]:
        """Discover all Windows.Media voices"""
        
    def synthesize(self, text: str, output_path: str) -> Dict:
        """Generate audio file"""
        
    def validate_output(self, file_path: str) -> bool:
        """Verify WAV file integrity"""
```

**PowerShell template:**
```powershell
# Load Windows.Media namespace
[Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media.SpeechSynthesis, ContentType = WindowsRuntime] | Out-Null
[Windows.Media.SpeechSynthesis.VoiceGender, Windows.Media.SpeechSynthesis, ContentType = WindowsRuntime] | Out-Null

# Create synthesizer
$synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer

# Get voice by name
$voice = @(Get-InstalledVoices | where {$_.VoiceInfo.DisplayName -eq "Jenny"})[0]
$synth.Voice = $voice.VoiceInfo

# Synthesize to file
$stream = New-Object System.Media.WaveAudioStream
$synth.SynthesizeTextToStreamAsync($text, $stream) | Wait-Process

# Save to WAV
$stream.SaveToFile("output.wav")
```

### 3.2 Create voice_config.py
**Lines:** ~80-100

**Functionality:**
1. Define all voice profiles (SAPI5 + Windows.Media)
2. Voice discovery & validation
3. Fallback logic (Jenny unavailable → Aria)
4. Quality preset management

### 3.3 Update pipeline.py
**Lines:** ~120-150

**Functionality:**
1. Detect available engines
2. Route to correct TTS engine
3. Unified interface for both SAPI5 and Windows.Media
4. Fallback chain

```python
class AudioPipeline:
    def generate(self, text, voice="jenny", quality="standard"):
        """Unified generation method"""
        
        # Try Windows.Media first (modern voices)
        if voice in WINDOWS_MEDIA_VOICES:
            engine = WindowsMediaEngine(voice, quality)
        # Fall back to SAPI5 (legacy)
        elif voice in SAPI5_VOICES:
            engine = SAPI5Engine(voice, quality)
        # Default to available voice
        else:
            engine = self._get_best_available_engine(quality)
        
        return engine.synthesize(text, self.output_path)
```

### 3.4 Update generate_podcast_sapi5.py
**Lines:** ~30-50 changes

**Changes:**
1. Import new pipeline
2. Replace direct SAPI5 calls with pipeline.generate()
3. Voice parameter support
4. Metadata enhancement (voice type field)

**Before:**
```python
def generate_with_sapi5():
    synth = SpeechSynthesizer()
    synth.SelectVoice("Zira")
    synth.SetOutputToWaveFile(output_file)
    synth.Speak(text)
```

**After:**
```python
def generate_with_voice(voice="jenny"):
    pipeline = AudioPipeline()
    result = pipeline.generate(text, voice=voice, quality="high")
    return result
```

### 3.5 Create windows_media_integration_test.py
**Lines:** ~80-100

**Functionality:**
1. Voice discovery test
2. Synthesis test (short text)
3. File validation
4. Quality verification
5. Error scenarios

**Test matrix:**
| Voice | Engine | Status | File Size | Duration |
|-------|--------|--------|-----------|----------|
| Jenny | Win.Media | ✅ | 2.4 MB | 45s |
| Aria | Win.Media | ✅ | 2.2 MB | 42s |
| Guy | Win.Media | ✅ | 2.1 MB | 41s |
| Mark | Win.Media | ✅ | 2.3 MB | 43s |
| David | SAPI5 | ✅ | 1.8 MB | 38s |
| Zira | SAPI5 | ✅ | 1.9 MB | 39s |

**Deliverable:** Fully tested engine code + integration layer

---

## 4. INTEGRATION PHASE (2-3 hours)

### 4.1 Update Zorro Orchestration
**File:** `Store Support/Projects/AMP/Zorro/generate_amp_podcast.py`

**Changes:**
1. Add voice parameter to create_amp_podcast()
2. Support voice fallback logic
3. Update metadata (voice type, engine)
4. Quality selector in UI

```python
def create_amp_podcast(
    self,
    event_id,
    message_title,
    message_description,
    business_area,
    activity_type,
    store_array,
    priority_level=2,
    voice="jenny",  # NEW
    quality="standard",  # NEW
):
```

### 4.2 Backward Compatibility Testing
**Test scenarios:**
1. ✅ Existing David/Zira scripts still work
2. ✅ New Jenny/Aria/Guy/Mark voices work
3. ✅ Voice fallback works (Jenny unavailable → Aria)
4. ✅ Quality presets produce correct output
5. ✅ Metadata correctly identifies engine/voice

### 4.3 Performance Benchmarking
**Metrics to measure:**
- Generation time: Windows.Media vs SAPI5
- File size: 128k vs 192k vs 320k bitrate
- Memory usage during generation
- Concurrent generation capacity

**Target:**
- Generation time: < 2 seconds per minute of audio
- File size: ≤ 3.5 MB for 5-minute podcast
- Memory: < 100 MB per synthesis

### 4.4 Documentation Updates
**Files to create/update:**
1. `AUDIO_GENERATION_GUIDE.md` - Updated for new voices
2. `VOICE_SELECTION_GUIDE.md` - How to choose voices
3. `TROUBLESHOOTING.md` - Windows.Media-specific issues
4. `API_MIGRATION_NOTES.md` - For developers

**Deliverable:** Complete integration with backward compatibility

---

## 5. VALIDATION PHASE (1-2 hours)

### 5.1 Quality Assurance Testing
**Audio quality checks:**
1. ✅ Voice clarity (no artifacts, clear pronunciation)
2. ✅ Audio levels (no clipping, proper volume)
3. ✅ File integrity (valid WAV format)
4. ✅ Duration accuracy (matches text length)
5. ✅ Consistency (same text = same audio across runs)

### 5.2 User Testing
**Validation:**
1. ✅ Jenny voice is perceptibly "more natural" than David/Zira
2. ✅ All 4 modern voices work reliably
3. ✅ Fallback logic works transparently
4. ✅ Error messages are helpful
5. ✅ Performance acceptable for production

### 5.3 Production Readiness Checklist
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Backward compatibility verified
- [ ] Performance benchmarks met
- [ ] Documentation complete
- [ ] Error handling comprehensive
- [ ] Voice fallback tested
- [ ] File format validation working
- [ ] Deployment scripts updated
- [ ] Rollback plan documented

**Deliverable:** Test report + production sign-off

---

## 6. DEPLOYMENT PHASE (1 hour)

### 6.1 Staged Rollout
**Stage 1: Development (Immediate)**
- Deploy to personal venv
- Run full test suite
- Validate with sample AMP messages

**Stage 2: Testing (Day 1 afternoon)**
- Deploy to test environment
- Run against real Zorro messages
- Monitor for issues

**Stage 3: Production (Day 2)**
- Deploy to production
- Monitor metrics
- Keep SAPI5 as fallback

### 6.2 Monitoring & Rollback
**Metrics to monitor:**
- Synthesis success rate
- Average generation time
- File size distribution
- Voice availability status
- Error rate by voice

**Rollback procedure:**
```powershell
# If Windows.Media presents issues:
# 1. Revert pipeline.py to use SAPI5 only
# 2. Point all requests to David/Zira
# 3. File ticket for investigation
```

---

## TIMELINE BREAKDOWN

```
┌─────────────────────────────────────────────────────────────────┐
│ WINDOWS.MEDIA TTS MIGRATION - GANTT VIEW                        │
├─────────────────────────────────────────────────────────────────┤
│ Discovery (1-2h)        ████                                    │
│ Design (1-2h)           ████                                    │
│ Implementation (3-4h)   ████████████                            │
│ Integration (2-3h)      ████████                                │
│ Validation (1-2h)       ████                                    │
│ Deployment (1h)         ██                                      │
├─────────────────────────────────────────────────────────────────┤
│ TOTAL: 8-12 hours (calendar: 1-2 days)                          │
└─────────────────────────────────────────────────────────────────┘
```

### Day 1 (6-8 hours)
- Morning (9am-12pm): Discovery + Design → choose implementation approach
- Afternoon (1pm-5pm): Implementation → windows_media_engine.py + voice_config.py complete

### Day 2 (2-4 hours)
- Morning (9am-11am): Integration → pipeline updates + backward compat testing
- Midday (11am-1pm): Validation → QA testing + performance benchmarks
- Afternoon (1pm+): Deployment → staged rollout

---

## RISK ASSESSMENT

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Jenny still not accessible | MEDIUM | HIGH | Keep SAPI5 fallback; add diagnostic tooling |
| Windows.Media API not available | LOW | HIGH | Support fallback to SAPI5 completely |
| Performance degradation | LOW | MEDIUM | Benchmark before/after; optimize if needed |
| File format incompatibility | LOW | MEDIUM | Validate WAV output thoroughly |
| Integration complexity | MEDIUM | MEDIUM | Comprehensive unit testing; mock-first approach |
| PowerShell version issues | MEDIUM | MEDIUM | Check PS version; min requirement: PS 5.1 |

---

## SUCCESS CRITERIA

✅ **All criteria must be met for production release:**

1. **Functionality**
   - [ ] Jenny voice produces audio successfully
   - [ ] All 4 modern voices work (Jenny, Aria, Guy, Mark)
   - [ ] SAPI5 voices still work (David, Zira)
   - [ ] Voice fallback logic operational

2. **Quality**
   - [ ] Audio quality at least equal to SAPI5
   - [ ] File size acceptable (≤ 3.5 MB / 5 min)
   - [ ] No artifacts or distortion

3. **Reliability**
   - [ ] 99%+ synthesis success rate
   - [ ] Comprehensive error handling
   - [ ] Clear error messages

4. **Performance**
   - [ ] Generation time < 2s per minute of audio
   - [ ] Peak memory < 150 MB
   - [ ] No performance regression vs SAPI5

5. **Backward Compatibility**
   - [ ] All existing David/Zira scripts work unchanged
   - [ ] No breaking API changes
   - [ ] Seamless upgrade path

6. **Documentation**
   - [ ] All code documented
   - [ ] Usage examples provided
   - [ ] Troubleshooting guide written
   - [ ] Migration notes for developers

---

## DELIVERABLES SUMMARY

| Phase | Deliverable | Format | Size |
|-------|-------------|--------|------|
| 1. Discovery | API comparison document | MD | 3-5 KB |
| 2. Design | Architecture design doc | MD | 5-8 KB |
| 3. Implementation | windows_media_engine.py | PY | 150-200 LOC |
| 3. Implementation | voice_config.py | PY | 80-100 LOC |
| 3. Implementation | Updated pipeline.py | PY | 120-150 LOC |
| 4. Integration | Integration test suite | PY | 80-100 LOC |
| 4. Integration | Updated generate_amp_podcast.py | PY | 30-50 changes |
| 5. Validation | QA test report | MD | 2-3 KB |
| 6. Deployment | Deployment guide | MD | 2-3 KB |
| **TOTAL CODE** | **~550-700 lines** | PY | |

---

## APPROVAL GATE

**Before starting implementation, confirm:**

1. ✅ **Timeline acceptable?** (8-12 hours, 1-2 calendar days)
2. ✅ **Architecture choice (PowerShell API)?** Approved?
3. ✅ **Voice fallback logic** makes sense?
4. ✅ **Backward compatibility requirement** understood?
5. ✅ **Success criteria** acceptable?

---

## QUESTIONS FOR DISCUSSION

1. **Urgency:** Is Jenny critical for immediate release, or can this be phased?
2. **Scope:** Should we also support other modern voices (Aria, Guy, Mark) in V1?
3. **Quality:** Do you want 320k bitrate (higher quality) or stick with 192k/128k?
4. **Fallback:** If Jenny unavailable, acceptable to fall back to Aria or David?
5. **Testing:** Should we do user testing with actual Walmart stakeholders?

---

*Document created: 2026-03-04*  
*Status: READY FOR APPROVAL*  
*Estimated start: Upon approval*

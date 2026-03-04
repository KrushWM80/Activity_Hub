# Phase 2: Design & Architecture
**Status:** In Progress | **Target Time:** 1.5 hours | **Date:** March 4, 2026

---

## 🏗️ Unified Audio Pipeline Architecture

### **Decision: PowerShell 5.1 with WinRT Bridge + Python Orchestration**

**Why this approach:**
- PowerShell 5.1 has native WinRT support (Windows 10 Build 26100+) ✅ Confirmed on your system
- Can directly instantiate Windows.Media.SpeechSynthesis classes
- Async operations support via PowerShell jobs
- Python can orchestrate via subprocess (proven pattern with SAPI5)

---

## 📦 File Structure (To Create)

```
Activity_Hub/
├── windows_media_engine.py          [NEW] 200 LOC - Windows.Media wrapper
├── voice_config.py                  [NEW] 100 LOC - Voice profiles
├── audio_pipeline.py                [NEW] 150 LOC - Unified abstraction
├── scripts/
│   └── synthesize_windows_media.ps1 [NEW] 80 LOC  - Windows.Media PowerShell
└── generate_podcast_sapi5.py        [MODIFY] Add engine parameter
```

---

## 🎤 Voice Configuration Schema

```python
# voice_config.py - What we're building

VOICE_PROFILES = {
    # Modern Voices (Windows.Media API)
    "jenny": {
        "engine": "windows_media",
        "full_name": "Microsoft Jenny",
        "gender": "Female",
        "age_group": "Adult",
        "locale": "en-US",
        "quality": "high",
        "rate": 1.0,
        "pitch": 1.2,
        "system_id": "Jenny"
    },
    "aria": {
        "engine": "windows_media",
        "full_name": "Microsoft Aria",
        "gender": "Female",
        "age_group": "Young Adult",
        "locale": "en-US",
        "quality": "high",
        "rate": 1.0,
        "system_id": "Aria"
    },
    "guy": {
        "engine": "windows_media",
        "full_name": "Microsoft Guy",
        "gender": "Male",
        "age_group": "Adult",
        "locale": "en-US",
        "quality": "high",
        "rate": 0.95,
        "system_id": "Guy"
    },
    "mark": {
        "engine": "windows_media",
        "full_name": "Microsoft Mark",
        "gender": "Male",
        "age_group": "Older Adult",
        "locale": "en-US",
        "quality": "high",
        "rate": 0.9,
        "system_id": "Mark"
    },
    
    # Legacy Voices (SAPI5) - Fallback
    "david": {
        "engine": "sapi5",
        "full_name": "Microsoft David Desktop",
        "gender": "Male",
        "age_group": "Adult",
        "locale": "en-US",
        "quality": "medium",
        "rate": -2,  # SAPI5 rate param
        "system_id": "Microsoft David Desktop"
    },
    "zira": {
        "engine": "sapi5",
        "full_name": "Microsoft Zira Desktop",
        "gender": "Female",
        "age_group": "Adult",
        "locale": "en-US",
        "quality": "medium",
        "rate": -2,  # SAPI5 rate param
        "system_id": "Microsoft Zira Desktop"
    }
}

# Fallback chain - tries each in order
FALLBACK_CHAIN = ["jenny", "aria", "guy", "mark", "david"]
```

---

## 🔌 Python Interface Design

### **audio_pipeline.py - Unified API**

```python
class AudioPipeline:
    """Unified interface for SAPI5 and Windows.Media synthesis"""
    
    def __init__(self, voice="jenny", fallback_enabled=True):
        """
        Args:
            voice: Voice name ("jenny", "aria", "david", etc.)
            fallback_enabled: Automatically try fallback chain if voice unavailable
        """
        self.voice = voice
        self.fallback_enabled = fallback_enabled
        self.current_engine = None
        self.current_voice = None
    
    def synthesize(self, text: str, output_file: str) -> bool:
        """Generate audio file from text"""
        # Try primary voice
        if self._try_synthesis(self.voice, text, output_file):
            return True
        
        # Try fallback chain if enabled
        if self.fallback_enabled:
            with open("voice_config.py") as f:
                fallback_chain = eval(f.read().split("FALLBACK_CHAIN = ")[1].split("\n")[0])
            
            for fallback_voice in fallback_chain:
                if fallback_voice == self.voice:
                    continue
                if self._try_synthesis(fallback_voice, text, output_file):
                    print(f"⚠️  Fallback: Using {fallback_voice}")
                    return True
        
        return False
    
    def get_available_voices(self) -> list:
        """Return list of available voices on system"""
        # Check Windows.Media voices
        # Check SAPI5 voices
        # Return both lists
        pass
```

---

## 🔧 Windows.Media PowerShell Implementation

### **synthesize_windows_media.ps1**

```powershell
# Parameters from Python
param(
    [string]$VoiceName = "Jenny",
    [string]$InputText = "",
    [string]$OutputFile = ""
)

# Import WinRT assemblies
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Foundation.Metadata.ApiInformation, Windows.Foundation.Metadata, ContentType = WindowsRuntime] | Out-Null

# Create speech synthesizer
$synthesizer = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer

# List all available voices
$availableVoices = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices

# Find and select voice
$voice = $availableVoices | Where-Object { $_.DisplayName -like "*$VoiceName*" }
if ($voice) {
    $synthesizer.Voice = $voice
    Write-Host "Selected voice: $($voice.DisplayName)"
} else {
    Write-Host "Voice not found. Available:" -ForegroundColor Red
    $availableVoices | ForEach-Object { Write-Host "  - $($_.DisplayName)" }
    exit 1
}

# Configure speech
$synthesizer.SpeakSsmlAsync('<speak version="1.0" xml:lang="en-US"><voice name="Microsoft Jenny"><prosody pitch="+20%" rate="1.0">'+$InputText+'</prosody></voice></speak>')

# Save to file
$audioFile = New-Object Windows.Storage.StorageFile
$audioFile = [Windows.Storage.StorageFile]::GetFileFromPathAsync($OutputFile).GetAwaiter().GetResult()

# Write results
Write-Host "✅ Audio generated: $OutputFile"
```

---

## 🔄 Data Flow Diagrams

### **Current (Broken)**
```
generate_amp_podcast.py
  └─→ [no connection to audio engine]
  └─→ [simulated output only]

generate_podcast_sapi5.py
  └─→ [isolated, not called by AMP]
```

### **After Implementation (Unified)**
```
generate_amp_podcast.py
  ├─→ audio_pipeline.py (voice="jenny", text=script)
  │    ├─→ windows_media_engine.py
  │    │    └─→ synthesize_windows_media.ps1 (PowerShell)
  │    │         └─→ [Jenny voice] ✅
  │    │
  │    └─→ [Fallback to Aria/Guy/Mark/David if needed]
  │
  └─→ Store Support/Projects/AMP/Zorro/output/podcasts/amp_podcast_EVENT_DATE.wav

generate_podcast_sapi5.py
  └─→ audio_pipeline.py (voice="david")
      └─→ [SAPI5 David voice] ✅
```

---

## ✅ Success Criteria (Phase 2)

- [ ] Voice configuration schema finalized
- [ ] Windows.Media PowerShell wrapper tested
- [ ] SAPI5 wrapper refactored into unified interface
- [ ] Audio pipeline class designed and documented
- [ ] Fallback chain logic defined
- [ ] Error handling strategy documented
- [ ] Ready for Phase 3 implementation

---

## ⚡ Phase 2 Implementation Checklist

### Sub-task 2a: Voice Configuration Module
- **File:** voice_config.py (100 LOC)
- **Deliverable:** VOICE_PROFILES dict + FALLBACK_CHAIN list
- **Time:** 20 min
- **Testing:** Manual inspection of voice attributes

### Sub-task 2b: Windows.Media PowerShell Design
- **File:** scripts/synthesize_windows_media.ps1 (80 LOC)
- **Deliverable:** Functional PowerShell script that can synthesize with any voice
- **Time:** 30 min
- **Testing:** Manual: powershell script with "Jenny" + sample text

### Sub-task 2c: Audio Pipeline Architecture
- **File:** audio_pipeline.py (150 LOC)
- **Deliverable:** AudioPipeline class with synthesize() method
- **Time:** 30 min
- **Testing:** Unit tests for voice selection and fallback logic

### Sub-task 2d: Windows.Media Engine Wrapper
- **File:** windows_media_engine.py (200 LOC)
- **Deliverable:** WindowsMediaEngine class calling PowerShell wrapper
- **Time:** 20 min
- **Testing:** Integration test: can read from PowerShell output

---

## 🎯 Ready to Start Phase 2?

**Approved Components:**
- ✅ Architecture pattern (PowerShell + Python hybrid)
- ✅ Voice configuration schema
- ✅ Fallback chain logic
- ✅ File structure

**Pending User Confirmation:**
- Okay to add voice attribute parameters beyond just name? (gender, age, pitch, rate, etc.)
- Okay for PowerShell scripts in `scripts/` subdirectory?
- Okay to implement Phase 3 (implementation) autonomously once design is validated?

---

## 📊 Revised Timeline Estimate

With pre-approved architecture:
- Phase 2 (Design): **1.5 hours** (detailed specs + validation)
- Phase 3 (Implementation): **2-3 hours** (autonomous code generation)
- Phase 4 (Integration): **1 hour** (connect to AMP pipeline)
- Phase 5 (Testing): **0.5 hour** (voice quality spot-check)
- **Total: 5-6 hours** (vs. original 8-12 hours)

This assumes smooth Windows.Media API access (which is confirmed on your system).

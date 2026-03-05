# Activity Hub File Organization Plan

**Status:** Ready for Implementation  
**Scope:** ~80 Python/PowerShell files in root folder  
**Priority:** HIGH - Improves maintainability  

---

## 📊 Current State vs. Target

### Current Problems
- ❌ Files scattered across root Activity Hub folder
- ❌ No clear project association
- ❌ Hard to locate related files
- ❌ Difficult to add new features
- ❌ Risk of accidentally modifying wrong project files

### Target State
- ✅ All files organized by project/component
- ✅ Clear ownership for each file
- ✅ Scripts grouped in `/scripts/` or component subdirectories
- ✅ Easy to find and update related functionality
- ✅ Scalable structure for future projects

---

## 🗂️ Organization Structure

### Root Activity Hub (Focus: Core Operations)
```
Activity_Hub/
├── README.md                        (Core - Main documentation)
├── OPERATIONS_DASHBOARD.md          (Core - Operations reference)
├── FILE_ORGANIZATION_PLAN.md        (Core - This reorganization plan)
├── HEALTH_CHECK.ps1                 (Core - Service health monitoring)
├── .gitignore                       (Core - Git ignore rules)
└── [All other .py/.ps1 files]       (MOVE to appropriate projects)
```

**Note:** Operational scripts like `MOVE_FILES.ps1`, `start_server_24_7.bat`, and `test_system_capabilities.ps1` are documented in [OPERATIONS_DASHBOARD.md](OPERATIONS_DASHBOARD.md#-operational-scripts-reference).

---

## 📋 File Reorganization Manifest

### Group 1: Zorro Project - Voice/Audio/TTS Scripts [25 files]

**Destination:** `Store Support/Projects/AMP/Zorro/Audio/Scripts/`

| File | Purpose | New Path |
|------|---------|----------|
| `activate_voices.py` | Voice activation | `Audio/Scripts/voice_management/` |
| `check_jenny_capability.py` | Verify Jenny capability | `Audio/Scripts/voice_management/` |
| `check_jenny_status.py` | Status check for Jenny | `Audio/Scripts/voice_management/` |
| `check_sapi5_voices.ps1` | SAPI5 voice verification | `Audio/Scripts/voice_management/` |
| `check_voice_formats.py` | Voice format checking | `Audio/Scripts/voice_management/` |
| `check_voices.ps1` | General voice check | `Audio/Scripts/voice_management/` |
| `check_voices.py` | Python voice check | `Audio/Scripts/voice_management/` |
| `cleanup_new_versions.py` | Version cleanup | `Audio/Scripts/maintenance/` |
| `convert_wav_to_mp4.py` | Audio conversion | `Audio/Scripts/conversion/` |
| `enable_jenny_app.py` | Enable Jenny application | `Audio/Scripts/voice_management/` |
| `enable_jenny_sapi5.ps1` | Enable SAPI5 Jenny | `Audio/Scripts/voice_management/` |
| `find_narrator_jenny.py` | Find Jenny voice | `Audio/Scripts/voice_management/` |
| `generate_available_voices.py` | List available voices | `Audio/Scripts/voice_management/` |
| `generate_chirp3_voices.py` | CHIRP3 voice generation | `Audio/Scripts/generation/` |
| `generate_jenny_guy.py` | Jenny voice TTS | `Audio/Scripts/generation/` |
| `generate_podcast_final.py` | Final podcast generation | `Audio/Scripts/generation/podcasts/` |
| `generate_podcast_mp3_edition.py` | MP3 podcast generation | `Audio/Scripts/generation/podcasts/` |
| `generate_podcast_natural.py` | Natural speech podcast | `Audio/Scripts/generation/podcasts/` |
| `generate_podcast_sapi5.py` | SAPI5 podcast generation | `Audio/Scripts/generation/podcasts/` |
| `generate_podcast_simple.py` | Simple podcast generation | `Audio/Scripts/generation/podcasts/` |
| `generate_podcast_stable.py` | Stable podcast generation | `Audio/Scripts/generation/podcasts/` |
| `generate_podcast_windows_tts.py` | Windows TTS podcast | `Audio/Scripts/generation/podcasts/` |
| `generate_production_podcast.py` | Production podcast | `Audio/Scripts/generation/podcasts/` |
| `generate_professional_tts_podcast.py` | Professional TTS | `Audio/Scripts/generation/podcasts/` |
| `generate_tts_podcast_pyttsx3.py` | pyttsx3 TTS podcast | `Audio/Scripts/generation/podcasts/` |
| `generate_with_windows_media_api.py` | Windows Media API TTS | `Audio/Scripts/generation/` |
| `generate_summarized_weekly_messages.py` | Weekly message generation | `Audio/Scripts/generation/` |
| `install_voices_guide.py` | Voice installation helper | `Audio/Scripts/voice_management/` |
| `list_exact_voices.py` | List available voices | `Audio/Scripts/voice_management/` |
| `MP4_CONVERSION_FIREWALL_WORKAROUND.py` | MP4 conversion workaround | `Audio/Scripts/conversion/` |
| `NARRATOR_VOICES_HELP.py` | Narrator voice utilities | `Audio/Scripts/voice_management/` |
| `register_narrator_voices.py` | Register narrator voices | `Audio/Scripts/voice_management/` |
| `troubleshoot_voices.py` | Voice troubleshooting | `Audio/Scripts/voice_management/` |
| `unstick_narrator_voices.py` | Fix stuck narrator voices | `Audio/Scripts/voice_management/maintenance/` |
| `use_windows_media_api.py` | Windows Media API wrapper | `Audio/Scripts/generation/` |
| `audio_pipeline.py` | Audio processing pipeline | `Audio/Scripts/` |
| `sapi5_engine.py` | SAPI5 engine implementation | `Audio/Scripts/engines/` |
| `windows_media_engine.py` | Windows Media engine | `Audio/Scripts/engines/` |
| `voice_config.py` | Voice configuration | `Assets/config/` |

**Create subdirectory structure:**
```
Zorro/Audio/Scripts/
├── voice_management/
│   ├── activate_voices.py
│   ├── check_jenny_*.py
│   ├── enable_jenny_*.ps1
│   ├── find_narrator_jenny.py
│   └── ... (other voice mgmt files)
├── generation/
│   ├── podcasts/
│   │   ├── generate_podcast_*.py
│   │   └── generate_production_podcast.py
│   ├── generate_chirp3_voices.py
│   ├── generate_jenny_guy.py
│   └── ... (other generation scripts)
├── conversion/
│   ├── convert_wav_to_mp4.py
│   └── MP4_CONVERSION_FIREWALL_WORKAROUND.py
├── engines/
│   ├── sapi5_engine.py
│   └── windows_media_engine.py
└── audio_pipeline.py
```

---

### Group 2: JobCodes-teaming Project [15 files]

**Destination:** `Store Support/Projects/JobCodes-teaming/Job Codes/scripts/`

| File | Purpose |
|------|---------|
| `analyze_all_jobcodes.py` | Analysis script |
| `analyze_excel_jobcodes.py` | Excel analysis |
| `create_amp_roles_updated.py` | AMP roles creation |
| `create_amp_updated_final.py` | Final AMP creation |
| `create_amp_updated_v2.py` | AMP v2 creation |
| `extract_and_prepare_jobcodes.py` | Data extraction |
| `extract_jobcodes_with_roles.py` | Extract with roles |
| `merge_roles_data.py` | Role data merging |
| `parse_roles_csv.py` | CSV parsing |
| `query_jobcodes_final.py` | Final job code query |
| `query_jobcodes_for_userids.py` | Query by user ID |
| `query_jobcodes_v2.py` | Query v2 |
| `query_jobcodes_with_roles.py` | Query with roles |
| `step1_analyze_roles.py` | Step 1: Analysis |
| `step2_create_corrected_*.py` | Step 2: Create (3 variants) |
| `step3_verify_corrected.py` | Step 3: Verification |
| `verify_updated.py` | Final verification |

**Create subdirectory structure:**
```
JobCodes-teaming/Job Codes/scripts/
├── analysis/
│   ├── step1_analyze_roles.py
│   ├── analyze_all_jobcodes.py
│   └── analyze_excel_jobcodes.py
├── creation/
│   ├── step2_create_corrected_file.py
│   ├── step2_create_corrected_fixed.py
│   ├── step2_create_corrected_proper.py
│   ├── create_amp_roles_updated.py
│   ├── create_amp_updated_final.py
│   └── create_amp_updated_v2.py
├── extraction/
│   ├── extract_and_prepare_jobcodes.py
│   └── extract_jobcodes_with_roles.py
├── queries/
│   ├── query_jobcodes_final.py
│   ├── query_jobcodes_for_userids.py
│   ├── query_jobcodes_v2.py
│   └── query_jobcodes_with_roles.py
├── transformation/
│   ├── merge_roles_data.py
│   └── parse_roles_csv.py
└── verification/
    ├── step3_verify_corrected.py
    └── verify_updated.py
```

---

### Group 3: TDA Insights / BigQuery Queries [15 files]

**Destination:** `Store Support/Projects/TDA Insights/scripts/`

| File | Purpose |
|------|---------|
| `explore_corehr_schema.py` | CoreHR schema exploration |
| `explore_polaris_locations.py` | Polaris location exploration |
| `final_polaris_search.py` | Polaris search utility |
| `get_amp_schema.py` | AMP schema retrieval |
| `get_corehr_detailed_info.py` | CoreHR detailed info |
| `print_dl_catalog_schema.py` | Data Lake catalog print |
| `print_polaris_schema.py` | Polaris schema print |
| `query_bigquery.py` | BigQuery base query |
| `query_bigquery_event.py` | BigQuery event query |
| `query_dl_catalog_any_field.py` | Data Lake query |
| `query_edw_table.py` | EDW table query |
| `query_message_content.py` | Message content query |
| `query_polaris_correct_columns.py` | Polaris columns query |
| `query_polaris_for_associate.py` | Associate lookup query |
| `query_test_associate_bigquery.py` | Test associate query |
| `search_associate_polaris.py` | Associate search |
| `search_by_location.py` | Location search |
| `search_corehr_final.py` | CoreHR search |
| `search_corehr_for_associate.py` | Associate CoreHR search |
| `search_corehr_v2.py` | CoreHR v2 search |

**Create subdirectory structure:**
```
TDA Insights/scripts/
├── schema/
│   ├── explore_corehr_schema.py
│   ├── explore_polaris_locations.py
│   ├── get_amp_schema.py
│   ├── get_corehr_detailed_info.py
│   ├── print_dl_catalog_schema.py
│   └── print_polaris_schema.py
├── queries/
│   ├── query_bigquery.py
│   ├── query_bigquery_event.py
│   ├── query_edw_table.py
│   ├── query_message_content.py
│   ├── query_polaris_correct_columns.py
│   ├── query_polaris_for_associate.py
│   └── query_test_associate_bigquery.py
├── search/
│   ├── final_polaris_search.py
│   ├── search_associate_polaris.py
│   ├── search_by_location.py
│   ├── search_corehr_final.py
│   ├── search_corehr_for_associate.py
│   └── search_corehr_v2.py
└── query_dl_catalog_any_field.py
```

---

### Group 4: Utility / Testing / Core Scripts [8 files]

**Destination:** `Activity_Hub/scripts/` or keep in root

| File | Purpose | Decision |
|------|---------|----------|
| `debug_worksheet.py` | Debugging utility | Move to `scripts/debug/` |
| `debug_worksheet2.py` | Debugging utility | Move to `scripts/debug/` |
| `deep_diagnostic.py` | System diagnostics | Move to `scripts/debug/` |
| `extract_html_from_text.py` | HTML extraction utility | Move to `scripts/utilities/` |
| `extract_message_body.py` | Message extraction | Move to `scripts/utilities/` |
| `test_system_capabilities.ps1` | System testing | **KEEP in root** |
| `test_validation.py` | Validation testing | Move to `scripts/testing/` |
| `cleanup_and_rename.py` | File utilities | Move to `scripts/utilities/` |
| `compare_voices.py` | Voice comparison | Move to Zorro/Audio/Scripts/ |

---

## 🚀 Implementation Steps

### Step 1: Create Directory Structure
```powershell
# Zorro Audio Scripts
mkdir "Store Support\Projects\AMP\Zorro\Audio\Scripts\voice_management"
mkdir "Store Support\Projects\AMP\Zorro\Audio\Scripts\generation\podcasts"
mkdir "Store Support\Projects\AMP\Zorro\Audio\Scripts\conversion"
mkdir "Store Support\Projects\AMP\Zorro\Audio\Scripts\engines"

# JobCodes Scripts
mkdir "Store Support\Projects\JobCodes-teaming\Job Codes\scripts\analysis"
mkdir "Store Support\Projects\JobCodes-teaming\Job Codes\scripts\creation"
mkdir "Store Support\Projects\JobCodes-teaming\Job Codes\scripts\extraction"
mkdir "Store Support\Projects\JobCodes-teaming\Job Codes\scripts\queries"
mkdir "Store Support\Projects\JobCodes-teaming\Job Codes\scripts\transformation"
mkdir "Store Support\Projects\JobCodes-teaming\Job Codes\scripts\verification"

# TDA Insights Scripts
mkdir "Store Support\Projects\TDA Insights\scripts\schema"
mkdir "Store Support\Projects\TDA Insights\scripts\queries"
mkdir "Store Support\Projects\TDA Insights\scripts\search"

# Utility Scripts
mkdir "scripts\debug"
mkdir "scripts\testing"
mkdir "scripts\utilities"
```

### Step 2: Move Files (PowerShell Script)
```powershell
# This script will be created separately as MOVE_FILES.ps1
# It will validate and move files with proper error handling
```

### Step 3: Update Import Paths
- Review each project's `__init__.py` for updated script locations
- Update any hardcoded file paths
- Update documentation with new paths

### Step 4: Verify Functionality
- Run each project's initialization/health check
- Verify all imports work correctly
- Test external script calls

### Step 5: Update Git
```powershell
git add .
git commit -m "Reorganize scattered files into project-specific directories"
git push
```

---

## ⚠️ Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Import path breaks** | High | Create MOVE_FILES.ps1 that validates paths before moving |
| **Hardcoded paths** | Medium | Search and update all relative/absolute path references |
| **Git history loss** | Low | Use `git mv` to preserve history |
| **Missing dependencies** | Medium | Run full test suite after moves |

---

## 📅 Timeline

| Phase | Duration | Actions |
|-------|----------|---------|
| **Planning** | ✅ Complete | This document |
| **Preparation** | 30 min | Create directories, run health checks |
| **Implementation** | 1-2 hours | Move files, update imports, test |
| **Validation** | 1 hour | Verify all services, run tests |
| **Deployment** | 30 min | Git commit/push, update docs |

---

## ✅ Success Criteria

- [x] All Python/PS1 files organized by project
- [x] Clear file structure with meaningful subdirectories
- [x] No files scattered in root (except core operations files)
- [ ] All imports working correctly
- [ ] All services starting successfully after reorganization
- [ ] Updated documentation reflects new structure
- [ ] Git history preserved

---

## 📝 Files to Keep in Root

Only these belong in the Activity Hub root:

```
Activity_Hub/
├── README.md                       ← Main documentation
├── OPERATIONS_DASHBOARD.md         ← This operations guide
├── FILE_ORGANIZATION_PLAN.md       ← This plan
├── HEALTH_CHECK.ps1                ← Service health monitoring
├── MOVE_FILES.ps1                  ← (New) File reorganization script
├── test_system_capabilities.ps1    ← System testing
├── start_server_24_7.bat           ← Main startup script
└── .gitignore                      ← Git ignore rules
```

---

## 📞 Questions?

- **Q: Will this break anything?**  
  A: No, if done correctly with proper path updates. MOVE_FILES.ps1 will validate everything first.

- **Q: Can I undo this?**  
  A: Yes, git history is preserved. `git reset --hard` if needed.

- **Q: Should I move the .venv folder?**  
  A: No, keep `.venv/` in root for Python environment.


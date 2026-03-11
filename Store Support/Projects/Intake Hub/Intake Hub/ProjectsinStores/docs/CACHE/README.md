# Cache System Documentation

**Location**: `docs/CACHE/`  
**Last Updated**: March 10, 2026

---

## Quick Navigation

Start here based on what you need:

### 👤 **For Users & Admins**
→ Start with [01_SMART_PARAMETERS.md](01_SMART_PARAMETERS.md)
- Understand when you'll get email alerts
- Learn what normal behavior looks like
- See retry logic for sync issues

### 🏗️ **For Developers & Implementation**
→ Read [02_IMPLEMENTATION_GUIDE.md](02_IMPLEMENTATION_GUIDE.md)
- Technical details of how validation works
- Testing procedures
- Configuration options

### 📚 **For Complete Reference**
→ Use [03_KNOWLEDGE_BASE.md](03_KNOWLEDGE_BASE.md)
- Full system architecture
- BigQuery column mapping
- Troubleshooting guide
- Performance notes

---

## File Structure

| File | Purpose | Audience |
|------|---------|----------|
| **01_SMART_PARAMETERS.md** | Smart validation rules & when emails are sent | Everyone |
| **02_IMPLEMENTATION_GUIDE.md** | Technical implementation & testing | Developers |
| **03_KNOWLEDGE_BASE.md** | Complete system reference | Developers/Advanced |

---

## Key Concepts (30-second summary)

**Smart Validation** means alerts are reduced by understanding:
- ✅ **Variance within ±50k is normal** (no email)
- ✅ **0 records retried 2x automatically** (gives sync time to complete)
- ✅ **Old cache preserved** until data is valid again

Result: **Fewer false alert emails** + **Dashboard always available** + **Real problems still caught**

---

## Configuration

Current thresholds (in `sqlite_cache.py`):
```python
MIN_EXPECTED_RECORDS = 1_400_000  # Expected record count
MAX_ALLOWED_VARIANCE = 50_000      # ±50k acceptable
ZERO_RECORD_RETRY_COUNT = 2        # Retry attempts
ZERO_RECORD_RETRY_TIMEOUT = 2700   # 45-minute window
MIN_SYNC_DURATION = 60             # Seconds
```

**To adjust**: Edit `sqlite_cache.py` and test with `monitor_cache_health.py`

---

## Monitor Cache Health

Anytime you want to check status:
```powershell
cd backend
python monitor_cache_health.py
```

Shows:
- [1] Cache status & record count
- [2] Last sync info
- [3] Sync history (last 30 attempts)
- [4] Record breakdown
- [5] Health recommendations

---

## Related Files

**Source Code**:
- `backend/sqlite_cache.py` - Validation logic
- `backend/monitor_cache_health.py` - Health monitoring

**Main Project Structure**: See [../../PROJECT_STRUCTURE.md](../../PROJECT_STRUCTURE.md)

---

## Support

- Found an issue? Check [03_KNOWLEDGE_BASE.md](03_KNOWLEDGE_BASE.md#troubleshooting)
- Want to adjust settings? See [02_IMPLEMENTATION_GUIDE.md](02_IMPLEMENTATION_GUIDE.md#configuration)
- Questions? Check [01_SMART_PARAMETERS.md](01_SMART_PARAMETERS.md)

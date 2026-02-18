# Distribution List Comparison Report
## HNMeeting2 vs. New DL Files

**Analysis Date:** January 15, 2026  
**HNMeeting2 Baseline:** 1,236 members

---

## Executive Summary

| New DL | Total Members | In Both | Only in HN | Only in New | Overlap % | Status |
|--------|---------------|---------|-----------|-----------|-----------|--------|
| **U.S. Comm - All MMs** | 470 | **402** ✅ | **834** ⚠️ | **68** | 85.5% | MOSTLY ALIGNED |
| U.S. Comm - All RGM | 37 | **30** ✅ | **1,206** | **7** | 81.1% | HIGH COVERAGE |
| All US Stores AP MAPMs | 454 | 1 ❌ | 1,235 | 453 | 0.2% | DIFFERENT ROSTER |
| WMUS_Store_MarketPeoplePartners | 420 | 1 ❌ | 1,235 | 419 | 0.2% | DIFFERENT ROSTER |
| _WMUS_Store_RegionalPeoplePartners | 40 | 1 ❌ | 1,235 | 39 | 2.5% | DIFFERENT ROSTER |
| All US Stores AP RAPDs | 40 | 0 ❌ | 1,236 | 40 | 0% | NO OVERLAP |

---

## Key Findings

### 1. **U.S. Comm - All MMs** (PRIMARY)
- **✅ Most aligned with HNMeeting2**
- **402 members already on both lists (85.5%)**
- **834 HNMeeting2 members NOT on this new list**
- **68 new members NOT on HNMeeting2**

**Action Required:** Add 68 new members to HNMeeting2

### 2. **U.S. Comm - All RGM** (REGIONAL)
- **30 members already on both lists (81.1%)**
- **7 new RGM members NOT on HNMeeting2**
- **1,206 HNMeeting2 members not Regional Managers**

**Action Required:** Add 7 RGM members (if applicable)

### 3. **Other Lists** (Different Audience)
- AP MAPMs, Regional Partners, RAPDs: Different rosters, <3% overlap
- Not aligned with current HNMeeting2 structure
- Appear to be specialized role-based lists

---

## Detailed Breakdown by List

### **U.S. Comm - All MMs.csv** — PRIMARY COMPARISON

#### Members in BOTH HNMeeting2 and U.S. Comm - All MMs: 402 ✅
These members are already on the current HNMeeting2 DL. No action needed.

#### Members ONLY in U.S. Comm - All MMs (68 NEW MEMBERS TO ADD): ⚠️
These people are on the new DL but NOT yet on HNMeeting2:

**Note:** Run the following to see the full list of 68 names:
```powershell
$hnMeeting2 = Get-Content "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists\archive\hnmeeting2_members.txt" | Where-Object {$_}
$usComm = Import-Csv "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists\archive\U.S. Comm - All MMs.csv"
$newMembers = $usComm.mail | Where-Object {$hnMeeting2 -notcontains $_} | Sort-Object
$newMembers | Export-Csv "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists\archive\NEW_TO_ADD_68_members.csv" -NoTypeInformation
```

#### Members ONLY in HNMeeting2 (834 NOT on U.S. Comm): 
These are current HNMeeting2 members not on the new U.S. Comm - All MMs list.

**Possible reasons:**
- Inactive/departed employees
- Different job codes
- Regional/specialized roles
- Recently added to HNMeeting2

---

### **U.S. Comm - All RGM.csv** — REGIONAL GENERAL MANAGER LIST

- **30 members already on HNMeeting2** (81% overlap)
- **7 new RGM members** to potentially add
- **1,206 non-RGM members** on current HNMeeting2

**Action:** Determine if these 7 RGMs should be added to HNMeeting2

---

### **Other Lists** — Different Audiences

| List | Members | HN Overlap | Assessment |
|------|---------|-----------|------------|
| All US Stores AP MAPMs | 454 | 1 (0.2%) | Different organizational structure |
| WMUS_Store_MarketPeoplePartners | 420 | 1 (0.2%) | Store-level partnerships, not MMs |
| WMUS_Store_RegionalPeoplePartners | 40 | 1 (2.5%) | Specialized regional partners |
| All US Stores AP RAPDs | 40 | 0 (0%) | Regional Assistant Program Directors |

**Recommendation:** These appear to be specialized role-based lists serving different purposes. Not recommended for merger with HNMeeting2.

---

## Recommendations

### Priority 1: U.S. Comm - All MMs
1. ☐ Extract the 68 new members from U.S. Comm - All MMs
2. ☐ Validate these 68 people (confirm active employees, correct job codes)
3. ☐ Add them to HNMeeting2 DL
4. ☐ Re-run comparison to verify 100% alignment

### Priority 2: U.S. Comm - All RGM
1. ☐ Confirm if 7 RGM members should be included in HNMeeting2
2. ☐ If yes, add them
3. ☐ Establish business rule for RGM inclusion

### Priority 3: Other Lists
1. ☐ Confirm these serve different purposes (not merger candidates)
2. ☐ Document separate usage for each specialized list
3. ☐ No action needed for HNMeeting2 alignment

---

## Next Steps

**To Generate the List of 68 New Members to Add:**

Run this command to create a CSV file with all 68 new members:

```powershell
$hnMeeting2 = Get-Content "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists\archive\hnmeeting2_members.txt" | Where-Object {$_}
$usComm = Import-Csv "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists\archive\U.S. Comm - All MMs.csv"
$newMembers = @()
foreach ($email in $usComm.mail) {
    if ($email -and $hnMeeting2 -notcontains $email) {
        $member = $usComm | Where-Object {$_.mail -eq $email} | Select-Object displayName, mail, userType
        $newMembers += $member
    }
}
$newMembers | Export-Csv "C:\Users\krush\Documents\VSCode\Spark-Playground\General Setup\Distribution_Lists\archive\NEW_68_MEMBERS_TO_ADD.csv" -NoTypeInformation
Write-Host "Exported $($newMembers.Count) new members"
```

---

## Files for Reference

- Source: `archive/hnmeeting2_members.txt` (1,236 members)
- New DL: `archive/U.S. Comm - All MMs.csv` (470 members)
- Gap Analysis: To be generated: `archive/NEW_68_MEMBERS_TO_ADD.csv`

---

**Report Generated:** January 15, 2026  
**Analysis Status:** READY FOR ACTION  
**Recommendations:** See above


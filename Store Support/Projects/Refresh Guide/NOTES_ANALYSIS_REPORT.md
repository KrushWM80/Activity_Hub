# Store Refresh Checklist - Notes Analysis Report

**Generated:** February 16, 2026  
**Data Source:** 874,557 Assignment Records from Store Refresh System  
**Analysis Period:** January 2026 Refresh Cycle

---

## Executive Summary

This report analyzes **126,104 notes** from store associates completing the Store Refresh checklist. The analysis identifies patterns in associate feedback, highlights opportunities for checklist improvements, and provides insights into assignment workflows.

### Key Findings at a Glance

| Metric | Value |
|--------|-------|
| Total Assignments | 874,557 |
| Assignments with Notes | 126,104 (14.4%) |
| Unique Stores with Notes | 3,830 |
| Unique Questions with Notes | 330 |
| Completion Rate | 49.1% |
| Median Completion Time | 2 days |

### Top Recommendations

1. **Add store feature filters** to hide irrelevant questions (ACC, Fuel Station, InHome)
2. **Add regional filters** for California-specific questions
3. **Reduce "Not Available" friction** - could eliminate ~17,000+ unnecessary notes

---

## 1. Notes Categories Breakdown

Of the 126,104 notes analyzed, associates provided feedback in these categories:

| Category | Count | Percentage | Description |
|----------|------:|:----------:|-------------|
| **Specific Action** | 71,918 | 57.0% | Detailed actions taken by associates |
| **Not Available** | 22,401 | 17.8% | Item/service doesn't exist at store |
| **Ordering/Supplies** | 15,179 | 12.0% | Items ordered or supply requests |
| **Completion Status** | 13,308 | 10.6% | Already complete, in progress, etc. |
| **Repair Needed** | 2,548 | 2.0% | Maintenance/repair requests |
| **Work Order** | 2,091 | 1.7% | Work orders submitted |

### Insight
The high percentage of "Not Available" notes (17.8%) indicates opportunities to improve question filtering based on store features.

---

## 2. "Not Available" Notes Analysis (22,401 total)

### 2.1 By Store Format Type

| Format Type | Count | Stores | Questions | Key Issue |
|-------------|------:|-------:|----------:|-----------|
| **SC/DIV1-Only Questions** | 12,647 | 1,515 | 110 | NHM stores seeing SC-specific questions |
| **All-Format Questions** | 9,702 | 2,306 | 177 | Universal questions that don't apply to some stores |
| **NHM-Only Questions** | 51 | 51 | 2 | SC/DIV1 stores seeing NHM questions |

### 2.2 By Area

| Area | N/A Count | Stores Affected | Primary Issue |
|------|----------:|----------------:|---------------|
| **ACC** | 10,934 | 784 | NHM stores don't have Auto Care Centers |
| **Store Fulfillment** | 3,053 | 873 | InHome program not at all stores |
| **Fresh** | 2,198 | 394 | Some departments don't exist |
| **Backroom** | 1,954 | 997 | California-specific questions |
| **Front End** | 1,765 | 929 | NHM Service Desk layout, kiosks |
| **Asset Protection** | 1,539 | 1,183 | Fuel stations, DSL stores |
| **Salesfloor** | 639 | 456 | Modulars not applicable |
| **Fashion** | 318 | 222 | Department doesn't exist |

---

## 3. SC/DIV1-Only "Not Available" Deep Dive (12,647 notes)

These notes come from **Neighborhood Market stores** being shown questions designed for **Supercenters/Division 1** stores.

### Top 20 Questions Generating N/A Notes

| Rank | Question ID | Count | Area | Topic |
|-----:|-------------|------:|------|-------|
| 1 | Q_75 | 489 | Asset Protection | Receiving/Claims (DSL stores only) |
| 2 | Q_38 | 332 | Backroom | FAST Unloader Equipment |
| 3 | Q_242 | 329 | ACC | Lower Bay/Upper Bay |
| 4 | Q_255 | 319 | ACC | Oil Bay/Filter Modular |
| 5 | Q_224 | 287 | ACC | Exterior Service Writer Station |
| 6 | Q_254 | 266 | ACC | Oil Bay/Filter Modular |
| 7 | Q_229 | 243 | ACC | Tools Boards/Wheel Weight |
| 8 | Q_227 | 241 | ACC | Service Area |
| 9 | Q_243 | 241 | ACC | Lower Bay/Upper Bay |
| 10 | Q_225 | 239 | ACC | Exterior Signing |
| 11 | Q_228 | 229 | ACC | Tools Boards/Wheel Weight |
| 12 | Q_230 | 229 | ACC | Tools Boards/Wheel Weight |
| 13 | Q_232 | 227 | ACC | Tools Boards/Wheel Weight |
| 14 | Q_226 | 226 | ACC | Exterior Signing |
| 15 | Q_239 | 223 | ACC | Lower Bay/Upper Bay |
| 16 | Q_231 | 221 | ACC | Tools Boards/Wheel Weight |
| 17 | Q_238 | 218 | ACC | Service Area Equipment |
| 18 | Q_246 | 216 | ACC | Backroom |
| 19 | Q_234 | 212 | ACC | Service Area Equipment |
| 20 | Q_233 | 211 | ACC | Service Area Equipment |

### Sample Associate Notes
- *"We do not have an ACC"*
- *"not available in store"*
- *"N/A"*

### Key Finding
**~90% of SC/DIV1-Only "Not Available" notes are ACC questions** being shown to stores without Auto Care Centers. This is a checklist filtering issue.

---

## 4. All-Format "Not Available" Analysis (9,702 notes)

These are questions sent to **all store formats** but still receive "Not Available" responses.

### Top Questions Driving N/A Notes

| Question ID | Count | Area | Topic | Root Cause |
|-------------|------:|------|-------|------------|
| Q_68 | 928 | Asset Protection | Security | **No Fuel Station** at store |
| Q_33 | 602 | Backroom | Compactor/Baler | **Non-California** stores |
| Q_223 | 593 | Store Fulfillment | InHome | **No InHome program** |
| Q_202 | 585 | Store Fulfillment | Equipment Readiness | **No InHome program** |
| Q_220 | 583 | Store Fulfillment | InHome | **No InHome program** |
| Q_221 | 582 | Store Fulfillment | InHome | **No InHome program** |
| Q_222 | 503 | Store Fulfillment | InHome | **No InHome program** |
| Q_307 | 464 | Front End | Service Desk | **NHM Service Desk** layout N/A for SC |
| Q_41 | 303 | Backroom | Fixture Cage | Not applicable |
| Q_282 | 238 | Front End | First Impressions | **No smoking area canopy** |
| Q_148 | 228 | Salesfloor | Modulars | Modular not set up |
| Q_331 | 160 | Front End | Tenant Services | **No tenant services** |
| Q_310 | 159 | Front End | Marketplace Returns | Not applicable |
| Q_100 | 144 | Fresh | Bakery | **No bakery** at store |
| Q_93 | 130 | Fresh | Meat | Meat department N/A |
| Q_48 | 129 | Backroom | Trailers | **No trailer area** |
| Q_324-326 | ~358 | Front End | Automated Kiosks | **No kiosks/vending** |

### Sample Associate Notes
- *"we are not California"* (Q_33)
- *"N/A"* (InHome questions)
- *"not applicable"* (various)
- *"we don't have the space to do it"* (Q_301)

---

## 5. Specific Action Notes Analysis (102,760 notes)

These notes describe actual actions taken by associates.

### Action Categories

| Category | Count | Percentage | Description |
|----------|------:|:----------:|-------------|
| **Uncategorized** | 70,340 | 68.5% | Unique/mixed actions |
| **Ordered** | 9,669 | 9.4% | Supplies/equipment ordered via GNFR |
| **Issues Found** | 4,631 | 4.5% | Missing, broken, damaged items |
| **Cleaned** | 4,076 | 4.0% | Cleaning/sanitization completed |
| **Verified** | 3,754 | 3.7% | Inspected/confirmed items in place |
| **Submitted** | 3,453 | 3.4% | Work orders/tickets submitted |
| **Replaced** | 2,646 | 2.6% | Items replaced/swapped |
| **Good Condition** | 2,614 | 2.5% | Confirmed item in good shape |
| **Delegation** | 2,256 | 2.2% | Assigned to team lead/coach |
| **Waiting** | 1,900 | 1.8% | Pending delivery/backorder |
| **Stocked** | 1,144 | 1.1% | Filled/restocked supplies |
| **Installed** | 985 | 1.0% | Set up/mounted equipment |
| **Repaired** | 708 | 0.7% | Fixed items on site |
| **Removed** | 701 | 0.7% | Cleared/discarded items |
| **Moved** | 402 | 0.4% | Relocated/adjusted placement |
| **Trained** | 216 | 0.2% | Coached/trained associates |

### Top Actions by Area

| Action | #1 Area | #2 Area | #3 Area |
|--------|---------|---------|---------|
| **Ordered** | Front End (2,189) | Asset Protection (1,738) | Backroom (1,617) |
| **Issues Found** | Fresh (988) | Front End (779) | Backroom (693) |
| **Cleaned** | Fresh (1,230) | Backroom (960) | Front End (823) |
| **Verified** | Fresh (774) | Front End (757) | Asset Protection (628) |

### Sample Specific Action Notes

**Ordered:**
- *"Anti Fatigue for Frontend 2 registers, ACC rubber mat ordered"*
- *"food prep mats are missing in deli, bakery and produce. order submitted through gnfr"*

**Cleaned:**
- *"Wipe down any metal/steel with dazzle after cleaning"*
- *"Vents cleaned top and bottom"*

**Submitted:**
- *"We have a ticket in for the front and rear apron to be pressure washed"*
- *"work order put in waiting for new battery testers"*

---

## 6. Recommended Question Improvements

### High Priority - Add Store Feature Filters

| Question | Area | Current Issue | Recommendation |
|----------|------|---------------|----------------|
| **All ACC Questions (Q_224-Q_267)** | ACC | 10,934 N/A notes from NHM | Add: "Does store have ACC?" → Hide if No |
| **Q_68** (Fuel Station panic buttons) | Asset Protection | 928 N/A | Add: "Does store have Fuel Station?" |
| **Q_33** (California baler keys) | Backroom | 602 N/A | Filter: Store state = California only |
| **InHome Questions (Q_202, Q_220-223)** | Store Fulfillment | ~2,846 N/A | Add: "Does store have InHome program?" |
| **Q_307** (NHM Service Desk Layout) | Front End | 464 N/A from SC | Make NHM-format only |

### Medium Priority - Clarify Department Existence

| Question | Area | Issue | Recommendation |
|----------|------|-------|----------------|
| **Q_100** (Bakery) | Fresh | 144 "no bakery" | Pre-question: "Does store have Bakery?" |
| **Q_93** (Meat) | Fresh | 130 N/A | Pre-question: "Does store have Meat dept?" |
| **Q_324-326** (Kiosks/Vending) | Front End | ~358 N/A | Add: "Does store have kiosks?" |
| **Q_331** (Tenant Services) | Front End | 160 N/A | Add: "Does store have tenant services?" |
| **Q_75** (DSL Blue Tote) | Asset Protection | 489 N/A | Add: "Is store a DSL store?" |

### Lower Priority - Clarify Question Text

| Question | Area | Issue | Suggestion |
|----------|------|-------|------------|
| **Q_41** (Fixture Cage) | Backroom | 303 N/A | Add "if applicable" or pre-filter |
| **Q_282** (Smoking Area Canopy) | Front End | 238 N/A | Add "if your store has one" |
| **Q_48** (Trailers) | Backroom | 129 N/A | Add "if your store has trailer area" |

### Estimated Impact

Implementing smart filtering could **eliminate ~17,000+ "Not Available" notes**:

| Filter | Notes Eliminated |
|--------|----------------:|
| ACC Store Feature | ~10,934 |
| InHome Program | ~2,846 |
| Fuel Station | ~928 |
| California Stores | ~602 |
| DSL Store | ~489 |
| NHM Service Desk | ~464 |
| Tenant/Kiosk Services | ~518 |
| Fresh Departments | ~274 |
| **Total** | **~17,055+** |

---

## 7. Assignment Role Patterns

### Overall Statistics

| Metric | Value |
|--------|-------|
| Total Assignments | 874,557 |
| Unique Assigners | 38,011 |
| Unique Assignees | 79,354 |
| Self-Assigned | 387,489 (44.3%) |
| Cross-Assigned | 487,068 (55.7%) |

### Store-Level Patterns

| Metric | Value |
|--------|-------|
| Total Stores | 4,102 |
| Avg Assigners per Store | 9.3 |
| Avg Assignees per Store | 19.3 |
| Avg Self-Assigned % | 45.5% |

### Top Assignees by Task Completion

| User ID | Tasks Received | Completion Rate | Stores |
|---------|---------------:|----------------:|-------:|
| htgrady | 316 | 99.4% | 1 |
| jmf00a7 | 266 | 100.0% | 1 |
| k0t00tr | 260 | 99.2% | 1 |
| j0g0r1x | 253 | 100.0% | 1 |
| w0m00se | 227 | 67.0% | 1 |
| bnfox | 220 | 89.5% | 1 |
| r0s021o | 202 | 100.0% | 1 |
| sadean | 197 | 100.0% | 1 |
| dzwrigh | 195 | 98.5% | 1 |
| cms00f3 | 193 | 97.9% | 1 |

### Key Insight
All top assigners operate within single stores, indicating **store-level management** rather than market/regional assignment patterns.

---

## 8. Assignment-to-Completion Timing

### Overall Status

| Metric | Value |
|--------|-------|
| Total Completed | 429,743 |
| Total Pending | 444,814 |
| Completion Rate | 49.1% |
| With Timing Data | 241,913 |

### Completion Time Statistics

| Percentile | Days |
|------------|-----:|
| Minimum | 0 |
| 25th Percentile | 1 |
| **Median** | **2** |
| Mean | 2.8 |
| 75th Percentile | 4 |
| 90th Percentile | 6 |
| 95th Percentile | 7 |
| Maximum | 18 |

### Speed Categories

| Category | Count | Percentage |
|----------|------:|:----------:|
| **Quick** (<1 day) | 45,637 | 18.9% |
| **Normal** (1-7 days) | 187,770 | 77.6% |
| **Slow** (8-14 days) | 8,492 | 3.5% |
| **Very Slow** (>14 days) | 14 | 0.0% |

### Time Distribution

```
0 days:  ████████████████████  45,637 (18.9%)
1 day:   █████████████████     41,345 (17.1%)
2 days:  ███████████████       37,878 (15.7%)
3 days:  ██████████████        35,241 (14.6%)
4 days:  ███████████           27,508 (11.4%)
5 days:  ████████              19,307 (8.0%)
6 days:  ███████               16,208 (6.7%)
7 days:  █████                 10,283 (4.3%)
```

### Key Insights

1. **97% of tasks complete within 1 week** - Strong performance
2. **Median 2 days** - Most tasks completed quickly
3. **19% same-day completion** - Quick turnaround for urgent items
4. **Only 3.5% take >7 days** - Few stragglers

---

## 9. Top Questions by Note Count

| Rank | Question ID | Area | Topic | Note Count |
|-----:|-------------|------|-------|----------:|
| 1 | Q_68 | Asset Protection | Security (Fuel Station) | 1,728 |
| 2 | Q_67 | Asset Protection | CCTV System | 1,175 |
| 3 | Q_202 | Store Fulfillment | InHome Equipment | 1,107 |
| 4 | Q_33 | Backroom | California Baler Keys | 1,081 |
| 5 | Q_221 | Store Fulfillment | InHome Vehicle Guide | 1,041 |
| 6 | Q_223 | Store Fulfillment | InHome Pre-trip | 1,037 |
| 7 | Q_220 | Store Fulfillment | InHome Shift Guide | 1,000 |
| 8 | Q_70 | Asset Protection | Call Boxes | 991 |
| 9 | Q_222 | Store Fulfillment | InHome Uniforms | 990 |
| 10 | Q_75 | Asset Protection | DSL Blue Tote | 889 |

---

## 10. Conclusion & Next Steps

### Summary
- **22,401 "Not Available" notes** (17.8% of all notes) represent unnecessary friction
- **ACC questions account for 49%** of all N/A notes - stores without ACC still see these
- **InHome questions generate 2,846 N/A notes** from non-InHome stores
- **California-specific questions** shown to all stores nationally

### Recommended Actions

1. **Implement Store Feature Filters**
   - ACC presence
   - Fuel Station presence
   - InHome program participation
   - State-based filtering (California)

2. **Add Department Existence Checks**
   - Bakery, Meat, Fashion departments
   - Tenant services, Kiosks

3. **Review Assignment Workflow**
   - 49.1% completion rate indicates room for improvement
   - Consider deadline reminders

4. **Leverage High Performers**
   - Multiple associates show 100% completion rates
   - Identify best practices from top performers

---

## Appendix: Data Files Generated

| File | Description |
|------|-------------|
| `notes-analysis-full.json` | Complete notes categorization |
| `not-available-format-analysis.json` | N/A notes by store format |
| `specific-action-analysis.json` | Action pattern categorization |
| `assignment-roles-analysis.json` | AssignedTo/AssignedBy patterns |
| `completion-timing-analysis.json` | Timing statistics |

---

*Report generated by Store Refresh Analysis System*  
*Contact: Store Refresh Team*

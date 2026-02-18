# Event Data Results - 5b635469-0694-4a39-bbe8-ee873d3d22b5

## Complete Data Mapping Table

| Dashboard Column | Source Column (BigQuery) | Actual Value |
|-----------------|-------------------------|--------------|
| **event_id** | event_id | 5b635469-0694-4a39-bbe8-ee873d3d22b5 |
| **message_title** | actv_title_home_ofc_nm | Your Week 2 Messages Are Here |
| **message_subject** | msg_subj_nm.array | ["Your Week 2 Messages Are Here"] |
| **message_description** | msg_txt.array | [Full HTML content - message summary] |
| **message_start_date** | msg_start_dt | 2026-02-07 |
| **message_end_date** | msg_end_dt | 2026-02-13 |
| **business_area** | bus_domain_nm | AMP-Marketing |
| **message_type** | msg_type_nm | 1 |
| **message_status** | msg_status_id | 4 |
| **message_secondary_status** | msg_scndry_status_id | 4 |
| **priority_level** | priority_status_ind | 0 |
| **impact_status** | impct_status_ind | 0 |
| **urgent_indicator** | urgent_ind | 0 |
| **store_array** | trgt_store_nbr_array | [Array of 4,387+ store numbers from "1" to "20000"] |
| **all_stores_indicator** | trgt_all_store_ind | 0 (false - specific stores targeted) |
| **geographic_region** | geo_region_cd | (empty string) |
| **walmart_year_week** | wm_yr_and_wk | 2027-2 |
| **event_date** | event_dt | 2026-02-11 |
| **fiscal_year** | EXTRACT(YEAR FROM msg_start_dt) | 2026 |
| **week_number** | EXTRACT(WEEK FROM msg_start_dt) | 5 |
| **hidden_status** | msg_hide_ind | 0 (not hidden) |
| **legal_status** | msg_leg_status_nm | NOT_REQUESTED-Megan Guerndt |
| **completed_status** | cmpltd_sts_ind | 0 (not completed) |
| **stores_uncompleted_count** | store_uncmpltd_cnt | null |
| **auto_feed_id** | auto_feed_id | null |
| **auto_feed_title** | auto_feed_title_nm | "null" (string) |
| **relative_week_number** | reltv_wk_nbr | null |
| **created_by** | create_user | (empty string) |
| **created_datetime** | create_ts | 2026-02-12 09:37:57 |
| **modified_by** | upd_user | (empty string) |
| **modified_datetime** | upd_ts | 2026-02-12 09:37:57 |
| **published_datetime** | src_rcv_ts | 2026-02-12 09:37:57 |
| **keyword_array** | msg_kw_array | "null" (string) |
| **attachment_location** | msg_atch_loc_nm | "null" (string) |
| **attachment_location_id** | atch_loc_id | 6daf0876-867e-45a7-8b59-a58300b838c4 |
| **target_user_array** | trgt_user_id_array | "0" |
| **team_id_array** | team_id_array | ["allNewTeams"] |
| **team_name_array** | team_nm_array | ["TN0"] |
| **platform_type_array** | msg_pltf_type_array | [4,0] |
| **spanish_translation** | msg_spanish_translate_ind | 0 (no Spanish translation) |
| **data_source_code** | data_src_cd | AMPCOSMOS |
| **operating_company_code** | op_cmpny_cd | WMT-US |
| **timezone_code** | tz_cd | UTC |

## Key Insights

**Event Type:** Weekly Message Summary (Week 2)  
**Target Audience:** 4,387+ Walmart stores across all divisions  
**Date Range:** February 7-13, 2026  
**Business Area:** Marketing  
**Status:** Active (Status ID: 4)  
**Created:** February 12, 2026 at 9:37 AM UTC  

**Message Content:** Weekly store communications covering:
- Food & Consumables merchant messages
- General Merchandise updates
- Operations messages (Asset Protection, Backroom, Frontend, Store Fulfillment, People)
- Department-specific action items for Valentine's Day and the Big Game

**Store Count:** Targeted to stores ranging from store #1 to store #20000 (with gaps)

## Dashboard Field Mapping

These fields should populate the dashboard as follows:

1. **Event_ID** → event_id
2. **Title** → actv_title_home_ofc_nm (message_title)
3. **FY** → fiscal_year (2026)
4. **Week** → week_number (5) or walmart_year_week (2027-2)
5. **Message Type** → msg_type_nm (currently shows "1" - needs lookup table)
6. **Activity Type** → NOT IN THIS TABLE (missing field)
7. **Status** → msg_status_id (4 = Active, needs lookup)
8. **Division** → Require join to Store dimension table
9. **Region** → Require join to Store dimension table
10. **Market** → Require join to Store dimension table
11. **Store** → trgt_store_nbr_array (array of stores)
12. **Edit Link** → NOT IN THIS TABLE (needs to be constructed)
13. **Preview Link** → NOT IN THIS TABLE (needs to be constructed)
14. **Store Count** → Calculate from array length (4,387+ stores)
15. **Verification Status** → cmpltd_sts_ind (0 = incomplete)
16. **Store Area** → NOT IN THIS TABLE (missing field)
17. **Audience** → NOT IN THIS TABLE (missing field)
18. **Business Area** → bus_domain_nm (AMP-Marketing)
19. **Click Data** → Requires separate join to Audience/Device/Time tables

## Missing Fields Identified

These dashboard requirements are **NOT available** in the AMP event table:
- **Activity Type** (e.g., "Action Required", "FYI") - Not in schema
- **Division** - Must join with Store dimension on trgt_store_nbr_array
- **Region** - Must join with Store dimension on trgt_store_nbr_array
- **Market** - Must join with Store dimension on trgt_store_nbr_array  
- **Edit Link** - Must be constructed from event_id
- **Preview Link** - Must be constructed from event_id
- **Store Area** - Not in schema
- **Audience** - Not in schema (may be in click data tables)
- **Audience Clicks** - In separate click data table
- **Device Clicks** - In separate click data table
- **Time Spent** - In separate click data table

## Next Steps

1. **Lookup Tables Needed:**
   - Message Type ID → Message Type Name (1 = ?)
   - Message Status ID → Status Name (4 = Active?)

2. **Join Required with Store Dimension:**
   ```sql
   JOIN `wmt-loc-cat-prod.catalog_location_views.businessunit_view` 
   ON store_number IN UNNEST(trgt_store_nbr_array)
   ```

3. **Click Data Join Required:**
   ```sql
   LEFT JOIN audience_clicks ON event_id = '5b635469...'
   LEFT JOIN device_clicks ON event_id = '5b635469...'
   LEFT JOIN time_spent ON event_id = '5b635469...'
   ```

4. **Link Construction:**
   - Edit Link: `https://amp.walmart.com/edit/{event_id}`
   - Preview Link: `https://amp.walmart.com/preview/{event_id}`

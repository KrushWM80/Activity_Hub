# 🗂️ Step 0: Clipper Setup & Product ID Creation

**Timeline:** 3-5 days  
**Owner:** Product Owner / Application Lead  
**Prerequisites:** None - this is the foundational step
**Next Step:** DQC Assignment (Step 1)

---

## 🎯 Overview

**Clipper** is Walmart's Enterprise Product Portfolio Management system (https://clipper.walmart.com). Before you can proceed with APM registration and compliance workflows, you must:

1. **Confirm your account** in Clipper
2. **Create a Product ID** for your application
3. **Ensure cost center is white-listed** (critical blocker if missing)

**Why Clipper First?**
- Product ID created in Clipper is required for APM registration
- APM registration depends on having an active Product ID in the system
- System propagation takes 3-5 business days, so this should be done early
- All subsequent steps reference your Clipper Product ID

---

## ✅ What You Need to Do

### Phase 1: Account Confirmation (Days 1-2)

#### 1. Access Clipper
- **URL:** https://clipper.walmart.com/people
- **Authentication:** Use your Walmart SSO credentials
- **Expected Page:** "All Entities" or "Clipper Products" dashboard

#### 2. Confirm Your Account
- [ ] Log into Clipper at https://clipper.walmart.com/people
- [ ] Verify your profile is complete
- [ ] Check that your account status shows "Active"

#### 3. **CRITICAL:** Verify Cost Center White List
- [ ] Contact your Finance/Cost Center owner
- [ ] Confirm your cost center is added to Clipper's white list
- [ ] **If not white-listed:** This blocks account confirmation - must be resolved first
- [ ] Reconfirm account after white-list addition

**⚠️ Common Blocker:** Cost Center white-list requirement is NOT always documented. If you cannot confirm your account, verify white-list status before proceeding.

---

### Phase 2: Create Product ID (Days 2-3)

#### 1. Navigate to Product Creation
- [ ] In Clipper, go to **Products** → **All Products**
- [ ] Click **Create Product** or similar option
- [ ] Select appropriate product category

#### 2. Complete Product Registration Form
- [ ] **Product Name:** Activity Hub (or your product name)
- [ ] **Business Group:** Select applicable group (e.g., "Business Groups - Walmart US")
- [ ] **Pillar:** Select applicable pillar (e.g., "Store Support")
- [ ] **Description:** Brief description of application purpose
- [ ] **Assign Engineering Manager:** (e.g., Kendall Rush)
- [ ] **Assign Product Manager:** (e.g., Kendall Rush)

#### 3. Submit Product Creation
- [ ] Review all information
- [ ] Submit form
- [ ] **Save the Product ID** (this is critical for next steps)

#### Expected Outcome:
- ✅ Product ID created in Clipper
- ✅ Product page accessible at: `https://clipper.walmart.com/products/entity/product/[PRODUCT_ID]`
- ⏳ System propagation: 3-5 business days for availability in other systems

---

## 📊 Progress Tracking

### Activity Hub Example (Completed January 2026)

| Step | Status | Details | Date |
|------|--------|---------|------|
| **Account Confirmation** | ✅ Complete | Clipper account confirmed after cost center white-list addition | Jan 2026 |
| **Cost Center White List** | ✅ Resolved | Cost center added to white list - this was the critical blocker | Jan 2026 |
| **Product ID Creation** | ✅ Complete | Product ID: 6426 | Jan 2026 |
| **Product URL** | ✅ Created | https://clipper.walmart.com/products/entity/product/6426 | Jan 2026 |
| **System Propagation** | 🔄 In Progress | Awaiting 3-5 day system update for APM availability | Jan 12-17, 2026 |

---

## 🔗 Key Information

### Your Product Details
- **Product Name:** Activity Hub
- **Product ID:** 6426
- **Product URL:** https://clipper.walmart.com/products/entity/product/6426
- **Business Group:** Business Groups - Walmart US
- **Engineering Manager:** Kendall Rush
- **Product Manager:** Kendall Rush
- **DQC:** Kevin Tadda

---

## ⚠️ Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| **Cannot log into Clipper** | SSO authentication issue | Verify Walmart credentials; try incognito mode; contact IT support |
| **Account confirms but no dashboard** | Cost center not white-listed | Contact Finance/Cost Center owner; request white-list addition |
| **Product creation fails** | Missing required fields | Verify all required fields are complete; check Business Group/Pillar selections |
| **Product ID created but not in APM** | System propagation delay | Wait 3-5 business days; refresh APM system; contact APM team if >5 days |
| **Cannot find Products section** | UI navigation issue | Ensure you're in "Products" section (left sidebar); check for "All Products" tab |

---

## 📝 Next Steps

### After Product ID Creation:

1. **Document Product ID**
   - Save: Product ID: 6426
   - Save: Product URL: https://clipper.walmart.com/products/entity/product/6426
   - Share with team leads

2. **Wait for System Propagation** (3-5 business days)
   - Product ID will appear in APM registration system
   - Product ID will be available in downstream processes

3. **Proceed to Step 1: DQC Assignment**
   - Contact Kevin Tadda (DQC for Walmart US)
   - Inform him of your Product ID
   - Coordinate on Team Rosters request

---

## 🔗 References

- **Clipper Main Site:** https://clipper.walmart.com
- **Clipper Products Dashboard:** https://clipper.walmart.com/products
- **Clipper People Management:** https://clipper.walmart.com/people
- **DQC Network List:** https://walmart.sharepoint.com/sites/dqc-network
- **Related Process:** [Step 1: DQC Assignment](../01-DQC_Assignment/README.md)
- **Related Process:** [Step 3: APM Setup](../03-APM_Setup/README.md)

---

## 📞 Contacts & Support

| Role | Name | Purpose |
|------|------|---------|
| **DQC** | Kevin Tadda | Data Quality Champion for Walmart US pillar |
| **Clipper Support** | IT Service Portal | Technical issues with Clipper access/functionality |
| **Cost Center Owner** | [Your Finance Lead] | Cost center white-list authorization |
| **Product Manager** | Kendall Rush | Product ID management and coordination |

---

## ✅ Completion Checklist

- [ ] Accessed Clipper (https://clipper.walmart.com)
- [ ] Confirmed account status (Active)
- [ ] Verified cost center white-list status
- [ ] Created Product ID in Clipper
- [ ] Documented Product ID (6426)
- [ ] Saved Product URL
- [ ] Shared Product ID with team
- [ ] Waiting for system propagation (3-5 days)
- [ ] Ready to proceed to Step 1: DQC Assignment

**Status:** ✅ COMPLETE - Awaiting system propagation  
**Completed:** January 12, 2026  
**Propagation Window:** January 12-17, 2026

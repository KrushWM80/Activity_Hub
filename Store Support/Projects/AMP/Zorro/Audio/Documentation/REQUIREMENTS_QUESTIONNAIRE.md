# Audio Template Requirements Questionnaire

*Use this form when a user requests a new Audio Template for Zorro*

---

## SECTION A: Template Identification

**Q1. Template Name**
```
What should this template be called?
(e.g., "Weekly Messages Audio Template - Summarized", "Daily Store Briefing", "Monthly Compliance Update")

Answer: _________________________________
```

**Q2. Template Type**
```
Classification type:
- [ ] Weekly
- [ ] Bi-Weekly
- [ ] Monthly
- [ ] Daily
- [ ] Quarterly
- [ ] Other: _______________________

Answer: _________________________________
```

**Q3. Recurring Frequency**
```
How often will this template be used/updated?
- [ ] Once per week (52/year)
- [ ] Once every 2 weeks (26/year)
- [ ] Once per month (12/year)
- [ ] Multiple times per week
- [ ] Daily
- [ ] Other: _______________________

Answer: _________________________________
```

---

## SECTION B: Content Structure

**Q4. Opening/Intro Text**
```
What should the opening say?

Example formats:
- "Hello! Your Week [X] Weekly Messages are Here!"
- "Good morning, this is your daily store briefing"
- "Welcome to this month's compliance update"

Proposed Text: _________________________________
              _________________________________
              _________________________________

Variables needed: [ ] Week/Month/Date [ ] Store Number [ ] Other: ______
```

**Q5. Main Content Organization**
```
How should the main content be structured?

Number of sections: ____

Section Names & Order:
1. _________________________________
2. _________________________________
3. _________________________________
4. _________________________________
5. _________________________________

Will each section contain:
- [ ] Titles only
- [ ] Titles + brief descriptions  
- [ ] Titles + detailed content
- [ ] Other: _______________________

Typical content length per section: ______ words / ______ minutes
```

**Q6. Closing/Outro Text**
```
What should the closing say?

Example formats:
- "That's your Week [X] Weekly Messages, Have a Great Week!"
- "Thank you for tuning in to today's briefing"
- "See you next time!"

Proposed Text: _________________________________
              _________________________________
              _________________________________
```

---

## SECTION C: Content Rules

**Q7. Content Formatting Guidelines**
```
How should content be formatted for audio reading?

- [ ] Full sentences (natural speech)
- [ ] Bullet points (concise)
- [ ] Numbered lists
- [ ] Mixed format

Abbreviations:
- [ ] Spell out all (A-M-P → "A M P")
- [ ] Natural reading (AMP → "AMP")
- [ ] Context-dependent

Examples of expected content style:
_________________________________________________________________
_________________________________________________________________
```

**Q8. Content Source**
```
Where will content come from?

Primary Source:
- [ ] AMP Activities/Messages
- [ ] Custom written content
- [ ] Database queries
- [ ] Hybrid (mix of above)
- [ ] Other: _______________________

Will content be:
- [ ] Pulled automatically (API/query)
- [ ] Manually prepared
- [ ] Semi-automated (template + manual updates)
```

**Q9. Content Selection Criteria**
```
How is content selected/filtered for this template?

Filtering Rules:
- By Department(s): [ ] Yes [ ] No → Which? _____________
- By Status/Type: [ ] Yes [ ] No → Which? _____________
- By Activity Tag: [ ] Yes [ ] No → Which? _____________
- By Time Period: [ ] Yes [ ] No → Which? _____________
- All activities (no filter): [ ] Yes

Example: "Pull all Merchant Messages from Week [X], status='Active'"
_________________________________________________________________
_________________________________________________________________
```

---

## SECTION D: Voice & Narration

**Q10. Voice(s) Needed**
```
Which voice(s) for narration?

- [ ] David (Male) only
- [ ] Zira (Female) only
- [ ] Both (David & Zira versions)
- [ ] Multiple narrators (different people for different sections)
- [ ] Other: _______________________

Available voices:
- Microsoft David Desktop (Male, professional)
- Microsoft Zira Desktop (Female, energetic)
```

**Q11. Speech Rate Preference**
```
How fast/slow should narration be?

- [ ] Slower (easier to follow, rate: -2)
- [ ] Normal (standard, rate: 0)
- [ ] Faster (efficient, rate: +2)
- [ ] User comment: _______________________

Typical duration for this template: _____ minutes
```

**Q12. Audio Quality**
```
Audio quality requirements:

- [ ] Standard (44.1 kHz, good for dashboard/web)
- [ ] Enhanced (44.1 kHz, higher bitrate, richer sound)
- [ ] Mobile-optimized (lower file size)

Target file size: ______ MB
Playback context: [ ] Dashboard [ ] Vimeo [ ] Email [ ] Download [ ] Other

Volume preference: [ ] Standard [ ] Enhanced [ ] Normalized
```

---

## SECTION E: Visual Branding

**Q13. Thumbnail Image Needed**
```
Does this need a custom thumbnail/cover image?

- [ ] Yes (unique thumbnail for template)
- [ ] No (audio only)
- [ ] Yes, but reuse existing: __________________

Current example: ___________________________
```

**Q14. Thumbnail Design (if needed)**
```
Thumbnail specifications:

Background:
- [ ] Color: ___________________________
- [ ] Image/Pattern: ___________________________
- [ ] Gradient: ___________________________

Text Elements:
- [ ] Template name: [ ] Static [ ] Variable
- [ ] Current date/week: [ ] Yes [ ] No
- [ ] "Listen Now" label: [ ] Yes [ ] No
- [ ] Custom text: _______________________

Icon/Logo:
- [ ] Microphone icon: [ ] Yes [ ] No
- [ ] Organization logo: [ ] Yes [ ] No
- [ ] Custom icon: _______________________

Brand Guidelines to Follow:
- Color palette: [ ] Yes [ ] No
- Font family: [ ] Yes [ ] No
- Logo placement: [ ] Yes [ ] No
- Other: _________________________________

Reference: Does this match existing Zorro branding?
[ ] Yes - use existing brand assets
[ ] No - create new design
[ ] Unclear - need design review

Thumbnail Dimensions: 1920x1080 (standard Vimeo)
```

---

## SECTION F: Distribution Requirements

**Q15. Vimeo Upload**
```
Does this content go to Vimeo?

- [ ] Yes (publish to Vimeo channel)
- [ ] No (dashboard only)
- [ ] Conditional (depends on content)

If yes to Vimeo:
- Channel/Project: _______________________
- Playlist: _______________________
- Private/Public: [ ] Private [ ] Public [ ] Unlisted
- Share settings: [ ] Anyone [ ] Team only [ ] Other

Vimeo Optimization:
- [ ] Add thumbnail overlay
- [ ] H.264 codec
- [ ] AAC audio (128k)
- [ ] yuv420p (pixel format)
All standard requirements: [ ] Yes [ ] No
```

**Q16. Other Distribution Channels**
```
Besides Vimeo, where will this be distributed?

- [ ] Dashboard/Web player
- [ ] Email embed
- [ ] Social media
- [ ] Download link
- [ ] Podcast feed
- [ ] Teams/Slack
- [ ] Other: _______________________

File format needs:
- MP4 (primary): [ ] Yes
- WAV (archive): [ ] Yes [ ] No
- Multiple bitrates: [ ] Yes [ ] No
```

**Q17. Dashboard Hosting**
```
Will this be hosted on Zorro dashboard?

- [ ] Yes (public, anyone can see)
- [ ] Yes (private, authenticated users)
- [ ] Yes (temporary, auto-expire after X days)
- [ ] No (Vimeo only)
- [ ] No (download only)

If dashboard hosting:
- Typical lifespan on dashboard: _____ weeks
- Auto-cleanup needed: [ ] Yes [ ] No
- Archive old versions: [ ] Yes [ ] No
```

---

## SECTION G: Variations & Reusability

**Q18. Lifecycle Variations**
```
How many times will this template be populated/used over its lifetime?

Example: Weekly Messages = 52 variations per year

- [ ] One-time use (no variations)
- [ ] Quarterly (4/year)
- [ ] Monthly (12/year)
- [ ] Weekly (52/year)
- [ ] Daily (365/year)
- [ ] Custom frequency: _____ per year
- [ ] Indefinite (ongoing series)

Total expected variations: ______
Time period covered: _____ to _____
```

**Q19. Content Change Frequency**
```
How much will content change between variations?

- [ ] Completely different each time (1% reuse)
- [ ] Mostly different, same structure (20% reuse)
- [ ] Mix of static and dynamic content (50% reuse)
- [ ] Minor updates only (80% reuse)
- [ ] Static - no changes needed (100% reuse)

What stays the same?
- [ ] Intro/Outro
- [ ] Section structure
- [ ] Section names
- [ ] Branding/Thumbnail
- [ ] Other: _______________________

What changes?
- [ ] Main content
- [ ] Specific data points
- [ ] Dates/week numbers
- [ ] Featured items
- [ ] Other: _______________________
```

**Q20. Voice Consistency**
```
Will voice remain the same across variations?

- [ ] Yes, same voice every time (recommend: Zira)
- [ ] No, rotate voices (David ↔ Zira)
- [ ] Yes, but with variations (same voice, different settings)
- [ ] Varies by content type

Voice assignment:
- Primary voice: [ ] David [ ] Zira [ ] Other
- Backup voice (if primary unavailable): [ ] David [ ] Zira [ ] None
```

---

## SUMMARY & SIGN-OFF

**Template Overview:**
```
Name: _________________________________
Type: ________________________________
Frequency: _____ per _______
Expected variations: _____ over _____ [time period]
Primary voice(s): _______________________
Vimeo required: [ ] Yes [ ] No
```

**Additional Requirements/Notes:**
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

**Approval:**
```
Requested by: _________________________ Date: __________
Reviewed by: _________________________ Date: __________
Approved by: _________________________ Date: __________
```

**Next Steps:**
```
[ ] 1. Design script template
[ ] 2. Create sample content
[ ] 3. Generate sample audio (voice test)
[ ] 4. Present to stakeholder for approval
[ ] 5. Create thumbnail (if needed)
[ ] 6. Generate all output versions
[ ] 7. Create usage/generation guide
[ ] 8. Move to Templates folder for reuse
[ ] 9. Document in TEMPLATE_LIBRARY.md
[ ] 10. Archive for production use
```

---

**Form Version**: 1.0  
**Last Updated**: February 27, 2026  
**Status**: Active - Ready for use in Zorro platform

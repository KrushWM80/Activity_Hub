# Audio Process Flow Diagrams - Zorro

## Diagram 1: Complete Two-Process Comparison

```mermaid
graph TB
    Start{User Request: Create Audio} -->|One-time use| Standard["<b>STANDARD AUDIO PROCESS</b><br/>Convert AMP Activity to Audio"]
    Start -->|Recurring Series| Template["<b>AUDIO TEMPLATE PROCESS</b><br/>Create Reusable Template"]
    
    Standard --> S1["1. Select AMP Activity/Message"]
    S1 --> S2["2. Choose Voice<br/>David or Zira"]
    S2 --> S3["3. Select Options<br/>Vimeo? Quality?"]
    S3 --> S4["4. Generate WAV<br/>PowerShell SAPI5"]
    S4 --> S5["5. Convert WAV → MP4"]
    S5 --> S6["6. Convert MP4 → Vimeo MP4<br/>H.264 + AAC + Thumbnail"]
    S6 --> S7["✅ OUTPUT: Ready-to-Use<br/>MP4 File"]
    
    Template --> T1["1. Send Requirements<br/>Questionnaire"]
    T1 --> T2["2. Gather Content Details<br/>Structure, Frequency, Content Rules"]
    T2 --> T3["3. Design Script Template<br/>Intro + Sections + Outro"]
    T3 --> T4["4. Create Thumbnail<br/>Brand Assets"]
    T4 --> T5["5. Generate Sample WAV<br/>Populate with demo content"]
    T5 --> T6["6. Convert to MP4<br/>& Vimeo-Compatible"]
    T6 --> T7["7. Present to User<br/>Approve Sample Output"]
    T7 --> T8{Approved?}
    T8 -->|No| T3
    T8 -->|Yes| T9["8. Create Generation Script<br/>Reusable Python template"]
    T9 --> T10["9. Document Usage Guide<br/>How to populate for future uses"]
    T10 --> T11["✅ OUTPUT: Reusable Template<br/>+ Generation Script"]
    
    S7 --> End1["📦 Deliver to User<br/>Vimeo Link / Dashboard"]
    T11 --> End2["📦 Template Ready for Production<br/>Use 50+ times per year"]
    
    style Start fill:#e1f5ff
    style Standard fill:#fff3e0
    style Template fill:#f3e5f5
    style S7 fill:#c8e6c9
    style T11 fill:#c8e6c9
    style End1 fill:#a5d6a7
    style End2 fill:#a5d6a7
```

---

## Diagram 2: Standard Audio Process - Detailed

```mermaid
graph LR
    A["AMP Activity/<br/>Message Body"] --> B["Select<br/>Voice"]
    B --> C["PowerShell SAPI5<br/>TTS"]
    C --> D["Generate<br/>WAV"]
    D --> E["FFmpeg<br/>Convert"]
    E --> F["Standard<br/>MP4"]
    F --> G["Vimeo<br/>Conversion"]
    G --> H["Vimeo-Compatible<br/>MP4<br/>H.264 Video<br/>AAC Audio<br/>Thumbnail Overlay"]
    H --> I["📦 Delivery"]
    I --> J["Dashboard<br/>or Vimeo"]
    
    B --> B1["David or Zira"]
    C --> C1["Rate: -2<br/>Volume: 100%"]
    E --> E1["libx264<br/>128k AAC<br/>yuv420p"]
    G --> G1["+ merch_msg_thumbnail.jpeg<br/>1920x1080px"]
    
    style A fill:#e3f2fd
    style D fill:#fff9c4
    style F fill:#fff9c4
    style H fill:#c8e6c9
    style J fill:#a5d6a7
```

---

## Diagram 3: Audio Template Creation Process - Detailed

```mermaid
graph TB
    A["User Requests<br/>New Template"] --> B["Send Requirements<br/>Questionnaire"]
    B --> C["Gather:<br/>Name | Type | Frequency<br/>Content Structure<br/>Voice Requirements<br/>Branding Needs<br/>Distribution Rules"]
    C --> D["Design<br/>Script Template"]
    D --> E["Create Frame<br/>Intro placeholder<br/>Content sections<br/>Outro placeholder"]
    E --> F["Generate<br/>Thumbnail"]
    F --> G["Populate with<br/>Sample Content"]
    G --> H["Generate Sample<br/>WAV Files"]
    H --> I["Multiple Voices?"]
    I -->|Yes| I1["Generate David"]
    I -->|Yes| I2["Generate Zira"]
    I -->|No| I3["Single Voice"]
    I1 --> J["Convert All to<br/>Standard MP4"]
    I2 --> J
    I3 --> J
    J --> K["Vimeo<br/>Conversion"]
    K --> L["Present<br/>Sample to User"]
    L --> M{Approved?}
    M -->|Revise| D
    M -->|Approved| N["Create Generation<br/>Script"]
    N --> O["Python Template<br/>Reusable across<br/>variations"]
    O --> P["Document<br/>Usage Guide"]
    P --> Q["How to populate<br/>How to generate<br/>Output formats"]
    Q --> R["Archive Template"]
    R --> S["Templates/<br/>template-name/<br/>folder"]
    S --> T["✅ Ready for<br/>Production Use<br/>50+ variations"]
    
    style A fill:#f3e5f5
    style C fill:#f3e5f5
    style M fill:#ffebee
    style T fill:#c8e6c9
```

---

## Diagram 4: Decision Tree - Which Process to Use?

```mermaid
graph TD
    Q1{User Needs<br/>Audio Content} -->|YES| Q2{Will this be<br/>used multiple times?}
    Q1 -->|NO| NO["Not an audio project"]
    
    Q2 -->|No - One time only| Q3{Have content<br/>already?}
    Q2 -->|Yes - Recurring| Q4{Is pattern<br/>standardized?}
    
    Q3 -->|Yes| STANDARD1["✅ STANDARD<br/>PROCESS<br/>Convert AMP to Audio"]
    Q3 -->|No| STANDARD2["✅ STANDARD<br/>PROCESS<br/>Prepare content first<br/>then convert"]
    
    Q4 -->|Yes - Same<br/>structure each time| TEMPLATE["✅ TEMPLATE<br/>PROCESS<br/>Create reusable<br/>template"]
    Q4 -->|No - Different<br/>each time| STANDARD3["✅ STANDARD<br/>PROCESS<br/>Generate individually"]
    
    STANDARD1 --> TIME1["⏱️ 10-15 min"]
    STANDARD2 --> TIME2["⏱️ 15-20 min"]
    STANDARD3 --> TIME3["⏱️ 10-15 min per"]
    TEMPLATE --> TIME4["⏱️ 2-4 hours<br/>first time<br/>then 10-15 min<br/>each use"]
    
    style Q1 fill:#e1f5ff
    style Q2 fill:#e1f5ff
    style Q3 fill:#e1f5ff
    style Q4 fill:#e1f5ff
    style STANDARD1 fill:#fff3e0
    style STANDARD2 fill:#fff3e0
    style STANDARD3 fill:#fff3e0
    style TEMPLATE fill:#f3e5f5
    style TIME1 fill:#c8e6c9
    style TIME2 fill:#c8e6c9
    style TIME3 fill:#c8e6c9
    style TIME4 fill:#c8e6c9
```

---

## Diagram 5: File Organization in Zorro

```
Store Support/Projects/AMP/Zorro/
│
├── 📁 Audio/ ━━━━━ [ALL AUDIO PRODUCTION WORK]
│   │
│   ├── 📁 Templates/ ━━━━━ [REUSABLE TEMPLATES]
│   │   ├── 📁 weekly-messages-summarized/
│   │   │   ├── generate_weekly_messages.py
│   │   │   ├── script_template.md
│   │   │   ├── requirements.txt
│   │   │   └── thumbnail.jpeg
│   │   │
│   │   ├── 📁 [other-templates]/
│   │   └── TEMPLATE_LIBRARY.md
│   │
│   ├── 📁 Scripts/ ━━━━━ [CORE UTILITIES]
│   │   ├── generate_both_voices.py
│   │   ├── generate_summarized_final_zira.py
│   │   ├── convert_wav_to_mp4_installer.py
│   │   ├── convert_standard_to_vimeo.py
│   │   ├── create_audio_thumbnail.py
│   │   └── podcast_server.py
│   │
│   ├── 📁 Output/ ━━━━━ [GENERATED FILES]
│   │   ├── 📁 podcasts/
│   │   │   ├── *.mp4 [Final audio files]
│   │   │   └── .jpeg [Thumbnails]
│   │   │
│   │   └── 📁 archive/
│   │       └── [Older versions]
│   │
│   └── 📁 Documentation/ ━━━━━ [KNOWLEDGE BASE]
│       ├── AUDIO_PROCESS_GUIDE.md ⬅️ THIS FILE
│       ├── REQUIREMENTS_QUESTIONNAIRE.md
│       ├── TEMPLATE_LIBRARY.md
│       └── GENERATION_SCRIPTS.md
│
└── [Other Zorro folders...]
```

---

## Diagram 6: Template Lifecycle - Weekly Messages Example

```mermaid
timeline
    title Weekly Messages Audio Template - Lifecycle
    
    section Month 1 (February)
    Feb 27 : Template Created : Requirements gathered : Script designed : Sample generated : Approved
    
    section Weeks 5-8 (March)
    Week 5 : Populate content : Generate : Upload to Vimeo : Deploy to dashboard
    Week 6 : Populate content : Generate : Upload to Vimeo : Deploy to dashboard
    Week 7 : Populate content : Generate : Upload to Vimeo : Deploy to dashboard
    Week 8 : Populate content : Generate : Upload to Vimeo : Deploy to dashboard
    
    section Weeks 9-52 (April - December)
    Ongoing : Repeat process : Each week : Consistent quality : Standard format
    
    section Year 2
    52 more weeks : Same template : Same voice : Same branding : Different content
    
    section Year 3+
    Continuous : Template still in use : May need minor updates : Reusable for years
```


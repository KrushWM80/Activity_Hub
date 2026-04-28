# Spark Logo in Emails - Implementation Guide

## Overview
The Walmart Spark logo must be embedded in all Activity Hub emails using **CID (Content-ID) MIME attachment**, not base64 data URIs. This is the only method that works reliably across all email clients including Outlook.

## Why NOT Data URIs
```html
<!-- ❌ DO NOT USE - Blocked by Outlook, Gmail, and most email clients -->
<img src="data:image/png;base64,iVBORw0KGgo..." />
```
- **Outlook** blocks `data:` URIs entirely — renders as broken image or placeholder
- **Gmail** strips `data:` URIs from HTML
- **Apple Mail** sometimes works, but inconsistent
- Data URIs bloat the HTML body and can trigger spam filters

## Correct Method: CID Attachment

### Step 1: HTML Reference
Use `cid:spark_logo` as the image `src`:
```html
<img src="cid:spark_logo" width="48" height="48" alt="Spark" style="display:block;" />
```

### Step 2: MIME Structure
Build the email with `MIMEMultipart('related')` so the inline image travels with the HTML:

```python
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# 1. Outer container must be 'related' for inline images
msg = MIMEMultipart('related')
msg['From'] = sender
msg['To'] = recipient
msg['Subject'] = subject

# 2. HTML goes inside an 'alternative' sub-part
msg_alt = MIMEMultipart('alternative')
msg_alt.attach(MIMEText(html_body, 'html', 'utf-8'))
msg.attach(msg_alt)

# 3. Attach the PNG with Content-ID matching the cid: in HTML
with open('Interface/Spark_Blank.png', 'rb') as f:
    logo_data = f.read()
logo_img = MIMEImage(logo_data, _subtype='png')
logo_img.add_header('Content-ID', '<spark_logo>')          # Must match cid:spark_logo
logo_img.add_header('Content-Disposition', 'inline', filename='Spark_Blank.png')
msg.attach(logo_img)
```

### Step 3: MIME Hierarchy
```
MIMEMultipart('related')
├── MIMEMultipart('alternative')
│   └── MIMEText(html, 'html')      ← HTML body with <img src="cid:spark_logo">
└── MIMEImage(png_bytes, 'png')      ← Spark_Blank.png with Content-ID: <spark_logo>
```

## Logo File Details

| Property | Value |
|----------|-------|
| **File** | `Interface/Spark_Blank.png` |
| **Also at** | `Platform/Design/walmart-spark-logo.png` |
| **Format** | PNG with transparency |
| **Size** | 7,446 bytes |
| **Dimensions** | 300 x 300 px (source) |
| **Display Size** | 48 x 48 px in email header |
| **PNG Signature** | `89504e470d0a1a0a` (valid) |

## Email Header Template
```html
<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td bgcolor="#004C91" style="background-color:#004C91; padding: 24px 30px;">
    <table cellpadding="0" cellspacing="0" border="0">
    <tr>
    <td style="padding-right: 15px; vertical-align: middle;">
        <img src="cid:spark_logo" width="48" height="48" alt="Spark" style="display:block;" />
    </td>
    <td style="vertical-align: middle;">
        <div style="color: white; font-size: 26px; font-weight: 700;">Projects</div>
        <div style="color: #cccccc; font-size: 13px; margin-top: 2px;">by Activity Hub</div>
    </td>
    </tr>
    </table>
</td>
</tr>
</table>
```

## Helper Functions
Located in `Interface/send_projects_emails.py`:

| Function | Purpose |
|----------|---------|
| `_get_spark_logo_path()` | Finds PNG across 4 fallback paths |
| `get_spark_logo_base64()` | Returns base64 string (used for sample HTML files only) |
| `get_spark_logo_html(size)` | Returns `<img src="cid:spark_logo" ...>` tag |
| `send_smtp_email()` | Attaches PNG as CID inline image |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "W" shows instead of logo | HTML has hardcoded `W` placeholder | Use `get_spark_logo_html("48")` |
| Broken image icon | `data:` URI blocked by email client | Switch to CID attachment |
| Logo missing entirely | PNG file not found | Check `_get_spark_logo_path()` logs |
| Logo shows as attachment | `Content-Disposition` set to `attachment` | Must be `inline` |
| Logo appears twice | Missing `Content-ID` header | Ensure `<spark_logo>` with angle brackets |

## Testing
1. Run: `.venv\Scripts\python Interface\send_projects_emails.py`
2. Check inbox for Spark logo in email header
3. Verify across: Outlook desktop, Outlook web, mobile

---
*Last Updated: April 28, 2026*
*Issue Resolved: Hardcoded "W" placeholder + data URI blocked by Outlook → CID attachment*

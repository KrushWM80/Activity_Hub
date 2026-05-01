Add-Type -AssemblyName System.Runtime.InteropServices
$outlook = New-Object -ComObject Outlook.Application
$namespace = $outlook.GetNamespace('MAPI')

# Get the default Drafts folder (3 = olFolderDrafts)
$draftsFolder = $namespace.GetDefaultFolder(3)

# Create a new mail item
$mail = $draftsFolder.Items.Add(0)  # 0 = olMailItem

# Set email properties
$mail.Subject = 'CORRECTION: Manager Information in PayCycle 07 Email - May 1, 2026'
$mail.To = '[DC Leadership Distribution - Draft]'

# HTML Body content
$htmlBody = @'
<html>
<head>
<style>
body { font-family: Calibri, sans-serif; }
table { border-collapse: collapse; width: 100%; margin: 15px 0; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
th { background-color: #f2f2f2; }
h2 { color: #c00; }
h3 { color: #333; margin-top: 15px; }
.correct { color: green; font-weight: bold; }
.wrong { color: red; }
code { background: #f4f4f4; padding: 2px 5px; }
</style>
</head>
<body>

<p><strong>RE: Your email from May 1, 2026 with subject "Store Manager Changes - PayCycle 07"</strong></p>

<h2>CORRECTION NOTICE</h2>

<p>The manager information and store locations in that email were <strong>INACCURATE</strong>. Below are the <strong>correct details</strong> from our authoritative ELM system:</p>

<h3>CORRECTED STORE MANAGER INFORMATION</h3>

<table>
<tr>
<th>Store</th>
<th>Location</th>
<th class="wrong">Wrong Data Sent</th>
<th class="correct">Correct Manager</th>
<th>City, State</th>
<th>ELM Link</th>
</tr>
<tr>
<td>100</td>
<td>Bentonville S Walton Blvd</td>
<td class="wrong">JAMES RICHARDSON</td>
<td class="correct">KACEY WARD</td>
<td>Bentonville, AR</td>
<td><a href="https://elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com/search?business_unit_nbr=100">View in ELM</a></td>
</tr>
<tr>
<td>103</td>
<td>Shawnee</td>
<td class="wrong">LISA ANDERSON</td>
<td class="correct">LAURA GREEN</td>
<td>Shawnee, OK</td>
<td><a href="https://elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com/search?business_unit_nbr=103">View in ELM</a></td>
</tr>
<tr>
<td>121</td>
<td>Okmulgee</td>
<td class="wrong">PATRICIA LOPEZ</td>
<td class="correct">RUSSELL MOORE</td>
<td>Okmulgee, OK</td>
<td><a href="https://elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com/search?business_unit_nbr=121">View in ELM</a></td>
</tr>
<tr>
<td>130</td>
<td>Muskogee</td>
<td class="wrong">DAVID BROWN</td>
<td class="correct">PHILLIP CRUMBLISS</td>
<td>Muskogee, OK</td>
<td><a href="https://elmsearchui.prod.elm-ui.telocmdm.prod.walmart.com/search?business_unit_nbr=130">View in ELM</a></td>
</tr>
</table>

<h3>WHAT HAPPENED</h3>

<p>Our system reused a 6-day-old <strong>synthetic test snapshot</strong> from April 29 without validating the date:</p>
<ul>
<li>April 29: Created synthetic test data with fake manager changes</li>
<li>May 1: System reused cached file without checking if it was current</li>
<li>Result: Fake data sent to DC leadership</li>
</ul>

<h3>ROOT CAUSE AND FIXES</h3>

<p><strong>The Bug:</strong> The system checked if the file exists but never validated if it was today date.</p>

<p><strong>Immediate Fix:</strong></p>
<ul>
<li>Delete all cached snapshots before fetching</li>
<li>Force fresh data fetch every time</li>
<li>Never reuse stale cache</li>
</ul>

<p><strong>Long-Term Solution:</strong></p>
<ul>
<li>Replaced fragile web scraper with direct ELM BigQuery API</li>
<li>Added UTC timestamp to every snapshot</li>
<li>Complete audit trail metadata</li>
</ul>

<p><strong>Incident Reference:</strong> 2026-05-01-ELM-5645-LOCATIONS (May 1, 2026 19:53:10 UTC)</p>

<h3>REAL PAYCYCLE 07 DATA</h3>

<p>For PayCycle 07 (May 1-14, 2026):</p>
<ul>
<li><strong>Manager Changes Detected:</strong> 0 (No actual changes)</li>
<li><strong>Data Source:</strong> ELM BigQuery (verified, production system)</li>
<li><strong>Validation:</strong> Compared April 17 vs May 1 equals 0 changes (expected for 14-day window)</li>
</ul>

<p><strong>Action Required:</strong> Please disregard the previous email. The stores listed above show the CORRECT managers per ELM as of May 1, 2026.</p>

<p>---</p>

<p>ATC Team Support<br/>
atcteamsupport@walmart.com</p>

</body>
</html>
'@

$mail.HTMLBody = $htmlBody

# Save the draft (do not send)
$mail.Save()

Write-Host ''
Write-Host '====================================================================' -ForegroundColor Cyan
Write-Host 'SUCCESS: Draft email created in Outlook Drafts' -ForegroundColor Green
Write-Host '====================================================================' -ForegroundColor Cyan
Write-Host "Subject: $($mail.Subject)" -ForegroundColor White
Write-Host "To: $($mail.To)" -ForegroundColor White
Write-Host "Status: DRAFT (Not sent - Ready for review)" -ForegroundColor Yellow
Write-Host ''
Write-Host 'The email is in your Outlook Drafts folder.' -ForegroundColor Green
Write-Host 'You can open it, review, modify, and send when ready.' -ForegroundColor Green
Write-Host ''

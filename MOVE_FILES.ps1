#!/usr/bin/env powershell
# Activity Hub - File Reorganization Script

param(
    [switch]$Confirm = $true,
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"
Push-Location "C:\Users\krush\OneDrive - Walmart Inc\Documents\VSCode\Activity_Hub"

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  ACTIVITY HUB - FILE REORGANIZATION SCRIPT" -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "  Mode: DRY RUN (Preview only)" -ForegroundColor Yellow
} else {
    Write-Host "  Mode: LIVE MODE (Files will be moved)" -ForegroundColor Red
}
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# File mapping data
$fileMappings = @(
    @{ Files = @("activate_voices.py","check_jenny_status.py","find_narrator_jenny.py","install_voices_guide.py","list_exact_voices.py","register_narrator_voices.py","troubleshoot_voices.py","unstick_narrator_voices.py","NARRATOR_VOICES_HELP.py"); Dest = "Store Support\Projects\AMP\Zorro\Audio\Scripts\voice_management"; Category = "Zorro - Voices" },
    @{ Files = @("generate_both_voices.py","generate_jenny_guy.py","generate_podcast_final.py","generate_podcast_mp3_edition.py","generate_podcast_natural.py","generate_podcast_sapi5.py","generate_podcast_simple.py","generate_podcast_stable.py","generate_podcast_windows_tts.py","generate_production_podcast.py","generate_professional_tts_podcast.py","generate_tts_podcast_pyttsx3.py","generate_available_voices.py"); Dest = "Store Support\Projects\AMP\Zorro\Audio\Scripts\generation"; Category = "Zorro - Generation" },
    @{ Files = @("extract_html_from_text.py"); Dest = "Store Support\Projects\AMP\Zorro\Audio\Scripts\conversion"; Category = "Zorro - Conversion" },
    @{ Files = @("use_windows_media_api.py","generate_with_windows_media_api.py"); Dest = "Store Support\Projects\AMP\Zorro\Audio\Scripts\engines"; Category = "Zorro - Engines" },
    @{ Files = @("check_data_availability.py","parse_roles_csv.py","compare_voices.py"); Dest = "Store Support\Projects\JobCodes-teaming\Job Codes\scripts\analysis"; Category = "JobCodes - Analysis" },
    @{ Files = @("query_bigquery.py","query_bigquery_event.py","query_dl_catalog_any_field.py","query_edw_table.py","query_jobcodes_for_userids.py","query_jobcodes_v2.py","query_message_content.py","query_polaris_correct_columns.py","query_polaris_for_associate.py","query_test_associate_bigquery.py"); Dest = "Store Support\Projects\JobCodes-teaming\Job Codes\scripts\queries"; Category = "JobCodes - Queries" },
    @{ Files = @("cleanup_and_rename.py"); Dest = "Store Support\Projects\JobCodes-teaming\Job Codes\scripts\transformation"; Category = "JobCodes - Transform" },
    @{ Files = @("search_associate_polaris.py","search_by_location.py","search_corehr_final.py","search_corehr_for_associate.py","search_corehr_v2.py"); Dest = "Store Support\Projects\JobCodes-teaming\Job Codes\scripts\search"; Category = "JobCodes - Search" },
    @{ Files = @("get_amp_schema.py","get_corehr_detailed_info.py","print_dl_catalog_schema.py","print_polaris_schema.py","explore_corehr_schema.py","explore_polaris_locations.py","polaris_schema_output.txt"); Dest = "Store Support\Projects\TDA Insights\scripts\schema"; Category = "TDA - Schema" },
    @{ Files = @("final_polaris_search.py","check_voice_formats.py","check_voices.py"); Dest = "Store Support\Projects\TDA Insights\scripts\queries"; Category = "TDA - Queries" },
    @{ Files = @("extract_message_body.py","amp_event_message.txt","temp_request.txt","deep_diagnostic.py"); Dest = "Store Support\Projects\TDA Insights\scripts\utilities"; Category = "TDA - Utilities" }
)

Write-Host "STEP 1: Creating Destination Directories..." -ForegroundColor Yellow
$directories = @()
foreach ($mapping in $fileMappings) {
    $directories += $mapping.Dest
}
$directories = $directories | Select-Object -Unique

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        if ($DryRun) {
            Write-Host "  [DRY] Would create: $dir" -ForegroundColor Gray
        } else {
            New-Item -ItemType Directory -Path $dir -Force -ErrorAction SilentlyContinue | Out-Null
            Write-Host "  Created: $dir" -ForegroundColor Green
        }
    }
}
Write-Host ""

Write-Host "STEP 2: Moving Files..." -ForegroundColor Yellow
$moved = 0
$skipped = 0
$errors = 0
$total = 0

foreach ($mapping in $fileMappings) {
    if ($mapping.Files.Count -gt 0) {
        Write-Host "  Category: $($mapping.Category)" -ForegroundColor Cyan
        
        foreach ($file in $mapping.Files) {
            $total++
            if (Test-Path $file) {
                $destPath = Join-Path $mapping.Dest $file
                if ($DryRun) {
                    Write-Host "    [DRY] $file" -ForegroundColor Gray
                    $moved++
                } else {
                    try {
                        Move-Item -Path $file -Destination $destPath -Force -ErrorAction Stop
                        Write-Host "    Moved: $file" -ForegroundColor Green
                        $moved++
                    } catch {
                        Write-Host "    ERROR: $file - $_" -ForegroundColor Red
                        $errors++
                    }
                }
            } else {
                Write-Host "    [SKIP] $file (not found)" -ForegroundColor Gray
                $skipped++
            }
        }
    }
}
Write-Host ""

Write-Host "STEP 3: Report" -ForegroundColor Yellow
Write-Host "  Total files checked: $total"
Write-Host "  Processed: $moved"
Write-Host "  Skipped: $skipped"
Write-Host "  Errors: $errors"

if ($DryRun) {
    Write-Host ""
    Write-Host "  [DRY RUN COMPLETE] No files were moved." -ForegroundColor Cyan
    Write-Host "  Run without -DryRun flag to execute the move." -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

Pop-Location

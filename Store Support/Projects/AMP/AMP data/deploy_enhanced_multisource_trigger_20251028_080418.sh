#!/bin/bash
# Enhanced Multi-Source AMP BigQuery Trigger System Deployment
# Deploys Cloud Functions and Cloud Scheduler for AMP Events + Dimension monitoring

set -e

echo "🚀 Deploying Enhanced Multi-Source AMP Trigger System..."

# Configuration
PROJECT_ID="wmt-assetprotection-prod"
FUNCTION_NAME="enhanced-amp-sync-trigger"
REGION="us-central1"
PUBSUB_TOPIC="enhanced-amp-sync-topic"

# Scheduler job names
AMP_SCHEDULER_JOB="amp-realtime-sync"  # Every 15 minutes
DIMENSION_SCHEDULER_JOB="amp-dimension-sync"  # Monthly

echo "📡 Creating Pub/Sub topics..."
gcloud pubsub topics create $PUBSUB_TOPIC --project=$PROJECT_ID || echo "Topic already exists"
gcloud pubsub topics create amp-dimension-topic --project=$PROJECT_ID || echo "Dimension topic already exists"

echo "☁️ Deploying enhanced Cloud Functions..."

# Main enhanced sync function (responds to scheduled triggers)
gcloud functions deploy $FUNCTION_NAME \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=. \
    --entry-point=enhanced_amp_sync_scheduled \
    --trigger-topic=$PUBSUB_TOPIC \
    --project=$PROJECT_ID \
    --memory=1GB \
    --timeout=900s \
    --service-account=bigquery-data-sync@$PROJECT_ID.iam.gserviceaccount.com

# HTTP trigger for manual execution
gcloud functions deploy $FUNCTION_NAME-http \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=. \
    --entry-point=enhanced_amp_sync_trigger \
    --trigger-http \
    --allow-unauthenticated \
    --project=$PROJECT_ID \
    --memory=1GB \
    --timeout=900s \
    --service-account=bigquery-data-sync@$PROJECT_ID.iam.gserviceaccount.com

# Monthly dimension refresh function
gcloud functions deploy monthly-dimension-refresh \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=. \
    --entry-point=monthly_dimension_refresh \
    --trigger-http \
    --allow-unauthenticated \
    --project=$PROJECT_ID \
    --memory=1GB \
    --timeout=1200s \
    --service-account=bigquery-data-sync@$PROJECT_ID.iam.gserviceaccount.com

echo "⏰ Creating Cloud Scheduler jobs..."

# AMP real-time sync (every 15 minutes)
gcloud scheduler jobs create pubsub $AMP_SCHEDULER_JOB \
    --location=$REGION \
    --schedule="*/15 * * * *" \
    --topic=$PUBSUB_TOPIC \
    --message-body="{"sync_type": "realtime"}" \
    --project=$PROJECT_ID \
    --description="Real-time AMP data sync - runs every 15 minutes"

# Dimension sync (1st day of each month at 2 AM)
gcloud scheduler jobs create pubsub $DIMENSION_SCHEDULER_JOB \
    --location=$REGION \
    --schedule="0 2 1 * *" \
    --topic=amp-dimension-topic \
    --message-body="{"sync_type": "dimension_refresh"}" \
    --project=$PROJECT_ID \
    --description="Monthly dimension refresh - runs on 1st of each month at 2 AM"

# Additional dimension check on 3rd day (backup)
gcloud scheduler jobs create pubsub amp-dimension-backup \
    --location=$REGION \
    --schedule="0 6 3 * *" \
    --topic=amp-dimension-topic \
    --message-body="{"sync_type": "dimension_check"}" \
    --project=$PROJECT_ID \
    --description="Backup dimension check - runs on 3rd of each month at 6 AM"

echo "✅ Enhanced deployment complete!"
echo ""
echo "📋 Deployment Summary:"
echo "   • Main Function: $FUNCTION_NAME (AMP real-time sync)"
echo "   • HTTP Endpoint: https://$REGION-$PROJECT_ID.cloudfunctions.net/$FUNCTION_NAME-http"
echo "   • Monthly Refresh: https://$REGION-$PROJECT_ID.cloudfunctions.net/monthly-dimension-refresh"
echo "   • AMP Schedule: Every 15 minutes"
echo "   • Dimension Schedule: Monthly (1st and 3rd of month)"
echo ""
echo "🔧 Manual Trigger Commands:"
echo "   • Real-time sync: curl https://$REGION-$PROJECT_ID.cloudfunctions.net/$FUNCTION_NAME-http"
echo "   • Force full refresh: curl -X POST -H "Content-Type: application/json" -d '{"force_full_refresh": true}' https://$REGION-$PROJECT_ID.cloudfunctions.net/$FUNCTION_NAME-http"
echo "   • Monthly dimension refresh: curl https://$REGION-$PROJECT_ID.cloudfunctions.net/monthly-dimension-refresh"
echo ""
echo "📊 Monitor Updates:"
echo "   SELECT trigger_type, records_updated, additional_info FROM \`wmt-assetprotection-prod.Store_Support_Dev.AMP_Data_Update_Log\` ORDER BY update_timestamp DESC LIMIT 10;"

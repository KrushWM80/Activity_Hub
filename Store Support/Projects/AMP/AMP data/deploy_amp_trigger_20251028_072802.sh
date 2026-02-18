#!/bin/bash
# AMP BigQuery Trigger System Deployment Script
# Deploys Cloud Function and Cloud Scheduler for automated data sync

set -e

echo "🚀 Deploying AMP BigQuery Trigger System..."

# Configuration
PROJECT_ID="wmt-assetprotection-prod"
FUNCTION_NAME="amp-data-sync-trigger"
REGION="us-central1"
SCHEDULER_JOB_NAME="amp-data-sync-schedule"
PUBSUB_TOPIC="amp-data-sync-topic"

# Step 1: Create Pub/Sub topic
echo "📡 Creating Pub/Sub topic..."
gcloud pubsub topics create $PUBSUB_TOPIC --project=$PROJECT_ID || echo "Topic already exists"

# Step 2: Deploy Cloud Function
echo "☁️ Deploying Cloud Function..."
gcloud functions deploy $FUNCTION_NAME \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=. \
    --entry-point=amp_data_sync_pubsub \
    --trigger-topic=$PUBSUB_TOPIC \
    --project=$PROJECT_ID \
    --memory=512MB \
    --timeout=540s \
    --service-account=bigquery-data-sync@$PROJECT_ID.iam.gserviceaccount.com

# Step 3: Create Cloud Scheduler job (runs every 15 minutes)
echo "⏰ Creating Cloud Scheduler job..."
gcloud scheduler jobs create pubsub $SCHEDULER_JOB_NAME \
    --location=$REGION \
    --schedule="*/15 * * * *" \
    --topic=$PUBSUB_TOPIC \
    --message-body="trigger" \
    --project=$PROJECT_ID \
    --description="Automated AMP data sync trigger - runs every 15 minutes"

# Step 4: Create HTTP trigger for manual execution
echo "🌐 Creating HTTP trigger function..."
gcloud functions deploy $FUNCTION_NAME-http \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=. \
    --entry-point=amp_data_sync_trigger \
    --trigger-http \
    --allow-unauthenticated \
    --project=$PROJECT_ID \
    --memory=512MB \
    --timeout=540s \
    --service-account=bigquery-data-sync@$PROJECT_ID.iam.gserviceaccount.com

echo "✅ Deployment complete!"
echo ""
echo "📋 Deployment Summary:"
echo "   • Cloud Function: $FUNCTION_NAME"
echo "   • HTTP Endpoint: https://$REGION-$PROJECT_ID.cloudfunctions.net/$FUNCTION_NAME-http"
echo "   • Scheduler: Runs every 15 minutes"
echo "   • Pub/Sub Topic: $PUBSUB_TOPIC"
echo ""
echo "🔧 Manual Trigger Command:"
echo "   curl https://$REGION-$PROJECT_ID.cloudfunctions.net/$FUNCTION_NAME-http"
echo ""
echo "📊 Monitor Updates:"
echo "   SELECT * FROM \`wmt-assetprotection-prod.Store_Support.AMP_Data_Update_Log\` ORDER BY update_timestamp DESC LIMIT 10;"

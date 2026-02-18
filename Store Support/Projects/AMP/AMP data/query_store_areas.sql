-- Get distinct Store Areas
SELECT DISTINCT Store_Area FROM `wmt-assetprotection-prod.Store_Support_Dev.Output - AMP ALL 2` WHERE Store_Area IS NOT NULL ORDER BY Store_Area;

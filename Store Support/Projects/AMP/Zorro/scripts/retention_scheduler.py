#!/usr/bin/env python3
"""Automated data retention cleanup scheduler.

Schedules and executes periodic cleanup of expired data according to
retention policies. Can be run as:
1. One-time job (python retention_scheduler.py --once)
2. Scheduled job (cron/Windows Task Scheduler)
3. Background daemon (python retention_scheduler.py --daemon)

Usage:
    # Dry run (preview what would be deleted)
    python retention_scheduler.py --dry-run
    
    # Execute cleanup
    python retention_scheduler.py
    
    # Run as daemon (check every 24 hours)
    python retention_scheduler.py --daemon
"""

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.compliance import RetentionManager, cleanup_expired_data
from src.utils import get_logger

logger = get_logger(__name__)


def run_cleanup(dry_run: bool = False) -> dict:
    """
    Execute retention cleanup.
    
    Args:
        dry_run: If True, only report what would be deleted
        
    Returns:
        dict: Cleanup results
    """
    logger.info(
        "retention_cleanup_started",
        dry_run=dry_run,
        timestamp=datetime.utcnow().isoformat()
    )
    
    try:
        results = cleanup_expired_data(dry_run=dry_run)
        
        # Log summary
        total_deleted = sum(
            r.get("deleted_count", 0)
            for r in results.values()
            if isinstance(r, dict)
        )
        
        logger.info(
            "retention_cleanup_completed",
            total_deleted=total_deleted,
            results=results,
            dry_run=dry_run
        )
        
        return results
    
    except Exception as e:
        logger.error(
            "retention_cleanup_failed",
            error=str(e),
            dry_run=dry_run
        )
        raise


def generate_report(output_file: str = "retention_report.json"):
    """
    Generate and save retention compliance report.
    
    Args:
        output_file: Path to save report
    """
    import json
    
    logger.info("generating_retention_report")
    
    manager = RetentionManager()
    report = manager.generate_retention_report()
    
    # Save report
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    
    logger.info(
        "retention_report_generated",
        output_file=str(output_path)
    )
    
    # Print summary
    print(f"\n{'='*60}")
    print("DATA RETENTION REPORT")
    print(f"{'='*60}")
    print(f"Generated: {report['generated_at']}")
    print(f"\nPolicies:")
    for data_type, policy in report['policies'].items():
        print(f"  {data_type}:")
        print(f"    - Retention: {policy['retention_days']} days")
        print(f"    - Auto-delete: {policy['auto_delete']}")
        print(f"    - Cutoff date: {policy['cutoff_date']}")
    
    if "summary" in report:
        print(f"\nData Summary:")
        for data_type, summary in report['summary'].items():
            print(f"  {data_type}:")
            print(f"    - Total: {summary['total']}")
            print(f"    - Expired: {summary['expired']}")
            print(f"    - Active: {summary['active']}")
    
    print(f"\nFull report saved to: {output_path}")
    print(f"{'='*60}\n")


def daemon_mode(interval_hours: int = 24):
    """
    Run cleanup in daemon mode (continuous).
    
    Args:
        interval_hours: Hours between cleanup runs
    """
    logger.info(
        "daemon_mode_started",
        interval_hours=interval_hours
    )
    
    print(f"Starting retention cleanup daemon...")
    print(f"Will run cleanup every {interval_hours} hours")
    print(f"Press Ctrl+C to stop\n")
    
    try:
        while True:
            try:
                results = run_cleanup(dry_run=False)
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Cleanup completed")
                
                for data_type, result in results.items():
                    if isinstance(result, dict) and result.get("status") == "completed":
                        deleted = result.get("deleted_count", 0)
                        print(f"  - {data_type}: {deleted} items deleted")
            
            except Exception as e:
                logger.error("daemon_cleanup_failed", error=str(e))
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {e}")
            
            # Sleep until next run
            sleep_seconds = interval_hours * 3600
            print(f"\nNext cleanup in {interval_hours} hours...\n")
            time.sleep(sleep_seconds)
    
    except KeyboardInterrupt:
        print("\n\nDaemon stopped by user")
        logger.info("daemon_mode_stopped")


def main():
    parser = argparse.ArgumentParser(
        description="Automated data retention cleanup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Preview what would be deleted
  python retention_scheduler.py --dry-run
  
  # Execute cleanup
  python retention_scheduler.py
  
  # Generate report only
  python retention_scheduler.py --report-only
  
  # Run as background daemon
  python retention_scheduler.py --daemon --interval 24
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be deleted without actually deleting"
    )
    
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run as continuous daemon"
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        default=24,
        help="Hours between cleanup runs in daemon mode (default: 24)"
    )
    
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Generate retention report without cleanup"
    )
    
    parser.add_argument(
        "--output",
        default="retention_report.json",
        help="Output file for report (default: retention_report.json)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.report_only:
            generate_report(args.output)
        elif args.daemon:
            daemon_mode(args.interval)
        else:
            results = run_cleanup(dry_run=args.dry_run)
            
            # Print results
            print(f"\n{'='*60}")
            print(f"RETENTION CLEANUP {'(DRY RUN)' if args.dry_run else 'COMPLETED'}")
            print(f"{'='*60}")
            
            for data_type, result in results.items():
                if isinstance(result, dict):
                    status = result.get("status", "unknown")
                    print(f"\n{data_type}:")
                    print(f"  Status: {status}")
                    
                    if status == "completed":
                        deleted = result.get("deleted_count", 0)
                        archived = result.get("archived_count", 0)
                        print(f"  Deleted: {deleted} items")
                        if archived > 0:
                            print(f"  Archived: {archived} items")
                    elif status == "skipped":
                        print(f"  Reason: {result.get('reason', 'unknown')}")
                    elif status == "error":
                        print(f"  Error: {result.get('error', 'unknown')}")
            
            print(f"\n{'='*60}\n")
            
            if args.dry_run:
                print("This was a dry run. No data was actually deleted.")
                print("Run without --dry-run to execute cleanup.\n")
    
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        logger.error("scheduler_failed", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()

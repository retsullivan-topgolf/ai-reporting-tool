## Single Venue Snapshot:
python generate_report.py --report-type snapshot --venue "Grand Prairie" --format all --force-analysis

## Single Venue Comparison:
python generate_report.py --report-type comparison --venue "Grand Prairie" --start-date 2026-04-01 --end-date 2026-04-30 --prev-start
2026-03-01 --prev-end 2026-03-31 --format all --force-analysis

## Multi-Venue Snapshot:
python generate_report.py --report-type multi-snapshot --start-date 2026-01-01 --end-date 2026-01-31 --format all --force-analysis

## Multi-Venue Comparison:
python generate_report.py --report-type multi-comparison --start-date 2026-01-01 --end-date 2026-01-31 --prev-start 2025-12-01 --prev-end 2025-12-31 --format all --force-analysis
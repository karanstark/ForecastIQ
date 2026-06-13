import csv
import os
import argparse
import re
from collections import defaultdict


def parse_num(s):
    if s is None:
        return 0.0
    s = str(s).strip()
    if s == '':
        return 0.0
    s = re.sub(r"[^0-9.\-]", "", s)
    try:
        return float(s)
    except Exception:
        return 0.0


def aggregate_data(data_dir: str):
    files = {
        'google_ads_campaign_stats.csv': 'Google',
        'meta_ads_campaign_stats.csv': 'Meta',
        'bing_campaign_stats.csv': 'Bing'
    }

    totals = defaultdict(lambda: {'rev': 0.0, 'spend': 0.0, 'count': 0})

    for fname, channel in files.items():
        path = os.path.join(data_dir, fname)
        if not os.path.exists(path):
            continue

        with open(path, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                rev = 0.0
                spend = 0.0
                for k, v in row.items():
                    key = (k or '').lower()
                    if 'revenue' in key or 'purchase conversion value' in key or 'conv. value' in key or 'conversion value' in key:
                        rev = parse_num(v) or rev
                    if 'spend' in key or 'amount spent' in key or 'cost' in key:
                        spend = parse_num(v) or spend

                totals[channel]['rev'] += rev
                totals[channel]['spend'] += spend
                totals[channel]['count'] += 1

    return totals


def write_forecast(totals, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.writer(fh)
        writer.writerow(['Channel', 'Forecast_Period', 'Forecast_Revenue', 'Forecast_ROAS'])
        for channel, stats in totals.items():
            if stats['count'] == 0:
                continue
            avg_daily_rev = (stats['rev'] / stats['count'])
            avg_daily_spend = (stats['spend'] / stats['count'])
            forecast_rev = avg_daily_rev * 30
            forecast_roas = (avg_daily_rev / avg_daily_spend) if avg_daily_spend > 0 else 0

            writer.writerow([channel, '30_days', round(forecast_rev, 2), round(forecast_roas, 4)])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', type=str)
    parser.add_argument('output_path', type=str)
    args = parser.parse_args()

    totals = aggregate_data(args.data_dir)
    if not totals:
        print('No data found for backup forecast. Exiting with failure.')
        raise SystemExit(1)

    write_forecast(totals, args.output_path)
    print(f'Backup predictions written to {args.output_path}')


if __name__ == '__main__':
    main()

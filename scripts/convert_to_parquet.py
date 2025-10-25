"""
Convert all CSV files to Parquet format
Maintains folder structure and creates Parquet files in same directories
"""

import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import pyarrow as pa
import pyarrow.parquet as pq

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')


class CSVToParquetConverter:
    """Convert all CSV files to Parquet format"""

    def __init__(self):
        self.conversion_stats = []
        self.total_files = 0
        self.total_csv_size = 0
        self.total_parquet_size = 0

    def get_file_size_mb(self, file_path):
        """Get file size in MB"""
        return os.path.getsize(file_path) / (1024 * 1024)

    def convert_csv_to_parquet(self, csv_path, parquet_path):
        """Convert single CSV file to Parquet"""
        try:
            # Read CSV
            df = pd.read_csv(csv_path)

            # Convert to Parquet with compression
            df.to_parquet(
                parquet_path,
                engine='pyarrow',
                compression='snappy',
                index=False
            )

            return True, len(df)
        except Exception as e:
            print(f"    ✗ Error converting {csv_path}: {str(e)}")
            return False, 0

    def convert_directory(self, directory):
        """Convert all CSV files in a directory"""
        csv_files = list(Path(directory).rglob('*.csv'))

        if not csv_files:
            return

        rel_path = os.path.relpath(directory, DATA_DIR)
        print(f"\n📁 Processing: {rel_path}")

        for csv_file in csv_files:
            csv_path = str(csv_file)
            parquet_path = csv_path.replace('.csv', '.parquet')

            # Get file sizes
            csv_size = self.get_file_size_mb(csv_path)

            # Convert
            file_name = os.path.basename(csv_path)
            print(f"  Converting {file_name}...", end=' ')

            success, row_count = self.convert_csv_to_parquet(csv_path, parquet_path)

            if success:
                parquet_size = self.get_file_size_mb(parquet_path)
                compression_ratio = (1 - parquet_size/csv_size) * 100 if csv_size > 0 else 0

                print(f"✓ ({row_count:,} rows, {csv_size:.2f}MB → {parquet_size:.2f}MB, {compression_ratio:.1f}% saved)")

                self.conversion_stats.append({
                    'file': file_name,
                    'path': os.path.relpath(csv_path, DATA_DIR),
                    'rows': row_count,
                    'csv_size_mb': csv_size,
                    'parquet_size_mb': parquet_size,
                    'compression_ratio': compression_ratio
                })

                self.total_files += 1
                self.total_csv_size += csv_size
                self.total_parquet_size += parquet_size

    def convert_all(self):
        """Convert all CSV files in data directory"""
        print("="*80)
        print("CSV TO PARQUET CONVERTER")
        print("="*80)
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Data Directory: {DATA_DIR}")

        # Convert SAP data
        sap_dir = os.path.join(DATA_DIR, 'sap')
        if os.path.exists(sap_dir):
            print("\n" + "="*80)
            print("SAP DATA CONVERSION")
            print("="*80)
            for root, dirs, files in os.walk(sap_dir):
                if any(f.endswith('.csv') for f in files):
                    self.convert_directory(root)

        # Convert CRM data
        crm_dir = os.path.join(DATA_DIR, 'crm')
        if os.path.exists(crm_dir):
            print("\n" + "="*80)
            print("CRM DATA CONVERSION")
            print("="*80)
            self.convert_directory(crm_dir)

        # Convert Cross-Reference data
        xref_dir = os.path.join(DATA_DIR, 'cross_reference')
        if os.path.exists(xref_dir):
            print("\n" + "="*80)
            print("CROSS-REFERENCE DATA CONVERSION")
            print("="*80)
            self.convert_directory(xref_dir)

    def print_summary(self):
        """Print conversion summary"""
        print("\n" + "="*80)
        print("CONVERSION SUMMARY")
        print("="*80)

        print(f"\nFiles Converted: {self.total_files}")
        print(f"Total CSV Size: {self.total_csv_size:.2f} MB")
        print(f"Total Parquet Size: {self.total_parquet_size:.2f} MB")

        if self.total_csv_size > 0:
            total_savings = (1 - self.total_parquet_size/self.total_csv_size) * 100
            print(f"Total Space Saved: {self.total_csv_size - self.total_parquet_size:.2f} MB ({total_savings:.1f}%)")

        # Top 10 largest files
        if self.conversion_stats:
            print("\n📊 Top 10 Largest Files (by row count):")
            sorted_stats = sorted(self.conversion_stats, key=lambda x: x['rows'], reverse=True)[:10]

            for i, stat in enumerate(sorted_stats, 1):
                print(f"  {i:2d}. {stat['file']:30s} - {stat['rows']:8,} rows, "
                      f"{stat['csv_size_mb']:6.2f}MB → {stat['parquet_size_mb']:6.2f}MB "
                      f"({stat['compression_ratio']:5.1f}% saved)")

        # Save stats to CSV
        stats_file = os.path.join(PROJECT_ROOT, 'conversion_stats.csv')
        if self.conversion_stats:
            pd.DataFrame(self.conversion_stats).to_csv(stats_file, index=False)
            print(f"\n✓ Detailed stats saved to: conversion_stats.csv")

        print("\n" + "="*80)
        print("CONVERSION COMPLETE!")
        print("="*80)
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """Main execution"""
    converter = CSVToParquetConverter()
    converter.convert_all()
    converter.print_summary()


if __name__ == "__main__":
    main()

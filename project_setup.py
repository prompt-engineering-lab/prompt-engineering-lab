#!/usr/bin/env python3
import os
import sys
from import_gtfs_to_sqlite import main as import_gtfs

def setup_project():
    """Setup project by importing GTFS data to SQLite database"""
    print("Starting GTFS data import...")
    
    # Check if GTFS folder exists
    gtfs_folder = "group-task-skeleton/OtwartyWroclaw_rozklad_jazdy_GTFS"
    if not os.path.exists(gtfs_folder):
        print(f"Error: GTFS folder not found at {gtfs_folder}")
        sys.exit(1)
    
    # Run the import
    try:
        import_gtfs()
        print("Project setup completed successfully!")
    except Exception as e:
        print(f"Error during import: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_project()

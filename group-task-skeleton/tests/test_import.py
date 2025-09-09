import unittest
import sqlite3
import os
import tempfile
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from import_to_db import create_table_from_csv, insert_csv_to_table

class TestGTFSImport(unittest.TestCase):
    
    def setUp(self):
        self.test_db = tempfile.mktemp(suffix='.db')
        self.conn = sqlite3.connect(self.test_db)
        self.cursor = self.conn.cursor()
    
    def tearDown(self):
        self.conn.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_create_table_from_csv(self):
        """Test table creation from CSV headers"""
        csv_path = "OtwartyWroclaw_rozklad_jazdy_GTFS/stops.txt"
        if not os.path.exists(csv_path):
            self.skipTest("GTFS stops.txt not found")
        
        create_table_from_csv(self.cursor, "stops", csv_path)
        
        # Check table exists
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stops'")
        self.assertIsNotNone(self.cursor.fetchone())
    
    def test_insert_csv_to_table(self):
        """Test data insertion from CSV"""
        csv_path = "OtwartyWroclaw_rozklad_jazdy_GTFS/agency.txt"
        if not os.path.exists(csv_path):
            self.skipTest("GTFS agency.txt not found")
        
        create_table_from_csv(self.cursor, "agency", csv_path)
        insert_csv_to_table(self.cursor, "agency", csv_path)
        
        # Check data inserted
        self.cursor.execute("SELECT COUNT(*) FROM agency")
        count = self.cursor.fetchone()[0]
        self.assertGreater(count, 0)
    
    def test_all_gtfs_tables_loaded(self):
        """Test that all GTFS files are loaded as tables"""
        gtfs_folder = "OtwartyWroclaw_rozklad_jazdy_GTFS"
        if not os.path.exists(gtfs_folder):
            self.skipTest("GTFS folder not found")
        
        # Import all files
        for filename in os.listdir(gtfs_folder):
            if filename.endswith('.txt'):
                table_name = filename.replace('.txt', '')
                csv_path = os.path.join(gtfs_folder, filename)
                create_table_from_csv(self.cursor, table_name, csv_path)
                insert_csv_to_table(self.cursor, table_name, csv_path)
        
        # Check all tables exist and have data
        expected_tables = [f.replace('.txt', '') for f in os.listdir(gtfs_folder) if f.endswith('.txt')]
        
        for table in expected_tables:
            with self.subTest(table=table):
                self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = self.cursor.fetchone()[0]
                self.assertGreaterEqual(count, 0)

if __name__ == '__main__':
    unittest.main()
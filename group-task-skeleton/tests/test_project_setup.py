import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from project_setup import setup_project


class TestProjectSetup(unittest.TestCase):
    
    @patch('project_setup.import_gtfs')
    @patch('project_setup.os.path.exists')
    @patch('builtins.print')
    def test_setup_project_success(self, mock_print, mock_exists, mock_import_gtfs):
        """Test successful project setup"""
        mock_exists.return_value = True
        mock_import_gtfs.return_value = None
        
        setup_project()
        
        mock_exists.assert_called_once_with("OtwartyWroclaw_rozklad_jazdy_GTFS")
        mock_import_gtfs.assert_called_once()
        mock_print.assert_any_call("Starting GTFS data import...")
        mock_print.assert_any_call("Project setup completed successfully!")
    
    @patch('project_setup.sys.exit')
    @patch('project_setup.os.path.exists')
    @patch('builtins.print')
    def test_setup_project_missing_gtfs_folder(self, mock_print, mock_exists, mock_exit):
        """Test setup fails when GTFS folder is missing"""
        mock_exists.return_value = False
        
        setup_project()
        
        mock_exists.assert_called_once_with("OtwartyWroclaw_rozklad_jazdy_GTFS")
        mock_print.assert_any_call("Error: GTFS folder not found at OtwartyWroclaw_rozklad_jazdy_GTFS")
        mock_exit.assert_called_once_with(1)
    
    @patch('project_setup.sys.exit')
    @patch('project_setup.import_gtfs')
    @patch('project_setup.os.path.exists')
    @patch('builtins.print')
    def test_setup_project_import_error(self, mock_print, mock_exists, mock_import_gtfs, mock_exit):
        """Test setup handles import errors"""
        mock_exists.return_value = True
        mock_import_gtfs.side_effect = Exception("Import failed")
        
        setup_project()
        
        mock_exists.assert_called_once_with("OtwartyWroclaw_rozklad_jazdy_GTFS")
        mock_import_gtfs.assert_called_once()
        mock_print.assert_any_call("Error during import: Import failed")
        mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
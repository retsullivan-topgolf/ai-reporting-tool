"""
Optional Flask REST API wrapper for the Topgolf reporting API.

This module provides REST endpoints for CSV parsing and venue data generation.
It can be used for web-based report generation in the future.

Usage:
    python app.py                    # Run on http://localhost:5000
    python app.py --port 8080        # Run on http://localhost:8080
    python app.py --host 0.0.0.0     # Listen on all interfaces

Endpoints:
    POST /api/parse-csv              - Parse a CSV file and return venue data
    GET /api/schemas                 - List available schemas
    GET /api/health                  - Health check
"""

import json
import os
import sys
from typing import Dict, Tuple
from pathlib import Path

try:
    from flask import Flask, request, jsonify
except ImportError:
    print("Flask not installed. Install with: pip install flask")
    sys.exit(1)

from . import csv_parser, venue_processor, schemas


def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)
    
    @app.route('/api/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({
            'status': 'ok',
            'service': 'Topgolf Reporting API',
            'version': '1.0.0'
        })
    
    @app.route('/api/schemas', methods=['GET'])
    def list_schemas():
        """List available schemas."""
        schema_list = []
        for schema_name in schemas.list_schemas():
            schema = schemas.get_schema(schema_name)
            schema_list.append({
                'name': schema['name'],
                'description': schema['description'],
                'detection_rule': schema['detection_rule'],
                'fields': list(schema['fields'].keys())
            })
        
        return jsonify({
            'schemas': schema_list
        })
    
    @app.route('/api/parse-csv', methods=['POST'])
    def parse_csv_endpoint():
        """Parse a CSV file and return venue data.
        
        Request:
            - file: CSV file (multipart/form-data)
            - OR csv_path: Path to CSV file (application/json)
        
        Response:
            {
                "success": true,
                "schema": "real",
                "venues": {
                    "grand_prairie": { ... },
                    ...
                }
            }
        """
        try:
            csv_file = None
            
            # Check for file upload
            if 'file' in request.files:
                file = request.files['file']
                if file.filename == '':
                    return jsonify({'error': 'No file selected'}), 400
                
                # Save temp file
                temp_path = f'/tmp/{file.filename}'
                file.save(temp_path)
                csv_file = temp_path
            
            # Check for csv_path in JSON body
            elif request.is_json:
                data = request.get_json()
                csv_file = data.get('csv_path')
            
            if not csv_file:
                return jsonify({'error': 'No CSV file provided'}), 400
            
            if not os.path.exists(csv_file):
                return jsonify({'error': f'File not found: {csv_file}'}), 404
            
            # Parse CSV
            rows, fieldnames = csv_parser.parse_csv(csv_file)
            schema_type = csv_parser.detect_schema(fieldnames)
            
            # Build venue data
            venue_data_dict = venue_processor.build_venue_data_dict(rows, schema_type)
            
            # Clean up temp file if created
            if 'file' in request.files:
                try:
                    os.remove(csv_file)
                except:
                    pass
            
            return jsonify({
                'success': True,
                'schema': schema_type,
                'venues': venue_data_dict
            })
        
        except csv_parser.CSVParseError as e:
            return jsonify({'error': f'CSV Parse Error: {str(e)}'}), 400
        except csv_parser.SchemaDetectionError as e:
            return jsonify({'error': f'Schema Detection Error: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'error': f'Error: {str(e)}'}), 500
    
    @app.route('/api/validate-row', methods=['POST'])
    def validate_row_endpoint():
        """Validate a single row against a schema.
        
        Request:
            {
                "schema": "real",
                "row": { "Venue": "...", "Combined NPS": "...", ... }
            }
        
        Response:
            {
                "valid": true,
                "error": null
            }
        """
        try:
            data = request.get_json()
            schema_name = data.get('schema')
            row = data.get('row')
            
            if not schema_name or not row:
                return jsonify({'error': 'Missing schema or row'}), 400
            
            is_valid, error = csv_parser.validate_row(row, schema_name)
            
            return jsonify({
                'valid': is_valid,
                'error': error
            })
        
        except Exception as e:
            return jsonify({'error': f'Error: {str(e)}'}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


def main():
    """Run the Flask app."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Topgolf Reporting API Server')
    parser.add_argument('--host', default='localhost', help='Host to bind to (default: localhost)')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    app = create_app()
    
    print(f"Starting Topgolf Reporting API on http://{args.host}:{args.port}")
    print(f"Available endpoints:")
    print(f"  GET  /api/health")
    print(f"  GET  /api/schemas")
    print(f"  POST /api/parse-csv")
    print(f"  POST /api/validate-row")
    
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()

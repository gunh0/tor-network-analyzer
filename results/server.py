#!/usr/bin/env python3
"""
Simple HTTP server with file listing API for Tor Analysis Results
"""
import json
import os
import glob
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import re

class ResultsHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # API endpoint to get file list
        if parsed_path.path == '/api/files':
            self.send_json_response(self.get_files_list())
            return
        
        # API endpoint to get specific analysis data
        if parsed_path.path.startswith('/api/data/'):
            timestamp = parsed_path.path.split('/')[-1]
            data = self.get_analysis_data(timestamp)
            if data:
                self.send_json_response(data)
            else:
                self.send_error(404, "Analysis data not found")
            return
        
        # Default file serving
        super().do_GET()
    
    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def get_files_list(self):
        """Get list of analysis files grouped by timestamp"""
        current_dir = os.getcwd()
        files_info = {}
        
        # Find all JSON files
        json_files = glob.glob('analysis_data_*.json')
        
        for json_file in json_files:
            # Extract timestamp from filename
            match = re.search(r'analysis_data_(\d{8}_\d{6})\.json', json_file)
            if match:
                timestamp = match.group(1)
                
                if timestamp not in files_info:
                    files_info[timestamp] = {
                        'timestamp': timestamp,
                        'files': {}
                    }
                
                # Check for related files
                files_info[timestamp]['files']['json'] = json_file
                
                # Look for corresponding PNG files
                response_time_chart = f'response_times_{timestamp}.png'
                success_rate_chart = f'success_rate_{timestamp}.png'
                report_file = f'analysis_report_{timestamp}.txt'
                
                if os.path.exists(response_time_chart):
                    files_info[timestamp]['files']['response_times_chart'] = response_time_chart
                
                if os.path.exists(success_rate_chart):
                    files_info[timestamp]['files']['success_rate_chart'] = success_rate_chart
                
                if os.path.exists(report_file):
                    files_info[timestamp]['files']['report'] = report_file
        
        # Sort by timestamp (newest first)
        sorted_files = dict(sorted(files_info.items(), key=lambda x: x[0], reverse=True))
        
        return {
            'files': sorted_files,
            'count': len(sorted_files)
        }
    
    def get_analysis_data(self, timestamp):
        """Get analysis data for specific timestamp"""
        json_file = f'analysis_data_{timestamp}.json'
        
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error reading {json_file}: {e}")
                return None
        
        return None

def run_server(port=8080):
    """Run the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ResultsHTTPRequestHandler)
    
    print(f"🚀 Starting Tor Analysis Results Server on port {port}")
    print(f"📊 Open http://localhost:{port} to view results")
    print(f"🔗 API endpoints:")
    print(f"   • GET /api/files - List all analysis files")
    print(f"   • GET /api/data/<timestamp> - Get specific analysis data")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == '__main__':
    import sys
    
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8080.")
    
    run_server(port)

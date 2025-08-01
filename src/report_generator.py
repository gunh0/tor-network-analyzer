#!/usr/bin/env python3
"""
Report Generator for Tor Anonymous Network Analysis
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class TorAnalysisReportGenerator:
    """Generate comprehensive analysis reports"""
    
    def __init__(self, results_dir: str = "results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.switch_backend('Agg')
        sns.set_style("whitegrid")
    
    def generate_report(self, results: List[Dict[str, Any]], 
                       connectivity_test: bool = False,
                       tor_ip: Optional[str] = None) -> Dict[str, str]:
        """Generate comprehensive analysis report"""
        report_files = {}
        
        # Text report
        text_path = self._generate_text_report(results, connectivity_test, tor_ip)
        report_files['text'] = str(text_path)
        
        # JSON report
        json_path = self._generate_json_report(results, connectivity_test, tor_ip)
        report_files['json'] = str(json_path)
        
        # Visualizations
        if results:
            viz_files = self._generate_visualizations(results)
            report_files.update(viz_files)
        
        return report_files
    
    def _generate_text_report(self, results: List[Dict[str, Any]], 
                            connectivity_test: bool, tor_ip: Optional[str]) -> Path:
        """Generate detailed text report"""
        report_path = self.results_dir / f"analysis_report_{self.timestamp}.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("TOR NETWORK ANALYSIS REPORT\n")
            f.write("=" * 60 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary
            total = len(results)
            successful = sum(1 for r in results if r.get('success', False))
            success_rate = (successful / total * 100) if total > 0 else 0
            
            f.write("SUMMARY\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total Sites: {total}\n")
            f.write(f"Successful: {successful}\n")
            f.write(f"Success Rate: {success_rate:.1f}%\n")
            f.write(f"Tor Status: {'CONNECTED' if connectivity_test else 'DISCONNECTED'}\n")
            if tor_ip:
                f.write(f"Exit IP: {tor_ip}\n")
            f.write("\n")
            
            # Details
            f.write("DETAILED RESULTS\n")
            f.write("-" * 20 + "\n")
            for i, result in enumerate(results, 1):
                f.write(f"\n{i}. {result.get('url', 'Unknown')}\n")
                if result.get('success'):
                    f.write(f"   ✓ SUCCESS - {result.get('title', 'No title')}\n")
                    f.write(f"   Status: {result.get('status_code')}\n")
                    f.write(f"   Size: {result.get('content_length', 0)} bytes\n")
                else:
                    f.write(f"   ✗ FAILED - {result.get('error', 'Unknown error')}\n")
        
        return report_path
    
    def _generate_json_report(self, results: List[Dict[str, Any]], 
                            connectivity_test: bool, tor_ip: Optional[str]) -> Path:
        """Generate JSON report"""
        report_path = self.results_dir / f"analysis_data_{self.timestamp}.json"
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "tor_connectivity": connectivity_test,
            "tor_exit_ip": tor_ip,
            "summary": {
                "total_sites": len(results),
                "successful": sum(1 for r in results if r.get('success', False)),
                "success_rate": (sum(1 for r in results if r.get('success', False)) / len(results) * 100) if results else 0
            },
            "results": results
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        return report_path
    
    def _generate_visualizations(self, results: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate visualization charts"""
        viz_files = {}
        
        # Success/Failure pie chart
        successful = sum(1 for r in results if r.get('success', False))
        failed = len(results) - successful
        
        plt.figure(figsize=(10, 6))
        plt.pie([successful, failed], labels=['Successful', 'Failed'], 
                autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'])
        plt.title('Tor Network Analysis Results')
        pie_path = self.results_dir / f"success_rate_{self.timestamp}.png"
        plt.savefig(pie_path, dpi=300, bbox_inches='tight')
        plt.close()
        viz_files['pie_chart'] = str(pie_path)
        
        # Response time chart (if available)
        response_times = [r.get('response_time', 0) for r in results if r.get('success')]
        if response_times:
            plt.figure(figsize=(12, 6))
            plt.bar(range(len(response_times)), response_times, color='#3498db')
            plt.xlabel('Site Index')
            plt.ylabel('Response Time (seconds)')
            plt.title('Response Times for Successful Connections')
            bar_path = self.results_dir / f"response_times_{self.timestamp}.png"
            plt.savefig(bar_path, dpi=300, bbox_inches='tight')
            plt.close()
            viz_files['response_chart'] = str(bar_path)
        
        return viz_files

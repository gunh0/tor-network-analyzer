#!/usr/bin/env python3
"""
Advanced Network Analysis Module for Tor Anonymous Network Analysis
"""

import time
from typing import Dict, List, Any


class TorNetworkAnalyzer:
    """Advanced network analysis for Tor hidden services"""
    
    def __init__(self, tor_analyzer):
        self.tor_analyzer = tor_analyzer
    
    def analyze_network_topology(self, addresses: List[str]) -> Dict[str, Any]:
        """Analyze network topology of multiple hidden services"""
        topology = {
            'total_services': len(addresses),
            'reachable_services': 0,
            'v2_services': 0,
            'v3_services': 0,
            'https_services': 0,
            'service_details': []
        }
        
        for address in addresses:
            onion_analysis = self.tor_analyzer.analyze_onion_structure(address)
            result = self.tor_analyzer.analyze_site(address, timeout=15)
            
            service_detail = {
                'address': address,
                'reachable': result.get('success', False),
                'onion_version': 'v3' if onion_analysis['is_v3_onion'] else 'v2',
                'protocol': onion_analysis['protocol'],
                'title': result.get('title', 'N/A')
            }
            
            topology['service_details'].append(service_detail)
            
            if result.get('success'):
                topology['reachable_services'] += 1
            
            if onion_analysis['is_v3_onion']:
                topology['v3_services'] += 1
            elif onion_analysis['is_v2_onion']:
                topology['v2_services'] += 1
            
            if address.startswith('https://'):
                topology['https_services'] += 1
        
        return topology
    
    def perform_latency_analysis(self, addresses: List[str], iterations: int = 3) -> Dict[str, Any]:
        """Perform detailed latency analysis"""
        results = {'results': [], 'statistics': {}}
        
        all_latencies = []
        
        for address in addresses:
            latencies = []
            successful = 0
            
            for _ in range(iterations):
                start_time = time.time()
                try:
                    response = self.tor_analyzer.session.get(address, timeout=10)
                    latency = time.time() - start_time
                    
                    if response.status_code == 200:
                        latencies.append(latency)
                        all_latencies.append(latency)
                        successful += 1
                except Exception:
                    pass
                
                time.sleep(1)
            
            results['results'].append({
                'address': address,
                'avg_latency': sum(latencies) / len(latencies) if latencies else 0,
                'successful_tests': successful
            })
        
        if all_latencies:
            results['statistics'] = {
                'overall_avg': sum(all_latencies) / len(all_latencies),
                'min_latency': min(all_latencies),
                'max_latency': max(all_latencies)
            }
        
        return results

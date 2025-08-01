#!/usr/bin/env python3
"""
Tor Anonymous Network Analysis Tool
Main entry point for the application
"""

import sys
import os
import time
from datetime import datetime
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.analyzer import TorAnalyzer
from src.report_generator import TorAnalysisReportGenerator


def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                Tor Anonymous Network Analysis                ║
    ║                        Version 1.0                          ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def load_target_addresses():
    """Load target addresses from assets file"""
    assets_file = Path(__file__).parent / 'src' / 'assets' / 'collect_target_address.txt'
    addresses = []
    
    try:
        with open(assets_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    addresses.append(line)
        print(f"✓ Loaded {len(addresses)} target address(es)")
        return addresses
    except FileNotFoundError:
        print(f"⚠ Warning: Target addresses file not found at {assets_file}")
        return []
    except Exception as e:
        print(f"✗ Error loading target addresses: {e}")
        return []


def run_connectivity_test():
    """Test basic connectivity and Tor proxy availability"""
    print("\n" + "="*60)
    print("🔍 CONNECTIVITY TEST")
    print("="*60)
    
    analyzer = TorAnalyzer()
    
    # Test 1: Check if Tor proxy is accessible
    print("1. Testing Tor proxy connectivity...")
    if analyzer.test_tor_proxy():
        print("   ✓ Tor proxy is accessible")
        return True
    else:
        print("   ✗ Tor proxy is not accessible")
        print("   💡 Make sure Tor is running on 127.0.0.1:9050")
        return False


def run_enhanced_analysis(addresses):
    """Run enhanced analysis tests on target addresses"""
    print("\n" + "="*60)
    print("🌐 ENHANCED TOR NETWORK ANALYSIS")
    print("="*60)
    
    analyzer = TorAnalyzer()
    results = []
    
    # Test circuit diversity first
    print("\n🔄 Testing Tor Circuit Diversity...")
    circuit_analysis = analyzer.test_circuit_diversity()
    print(f"   Exit IPs found: {circuit_analysis['unique_exit_ips']}")
    print(f"   Diversity score: {circuit_analysis['circuit_diversity_score']:.2f}")
    
    for i, address in enumerate(addresses, 1):
        print(f"\n{i}. Analyzing: {address}")
        print("-" * 50)
        
        # Onion structure analysis
        onion_analysis = analyzer.analyze_onion_structure(address)
        print(f"   🧅 Onion Type: {'v3' if onion_analysis['is_v3_onion'] else 'v2' if onion_analysis['is_v2_onion'] else 'Unknown'}")
        print(f"   🔒 Protocol: {onion_analysis['protocol'].upper()}")
        
        # Site analysis
        start_time = time.time()
        result = analyzer.analyze_site(address)
        end_time = time.time()
        
        result['response_time'] = round(end_time - start_time, 2)
        result['address'] = address
        result['onion_analysis'] = onion_analysis
        
        # Security analysis
        if result['success']:
            security_analysis = analyzer.analyze_hidden_service_security(address, result)
            result['security_analysis'] = security_analysis
            
            print(f"   ✓ Connection successful")
            print(f"   📄 Title: {result['title']}")
            print(f"   📊 Status: {result['status_code']}")
            print(f"   🛡️ Anonymity Score: {security_analysis['anonymity_score']}/100")
            print(f"   ⏱ Response time: {result['response_time']}s")
        else:
            print(f"   ✗ Connection failed")
            print(f"   ❌ Error: {result['error']}")
            print(f"   ⏱ Timeout after: {result['response_time']}s")
        
        results.append(result)
    
    # Add circuit analysis to results
    results.append({'circuit_analysis': circuit_analysis, 'type': 'circuit_diversity'})
    
    return results


def display_summary(results):
    """Display test summary"""
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    # Filter out non-site results (like circuit analysis)
    site_results = [r for r in results if r.get('type') != 'circuit_diversity' and 'address' in r]
    
    total_tests = len(site_results)
    successful = sum(1 for r in site_results if r.get('success', False))
    failed = total_tests - successful
    
    print(f"Total tests: {total_tests}")
    print(f"Successful: {successful} ✓")
    print(f"Failed: {failed} ✗")
    print(f"Success rate: {(successful/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
    
    if successful > 0:
        avg_response_time = sum(r.get('response_time', 0) for r in site_results if r.get('success', False)) / successful
        print(f"Average response time: {avg_response_time:.2f}s")
    
    # Display circuit diversity info
    circuit_result = next((r for r in results if r.get('type') == 'circuit_diversity'), None)
    if circuit_result and 'circuit_analysis' in circuit_result:
        circuit_data = circuit_result['circuit_analysis']
        print(f"\nTor Circuit Diversity: {circuit_data.get('unique_exit_ips', 0)} unique exit IPs")
        print(f"Diversity Score: {circuit_data.get('circuit_diversity_score', 0):.2f}")
    
    # Display detailed results
    print("\nDetailed Results:")
    print("-" * 40)
    for result in site_results:
        status = "✓" if result.get('success', False) else "✗"
        print(f"{status} {result.get('address', 'Unknown')}")
        if result.get('success', False):
            title = result.get('title', 'No title')
            print(f"    Title: {title[:50]}{'...' if len(title) > 50 else ''}")
            if 'security_analysis' in result:
                print(f"    Anonymity Score: {result['security_analysis'].get('anonymity_score', 0)}/100")
        else:
            print(f"    Error: {result.get('error', 'Unknown error')}")


def main():
    """Main application entry point"""
    print_banner()
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load target addresses
    addresses = load_target_addresses()
    
    # Add default DuckDuckGo onion if no addresses found
    if not addresses:
        print("📝 Using default DuckDuckGo onion address for testing")
        addresses = ["https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/"]
    
    # Run connectivity test
    if not run_connectivity_test():
        print("\n❌ Connectivity test failed. Please check your Tor installation.")
        return 1
    
    # Get current Tor IP for reporting
    analyzer = TorAnalyzer()
    tor_ip = analyzer.get_tor_ip() if run_connectivity_test() else None
    
    # Run enhanced analysis
    results = run_enhanced_analysis(addresses)
    
    # Display summary
    display_summary(results)
    
    # Generate comprehensive reports
    print("\n" + "="*60)
    print("📊 GENERATING ANALYSIS REPORTS")
    print("="*60)
    
    try:
        report_generator = TorAnalysisReportGenerator()
        report_files = report_generator.generate_report(
            results, 
            connectivity_test=run_connectivity_test(), 
            tor_ip=tor_ip
        )
        
        print("\n📁 Reports generated successfully:")
        for report_type, file_path in report_files.items():
            print(f"   • {report_type.replace('_', ' ').title()}: {file_path}")
        
        print(f"\n💾 All reports saved to: {Path('results').absolute()}")
        
    except Exception as e:
        print(f"\n⚠️ Warning: Report generation failed: {e}")
        print("Analysis completed but reports could not be saved.")
    
    print(f"\n🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

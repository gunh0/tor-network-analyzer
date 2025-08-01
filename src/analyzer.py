import requests
from bs4 import BeautifulSoup
import socket
import time
import re
import hashlib
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin, urlparse


class TorAnalyzer:
    """Tor network analyzer for testing .onion sites connectivity and analysis"""
    
    def __init__(self, proxy_host: str = "127.0.0.1", proxy_port: int = 9050):
        """
        Initialize TorAnalyzer
        
        Args:
            proxy_host: Tor SOCKS5 proxy host (default: 127.0.0.1)
            proxy_port: Tor SOCKS5 proxy port (default: 9050)
        """
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.session = None
        self._setup_session()
    
    def _setup_session(self) -> None:
        """Setup requests session with Tor proxy configuration"""
        self.session = requests.Session()
        # Configure Tor SOCKS5 proxy. 'socks5h' ensures DNS resolution is done through the proxy.
        proxy_url = f"socks5h://{self.proxy_host}:{self.proxy_port}"
        self.session.proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        
        # Set user agent to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def test_tor_proxy(self) -> bool:
        """
        Test if Tor proxy is accessible
        
        Returns:
            bool: True if proxy is accessible, False otherwise
        """
        try:
            # Try to connect to the SOCKS5 proxy
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.proxy_host, self.proxy_port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def analyze_site(self, url: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Analyze a .onion site
        
        Args:
            url: The .onion URL to analyze
            timeout: Request timeout in seconds
            
        Returns:
            Dict containing analysis results
        """
        result = {
            'success': False,
            'url': url,
            'status_code': None,
            'title': None,
            'content_length': None,
            'response_headers': None,
            'error': None,
            'server_info': None
        }
        
        try:
            response = self.session.get(url, timeout=timeout)
            result['status_code'] = response.status_code
            result['response_headers'] = dict(response.headers)
            result['content_length'] = len(response.content)
            
            if response.status_code == 200:
                # Parse HTML content
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract title
                if soup.title:
                    result['title'] = soup.title.string.strip()
                else:
                    result['title'] = "No title found"
                
                # Extract server information
                result['server_info'] = response.headers.get('Server', 'Unknown')
                
                result['success'] = True
            else:
                result['error'] = f"HTTP {response.status_code}"
                
        except requests.exceptions.ConnectTimeout:
            result['error'] = "Connection timeout"
        except requests.exceptions.ReadTimeout:
            result['error'] = "Read timeout"
        except requests.exceptions.ConnectionError as e:
            result['error'] = f"Connection error: {str(e)}"
        except requests.exceptions.RequestException as e:
            result['error'] = f"Request error: {str(e)}"
        except Exception as e:
            result['error'] = f"Unexpected error: {str(e)}"
        
        return result
    
    def get_tor_ip(self) -> Optional[str]:
        """
        Get current Tor exit node IP address
        
        Returns:
            str: Current IP address or None if failed
        """
        try:
            response = self.session.get('http://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                return response.json().get('origin')
        except Exception:
            pass
        return None
    
    def analyze_onion_structure(self, url: str) -> Dict[str, Any]:
        """
        Analyze .onion URL structure and extract information
        
        Args:
            url: The .onion URL to analyze
            
        Returns:
            Dict containing onion structure analysis
        """
        parsed = urlparse(url)
        onion_address = parsed.netloc
        
        analysis = {
            'onion_address': onion_address,
            'address_length': len(onion_address.replace('.onion', '')),
            'is_v3_onion': len(onion_address.replace('.onion', '')) == 56,  # v3 onions are 56 chars
            'is_v2_onion': len(onion_address.replace('.onion', '')) == 16,  # v2 onions are 16 chars
            'protocol': parsed.scheme,
            'path': parsed.path,
            'has_subdomain': '.' in onion_address.replace('.onion', ''),
            'address_hash': hashlib.sha256(onion_address.encode()).hexdigest()[:16]
        }
        
        return analysis
    
    def test_circuit_diversity(self, test_urls: List[str] = None) -> Dict[str, Any]:
        """
        Test Tor circuit diversity by checking exit node IPs
        
        Args:
            test_urls: List of test URLs to check IP diversity
            
        Returns:
            Dict containing circuit diversity analysis
        """
        if not test_urls:
            test_urls = [
                'http://httpbin.org/ip',
                'https://check.torproject.org/api/ip',
                'http://icanhazip.com'
            ]
        
        exit_ips = []
        successful_tests = 0
        
        for url in test_urls:
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    # Extract IP from different response formats
                    if 'httpbin.org' in url:
                        ip = response.json().get('origin', '').split(',')[0].strip()
                    elif 'torproject.org' in url:
                        ip = response.json().get('IP', '')
                    else:
                        ip = response.text.strip()
                    
                    if ip and ip not in exit_ips:
                        exit_ips.append(ip)
                    successful_tests += 1
                    
                    # Wait between requests to allow circuit changes
                    time.sleep(2)
            except Exception:
                continue
        
        return {
            'unique_exit_ips': len(exit_ips),
            'total_tests': len(test_urls),
            'successful_tests': successful_tests,
            'exit_ips': exit_ips,
            'circuit_diversity_score': len(exit_ips) / successful_tests if successful_tests > 0 else 0
        }
    
    def analyze_hidden_service_security(self, url: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze security aspects of a hidden service
        
        Args:
            url: The analyzed URL
            result: Previous analysis result
            
        Returns:
            Dict containing security analysis
        """
        security_analysis = {
            'https_enabled': url.startswith('https://'),
            'security_headers': {},
            'potential_vulnerabilities': [],
            'anonymity_score': 0
        }
        
        if result.get('success') and result.get('response_headers'):
            headers = result['response_headers']
            
            # Check security headers
            security_headers = {
                'Strict-Transport-Security': headers.get('Strict-Transport-Security'),
                'X-Frame-Options': headers.get('X-Frame-Options'),
                'X-Content-Type-Options': headers.get('X-Content-Type-Options'),
                'Content-Security-Policy': headers.get('Content-Security-Policy'),
                'X-XSS-Protection': headers.get('X-XSS-Protection')
            }
            
            security_analysis['security_headers'] = {k: v for k, v in security_headers.items() if v}
            
            # Calculate anonymity score based on various factors
            score = 50  # Base score
            
            if security_analysis['https_enabled']:
                score += 20
            
            if security_headers.get('Strict-Transport-Security'):
                score += 10
            
            if not headers.get('Server') or headers.get('Server') == 'Unknown':
                score += 10  # Server header obfuscation
            
            if len(security_analysis['security_headers']) >= 3:
                score += 10
            
            security_analysis['anonymity_score'] = min(score, 100)
        
        return security_analysis
    
    def close(self) -> None:
        """Close the session"""
        if self.session:
            self.session.close()


# Legacy function for backward compatibility
def get_tor_session():
    """Legacy function - use TorAnalyzer class instead"""
    analyzer = TorAnalyzer()
    return analyzer.session


def main():
    """Legacy main function - use main.py instead"""
    print("⚠ This module is now imported by main.py")
    print("Please run: python main.py")


if __name__ == "__main__":
    main()

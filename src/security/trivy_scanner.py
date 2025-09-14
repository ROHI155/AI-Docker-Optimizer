import subprocess
import json

class TrivyScanner:
    @staticmethod
    def scan_image(image_name):
        """Run Trivy scan on Docker image and return vulnerabilities"""
        try:
            result = subprocess.run([
                'trivy', 'image', '--format', 'json', image_name
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {'error': result.stderr}
                
        except subprocess.TimeoutExpired:
            return {'error': 'Trivy scan timed out'}
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def compare_vulnerabilities(original_scan, optimized_scan):
        """Compare vulnerability counts between scans"""
        orig_vulns = original_scan.get('Results', [{}])[0].get('Vulnerabilities', [])
        opt_vulns = optimized_scan.get('Results', [{}])[0].get('Vulnerabilities', [])
        
        return {
            'original_vulnerabilities': len(orig_vulns),
            'optimized_vulnerabilities': len(opt_vulns),
            'vulnerabilities_fixed': len(orig_vulns) - len(opt_vulns)
        }
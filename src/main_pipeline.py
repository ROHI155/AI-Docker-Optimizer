from analysis.dockerfile_parser import DockerfileParser
from analysis.ai_suggestor import GroqAISuggestor
from optimization.dockerfile_rewriter import DockerfileRewriter
from optimization.image_builder import ImageBuilder
from security.trivy_scanner import TrivyScanner
import os
import json
from datetime import datetime

def run_optimization_pipeline():
    print("🚀 Starting Docker Optimization Pipeline")
    print("=" * 60)
    
    # Check if Dockerfile exists
    if not os.path.exists('Dockerfile'):
        print("❌ Error: Dockerfile not found in current directory")
        print("   Please make sure you're running this from a directory with a Dockerfile")
        return
    
    # Step 1: AI Analysis
    print("1. 🤖 AI Analysis...")
    parser = DockerfileParser('Dockerfile')
    suggestor = GroqAISuggestor()
    ai_result = suggestor.get_suggestions('Dockerfile')
    
    if "error" in ai_result:
        print(f"❌ AI Error: {ai_result['error']}")
        return
    
    # Step 2: Dockerfile Optimization
    print("2. 🔧 Rewriting Dockerfile...")
    rewriter = DockerfileRewriter('Dockerfile')
    original_lines = rewriter.read_dockerfile()
    optimized_lines = rewriter.apply_optimizations(original_lines, ai_result['suggestions'])
    optimized_path = rewriter.write_optimized_dockerfile(optimized_lines)
    
    # Step 3: Build Images
    print("3. 🏗️ Building images...")
    builder = ImageBuilder()
    
    print("   Building original image...")
    original_stats = builder.build_image('Dockerfile', 'original-image')
    
    print("   Building optimized image...")
    optimized_stats = builder.build_image(optimized_path, 'optimized-image')
    
    if not original_stats['success']:
        print(f"❌ Original build failed: {original_stats['error']}")
        return
    if not optimized_stats['success']:
        print(f"❌ Optimized build failed: {optimized_stats['error']}")
        return
    
    # Step 4: Security Scan (Optional)
    print("5. 🔒 Security scanning...")
    scanner = TrivyScanner()
    original_scan = scanner.scan_image('original-image')
    optimized_scan = scanner.scan_image('optimized-image')
    
    vuln_comparison = scanner.compare_vulnerabilities(original_scan, optimized_scan)
    
    # Step 5: Generate Report
    print("6. 📊 Generating report...")
    report = {
        'timestamp': datetime.now().isoformat(),
        'original_image': {
            'size_mb': original_stats['size_mb'],
            'build_time_seconds': original_stats['build_time']
        },
        'optimized_image': {
            'size_mb': optimized_stats['size_mb'],
            'build_time_seconds': optimized_stats['build_time']
        },
        'improvements': builder.compare_images(original_stats, optimized_stats),
        'security_improvements': vuln_comparison,
        'ai_suggestions': ai_result['suggestions'][:500] + "..." if len(ai_result['suggestions']) > 500 else ai_result['suggestions']
    }
    
    # Save report
    with open('optimization_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n✅ OPTIMIZATION COMPLETE!")
    print("=" * 60)
    print(f"📦 Size: {original_stats['size_mb']}MB → {optimized_stats['size_mb']}MB")
    print(f"   Reduction: {report['improvements']['size_reduction_percent']}% ({report['improvements']['size_reduction_mb']}MB)")
    print(f"⏱️  Build Time: {original_stats['build_time']}s → {optimized_stats['build_time']}s")
    print(f"   Time Saved: {report['improvements']['time_saved_seconds']}s ({report['improvements']['time_saved_percent']}%)")
    
    if 'error' not in vuln_comparison:
        print(f"🔒 Vulnerabilities: {vuln_comparison['original_vulnerabilities']} → {vuln_comparison['optimized_vulnerabilities']}")
        print(f"   Fixed: {vuln_comparison['vulnerabilities_fixed']}")
    
    print("=" * 60)
    print("📄 Full report saved to: optimization_report.json")
    
    return report

if __name__ == "__main__":
    run_optimization_pipeline()
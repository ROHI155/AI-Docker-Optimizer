import docker
import time
import os

class ImageBuilder:
    def __init__(self):
        self.client = docker.from_env()
        
    def build_image(self, dockerfile_path, tag_name):
        """Build image and return size & build time"""
        start_time = time.time()
        
        try:
            # Get the directory containing the Dockerfile
            build_context = os.path.dirname(os.path.abspath(dockerfile_path))
            if not build_context:  # If Dockerfile is in current directory
                build_context = '.'
                
            image, logs = self.client.images.build(
                path=build_context,  # Use the directory as build context
                dockerfile=os.path.basename(dockerfile_path),
                tag=tag_name,
                rm=True,
                forcerm=True
            )
            
            build_time = time.time() - start_time
            image_size = image.attrs['Size']
            
            return {
                'image': image,
                'build_time': round(build_time, 2),
                'size_bytes': image_size,
                'size_mb': round(image_size / (1024 * 1024), 2),
                'success': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'build_time': 0,
                'size_mb': 0
            }
    
    def compare_images(self, original_stats, optimized_stats):
        """Compare before/after metrics"""
        if not original_stats['success'] or not optimized_stats['success']:
            return {'error': 'Build failed'}
        
        return {
            'size_reduction_mb': round(original_stats['size_mb'] - optimized_stats['size_mb'], 2),
            'size_reduction_percent': round((1 - optimized_stats['size_mb'] / original_stats['size_mb']) * 100, 2),
            'time_saved_seconds': round(original_stats['build_time'] - optimized_stats['build_time'], 2),
            'time_saved_percent': round((1 - optimized_stats['build_time'] / original_stats['build_time']) * 100, 2)
        }
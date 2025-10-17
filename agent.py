#!/usr/bin/env python3
import os
import sys
import time
import json
import socket
import psutil
import logging
from datetime import datetime

# Configuration from environment
API_KEY = os.getenv('CHECKLOGS_API_KEY')
API_HOST = os.getenv('CHECKLOGS_API_HOST', 'api.checklogs.dev')
API_PORT = int(os.getenv('CHECKLOGS_API_PORT', 9876))
SERVER_NAME = os.getenv('SERVER_NAME', socket.gethostname())
COLLECT_INTERVAL = int(os.getenv('COLLECT_INTERVAL', 10))

# Feature flags
COLLECT_CPU = os.getenv('COLLECT_CPU', 'true').lower() == 'true'
COLLECT_RAM = os.getenv('COLLECT_RAM', 'true').lower() == 'true'
COLLECT_DISK = os.getenv('COLLECT_DISK', 'true').lower() == 'true'
COLLECT_LOAD = os.getenv('COLLECT_LOAD', 'true').lower() == 'true'
COLLECT_PROCESSES = os.getenv('COLLECT_PROCESSES', 'true').lower() == 'true'
TOP_PROCESSES_COUNT = int(os.getenv('TOP_PROCESSES_COUNT', 10))

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_config():
    """Validate required configuration"""
    if not API_KEY:
        logger.error("❌ CHECKLOGS_API_KEY is required!")
        sys.exit(1)
    if not API_PORT:
        logger.error("❌ CHECKLOGS_API_PORT is required!")
        sys.exit(1)
    
    logger.info(f"✓ Configuration valid")
    logger.info(f"✓ API Key: {API_KEY[:8]}...")
    logger.info(f"✓ API Host: {API_HOST}:{API_PORT}")
    logger.info(f"✓ Server Name: {SERVER_NAME}")
    logger.info(f"✓ Collect Interval: {COLLECT_INTERVAL}s")

def collect_cpu_metrics():
    """Collect CPU metrics"""
    if not COLLECT_CPU:
        return None
    
    try:
        cpu_times = psutil.cpu_times_percent(interval=1)
        return {
            'usage_percent': psutil.cpu_percent(interval=None),
            'user_percent': cpu_times.user,
            'system_percent': cpu_times.system,
            'idle_percent': cpu_times.idle,
            'iowait_percent': getattr(cpu_times, 'iowait', 0)
        }
    except Exception as e:
        logger.error(f"Error collecting CPU metrics: {e}")
        return None

def collect_ram_metrics():
    """Collect RAM metrics"""
    if not COLLECT_RAM:
        return None
    
    try:
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total_mb': round(mem.total / 1024 / 1024, 2),
            'used_mb': round(mem.used / 1024 / 1024, 2),
            'free_mb': round(mem.free / 1024 / 1024, 2),
            'available_mb': round(mem.available / 1024 / 1024, 2),
            'usage_percent': mem.percent,
            'cached_mb': round(getattr(mem, 'cached', 0) / 1024 / 1024, 2),
            'buffers_mb': round(getattr(mem, 'buffers', 0) / 1024 / 1024, 2),
            'swap_total_mb': round(swap.total / 1024 / 1024, 2),
            'swap_used_mb': round(swap.used / 1024 / 1024, 2)
        }
    except Exception as e:
        logger.error(f"Error collecting RAM metrics: {e}")
        return None

def collect_disk_metrics():
    """Collect disk metrics"""
    if not COLLECT_DISK:
        return None
    
    try:
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'mount_point': partition.mountpoint,
                    'device': partition.device,
                    'filesystem': partition.fstype,
                    'total_gb': round(usage.total / 1024 / 1024 / 1024, 2),
                    'used_gb': round(usage.used / 1024 / 1024 / 1024, 2),
                    'free_gb': round(usage.free / 1024 / 1024 / 1024, 2),
                    'usage_percent': usage.percent,
                    'inodes_total': 0,
                    'inodes_used': 0,
                    'inodes_percent': 0
                })
            except PermissionError:
                continue
        return disks
    except Exception as e:
        logger.error(f"Error collecting disk metrics: {e}")
        return None

def collect_load_metrics():
    """Collect load average metrics"""
    if not COLLECT_LOAD:
        return None
    
    try:
        load = os.getloadavg()
        return {
            'load_1min': round(load[0], 2),
            'load_5min': round(load[1], 2),
            'load_15min': round(load[2], 2)
        }
    except Exception as e:
        logger.error(f"Error collecting load metrics: {e}")
        return None

def collect_uptime_metrics():
    """Collect uptime metrics"""
    try:
        boot_time = psutil.boot_time()
        uptime_seconds = int(time.time() - boot_time)
        
        return {
            'uptime_seconds': uptime_seconds,
            'boot_time': int(boot_time)
        }
    except Exception as e:
        logger.error(f"Error collecting uptime metrics: {e}")
        return None

def collect_process_metrics():
    """Collect top processes by CPU and memory"""
    if not COLLECT_PROCESSES:
        return None
    
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info', 'memory_percent', 'status', 'username']):
            try:
                info = proc.info
                processes.append({
                    'pid': info['pid'],
                    'name': info['name'],
                    'cmdline': ' '.join(info['cmdline'][:3]) if info['cmdline'] else '',
                    'cpu_percent': round(info['cpu_percent'], 2),
                    'ram_mb': round(info['memory_info'].rss / 1024 / 1024, 2),
                    'ram_percent': round(info['memory_percent'], 2),
                    'status': info['status'],
                    'username': info.get('username', 'unknown')
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage and get top processes
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        return processes[:TOP_PROCESSES_COUNT]
    
    except Exception as e:
        logger.error(f"Error collecting process metrics: {e}")
        return None

def send_metrics(metrics):
    """Send metrics via UDP"""
    try:
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Convert metrics to JSON
        data = json.dumps(metrics).encode('utf-8')
        
        # Send to API
        sock.sendto(data, (API_HOST, API_PORT))
        sock.close()
        
        logger.info(f"📦 Sent {len(data)} bytes to {API_HOST}:{API_PORT}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error sending metrics: {e}")
        return False

def collect_and_send():
    """Collect all metrics and send them"""
    try:
        metrics = {
            'api_key': API_KEY,
            'server_name': SERVER_NAME,
            'timestamp': int(time.time())
        }
        
        # Collect all metrics
        cpu = collect_cpu_metrics()
        if cpu:
            metrics['cpu'] = cpu
        
        ram = collect_ram_metrics()
        if ram:
            metrics['ram'] = ram
        
        disk = collect_disk_metrics()
        if disk:
            metrics['disk'] = disk
        
        load = collect_load_metrics()
        if load:
            metrics['load'] = load
        
        uptime = collect_uptime_metrics()
        if uptime:
            metrics['uptime'] = uptime
        
        processes = collect_process_metrics()
        if processes:
            metrics['processes'] = processes
        
        # Send metrics
        return send_metrics(metrics)
        
    except Exception as e:
        logger.error(f"Error in collect_and_send: {e}")
        return False

def main():
    """Main loop"""
    logger.info("🚀 CheckLogs Agent starting...")
    
    # Validate configuration
    validate_config()
    
    logger.info("✓ Agent started successfully")
    logger.info(f"📊 Collecting metrics every {COLLECT_INTERVAL} seconds")
    
    # Main loop
    while True:
        try:
            success = collect_and_send()
            if success:
                logger.debug("✓ Metrics collected and sent")
            else:
                logger.warning("⚠ Failed to send metrics")
            
            time.sleep(COLLECT_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("🛑 Agent stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(COLLECT_INTERVAL)

if __name__ == '__main__':
    main()
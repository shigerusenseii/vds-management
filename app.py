from flask import Flask, render_template_string, jsonify, request
import psutil
import platform
import os
from datetime import datetime
import json
import time

app = Flask(__name__)

TRANSLATIONS = {
    'en': {
        'dashboard': 'Dashboard',
        'system_monitor': 'System Monitor',
        'process_manager': 'Process Manager',
        'file_manager': 'File Manager',
        'network_monitor': 'Network Monitor',
        'disk_manager': 'Disk Manager',
        'services': 'Services Manager',
        'logs': 'System Logs',
        'security': 'Security & Firewall',
        'backup': 'Backup & Restore',
        'settings': 'Settings',
        'cpu_usage': 'CPU Usage',
        'ram_usage': 'RAM Usage',
        'network_usage': 'Network Usage',
        'disk_usage': 'Disk Usage',
        'uptime': 'System Uptime',
        'total': 'Total',
        'used': 'Used',
        'free': 'Free',
        'available': 'Available',
        'days': 'days',
        'hours': 'hours',
        'minutes': 'minutes',
        'system_info': 'System Information',
        'os': 'Operating System',
        'processor': 'Processor',
        'cores': 'Cores',
        'active_processes': 'Active Processes',
        'disk_partitions': 'Disk Partitions',
        'sent': 'Sent',
        'received': 'Received',
        'quick_actions': 'Quick Actions',
        'restart_service': 'Restart Service',
        'clear_cache': 'Clear Cache',
        'backup_system': 'Backup System',
        'update_system': 'Update System',
        'process_name': 'Process Name',
        'pid': 'PID',
        'cpu': 'CPU',
        'memory': 'Memory',
        'status': 'Status',
        'kill_process': 'Kill',
        'current_directory': 'Current Directory',
        'name': 'Name',
        'size': 'Size',
        'modified': 'Modified',
        'type': 'Type',
        'actions': 'Actions',
        'upload_file': 'Upload File',
        'create_folder': 'New Folder',
        'refresh': 'Refresh',
        'connections': 'Active Connections',
        'bandwidth': 'Bandwidth Usage',
        'interface': 'Interface',
        'ip_address': 'IP Address',
        'service_name': 'Service Name',
        'service_status': 'Status',
        'start': 'Start',
        'stop': 'Stop',
        'restart': 'Restart',
        'running': 'Running',
        'stopped': 'Stopped',
        'recent_logs': 'Recent System Logs',
        'timestamp': 'Timestamp',
        'level': 'Level',
        'message': 'Message',
        'temperature': 'Temperature',
        'fan_speed': 'Fan Speed'
    },
    'tr': {
        'dashboard': 'Kontrol Paneli',
        'system_monitor': 'Sistem İzleyici',
        'process_manager': 'İşlem Yöneticisi',
        'file_manager': 'Dosya Yöneticisi',
        'network_monitor': 'Ağ İzleyici',
        'disk_manager': 'Disk Yöneticisi',
        'services': 'Servis Yöneticisi',
        'logs': 'Sistem Günlükleri',
        'security': 'Güvenlik & Firewall',
        'backup': 'Yedekleme & Geri Yükleme',
        'settings': 'Ayarlar',
        'cpu_usage': 'CPU Kullanımı',
        'ram_usage': 'RAM Kullanımı',
        'network_usage': 'Ağ Kullanımı',
        'disk_usage': 'Disk Kullanımı',
        'uptime': 'Sistem Çalışma Süresi',
        'total': 'Toplam',
        'used': 'Kullanılan',
        'free': 'Boş',
        'available': 'Kullanılabilir',
        'days': 'gün',
        'hours': 'saat',
        'minutes': 'dakika',
        'system_info': 'Sistem Bilgisi',
        'os': 'İşletim Sistemi',
        'processor': 'İşlemci',
        'cores': 'Çekirdek',
        'active_processes': 'Aktif İşlemler',
        'disk_partitions': 'Disk Bölümleri',
        'sent': 'Gönderilen',
        'received': 'Alınan',
        'quick_actions': 'Hızlı İşlemler',
        'restart_service': 'Servisi Yeniden Başlat',
        'clear_cache': 'Önbelleği Temizle',
        'backup_system': 'Sistem Yedeği Al',
        'update_system': 'Sistemi Güncelle',
        'process_name': 'İşlem Adı',
        'pid': 'PID',
        'cpu': 'CPU',
        'memory': 'Bellek',
        'status': 'Durum',
        'kill_process': 'Sonlandır',
        'current_directory': 'Mevcut Dizin',
        'name': 'Ad',
        'size': 'Boyut',
        'modified': 'Değiştirilme',
        'type': 'Tür',
        'actions': 'İşlemler',
        'upload_file': 'Dosya Yükle',
        'create_folder': 'Yeni Klasör',
        'refresh': 'Yenile',
        'connections': 'Aktif Bağlantılar',
        'bandwidth': 'Bant Genişliği Kullanımı',
        'interface': 'Arayüz',
        'ip_address': 'IP Adresi',
        'service_name': 'Servis Adı',
        'service_status': 'Durum',
        'start': 'Başlat',
        'stop': 'Durdur',
        'restart': 'Yeniden Başlat',
        'running': 'Çalışıyor',
        'stopped': 'Durduruldu',
        'recent_logs': 'Son Sistem Günlükleri',
        'timestamp': 'Zaman',
        'level': 'Seviye',
        'message': 'Mesaj',
        'temperature': 'Sıcaklık',
        'fan_speed': 'Fan Hızı'
    }
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VDS Management Panel</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg-primary: #0a0a1a;
            --bg-secondary: #13131f;
            --bg-tertiary: #1c1c2e;
            --bg-hover: #25254a;
            --text-primary: #ffffff;
            --text-secondary: #a0a0b8;
            --text-muted: #6b6b8a;
            --accent-primary: #6366f1;
            --accent-secondary: #8b5cf6;
            --accent-hover: #7c3aed;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #3b82f6;
            --border: #2d2d4a;
            --shadow: rgba(0, 0, 0, 0.3);
            --shadow-lg: rgba(0, 0, 0, 0.5);
        }

        .light-theme {
            --bg-primary: #f8fafc;
            --bg-secondary: #ffffff;
            --bg-tertiary: #f1f5f9;
            --bg-hover: #e2e8f0;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #94a3b8;
            --accent-primary: #6366f1;
            --accent-secondary: #8b5cf6;
            --accent-hover: #7c3aed;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #3b82f6;
            --border: #e2e8f0;
            --shadow: rgba(15, 23, 42, 0.05);
            --shadow-lg: rgba(15, 23, 42, 0.1);
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            transition: all 0.3s ease;
            overflow-x: hidden;
        }

        .container {
            display: flex;
            min-height: 100vh;
        }

        .sidebar {
            width: 280px;
            background: var(--bg-secondary);
            border-right: 1px solid var(--border);
            padding: 2rem 0;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            transition: all 0.3s ease;
            z-index: 1000;
        }

        .sidebar::-webkit-scrollbar {
            width: 6px;
        }

        .sidebar::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }

        .sidebar::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 3px;
        }

        .logo {
            padding: 0 1.5rem;
            margin-bottom: 2.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
        }

        .logo h1 {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .nav-menu {
            list-style: none;
        }

        .nav-item {
            margin-bottom: 0.25rem;
        }

        .nav-link {
            display: flex;
            align-items: center;
            padding: 0.875rem 1.5rem;
            color: var(--text-secondary);
            text-decoration: none;
            transition: all 0.3s ease;
            position: relative;
            cursor: pointer;
        }

        .nav-link:hover {
            color: var(--text-primary);
            background: var(--bg-tertiary);
        }

        .nav-link.active {
            color: var(--text-primary);
            background: var(--bg-tertiary);
        }

        .nav-link.active::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, var(--accent-primary), var(--accent-secondary));
        }

        .nav-icon {
            width: 20px;
            margin-right: 0.875rem;
            text-align: center;
            font-size: 1rem;
        }

        .main-content {
            flex: 1;
            margin-left: 280px;
            padding: 2rem;
            min-height: 100vh;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            background: var(--bg-secondary);
            padding: 1.5rem 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 12px var(--shadow);
        }

        .header-title h2 {
            font-size: 1.875rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .header-subtitle {
            color: var(--text-secondary);
            font-size: 0.875rem;
        }

        .header-controls {
            display: flex;
            gap: 0.75rem;
            align-items: center;
        }

        .btn-icon {
            background: var(--bg-tertiary);
            color: var(--text-primary);
            width: 42px;
            height: 42px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid var(--border);
        }

        .btn-icon:hover {
            background: var(--bg-hover);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px var(--shadow);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: var(--bg-secondary);
            padding: 1.75rem;
            border-radius: 16px;
            box-shadow: 0 4px 12px var(--shadow);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            border: 1px solid var(--border);
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
        }

        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px var(--shadow-lg);
            border-color: var(--accent-primary);
        }

        .stat-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }

        .stat-title {
            color: var(--text-secondary);
            font-size: 0.8125rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .stat-icon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: white;
            font-size: 1.25rem;
        }

        .stat-value {
            font-size: 2.25rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, var(--text-primary), var(--text-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stat-label {
            color: var(--text-muted);
            font-size: 0.875rem;
        }

        .progress-bar {
            width: 100%;
            height: 6px;
            background: var(--bg-tertiary);
            border-radius: 3px;
            overflow: hidden;
            margin-top: 1rem;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            border-radius: 3px;
            transition: width 0.5s ease;
        }

        .content-card {
            background: var(--bg-secondary);
            padding: 1.75rem;
            border-radius: 16px;
            box-shadow: 0 4px 12px var(--shadow);
            margin-bottom: 1.5rem;
            border: 1px solid var(--border);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
        }

        .card-actions {
            display: flex;
            gap: 0.5rem;
        }

        .table-container {
            overflow-x: auto;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
        }

        .data-table thead {
            background: var(--bg-tertiary);
        }

        .data-table th {
            padding: 0.875rem 1rem;
            text-align: left;
            font-size: 0.8125rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .data-table td {
            padding: 1rem;
            border-top: 1px solid var(--border);
            font-size: 0.875rem;
        }

        .data-table tbody tr {
            transition: all 0.2s ease;
        }

        .data-table tbody tr:hover {
            background: var(--bg-tertiary);
        }

        .btn {
            padding: 0.625rem 1.25rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
            font-size: 0.875rem;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px var(--shadow);
        }

        .btn-danger {
            background: var(--danger);
            color: white;
        }

        .btn-sm {
            padding: 0.5rem 0.875rem;
            font-size: 0.8125rem;
        }

        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .badge-success {
            background: rgba(16, 185, 129, 0.15);
            color: var(--success);
        }

        .badge-danger {
            background: rgba(239, 68, 68, 0.15);
            color: var(--danger);
        }

        .badge-warning {
            background: rgba(245, 158, 11, 0.15);
            color: var(--warning);
        }

        .badge-info {
            background: rgba(59, 130, 246, 0.15);
            color: var(--info);
        }

        .file-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
        }

        .file-item {
            background: var(--bg-tertiary);
            padding: 1.25rem;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid var(--border);
            text-align: center;
        }

        .file-item:hover {
            background: var(--bg-hover);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px var(--shadow);
        }

        .file-icon {
            font-size: 2.5rem;
            margin-bottom: 0.75rem;
        }

        .file-name {
            font-weight: 500;
            margin-bottom: 0.25rem;
            word-break: break-all;
        }

        .file-size {
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .page-section {
            display: none;
        }

        .page-section.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .toast-container {
            position: fixed;
            top: 2rem;
            right: 2rem;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .toast {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem 1.25rem;
            min-width: 300px;
            max-width: 400px;
            box-shadow: 0 8px 24px var(--shadow-lg);
            display: flex;
            align-items: center;
            gap: 0.875rem;
            animation: slideIn 0.3s ease;
        }

        .toast-success {
            border-left: 4px solid var(--success);
        }

        .toast-error {
            border-left: 4px solid var(--danger);
        }

        .toast-warning {
            border-left: 4px solid var(--warning);
        }

        .toast-info {
            border-left: 4px solid var(--info);
        }

        .toast-icon {
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
        }

        .toast-content {
            flex: 1;
        }

        .toast-title {
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .toast-message {
            font-size: 0.875rem;
            color: var(--text-secondary);
        }

        .toast-close {
            cursor: pointer;
            opacity: 0.5;
            transition: opacity 0.2s;
        }

        .toast-close:hover {
            opacity: 1;
        }

        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }

        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 9998;
        }

        .modal-overlay.active {
            display: flex;
        }

        .modal {
            background: var(--bg-secondary);
            border-radius: 16px;
            padding: 2rem;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 20px 60px var(--shadow-lg);
            border: 1px solid var(--border);
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }

        .modal-title {
            font-size: 1.5rem;
            font-weight: 600;
        }

        .modal-close {
            cursor: pointer;
            font-size: 1.5rem;
            opacity: 0.5;
            transition: opacity 0.2s;
        }

        .modal-close:hover {
            opacity: 1;
        }

        .modal-body {
            margin-bottom: 1.5rem;
        }

        .form-group {
            margin-bottom: 1rem;
        }

        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            font-size: 0.875rem;
        }

        .form-input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--bg-tertiary);
            color: var(--text-primary);
            font-size: 0.875rem;
            transition: all 0.2s;
        }

        .form-input:focus {
            outline: none;
            border-color: var(--accent-primary);
        }

        .form-select {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--bg-tertiary);
            color: var(--text-primary);
            font-size: 0.875rem;
            cursor: pointer;
        }

        .modal-footer {
            display: flex;
            gap: 0.75rem;
            justify-content: flex-end;
        }

        .context-menu {
            position: fixed;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.5rem 0;
            box-shadow: 0 8px 24px var(--shadow-lg);
            z-index: 9999;
            display: none;
            min-width: 180px;
        }

        .context-menu.active {
            display: block;
        }

        .context-menu-item {
            padding: 0.75rem 1rem;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 0.875rem;
        }

        .context-menu-item:hover {
            background: var(--bg-tertiary);
        }

        .context-menu-divider {
            height: 1px;
            background: var(--border);
            margin: 0.5rem 0;
        }

        @media (max-width: 768px) {
            .sidebar {
                transform: translateX(-100%);
            }

            .sidebar.active {
                transform: translateX(0);
            }

            .main-content {
                margin-left: 0;
            }

            .stats-grid {
                grid-template-columns: 1fr;
            }

            .toast-container {
                left: 1rem;
                right: 1rem;
            }

            .toast {
                min-width: auto;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <aside class="sidebar">
            <div class="logo">
                <div class="logo-icon">
                    <i class="fas fa-server"></i>
                </div>
                <h1>VDS Panel</h1>
            </div>
            <nav>
                <ul class="nav-menu">
                    <li class="nav-item">
                        <a class="nav-link active" data-page="dashboard">
                            <i class="fas fa-th-large nav-icon"></i>
                            <span data-lang="dashboard">Dashboard</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-page="monitor">
                            <i class="fas fa-chart-line nav-icon"></i>
                            <span data-lang="system_monitor">System Monitor</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-page="processes">
                            <i class="fas fa-tasks nav-icon"></i>
                            <span data-lang="process_manager">Process Manager</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-page="files">
                            <i class="fas fa-folder-open nav-icon"></i>
                            <span data-lang="file_manager">File Manager</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-page="network">
                            <i class="fas fa-network-wired nav-icon"></i>
                            <span data-lang="network_monitor">Network Monitor</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-page="disk">
                            <i class="fas fa-hdd nav-icon"></i>
                            <span data-lang="disk_manager">Disk Manager</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-page="services">
                            <i class="fas fa-cogs nav-icon"></i>
                            <span data-lang="services">Services Manager</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-page="logs">
                            <i class="fas fa-file-alt nav-icon"></i>
                            <span data-lang="logs">System Logs</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-page="security">
                            <i class="fas fa-shield-alt nav-icon"></i>
                            <span data-lang="security">Security & Firewall</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-page="backup">
                            <i class="fas fa-database nav-icon"></i>
                            <span data-lang="backup">Backup & Restore</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" data-page="settings">
                            <i class="fas fa-sliders-h nav-icon"></i>
                            <span data-lang="settings">Settings</span>
                        </a>
                    </li>
                </ul>
            </nav>
        </aside>

        <main class="main-content">
            <header class="header">
                <div class="header-title">
                    <h2 id="page-title" data-lang="dashboard">Dashboard</h2>
                    <p class="header-subtitle" id="page-subtitle">Real-time system monitoring and management</p>
                </div>
                <div class="header-controls">
                    <div class="btn-icon" id="theme-toggle" title="Toggle Theme">
                        <i class="fas fa-moon"></i>
                    </div>
                    <div class="btn-icon" id="lang-toggle" title="Change Language">
                        <i class="fas fa-globe"></i>
                    </div>
                    <div class="btn-icon" id="refresh-btn" title="Refresh">
                        <i class="fas fa-sync-alt"></i>
                    </div>
                </div>
            </header>

            <div id="dashboard-page" class="page-section active">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-header">
                            <div>
                                <div class="stat-title" data-lang="cpu_usage">CPU Usage</div>
                                <div class="stat-value" id="cpu-value">0%</div>
                                <div class="stat-label" id="cpu-label">Calculating...</div>
                            </div>
                            <div class="stat-icon">
                                <i class="fas fa-microchip"></i>
                            </div>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" id="cpu-progress" style="width: 0%"></div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-header">
                            <div>
                                <div class="stat-title" data-lang="ram_usage">RAM Usage</div>
                                <div class="stat-value" id="ram-value">0%</div>
                                <div class="stat-label" id="ram-label">Calculating...</div>
                            </div>
                            <div class="stat-icon">
                                <i class="fas fa-memory"></i>
                            </div>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" id="ram-progress" style="width: 0%"></div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-header">
                            <div>
                                <div class="stat-title" data-lang="disk_usage">Disk Usage</div>
                                <div class="stat-value" id="disk-value">0%</div>
                                <div class="stat-label" id="disk-label">Calculating...</div>
                            </div>
                            <div class="stat-icon">
                                <i class="fas fa-hdd"></i>
                            </div>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" id="disk-progress" style="width: 0%"></div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-header">
                            <div>
                                <div class="stat-title" data-lang="uptime">System Uptime</div>
                                <div class="stat-value" id="uptime-value">0 days</div>
                                <div class="stat-label" id="uptime-label">System running smoothly</div>
                            </div>
                            <div class="stat-icon">
                                <i class="fas fa-clock"></i>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-header">
                            <div>
                                <div class="stat-title" data-lang="temperature">Temperature</div>
                                <div class="stat-value" id="temp-value">--°C</div>
                                <div class="stat-label">CPU Thermal</div>
                            </div>
                            <div class="stat-icon">
                                <i class="fas fa-thermometer-half"></i>
                            </div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-header">
                            <div>
                                <div class="stat-title">Swap Memory</div>
                                <div class="stat-value" id="swap-value">0%</div>
                                <div class="stat-label" id="swap-label">Swap Usage</div>
                            </div>
                            <div class="stat-icon">
                                <i class="fas fa-exchange-alt"></i>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="content-card">
                    <div class="card-header">
                        <h3 class="card-title" data-lang="system_info">System Information</h3>
                    </div>
                    <div class="table-container">
                        <table class="data-table" style="width: auto;">
                            <tbody>
                                <tr>
                                    <td data-lang="os">Operating System</td>
                                    <td id="os-info">Loading...</td>
                                </tr>
                                <tr>
                                    <td data-lang="processor">Processor</td>
                                    <td id="processor-info">Loading...</td>
                                </tr>
                                <tr>
                                    <td data-lang="cores">Cores</td>
                                    <td id="cores-info">Loading...</td>
                                </tr>
                                <tr>
                                    <td data-lang="active_processes">Active Processes</td>
                                    <td id="processes-count">Loading...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div id="monitor-page" class="page-section">
                <div class="content-card">
                    <div class="card-header">
                        <h3 class="card-title" data-lang="system_monitor">System Monitor</h3>
                    </div>
                    <div class="stats-grid" style="margin-bottom: 1.5rem;">
                        <div class="stat-card">
                            <div class="stat-title" data-lang="cpu_usage">CPU Usage</div>
                            <div class="stat-value" id="monitor-cpu-value">0%</div>
                            <div class="stat-label" id="monitor-cpu-label">...</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-title" data-lang="ram_usage">RAM Usage</div>
                            <div class="stat-value" id="monitor-ram-value">0%</div>
                            <div class="stat-label" id="monitor-ram-label">...</div>
                            <div class="progress-bar" style="margin-top: 0.5rem;">
                                <div class="progress-fill" id="monitor-ram-progress" style="width: 0%"></div>
                            </div>
                        </div>
                    </div>

                    <div class="content-card" style="margin-bottom: 0;">
                        <h4 class="card-title" style="font-size: 1.125rem; margin-bottom: 1rem;">Per-Core CPU Usage</h4>
                        <div id="cpu-cores-list">
                            </div>
                    </div>
                </div>
            </div>

            <div id="processes-page" class="page-section">
                <div class="content-card">
                    <div class="card-header">
                        <h3 class="card-title" data-lang="process_manager">Process Manager</h3>
                        <div class="card-actions">
                            <button class="btn btn-primary btn-sm" id="refresh-processes">
                                <i class="fas fa-sync-alt"></i>
                                <span data-lang="refresh">Refresh</span>
                            </button>
                        </div>
                    </div>
                    <div class="table-container">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th data-lang="process_name">Process Name</th>
                                    <th data-lang="pid">PID</th>
                                    <th data-lang="cpu">CPU %</th>
                                    <th data-lang="memory">Memory</th>
                                    <th data-lang="status">Status</th>
                                    <th data-lang="actions">Actions</th>
                                </tr>
                            </thead>
                            <tbody id="processes-tbody">
                                <tr>
                                    <td colspan="6" style="text-align: center;">Loading processes...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div id="files-page" class="page-section">
                <div class="content-card">
                    <div class="card-header">
                        <h3 class="card-title" data-lang="file_manager">File Manager</h3>
                        <div class="card-actions">
                            <button class="btn btn-primary btn-sm" id="upload-file-btn">
                                <i class="fas fa-upload"></i>
                                <span data-lang="upload_file">Upload File</span>
                            </button>
                            <button class="btn btn-primary btn-sm" id="create-folder-btn">
                                <i class="fas fa-folder-plus"></i>
                                <span data-lang="create_folder">New Folder</span>
                            </button>
                            <button class="btn btn-primary btn-sm" id="refresh-files">
                                <i class="fas fa-sync-alt"></i>
                                <span data-lang="refresh">Refresh</span>
                            </button>
                        </div>
                    </div>
                    <div style="margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                        <button class="btn btn-sm" id="back-btn" disabled>
                            <i class="fas fa-arrow-left"></i>
                        </button>
                        <strong data-lang="current_directory">Current Directory:</strong>
                        <span id="current-path" style="color: var(--accent-primary);">/</span>
                    </div>
                    <div class="file-grid" id="file-grid">
                        <div style="text-align: center; padding: 2rem;">Loading files...</div>
                    </div>
                </div>
            </div>

            <div id="network-page" class="page-section">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-title" data-lang="sent">Data Sent</div>
                        <div class="stat-value" id="net-sent-value">0 MB</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-title" data-lang="received">Data Received</div>
                        <div class="stat-value" id="net-recv-value">0 MB</div>
                    </div>
                </div>

                <div class="content-card">
                    <div class="card-header">
                        <h3 class="card-title" data-lang="connections">Active Connections (Top 15)</h3>
                    </div>
                    <div class="table-container">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th data-lang="type">Type</th>
                                    <th data-lang="ip_address">Local Address</th>
                                    <th data-lang="ip_address">Remote Address</th>
                                    <th data-lang="status">Status</th>
                                </tr>
                            </thead>
                            <tbody id="connections-tbody">
                                <tr>
                                    <td colspan="4" style="text-align: center;">Loading connections...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div id="disk-page" class="page-section">
                <div class="content-card">
                    <div class="card-header">
                        <h3 class="card-title" data-lang="disk_partitions">Disk Partitions</h3>
                    </div>
                    <div class="table-container">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th data-lang="name">Device</th>
                                    <th data-lang="total">Total Size</th>
                                    <th data-lang="used">Used</th>
                                    <th data-lang="free">Free</th>
                                    <th data-lang="disk_usage">Usage %</th>
                                </tr>
                            </thead>
                            <tbody id="disk-tbody">
                                <tr>
                                    <td colspan="5" style="text-align: center;">Loading disk data...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div id="services-page" class="page-section">
                <div class="content-card">
                    <div class="card-header">
                        <h3 class="card-title" data-lang="services">Services Manager (Mock)</h3>
                        <button class="btn btn-primary" id="refresh-services-btn">
                            <i class="fas fa-sync-alt"></i> <span data-lang="refresh">Refresh</span>
                        </button>
                    </div>
                    <div class="table-container">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th data-lang="service_name">Service Name</th>
                                    <th data-lang="service_status">Status</th>
                                    <th data-lang="actions">Actions</th>
                                </tr>
                            </thead>
                            <tbody id="services-tbody">
                                </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div id="logs-page" class="page-section">
                <div class="content-card">
                    <div class="card-header">
                        <h3 class="card-title" data-lang="recent_logs">Recent System Logs (Mock)</h3>
                        <button class="btn btn-primary" id="refresh-logs-btn">
                            <i class="fas fa-sync-alt"></i> <span data-lang="refresh">Refresh</span>
                        </button>
                    </div>
                    <div class="table-container">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th data-lang="timestamp">Timestamp</th>
                                    <th data-lang="level">Level</th>
                                    <th data-lang="message">Message</th>
                                </tr>
                            </thead>
                            <tbody id="logs-tbody">
                                </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div id="security-page" class="page-section">
                <div class="content-card">
                    <div class="card-header">
                        <h3 class="card-title">Firewall Rules (Mock)</h3>
                        <button class="btn btn-primary" id="add-rule-btn">
                            <i class="fas fa-plus"></i> Add Rule
                        </button>
                    </div>
                    <div class="table-container">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Rule Name</th>
                                    <th>Action</th>
                                    <th>Protocol</th>
                                    <th>Port</th>
                                    <th>Source</th>
                                    <th data-lang="status">Status</th>
                                    <th data-lang="actions">Actions</th>
                                </tr>
                            </thead>
                            <tbody id="firewall-tbody">
                                <tr>
                                    <td>Allow HTTP</td>
                                    <td><span class="badge badge-success">ALLOW</span></td>
                                    <td>TCP</td>
                                    <td>80</td>
                                    <td>0.0.0.0/0</td>
                                    <td><span class="badge badge-success">Active</span></td>
                                    <td>
                                        <button class="btn btn-danger btn-sm delete-rule" data-rule="HTTP">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Allow HTTPS</td>
                                    <td><span class="badge badge-success">ALLOW</span></td>
                                    <td>TCP</td>
                                    <td>443</td>
                                    <td>0.0.0.0/0</td>
                                    <td><span class="badge badge-success">Active</span></td>
                                    <td>
                                        <button class="btn btn-danger btn-sm delete-rule" data-rule="HTTPS">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Allow SSH</td>
                                    <td><span class="badge badge-success">ALLOW</span></td>
                                    <td>TCP</td>
                                    <td>22</td>
                                    <td>0.0.0.0/0</td>
                                    <td><span class="badge badge-success">Active</span></td>
                                    <td>
                                        <button class="btn btn-danger btn-sm delete-rule" data-rule="SSH">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div id="backup-page" class="page-section">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-title">Last Backup</div>
                        <div class="stat-value">2 Days Ago</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-title">Backup Size</div>
                        <div class="stat-value">15.7 GB</div>
                    </div>
                </div>

                <div class="content-card">
                    <div class="card-header">
                        <h3 class="card-title">Backup Management</h3>
                        <button class="btn btn-primary" id="create-backup-btn">
                            <i class="fas fa-download"></i> Create Backup Now
                        </button>
                    </div>
                    <p style="color: var(--text-secondary);">Automated backup configuration available here...</p>
                </div>
            </div>

            <div id="settings-page" class="page-section">
                <div class="content-card">
                    <div class="card-header">
                        <h3 class="card-title" data-lang="settings">Settings</h3>
                    </div>
                    <div style="max-width: 600px;">
                        <div style="margin-bottom: 1.5rem;">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Theme Preference</label>
                            <select class="btn" style="width: 100%;" id="theme-select">
                                <option>Dark Theme</option>
                                <option>Light Theme</option>
                            </select>
                        </div>
                        <div style="margin-bottom: 1.5rem;">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Language</label>
                            <select class="btn" style="width: 100%;" id="language-select">
                                <option value="en">English</option>
                                <option value="tr">Türkçe</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <div class="modal-overlay" id="create-folder-modal">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title" data-lang="create_folder">New Folder</h3>
                <span class="modal-close" data-modal="create-folder-modal">×</span>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label" data-lang="name">Folder Name</label>
                    <input type="text" class="form-input" id="folder-name-input" placeholder="Enter folder name">
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn" data-close-modal="create-folder-modal">Cancel</button>
                <button class="btn btn-primary" id="create-folder-submit">Create</button>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="upload-modal">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title" data-lang="upload_file">Upload File</h3>
                <span class="modal-close" data-modal="upload-modal">×</span>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Select File</label>
                    <input type="file" class="form-input" id="file-upload-input">
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn" data-close-modal="upload-modal">Cancel</button>
                <button class="btn btn-primary" id="upload-file-submit">Upload</button>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="add-rule-modal">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title">Add Firewall Rule</h3>
                <span class="modal-close" data-modal="add-rule-modal">×</span>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Rule Name</label>
                    <input type="text" class="form-input" id="rule-name" placeholder="e.g., Allow MySQL">
                </div>
                <div class="form-group">
                    <label class="form-label">Action</label>
                    <select class="form-select" id="rule-action">
                        <option value="allow">ALLOW</option>
                        <option value="deny">DENY</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Protocol</label>
                    <select class="form-select" id="rule-protocol">
                        <option value="tcp">TCP</option>
                        <option value="udp">UDP</option>
                        <option value="all">ALL</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Port</label>
                    <input type="text" class="form-input" id="rule-port" placeholder="e.g., 3306 or *">
                </div>
                <div class="form-group">
                    <label class="form-label">Source IP</label>
                    <input type="text" class="form-input" id="rule-source" placeholder="e.g., 0.0.0.0/0">
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn" data-close-modal="add-rule-modal">Cancel</button>
                <button class="btn btn-primary" id="add-rule-submit">Add Rule</button>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="rename-modal">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title">Rename</h3>
                <span class="modal-close" data-modal="rename-modal">×</span>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">New Name</label>
                    <input type="text" class="form-input" id="rename-input" placeholder="Enter new name">
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn" data-close-modal="rename-modal">Cancel</button>
                <button class="btn btn-primary" id="rename-submit">Rename</button>
            </div>
        </div>
    </div>

    <div class="context-menu" id="context-menu">
        <div class="context-menu-item" id="context-open">
            <i class="fas fa-folder-open"></i> <span data-lang="open">Open</span>
        </div>
        <div class="context-menu-item" id="context-rename">
            <i class="fas fa-i-cursor"></i> <span data-lang="rename">Rename</span>
        </div>
        <div class="context-menu-item" id="context-download">
            <i class="fas fa-download"></i> <span data-lang="download">Download</span>
        </div>
        <div class="context-menu-divider"></div>
        <div class="context-menu-item" id="context-delete" style="color: var(--danger);">
            <i class="fas fa-trash-alt"></i> <span data-lang="delete">Delete</span>
        </div>
    </div>

    <div class="toast-container" id="toast-container">
        </div>

    <script>
        let currentLang = localStorage.getItem('language') || 'en';
        const translations = {{ translations | tojson }};
        // HATA DÜZELTME 5: Python'dan platform bilgisi alındı.
        let serverPlatform = '{{ server_platform }}'; 
        let currentPage = 'dashboard';
        let currentPath = '/';
        let selectedFile = null;
        let lastNetIO = { bytes_sent: 0, bytes_recv: 0, timestamp: Date.now() };


        // Helper Functions
        function formatBytes(bytes) {
            if (bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
        }

        function formatUptime(seconds) {
            const d = Math.floor(seconds / (3600 * 24));
            const h = Math.floor(seconds % (3600 * 24) / 3600);
            const m = Math.floor(seconds % 3600 / 60);

            let parts = [];
            if (d > 0) parts.push(`${d} ${translations[currentLang].days}`);
            if (h > 0) parts.push(`${h} ${translations[currentLang].hours}`);
            if (m > 0 && d === 0) parts.push(`${m} ${translations[currentLang].minutes}`); // Sadece 1 saatten kısaysa dakika göster

            return parts.join(', ') || `1 ${translations[currentLang].minute}`;
        }

        function getFileIcon(filename, isDir) {
            if (isDir) return 'fas fa-folder';
            const ext = filename.split('.').pop().toLowerCase();
            const iconMap = {
                'pdf': 'file-pdf', 'doc': 'file-word', 'docx': 'file-word', 'xls': 'file-excel',
                'xlsx': 'file-excel', 'ppt': 'file-powerpoint', 'pptx': 'file-powerpoint',
                'zip': 'file-archive', 'rar': 'file-archive', '7z': 'file-archive',
                'jpg': 'file-image', 'jpeg': 'file-image', 'png': 'file-image', 'gif': 'file-image',
                'mp4': 'file-video', 'avi': 'file-video', 'mkv': 'file-video',
                'mp3': 'file-audio', 'wav': 'file-audio',
                'txt': 'file-alt', 'log': 'file-alt',
                'html': 'file-code', 'css': 'file-code', 'js': 'file-code', 'py': 'file-code',
            };
            return 'fas fa-' + (iconMap[ext] || 'file');
        }

        function showToast(type, title, message) {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.style.animationName = 'slideIn';
            toast.innerHTML = `
                <div class="toast-icon" style="color: var(--${type});"><i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'times-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i></div>
                <div class="toast-content">
                    <div class="toast-title">${title}</div>
                    <div class="toast-message">${message}</div>
                </div>
                <div class="toast-close"><i class="fas fa-times"></i></div>
            `;
            container.appendChild(toast);

            const closeBtn = toast.querySelector('.toast-close');
            closeBtn.addEventListener('click', () => hideToast(toast));

            setTimeout(() => hideToast(toast), 5000);
        }

        function hideToast(toast) {
            toast.style.animationName = 'slideOut';
            toast.addEventListener('animationend', () => {
                toast.remove();
            }, { once: true });
        }

        function openModal(id) {
            document.getElementById(id).classList.add('active');
        }

        function closeModal(id) {
            document.getElementById(id).classList.remove('active');
        }

        function closeContextMenu() {
            document.getElementById('context-menu').classList.remove('active');
            document.removeEventListener('click', closeContextMenu);
        }

        // Navigation and Data Fetching
        function switchPage(page) {
            document.querySelectorAll('.page-section').forEach(section => {
                section.classList.remove('active');
            });
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });

            document.getElementById(`${page}-page`).classList.add('active');
            document.querySelector(`.nav-link[data-page="${page}"]`).classList.add('active');

            document.getElementById('page-title').textContent = translations[currentLang][page] || page;
            document.getElementById('page-subtitle').textContent = ''; // Clear subtitle for other pages

            currentPage = page;

            // Trigger refresh based on page
            switch (page) {
                case 'dashboard':
                    refreshData();
                    break;
                case 'monitor':
                    refreshMonitor();
                    break;
                case 'processes':
                    refreshProcesses();
                    break;
                case 'files':
                    refreshFiles();
                    break;
                case 'network':
                    refreshNetwork();
                    break;
                case 'disk':
                    refreshDisk();
                    break;
                case 'services':
                    refreshServices();
                    break;
                case 'logs':
                    refreshLogs();
                    break;
            }
        }

        async function refreshData() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();

                // CPU
                const cpuPercent = data.cpu_percent.toFixed(1);
                document.getElementById('cpu-value').textContent = cpuPercent + '%';
                document.getElementById('cpu-progress').style.width = cpuPercent + '%';
                document.getElementById('cpu-label').textContent = data.cpu_count + ' ' + translations[currentLang].cores;

                // RAM
                const ramPercent = data.memory.percent.toFixed(1);
                document.getElementById('ram-value').textContent = ramPercent + '%';
                document.getElementById('ram-progress').style.width = ramPercent + '%';
                document.getElementById('ram-label').textContent = formatBytes(data.memory.used) + ' / ' + formatBytes(data.memory.total);

                // Disk
                if (data.disk_partitions.length > 0) {
                    const mainDisk = data.disk_partitions[0];
                    document.getElementById('disk-value').textContent = mainDisk.percent.toFixed(1) + '%';
                    document.getElementById('disk-progress').style.width = mainDisk.percent + '%';
                    document.getElementById('disk-label').textContent = formatBytes(mainDisk.used) + ' / ' + formatBytes(mainDisk.total);
                }

                // Uptime
                document.getElementById('uptime-value').textContent = formatUptime(data.uptime);
                document.getElementById('uptime-label').textContent = 'System running smoothly';

                // System Info
                document.getElementById('os-info').textContent = data.system.os;
                document.getElementById('processor-info').textContent = data.system.processor;
                document.getElementById('cores-info').textContent = data.cpu_count;
                document.getElementById('processes-count').textContent = data.system.processes;

                // Monitor stats (for swap and temperature on dashboard)
                document.getElementById('swap-value').textContent = data.swap.percent.toFixed(1) + '%';
                document.getElementById('swap-label').textContent = `${formatBytes(data.swap.used)} / ${formatBytes(data.swap.total)}`;

                if (data.temperature) {
                    document.getElementById('temp-value').textContent = data.temperature + '°C';
                } else {
                    document.getElementById('temp-value').textContent = '--°C';
                }

            } catch (error) {
                console.error('Error fetching data:', error);
                showToast('error', 'Error', 'Failed to fetch system data');
            }
        }

        async function refreshMonitor() {
            try {
                const response = await fetch('/api/monitor');
                const data = await response.json();

                // CPU General
                document.getElementById('monitor-cpu-value').textContent = data.cpu.percent.toFixed(1) + '%';
                document.getElementById('monitor-cpu-label').textContent = `${data.cpu.count} Cores Active`;

                // CPU Per Core
                const coresList = document.getElementById('cpu-cores-list');
                coresList.innerHTML = data.cpu.per_core.map((core, idx) => `
                    <div style="margin-bottom: 0.5rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem; font-size: 0.875rem;">
                            <span>Core ${idx + 1}</span>
                            <span>${core.toFixed(1)}%</span>
                        </div>
                        <div class="progress-bar" style="height: 4px;">
                            <div class="progress-fill" style="width: ${core}%"></div>
                        </div>
                    </div>
                `).join('');

                // RAM
                document.getElementById('monitor-ram-value').textContent = data.memory.percent.toFixed(1) + '%';
                document.getElementById('monitor-ram-label').textContent = `${formatBytes(data.memory.available)} Available`;
                document.getElementById('monitor-ram-progress').style.width = data.memory.percent + '%';
            } catch (error) {
                console.error('Error fetching monitor data:', error);
                showToast('error', 'Error', 'Failed to fetch monitor data');
            }
        }

        async function refreshProcesses() {
            try {
                const response = await fetch('/api/processes');
                const data = await response.json();
                const tbody = document.getElementById('processes-tbody');
                tbody.innerHTML = data.processes.slice(0, 20).map(proc => `
                    <tr>
                        <td>${proc.name}</td>
                        <td>${proc.pid}</td>
                        <td>${proc.cpu.toFixed(1)}%</td>
                        <td>${formatBytes(proc.memory)}</td>
                        <td><span class="badge badge-${proc.status === 'running' ? 'success' : 'danger'}">${proc.status}</span></td>
                        <td>
                            <button class="btn btn-danger btn-sm kill-process" data-pid="${proc.pid}">
                                <i class="fas fa-times"></i>
                            </button>
                        </td>
                    </tr>
                `).join('');

                document.querySelectorAll('.kill-process').forEach(btn => {
                    btn.addEventListener('click', function() {
                        const pid = this.getAttribute('data-pid');
                        killProcess(pid);
                    });
                });
            } catch (error) {
                console.error('Error fetching processes:', error);
                showToast('error', 'Error', 'Failed to fetch processes');
            }
        }

        async function refreshFiles() {
            try {
                const response = await fetch(`/api/files?path=${encodeURIComponent(currentPath)}`);
                const data = await response.json();

                currentPath = data.path;

                const grid = document.getElementById('file-grid');
                document.getElementById('current-path').textContent = currentPath;

                // Back button logic
                const backBtn = document.getElementById('back-btn');
                // Platform kontrolü serverPlatform değişkeni ile yapıldı
                if (currentPath === '/' || (currentPath.endsWith(':/') && serverPlatform === 'Windows')) {
                    backBtn.disabled = true;
                } else {
                    backBtn.disabled = false;
                }

                grid.innerHTML = data.files.map(file => {
                    const iconClass = getFileIcon(file.name, file.is_dir);
                    const fileType = file.is_dir ? 'Folder' : file.name.split('.').pop().toUpperCase() + ' File';

                    return `
                        <div class="file-item" data-path="${file.path}" data-name="${file.name}" data-is-dir="${file.is_dir}"
                             onclick="openFile('${file.path}', ${file.is_dir})"
                             oncontextmenu="showContextMenu(event, '${file.path}', '${file.name}', ${file.is_dir})">
                            <div class="file-icon"><i class="${iconClass}"></i></div>
                            <div class="file-name">${file.name}</div>
                            <div class="file-size">${file.is_dir ? (translations[currentLang].modified + ': ' + new Date(file.modified * 1000).toLocaleDateString()) : formatBytes(file.size)}</div>
                        </div>
                    `;
                }).join('');
            } catch (error) {
                console.error('Error fetching files:', error);
                showToast('error', 'Error', 'Failed to fetch file manager data');
            }
        }

        async function refreshNetwork() {
            try {
                const response = await fetch('/api/network');
                const data = await response.json();

                // Bandwidth
                const now = Date.now();
                const deltaT = (now - lastNetIO.timestamp) / 1000;
                
                let sentSpeed = (data.net_io.bytes_sent - lastNetIO.bytes_sent) / deltaT;
                let recvSpeed = (data.net_io.bytes_recv - lastNetIO.bytes_recv) / deltaT;

                document.getElementById('net-sent-value').textContent = `${formatBytes(sentSpeed)}/s`;
                document.getElementById('net-recv-value').textContent = `${formatBytes(recvSpeed)}/s`;

                lastNetIO = {
                    bytes_sent: data.net_io.bytes_sent,
                    bytes_recv: data.net_io.bytes_recv,
                    timestamp: now
                };

                // Connections
                const tbody = document.getElementById('connections-tbody');
                tbody.innerHTML = data.connections.map(conn => `
                    <tr>
                        <td>${conn.type}</td>
                        <td>${conn.laddr}</td>
                        <td>${conn.raddr || 'N/A'}</td>
                        <td><span class="badge badge-info">${conn.status}</span></td>
                    </tr>
                `).join('');

            } catch (error) {
                console.error('Error fetching network data:', error);
                showToast('error', 'Error', 'Failed to fetch network data');
            }
        }

        async function refreshDisk() {
            try {
                const response = await fetch('/api/disk');
                const data = await response.json();
                const tbody = document.getElementById('disk-tbody');
                tbody.innerHTML = data.disk_partitions.map(disk => `
                    <tr>
                        <td>${disk.device}</td>
                        <td>${formatBytes(disk.total)}</td>
                        <td>${formatBytes(disk.used)}</td>
                        <td>${formatBytes(disk.free)}</td>
                        <td>
                            <div class="progress-bar" style="width: 100px; margin: 0;">
                                <div class="progress-fill" style="width: ${disk.percent}%;">${disk.percent}%</div>
                            </div>
                        </td>
                    </tr>
                `).join('');
            } catch (error) {
                console.error('Error fetching disk data:', error);
                showToast('error', 'Error', 'Failed to fetch disk data');
            }
        }

        async function refreshServices() {
            // Mock Data
            const tbody = document.getElementById('services-tbody');
            tbody.innerHTML = `
                <tr>
                    <td>System Service</td>
                    <td><span class="badge badge-success">Running</span></td>
                    <td>
                        <button class="btn btn-danger btn-sm"><i class="fas fa-stop"></i> Stop</button>
                        <button class="btn btn-primary btn-sm"><i class="fas fa-redo"></i> Restart</button>
                    </td>
                </tr>
                <tr>
                    <td>Web Server</td>
                    <td><span class="badge badge-success">Running</span></td>
                    <td>
                        <button class="btn btn-danger btn-sm"><i class="fas fa-stop"></i> Stop</button>
                        <button class="btn btn-primary btn-sm"><i class="fas fa-redo"></i> Restart</button>
                    </td>
                </tr>
            `;
        }

        async function refreshLogs() {
            // Mock Data
            const tbody = document.getElementById('logs-tbody');
            const now = new Date();
            tbody.innerHTML = [
                { time: new Date(now - 60000), level: 'INFO', msg: 'System started successfully' },
                { time: new Date(now - 120000), level: 'WARNING', msg: 'High CPU usage detected' },
                { time: new Date(now - 180000), level: 'INFO', msg: 'Backup completed' }
            ].map(log => `
                <tr>
                    <td>${log.time.toLocaleString()}</td>
                    <td><span class="badge badge-${log.level === 'INFO' ? 'success' : 'warning'}">${log.level}</span></td>
                    <td>${log.msg}</td>
                </tr>
            `).join('');
        }


        // Action Functions
        function openFile(path, isDir) {
            // HATA DÜZELTME 6: Regex düzeltildi. (JavaScript tarafında /[\/\\]/ olması için)
            const pathSeparatorRegex = /[\\/\\\\]/; 

            if (isDir) {
                currentPath = path;
                refreshFiles();
                showToast('info', 'Navigation', `Opened folder: ${path.split(pathSeparatorRegex).pop() || '/'}`);
            } else {
                showToast('info', 'File', `Opening file: ${path.split(pathSeparatorRegex).pop()}`);
                // In a real application, you would add logic to stream or download the file here.
            }
        }

        function navigateUp() {
            if (currentPath === '/') return;
            
            // Handle Windows root paths (e.g., C:/) - serverPlatform kullanıldı
            if (serverPlatform === 'Windows' && currentPath.endsWith(':/')) {
                 currentPath = '/';
            } else {
                 // HATA DÜZELTME 6: Regex düzeltildi.
                 const parts = currentPath.split(/[\\/\\\\]/).filter(p => p); 
                 parts.pop();
                 // Windows'ta kök dizin kontrolü
                 if (serverPlatform === 'Windows' && parts.length === 1 && parts[0].length === 1 && parts[0].match(/[A-Za-z]/)) {
                    currentPath = parts[0] + ':/';
                 } else {
                    currentPath = parts.length ? '/' + parts.join('/') : '/';
                 }
            }
            refreshFiles();
        }

        function showContextMenu(event, path, name, isDir) {
            event.preventDefault(); // Prevent default browser context menu
            selectedFile = { path, name, isDir };
            const menu = document.getElementById('context-menu');

            // Adjust download option for folders
            const downloadItem = document.getElementById('context-download');
            downloadItem.style.color = isDir ? 'var(--text-muted)' : 'var(--text-primary)';
            downloadItem.style.cursor = isDir ? 'not-allowed' : 'pointer';
            downloadItem.onclick = isDir ? () => showToast('warning', 'Warning', 'Cannot download folders') : () => handleContextMenuAction('download');

            menu.style.left = event.pageX + 'px';
            menu.style.top = event.pageY + 'px';
            menu.classList.add('active');
            
            // Auto-close menu on next click
            setTimeout(() => { document.addEventListener('click', closeContextMenu); }, 10);
        }
        
        function handleContextMenuAction(action) {
            closeContextMenu();
            const file = selectedFile;
            
            if (!file) return;

            switch (action) {
                case 'open':
                    openFile(file.path, file.is_dir);
                    break;
                case 'rename':
                    document.getElementById('rename-input').value = file.name;
                    openModal('rename-modal');
                    break;
                case 'download':
                    if (!file.is_dir) {
                        showToast('info', 'Download', `Downloading ${file.name}...`);
                        // Logic to initiate file download
                    }
                    break;
                case 'delete':
                    if (confirm(`Are you sure you want to delete "${file.name}"?`)) {
                        // In a real app, send API call to delete
                        showToast('success', 'Deleted', `${file.name} has been deleted`);
                        setTimeout(() => refreshFiles(), 500);
                    }
                    break;
            }
        }

        function createFolder() {
            const name = document.getElementById('folder-name-input').value.trim();
            if (!name) { showToast('warning', 'Warning', 'Please enter a folder name'); return; }
            closeModal('create-folder-modal');
            showToast('success', 'Created', `Folder "${name}" created successfully`);
            document.getElementById('folder-name-input').value = '';
            setTimeout(() => refreshFiles(), 500);
        }

        function uploadFile() {
            const input = document.getElementById('file-upload-input');
            if (!input.files.length) { showToast('warning', 'Warning', 'Please select a file'); return; }
            closeModal('upload-modal');
            showToast('success', 'Uploaded', `File "${input.files[0].name}" uploaded successfully`);
            input.value = '';
            setTimeout(() => refreshFiles(), 500);
        }

        function renameFile() {
            const newName = document.getElementById('rename-input').value.trim();
            if (!newName) { showToast('warning', 'Warning', 'Please enter a new name'); return; }
            closeModal('rename-modal');
            showToast('success', 'Renamed', `Renamed to "${newName}"`);
            setTimeout(() => refreshFiles(), 500);
        }

        function killProcess(pid) {
            if (confirm('Are you sure you want to kill this process?')) {
                // In a real app, send API call to kill process
                showToast('success', 'Process Killed', `Process ${pid} has been terminated`);
                setTimeout(() => refreshProcesses(), 500);
            }
        }

        function addFirewallRule() {
            const name = document.getElementById('rule-name').value;
            const port = document.getElementById('rule-port').value;
            const source = document.getElementById('rule-source').value;
            if (!name || !port || !source) { showToast('warning', 'Warning', 'Please fill all fields'); return; }
            closeModal('add-rule-modal');
            showToast('success', 'Rule Added', `Firewall rule "${name}" has been created`);
            document.getElementById('rule-name').value = '';
            document.getElementById('rule-port').value = '';
            document.getElementById('rule-source').value = '';
        }

        function toggleTheme() {
            document.body.classList.toggle('light-theme');
            const icon = document.querySelector('#theme-toggle i');
            if (document.body.classList.contains('light-theme')) {
                icon.className = 'fas fa-sun';
                localStorage.setItem('theme', 'light');
                document.getElementById('theme-select').value = 'Light Theme';
            } else {
                icon.className = 'fas fa-moon';
                localStorage.setItem('theme', 'dark');
                document.getElementById('theme-select').value = 'Dark Theme';
            }
        }

        function updateLanguage() {
            document.querySelectorAll('[data-lang]').forEach(el => {
                const key = el.getAttribute('data-lang');
                if (translations[currentLang] && translations[currentLang][key]) {
                    el.textContent = translations[currentLang][key];
                }
            });
            // Update page title manually
            document.getElementById('page-title').textContent = translations[currentLang][currentPage] || currentPage;
        }

        // Event Listeners
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const page = this.getAttribute('data-page');
                switchPage(page);
            });
        });

        document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
        document.getElementById('lang-toggle').addEventListener('click', () => {
            currentLang = currentLang === 'en' ? 'tr' : 'en';
            updateLanguage();
            localStorage.setItem('language', currentLang);
            document.getElementById('language-select').value = currentLang;
        });
        document.getElementById('refresh-btn').addEventListener('click', () => switchPage(currentPage));

        // Page specific listeners
        document.getElementById('refresh-processes').addEventListener('click', refreshProcesses);
        document.getElementById('refresh-files').addEventListener('click', refreshFiles);
        document.getElementById('back-btn').addEventListener('click', navigateUp);
        document.getElementById('create-folder-btn').addEventListener('click', () => openModal('create-folder-modal'));
        document.getElementById('upload-file-btn').addEventListener('click', () => openModal('upload-modal'));
        document.getElementById('add-rule-btn').addEventListener('click', () => openModal('add-rule-modal'));
        document.getElementById('refresh-services-btn').addEventListener('click', refreshServices);
        document.getElementById('refresh-logs-btn').addEventListener('click', refreshLogs);

        // Modal submissions
        document.getElementById('create-folder-submit').addEventListener('click', createFolder);
        document.getElementById('upload-file-submit').addEventListener('click', uploadFile);
        document.getElementById('add-rule-submit').addEventListener('click', addFirewallRule);
        document.getElementById('rename-submit').addEventListener('click', renameFile);

        // Modal closing
        document.querySelectorAll('.modal-close, .modal-footer .btn').forEach(el => {
            el.addEventListener('click', function(e) {
                const modalId = e.target.closest('.modal-overlay').id;
                if (modalId && modalId.includes('modal')) {
                    closeModal(modalId);
                }
            });
        });

        // Settings interaction
        document.getElementById('theme-select').addEventListener('change', function() {
            if ((this.value === 'Light Theme' && !document.body.classList.contains('light-theme')) ||
                (this.value === 'Dark Theme' && document.body.classList.contains('light-theme'))) {
                toggleTheme();
            }
        });

        document.getElementById('language-select').addEventListener('change', function() {
            currentLang = this.value;
            updateLanguage();
            localStorage.setItem('language', currentLang);
        });

        // Context Menu Handlers
        document.getElementById('context-open').addEventListener('click', () => handleContextMenuAction('open'));
        document.getElementById('context-rename').addEventListener('click', () => handleContextMenuAction('rename'));
        document.getElementById('context-delete').addEventListener('click', () => handleContextMenuAction('delete'));


        // Initialize
        window.addEventListener('load', function() {
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme === 'light') {
                document.body.classList.add('light-theme');
                document.querySelector('#theme-toggle i').className = 'fas fa-sun';
                document.getElementById('theme-select').value = 'Light Theme';
            } else {
                 document.getElementById('theme-select').value = 'Dark Theme';
            }

            const savedLang = localStorage.getItem('language');
            if (savedLang) {
                currentLang = savedLang;
            }
            document.getElementById('language-select').value = currentLang;
            updateLanguage();
            
            refreshData(); // Initial dashboard load
            
            // Auto refresh for active pages
            setInterval(() => {
                if (currentPage === 'dashboard') {
                    refreshData();
                } else if (currentPage === 'monitor') {
                    refreshMonitor();
                } else if (currentPage === 'network') {
                    refreshNetwork();
                }
            }, 2000);
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    server_platform = platform.system() 
    return render_template_string(HTML_TEMPLATE, translations=TRANSLATIONS, server_platform=server_platform)

@app.route('/api/stats')
def get_stats():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=False)
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    uptime = time.time() - psutil.boot_time()
    
    disk_partitions = []
    for partition in psutil.disk_partitions():
        try:
            if platform.system() == 'Windows' and not partition.mountpoint.endswith(':\\'):
                continue
            if platform.system() == 'Linux' and not (partition.mountpoint == '/' or partition.mountpoint.startswith('/home')):
                continue

            usage = psutil.disk_usage(partition.mountpoint)
            disk_partitions.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            })
            if len(disk_partitions) > 0 and disk_partitions[0]['mountpoint'] == '/':
                break 
            if len(disk_partitions) > 0 and disk_partitions[0]['mountpoint'].upper() == 'C:\\':
                break 
        except:
            continue

    system_info = {
        'os': platform.platform(),
        'processor': platform.processor(),
        'processes': len(psutil.pids())
    }

    temperature = None
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                if entries:
                    temperature = int(entries[0].current)
                    break 
    except:
        pass

    return jsonify({
        'cpu_percent': cpu_percent,
        'cpu_count': cpu_count,
        'memory': {
            'total': memory.total,
            'used': memory.used,
            'percent': memory.percent
        },
        'swap': {
            'total': swap.total,
            'used': swap.used,
            'percent': swap.percent
        },
        'disk_partitions': disk_partitions,
        'uptime': uptime,
        'system': system_info,
        'temperature': temperature
    })

@app.route('/api/monitor')
def get_monitor():
    temperature = None
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                if entries:
                    temperature = int(entries[0].current)
                    break 
    except:
        pass 

    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    cpu_stats = {
        'percent': psutil.cpu_percent(interval=None),
        'count': psutil.cpu_count(logical=False),
        'per_core': psutil.cpu_percent(interval=None, percpu=True)
    }

    return jsonify({
        'cpu': cpu_stats,
        'memory': {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent
        },
        'swap': {
            'total': swap.total,
            'used': swap.used,
            'percent': swap.percent
        },
        'temperature': temperature
    })

@app.route('/api/processes')
def get_processes():
    processes = []
    for proc in sorted(psutil.process_iter(['name', 'cpu_percent', 'memory_info', 'status', 'pid']), key=lambda p: p.info['cpu_percent'], reverse=True)[:20]:
        try:
            processes.append({
                'name': proc.info['name'],
                'pid': proc.info['pid'],
                'cpu': proc.info['cpu_percent'],
                'memory': proc.info['memory_info'].rss,
                'status': proc.info['status']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return jsonify({'processes': processes})

@app.route('/api/files')
def get_files():
    path = request.args.get('path', '/')
    
    if '..' in path:
        return jsonify({'path': '/', 'files': []})
    
    try:
        if platform.system() == 'Windows' and path == '/':
            import string
            drives = []
            for letter in string.ascii_uppercase:
                drive_path = f"{letter}:/"
                if os.path.exists(drive_path):
                    try:
                        usage = psutil.disk_usage(drive_path)
                        drives.append({
                            'name': f"Drive {letter}:",
                            'path': drive_path,
                            'is_dir': True,
                            'size': usage.total,
                            'modified': os.path.getmtime(drive_path)
                        })
                    except:
                        pass
            return jsonify({'path': path, 'files': drives})
        
        items = os.listdir(path)
        files = []
        for item in items:
            item_path = os.path.join(path, item)
            try:
                is_dir = os.path.isdir(item_path)
                
                size = 0 if is_dir else os.path.getsize(item_path)
                files.append({
                    'name': item,
                    'path': item_path,
                    'is_dir': is_dir,
                    'size': size,
                    'modified': os.path.getmtime(item_path)
                })
            except:
                pass
        
        files.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        
        return jsonify({'path': path, 'files': files})
    except Exception as e:
        return jsonify({'path': path, 'files': [], 'error': str(e)})

@app.route('/api/network')
def get_network():
    net_io = psutil.net_io_counters()
    connections = []
    
    try:
        for conn in psutil.net_connections()[:15]:
            connections.append({
                'type': conn.type.name if hasattr(conn.type, 'name') else str(conn.type),
                'laddr': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else 'N/A',
                'raddr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                'status': conn.status
            })
    except (psutil.AccessDenied, NotImplementedError):
        pass

    return jsonify({
        'net_io': {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv
        },
        'connections': connections
    })

@app.route('/api/disk')
def get_disk():
    disk_partitions = []
    for partition in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_partitions.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            })
        except:
            continue
    return jsonify({'disk_partitions': disk_partitions})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

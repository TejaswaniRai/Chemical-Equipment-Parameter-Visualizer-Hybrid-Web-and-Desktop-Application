import sys
import os

# Check and install dependencies before importing
def check_dependencies():
    """Check if required packages are installed"""
    missing = []
    
    try:
        import PyQt5
    except ImportError:
        missing.append('PyQt5')
    
    try:
        import matplotlib
    except ImportError:
        missing.append('matplotlib')
    
    try:
        import requests
    except ImportError:
        missing.append('requests')
    
    try:
        import pandas
    except ImportError:
        missing.append('pandas')
    
    if missing:
        print("\n" + "="*60)
        print("ERROR: Missing required packages!")
        print("="*60)
        print(f"\nMissing packages: {', '.join(missing)}")
        print("\nPlease install dependencies:")
        print("1. Open PowerShell/Command Prompt")
        print("2. Navigate to frontend-desktop folder")
        print("3. Run: pip install -r requirements.txt")
        print("\nOr run the setup script: setup_desktop.bat")
        print("="*60 + "\n")
        input("Press Enter to exit...")
        sys.exit(1)

check_dependencies()

import requests
import pandas as pd

try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                 QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                                 QFileDialog, QTableWidget, QTableWidgetItem, 
                                 QMessageBox, QTabWidget, QGroupBox, QGridLayout,
                                 QTextEdit, QScrollArea, QFrame)
    from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
    from PyQt5.QtGui import QFont, QPalette, QColor
except ImportError as e:
    print(f"Error importing PyQt5: {e}")
    sys.exit(1)

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
except (ImportError, AttributeError):
    try:
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    except ImportError as e:
        print(f"Error importing matplotlib backend: {e}")
        print("Try: pip install matplotlib --upgrade")
        sys.exit(1)

from matplotlib.figure import Figure

API_BASE_URL = 'http://localhost:8000/api'


class AuthWindow(QWidget):
    """Authentication window for login/register"""
    
    auth_success = pyqtSignal(str, str)  # token, username
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Login')
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('🧪 Chemical Equipment Visualizer')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel('Desktop Application')
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.login_btn = QPushButton('Login')
        self.login_btn.clicked.connect(self.login)
        btn_layout.addWidget(self.login_btn)
        
        self.register_btn = QPushButton('Register')
        self.register_btn.clicked.connect(self.register)
        btn_layout.addWidget(self.register_btn)
        
        layout.addLayout(btn_layout)
        
        # Error label
        self.error_label = QLabel('')
        self.error_label.setStyleSheet('color: red;')
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label)
        
        layout.addStretch()
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.error_label.setText('⚠️ Please enter username and password')
            return
        
        try:
            response = requests.post(f'{API_BASE_URL}/auth/login/', 
                                    json={'username': username, 'password': password},
                                    timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'token' in data and 'username' in data:
                    self.auth_success.emit(data['token'], data['username'])
                    self.close()
                else:
                    self.error_label.setText('❌ Invalid response from server')
            elif response.status_code == 401:
                self.error_label.setText('❌ Invalid username or password')
            elif response.status_code == 400:
                error_msg = response.json().get('error', 'Bad request')
                self.error_label.setText(f'❌ {error_msg}')
            else:
                self.error_label.setText(f'❌ Login failed (Status: {response.status_code})')
        except requests.exceptions.ConnectionError:
            self.error_label.setText('❌ Backend server not running! Start it first.')
        except requests.exceptions.Timeout:
            self.error_label.setText('❌ Server timeout. Check backend connection.')
        except Exception as e:
            self.error_label.setText(f'❌ Error: {str(e)}')
    
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.error_label.setText('⚠️ Please enter username and password')
            return
        
        if len(password) < 6:
            self.error_label.setText('⚠️ Password must be at least 6 characters')
            return
        
        try:
            response = requests.post(f'{API_BASE_URL}/auth/register/', 
                                    json={'username': username, 'password': password},
                                    timeout=5)
            
            if response.status_code == 201:
                data = response.json()
                if 'token' in data and 'username' in data:
                    QMessageBox.information(self, 'Success', 
                        f'✅ Account created successfully!\nWelcome, {username}!')
                    self.auth_success.emit(data['token'], data['username'])
                    self.close()
                else:
                    self.error_label.setText('❌ Invalid response from server')
            elif response.status_code == 400:
                error_msg = response.json().get('error', 'Registration failed')
                if 'already exists' in error_msg:
                    self.error_label.setText('❌ Username already taken. Try another.')
                else:
                    self.error_label.setText(f'❌ {error_msg}')
            else:
                self.error_label.setText(f'❌ Registration failed (Status: {response.status_code})')
        except requests.exceptions.ConnectionError:
            self.error_label.setText('❌ Backend server not running! Start it first.')
        except requests.exceptions.Timeout:
            self.error_label.setText('❌ Server timeout. Check backend connection.')
        except Exception as e:
            self.error_label.setText(f'❌ Error: {str(e)}')


class ChartWidget(QWidget):
    """Widget for displaying matplotlib charts"""
    
    def __init__(self, parent=None, figsize=(10, 6)):
        super().__init__(parent)
        self.figure = Figure(figsize=figsize, dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def clear(self):
        self.figure.clear()
        self.canvas.draw()
    
    def plot_equipment_types(self, equipment_types):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        labels = list(equipment_types.keys())
        sizes = list(equipment_types.values())
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a']
        
        # Create pie chart with better styling
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%', 
            colors=colors[:len(labels)], 
            startangle=90,
            textprops={'fontsize': 11, 'weight': 'bold'},
            explode=[0.05] * len(labels)  # Slight separation
        )
        
        # Make percentage text more readable
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        
        ax.set_title('Equipment Type Distribution', fontsize=16, fontweight='bold', pad=20)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_parameters(self, equipment_items):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Limit to first 10 items for better readability
        items_to_plot = equipment_items[:10] if len(equipment_items) > 10 else equipment_items
        
        names = [item['equipment_name'] for item in items_to_plot]
        flowrates = [item['flowrate'] for item in items_to_plot]
        pressures = [item['pressure'] for item in items_to_plot]
        temperatures = [item['temperature'] for item in items_to_plot]
        
        y = range(len(names))
        height = 0.25
        
        # Create horizontal bars for better label readability
        ax.barh([i - height for i in y], flowrates, height, label='Flowrate', color='#667eea', alpha=0.8)
        ax.barh(y, pressures, height, label='Pressure', color='#764ba2', alpha=0.8)
        ax.barh([i + height for i in y], temperatures, height, label='Temperature', color='#f093fb', alpha=0.8)
        
        ax.set_ylabel('Equipment', fontweight='bold', fontsize=12)
        ax.set_xlabel('Value', fontweight='bold', fontsize=12)
        ax.set_title('Equipment Parameters Comparison', fontsize=16, fontweight='bold', pad=20)
        ax.set_yticks(y)
        ax.set_yticklabels(names, fontsize=10)
        ax.legend(loc='lower right', fontsize=10)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Add note if items were limited
        if len(equipment_items) > 10:
            ax.text(0.02, 0.98, f'Showing first 10 of {len(equipment_items)} items', 
                   transform=ax.transAxes, fontsize=9, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        self.figure.tight_layout()
        self.canvas.draw()


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.token = None
        self.username = None
        self.current_dataset = None
        self.datasets = []
        self.refresh_timer = None
        
        self.show_auth()
    
    def show_auth(self):
        """Show authentication window"""
        self.auth_window = AuthWindow()
        self.auth_window.auth_success.connect(self.on_auth_success)
        self.auth_window.show()
    
    def on_auth_success(self, token, username):
        """Handle successful authentication"""
        self.token = token
        self.username = username
        self.initUI()
        self.show()
        self.fetch_datasets()
        self.start_auto_refresh()
    
    def initUI(self):
        """Initialize the main UI"""
        self.setWindowTitle('Chemical Equipment Visualizer - Desktop')
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        header = QLabel(f'🧪 Chemical Equipment Visualizer - Welcome, {self.username}!')
        header.setFont(QFont('Arial', 16, QFont.Bold))
        header.setStyleSheet('color: white;')
        header_layout.addWidget(header)
        
        header_layout.addStretch()
        
        self.refresh_label = QLabel('🔄 Auto-refresh: ON')
        self.refresh_label.setStyleSheet('color: white; padding-right: 10px;')
        header_layout.addWidget(self.refresh_label)
        
        header_widget.setLayout(header_layout)
        header_widget.setStyleSheet('background-color: #667eea; padding: 15px;')
        main_layout.addWidget(header_widget)
        
        # Upload section
        upload_group = QGroupBox('Upload CSV Data')
        upload_layout = QHBoxLayout()
        
        self.file_label = QLabel('No file selected')
        upload_layout.addWidget(self.file_label)
        
        select_btn = QPushButton('Select File')
        select_btn.clicked.connect(self.select_file)
        upload_layout.addWidget(select_btn)
        
        self.upload_btn = QPushButton('Upload & Analyze')
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        upload_layout.addWidget(self.upload_btn)
        
        self.download_btn = QPushButton('Download PDF Report')
        self.download_btn.clicked.connect(self.download_report)
        self.download_btn.setEnabled(False)
        upload_layout.addWidget(self.download_btn)
        
        # Auto-refresh toggle button
        self.refresh_toggle_btn = QPushButton('🔄 Auto-Refresh: ON')
        self.refresh_toggle_btn.clicked.connect(self.toggle_auto_refresh)
        self.refresh_toggle_btn.setStyleSheet('background-color: #43e97b; color: black;')
        upload_layout.addWidget(self.refresh_toggle_btn)
        
        logout_btn = QPushButton('Logout')
        logout_btn.clicked.connect(self.logout)
        upload_layout.addWidget(logout_btn)
        
        upload_group.setLayout(upload_layout)
        main_layout.addWidget(upload_group)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Summary Tab
        self.summary_tab = QWidget()
        self.setup_summary_tab()
        self.tabs.addTab(self.summary_tab, 'Summary')
        
        # Charts Tab
        self.charts_tab = QWidget()
        self.setup_charts_tab()
        self.tabs.addTab(self.charts_tab, 'Charts')
        
        # Data Table Tab
        self.table_tab = QWidget()
        self.setup_table_tab()
        self.tabs.addTab(self.table_tab, 'Data Table')
        
        # History Tab
        self.history_tab = QWidget()
        self.setup_history_tab()
        self.tabs.addTab(self.history_tab, 'History')
        
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
        
        self.selected_file = None
    
    def setup_summary_tab(self):
        """Setup summary statistics tab with improved styling"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Stats grid with better styling
        stats_group = QGroupBox('Summary Statistics')
        stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                padding: 15px;
            }
        """)
        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)
        
        # Create styled stat cards
        def create_stat_card(title, label_widget):
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #667eea, stop:1 #764ba2);
                    border-radius: 10px;
                    padding: 15px;
                }
            """)
            card_layout = QVBoxLayout()
            
            title_label = QLabel(title)
            title_label.setStyleSheet('color: white; font-size: 12px; font-weight: normal;')
            title_label.setAlignment(Qt.AlignCenter)
            
            label_widget.setFont(QFont('Arial', 28, QFont.Bold))
            label_widget.setStyleSheet('color: white;')
            label_widget.setAlignment(Qt.AlignCenter)
            
            card_layout.addWidget(title_label)
            card_layout.addWidget(label_widget)
            card.setLayout(card_layout)
            return card
        
        self.total_count_label = QLabel('0')
        stats_layout.addWidget(create_stat_card('Total Equipment', self.total_count_label), 0, 0)
        
        self.avg_flowrate_label = QLabel('0.00')
        stats_layout.addWidget(create_stat_card('Avg Flowrate', self.avg_flowrate_label), 0, 1)
        
        self.avg_pressure_label = QLabel('0.00')
        stats_layout.addWidget(create_stat_card('Avg Pressure', self.avg_pressure_label), 0, 2)
        
        self.avg_temperature_label = QLabel('0.00')
        stats_layout.addWidget(create_stat_card('Avg Temperature', self.avg_temperature_label), 0, 3)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Dataset info
        info_group = QGroupBox('Dataset Information')
        info_group.setStyleSheet('QGroupBox { font-weight: bold; font-size: 14px; padding: 15px; }')
        info_layout = QVBoxLayout()
        
        self.dataset_info_text = QTextEdit()
        self.dataset_info_text.setReadOnly(True)
        self.dataset_info_text.setMaximumHeight(200)
        self.dataset_info_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
        """)
        info_layout.addWidget(self.dataset_info_text)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        layout.addStretch()
        self.summary_tab.setLayout(layout)
    
    def setup_charts_tab(self):
        """Setup charts tab with improved layout"""
        main_layout = QVBoxLayout()
        
        # Create scroll area for charts
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Container for all charts
        container = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Type distribution chart with group box
        type_group = QGroupBox('Equipment Type Distribution')
        type_group.setStyleSheet('QGroupBox { font-weight: bold; font-size: 14px; }')
        type_layout = QVBoxLayout()
        self.type_chart = ChartWidget(figsize=(10, 6))
        type_layout.addWidget(self.type_chart)
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)
        
        # Parameters chart with group box
        params_group = QGroupBox('Equipment Parameters Comparison')
        params_group.setStyleSheet('QGroupBox { font-weight: bold; font-size: 14px; }')
        params_layout = QVBoxLayout()
        self.params_chart = ChartWidget(figsize=(10, 8))
        params_layout.addWidget(self.params_chart)
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        layout.addStretch()
        container.setLayout(layout)
        scroll.setWidget(container)
        
        main_layout.addWidget(scroll)
        self.charts_tab.setLayout(main_layout)
    
    def setup_table_tab(self):
        """Setup data table tab with improved styling"""
        layout = QVBoxLayout()
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        
        # Improve table appearance
        self.data_table.setAlternatingRowColors(True)
        self.data_table.horizontalHeader().setStretchLastSection(True)
        self.data_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #667eea;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }
        """)
        
        layout.addWidget(self.data_table)
        self.table_tab.setLayout(layout)
    
    def setup_history_tab(self):
        """Setup history tab with improved styling"""
        layout = QVBoxLayout()
        
        self.history_list = QTextEdit()
        self.history_list.setReadOnly(True)
        self.history_list.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 15px;
                font-size: 13px;
                line-height: 1.6;
            }
        """)
        
        layout.addWidget(QLabel('<b style="font-size: 14px;">📜 Last 5 Uploaded Datasets (Your Uploads Only)</b>'))
        layout.addWidget(self.history_list)
        
        self.history_tab.setLayout(layout)
    
    def select_file(self):
        """Handle file selection"""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path.split('/')[-1])
            self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        """Upload and process CSV file"""
        if not self.selected_file:
            QMessageBox.warning(self, 'Error', 'Please select a file first')
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                headers = {'Authorization': f'Token {self.token}'}
                
                response = requests.post(f'{API_BASE_URL}/datasets/upload_csv/', 
                                       files=files, headers=headers)
                
                if response.status_code == 201:
                    self.current_dataset = response.json()
                    self.update_display()
                    self.fetch_datasets()
                    self.download_btn.setEnabled(True)
                    QMessageBox.information(self, 'Success', 'File uploaded successfully!')
                else:
                    QMessageBox.warning(self, 'Error', f'Upload failed: {response.text}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error uploading file: {str(e)}')
    
    def fetch_datasets(self):
        """Fetch dataset history"""
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(f'{API_BASE_URL}/datasets/', headers=headers)
            
            if response.status_code == 200:
                self.datasets = response.json()
                self.update_history()
        except Exception as e:
            print(f'Error fetching datasets: {str(e)}')
    
    def download_report(self):
        """Download PDF report"""
        if not self.current_dataset:
            QMessageBox.warning(self, 'Error', 'No dataset selected')
            return
        
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save PDF Report', 
                                                       f"report_{self.current_dataset['name']}", 
                                                       'PDF Files (*.pdf)')
            
            if file_path:
                headers = {'Authorization': f'Token {self.token}'}
                response = requests.get(
                    f"{API_BASE_URL}/datasets/{self.current_dataset['id']}/generate_report/",
                    headers=headers
                )
                
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, 'Success', 'Report downloaded successfully!')
                else:
                    QMessageBox.warning(self, 'Error', 'Failed to download report')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error downloading report: {str(e)}')
    
    def update_display(self):
        """Update all display elements with current dataset"""
        if not self.current_dataset:
            return
        
        # Update summary
        self.total_count_label.setText(str(self.current_dataset['total_count']))
        self.avg_flowrate_label.setText(f"{self.current_dataset['avg_flowrate']:.2f}")
        self.avg_pressure_label.setText(f"{self.current_dataset['avg_pressure']:.2f}")
        self.avg_temperature_label.setText(f"{self.current_dataset['avg_temperature']:.2f}")
        
        # Update dataset info
        info_text = f"Dataset Name: {self.current_dataset['name']}\n"
        info_text += f"Uploaded: {self.current_dataset['uploaded_at']}\n"
        info_text += f"Uploaded By: {self.current_dataset.get('uploaded_by_username', 'N/A')}\n\n"
        info_text += "Equipment Types:\n"
        for eq_type, count in self.current_dataset['equipment_types'].items():
            info_text += f"  - {eq_type}: {count}\n"
        
        self.dataset_info_text.setText(info_text)
        
        # Update charts
        self.type_chart.plot_equipment_types(self.current_dataset['equipment_types'])
        
        if self.current_dataset['equipment_items']:
            self.params_chart.plot_parameters(self.current_dataset['equipment_items'])
        
        # Update table
        equipment_items = self.current_dataset['equipment_items']
        self.data_table.setRowCount(len(equipment_items))
        
        for i, item in enumerate(equipment_items):
            self.data_table.setItem(i, 0, QTableWidgetItem(item['equipment_name']))
            self.data_table.setItem(i, 1, QTableWidgetItem(item['equipment_type']))
            self.data_table.setItem(i, 2, QTableWidgetItem(str(item['flowrate'])))
            self.data_table.setItem(i, 3, QTableWidgetItem(str(item['pressure'])))
            self.data_table.setItem(i, 4, QTableWidgetItem(str(item['temperature'])))
        
        # Auto-resize columns to content
        self.data_table.resizeColumnsToContents()
        self.data_table.horizontalHeader().setStretchLastSection(True)
    
    def update_history(self):
        """Update history list"""
        if not self.datasets:
            self.history_list.setText("No datasets uploaded yet.\n\nUpload a CSV file to get started!")
            return
        
        history_text = ""
        for dataset in self.datasets:
            history_text += f"📁 {dataset['name']}\n"
            history_text += f"   Uploaded: {dataset['uploaded_at']}\n"
            history_text += f"   Count: {dataset['total_count']} | "
            history_text += f"Avg Flowrate: {dataset['avg_flowrate']:.2f}\n"
            history_text += f"   User: {dataset.get('uploaded_by_username', 'Unknown')}\n\n"
        
        self.history_list.setText(history_text)
    
    def start_auto_refresh(self):
        """Start auto-refresh timer for real-time monitoring"""
        if self.refresh_timer is None:
            self.refresh_timer = QTimer()
            self.refresh_timer.timeout.connect(self.auto_refresh_data)
            self.refresh_timer.start(5000)  # Refresh every 5 seconds
            print("Auto-refresh started (every 5 seconds)")
    
    def stop_auto_refresh(self):
        """Stop auto-refresh timer"""
        if self.refresh_timer is not None:
            self.refresh_timer.stop()
            self.refresh_timer = None
            print("Auto-refresh stopped")
    
    def auto_refresh_data(self):
        """Auto-refresh datasets from backend"""
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(f'{API_BASE_URL}/datasets/', headers=headers, timeout=2)
            
            if response.status_code == 200:
                new_datasets = response.json()
                
                # Check if there are new datasets
                if new_datasets != self.datasets:
                    old_count = len(self.datasets)
                    self.datasets = new_datasets
                    self.update_history()
                    
                    # Update refresh label with timestamp
                    from datetime import datetime
                    now = datetime.now().strftime('%H:%M:%S')
                    self.refresh_label.setText(f'🔄 Updated: {now}')
                    
                    # Show notification if new dataset detected
                    if len(new_datasets) > old_count:
                        print(f"New dataset detected! Total: {len(new_datasets)}")
            else:
                print(f"Refresh failed: {response.status_code}")
        except Exception as e:
            print(f"Auto-refresh error: {str(e)}")
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh on/off"""
        if self.refresh_timer and self.refresh_timer.isActive():
            self.stop_auto_refresh()
            self.refresh_toggle_btn.setText('⏸️ Auto-Refresh: OFF')
            self.refresh_toggle_btn.setStyleSheet('background-color: #fa709a; color: white;')
            self.refresh_label.setText('⏸️ Auto-refresh paused')
        else:
            self.start_auto_refresh()
            self.refresh_toggle_btn.setText('🔄 Auto-Refresh: ON')
            self.refresh_toggle_btn.setStyleSheet('background-color: #43e97b; color: black;')
            from datetime import datetime
            now = datetime.now().strftime('%H:%M:%S')
            self.refresh_label.setText(f'🔄 Updated: {now}')
    
    def logout(self):
        """Handle logout"""
        self.stop_auto_refresh()
        self.token = None
        self.username = None
        self.current_dataset = None
        self.datasets = []
        self.close()
        self.show_auth()


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set color palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.Button, QColor(102, 126, 234))
    palette.setColor(QPalette.ButtonText, Qt.white)
    app.setPalette(palette)
    
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

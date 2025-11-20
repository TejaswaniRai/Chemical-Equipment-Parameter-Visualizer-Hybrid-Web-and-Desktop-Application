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
    from PyQt5.QtCore import Qt, QThread, pyqtSignal
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
            self.error_label.setText('Please enter username and password')
            return
        
        try:
            response = requests.post(f'{API_BASE_URL}/auth/login/', 
                                    json={'username': username, 'password': password})
            
            if response.status_code == 200:
                data = response.json()
                self.auth_success.emit(data['token'], data['username'])
                self.close()
            else:
                self.error_label.setText('Invalid credentials')
        except Exception as e:
            self.error_label.setText(f'Error: {str(e)}')
    
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.error_label.setText('Please enter username and password')
            return
        
        try:
            response = requests.post(f'{API_BASE_URL}/auth/register/', 
                                    json={'username': username, 'password': password})
            
            if response.status_code == 201:
                data = response.json()
                self.auth_success.emit(data['token'], data['username'])
                self.close()
            else:
                self.error_label.setText('Registration failed')
        except Exception as e:
            self.error_label.setText(f'Error: {str(e)}')


class ChartWidget(QWidget):
    """Widget for displaying matplotlib charts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout()
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
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold')
        
        self.canvas.draw()
    
    def plot_parameters(self, equipment_items):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        names = [item['equipment_name'] for item in equipment_items]
        flowrates = [item['flowrate'] for item in equipment_items]
        pressures = [item['pressure'] for item in equipment_items]
        temperatures = [item['temperature'] for item in equipment_items]
        
        x = range(len(names))
        width = 0.25
        
        ax.bar([i - width for i in x], flowrates, width, label='Flowrate', color='#667eea')
        ax.bar(x, pressures, width, label='Pressure', color='#764ba2')
        ax.bar([i + width for i in x], temperatures, width, label='Temperature', color='#f093fb')
        
        ax.set_xlabel('Equipment', fontweight='bold')
        ax.set_ylabel('Value', fontweight='bold')
        ax.set_title('Equipment Parameters Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right')
        ax.legend()
        
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
        header = QLabel(f'🧪 Chemical Equipment Visualizer - Welcome, {self.username}!')
        header.setFont(QFont('Arial', 16, QFont.Bold))
        header.setStyleSheet('background-color: #667eea; color: white; padding: 15px;')
        main_layout.addWidget(header)
        
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
        """Setup summary statistics tab"""
        layout = QVBoxLayout()
        
        # Stats grid
        stats_group = QGroupBox('Summary Statistics')
        stats_layout = QGridLayout()
        
        self.total_count_label = QLabel('0')
        self.total_count_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.total_count_label.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(QLabel('Total Equipment:'), 0, 0)
        stats_layout.addWidget(self.total_count_label, 1, 0)
        
        self.avg_flowrate_label = QLabel('0.00')
        self.avg_flowrate_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.avg_flowrate_label.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(QLabel('Avg Flowrate:'), 0, 1)
        stats_layout.addWidget(self.avg_flowrate_label, 1, 1)
        
        self.avg_pressure_label = QLabel('0.00')
        self.avg_pressure_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.avg_pressure_label.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(QLabel('Avg Pressure:'), 0, 2)
        stats_layout.addWidget(self.avg_pressure_label, 1, 2)
        
        self.avg_temperature_label = QLabel('0.00')
        self.avg_temperature_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.avg_temperature_label.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(QLabel('Avg Temperature:'), 0, 3)
        stats_layout.addWidget(self.avg_temperature_label, 1, 3)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Dataset info
        info_group = QGroupBox('Dataset Information')
        info_layout = QVBoxLayout()
        
        self.dataset_info_text = QTextEdit()
        self.dataset_info_text.setReadOnly(True)
        self.dataset_info_text.setMaximumHeight(150)
        info_layout.addWidget(self.dataset_info_text)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        layout.addStretch()
        self.summary_tab.setLayout(layout)
    
    def setup_charts_tab(self):
        """Setup charts tab"""
        layout = QVBoxLayout()
        
        # Type distribution chart
        self.type_chart = ChartWidget()
        layout.addWidget(QLabel('Equipment Type Distribution:'))
        layout.addWidget(self.type_chart)
        
        # Parameters chart
        self.params_chart = ChartWidget()
        layout.addWidget(QLabel('Parameters Comparison:'))
        layout.addWidget(self.params_chart)
        
        self.charts_tab.setLayout(layout)
    
    def setup_table_tab(self):
        """Setup data table tab"""
        layout = QVBoxLayout()
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        
        layout.addWidget(self.data_table)
        self.table_tab.setLayout(layout)
    
    def setup_history_tab(self):
        """Setup history tab"""
        layout = QVBoxLayout()
        
        self.history_list = QTextEdit()
        self.history_list.setReadOnly(True)
        
        layout.addWidget(QLabel('Last 5 Uploaded Datasets:'))
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
    
    def update_history(self):
        """Update history list"""
        history_text = ""
        for dataset in self.datasets:
            history_text += f"📁 {dataset['name']}\n"
            history_text += f"   Uploaded: {dataset['uploaded_at']}\n"
            history_text += f"   Count: {dataset['total_count']} | "
            history_text += f"Avg Flowrate: {dataset['avg_flowrate']:.2f}\n\n"
        
        self.history_list.setText(history_text)
    
    def logout(self):
        """Handle logout"""
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

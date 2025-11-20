# Chemical Equipment Parameter Visualizer
## Hybrid Web + Desktop Application

A comprehensive hybrid application for visualizing and analyzing chemical equipment parameters. Built with Django backend, React web frontend, and PyQt5 desktop application.

---

## 🎯 Project Overview

This application allows users to:
- Upload CSV files containing chemical equipment data
- View detailed analytics and summary statistics
- Visualize data through interactive charts
- Generate PDF reports
- Access data through both web and desktop interfaces
- Maintain history of last 5 uploaded datasets

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend (Web)** | React.js + Chart.js | Interactive web interface with data visualization |
| **Frontend (Desktop)** | PyQt5 + Matplotlib | Native desktop application with charts |
| **Backend** | Django + Django REST Framework | RESTful API server |
| **Data Processing** | Pandas | CSV parsing and analytics |
| **Database** | SQLite | Store datasets and equipment records |
| **Authentication** | Token Authentication | Secure API access |
| **PDF Generation** | ReportLab | Generate analysis reports |

---

## 📁 Project Structure

```
chemical-equipment-visualizer/
│
├── backend/                          # Django Backend
│   ├── chemical_equipment_backend/   # Project settings
│   │   ├── settings.py              # Django configuration
│   │   ├── urls.py                  # Main URL routing
│   │   └── ...
│   ├── equipment/                    # Equipment app
│   │   ├── models.py                # Dataset and Equipment models
│   │   ├── views.py                 # API endpoints
│   │   ├── serializers.py           # DRF serializers
│   │   ├── utils.py                 # Helper functions (CSV processing, PDF generation)
│   │   └── urls.py                  # App URL routing
│   ├── manage.py                    # Django management script
│   └── requirements.txt             # Python dependencies
│
├── frontend-web/                     # React Web Application
│   ├── public/                      # Static files
│   ├── src/
│   │   ├── App.js                   # Main React component
│   │   ├── App.css                  # Styling
│   │   └── index.js                 # Entry point
│   └── package.json                 # Node dependencies
│
├── frontend-desktop/                 # PyQt5 Desktop Application
│   ├── main.py                      # Desktop application entry point
│   ├── launcher.py                  # Smart launcher with dependency checks
│   ├── requirements.txt             # Python dependencies
│   └── venv/                        # Virtual environment
│
├── sample_equipment_data.csv        # Sample data for testing
├── .gitignore                       # Git ignore rules
├── .vscode/                         # VS Code configuration
└── ARCHITECTURE.md                  # Technical architecture documentation

```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+ installed (tested with Python 3.11+)
- Node.js 14+ and npm installed (tested with Node 16+)
- Git (optional, for cloning)

### 1. Get the Project

```bash
# If using Git
git clone <repository-url>
cd chemical-equipment-visualizer

# Or extract the project folder and navigate to it
cd "New folder"
```

### 2. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\activate
# On Windows CMD:
venv\Scripts\activate.bat
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

The backend API will be available at `http://127.0.0.1:8000/api/`

### 3. Web Frontend Setup (React)

Open a new terminal:

```bash
# Navigate to web frontend directory
cd frontend-web

# Install dependencies
npm install

# Start development server
npm start
```

The web application will open at `http://localhost:3000/`

### 4. Desktop Frontend Setup (PyQt5)

Open a new terminal:

```bash
# Navigate to desktop frontend directory
cd frontend-desktop

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\activate
# On Windows CMD:
venv\Scripts\activate.bat
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application (recommended - with dependency checker)
python launcher.py

# Or run directly
python main.py
```

The desktop application will open in a new window.

---

## 📊 Features

### ✅ CSV Upload
- Upload CSV files with equipment data
- Automatic validation of required columns
- Server-side processing with Pandas

### ✅ Data Analytics
- Calculate summary statistics (averages, totals)
- Equipment type distribution analysis
- Real-time data processing

### ✅ Visualizations

**Web (Chart.js):**
- Pie chart for equipment type distribution
- Bar chart for type counts
- Line chart for parameter comparison

**Desktop (Matplotlib):**
- Interactive pie chart
- Multi-bar chart for parameters
- High-quality vector graphics

### ✅ History Management
- Stores last 5 uploaded datasets
- View previous analyses
- Switch between datasets

### ✅ PDF Report Generation
- Professional formatted reports
- Summary statistics table
- Equipment type distribution
- Detailed equipment listings
- Downloadable from both interfaces

### ✅ Authentication
- User registration and login
- Token-based authentication
- Secure API endpoints
- Session management

---

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user

### Datasets
- `GET /api/datasets/` - List last 5 datasets (requires authentication)
- `POST /api/datasets/upload_csv/` - Upload CSV file (requires authentication)
- `GET /api/datasets/{id}/` - Get dataset details with full equipment list (requires authentication)
- `GET /api/datasets/{id}/summary/` - Get summary statistics (requires authentication)
- `GET /api/datasets/{id}/generate_report/` - Download PDF report (requires authentication)

**Note:** All dataset endpoints require `Authorization: Token <your-token>` header.

---

## 📝 CSV File Format

The CSV file should have the following columns:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Valve-1,Valve,60,4.1,105
...
```

**Required Columns:**
- `Equipment Name` - Name/ID of the equipment
- `Type` - Type/category of equipment
- `Flowrate` - Flow rate value
- `Pressure` - Pressure value
- `Temperature` - Temperature value

A sample file (`sample_equipment_data.csv`) is provided for testing.

---

## 🧪 Testing

### Test with Sample Data

1. **Start backend server**
   ```bash
   cd backend
   .\venv\Scripts\python.exe manage.py runserver
   ```

2. **Start desktop OR web app** (in new terminal)
   
   Desktop:
   ```bash
   cd frontend-desktop
   .\venv\Scripts\python.exe main.py
   ```
   
   Web:
   ```bash
   cd frontend-web
   npm start
   ```

3. **Register a new user** through the application
4. **Upload** `sample_equipment_data.csv` (15 equipment items)
5. **View** summary statistics:
   - Total: 15 items
   - Avg Flowrate: 127.13 L/min
   - Avg Pressure: 6.05 bar
   - Avg Temperature: 117.53°C
6. **View** visualizations in Charts tab
7. **Download** PDF report
8. **Check** history tab for saved datasets

### Creating Test Users

#### Via Application (Recommended):
- Use the registration form in web or desktop app
- No email verification required
- Instant token generation

#### Via Django Admin (Optional):
1. Create a superuser first: `python manage.py createsuperuser`
2. Go to `http://127.0.0.1:8000/admin/`
3. Login with superuser credentials
4. Create users and manually generate auth tokens

---

## 🎨 UI/UX Features

### Web Application
- Modern gradient design
- Responsive layout
- Interactive charts with Chart.js
- Real-time data updates
- Smooth animations

### Desktop Application
- Native Qt look and feel with Fusion style
- Tabbed interface (Summary, Charts, Data Table, History)
- High-quality matplotlib visualizations
- File dialogs for CSV upload and PDF save
- Authentication window with login/register
- Status messages and error handling
- Background server connectivity check

---

## 🔒 Security Features

- Token-based authentication
- Password encryption
- CORS configuration for API security
- Input validation
- SQL injection prevention (Django ORM)

---

## 📦 Database Models

### Dataset Model
- `name` - Dataset filename
- `uploaded_at` - Upload timestamp
- `uploaded_by` - User reference
- `total_count` - Total equipment count
- `avg_flowrate` - Average flowrate
- `avg_pressure` - Average pressure
- `avg_temperature` - Average temperature
- `equipment_types` - JSON field for type distribution

### Equipment Model
- `dataset` - Foreign key to Dataset
- `equipment_name` - Equipment name
- `equipment_type` - Equipment type
- `flowrate` - Flowrate value
- `pressure` - Pressure value
- `temperature` - Temperature value

---

## 🐛 Troubleshooting

### Backend Issues
- **Port already in use**: Change port with `python manage.py runserver 8001`
- **Module not found**: Ensure virtual environment is activated (`.\venv\Scripts\activate`) and dependencies installed
- **Database errors**: Run migrations with `python manage.py makemigrations` then `python manage.py migrate`
- **CORS errors**: Ensure `django-cors-headers` is installed and configured in settings.py

### Web Frontend Issues
- **npm install fails**: Try `npm install --legacy-peer-deps`
- **"Cannot connect to backend"**: Ensure Django server is running on `http://127.0.0.1:8000`
- **Port 3000 already in use**: Kill the process or use a different port
- **Deprecation warnings**: These are normal and don't affect functionality

### Desktop Frontend Issues
- **PyQt5 import errors in VS Code**: These are editor warnings only - the code runs fine. See `.vscode/settings.json` for configuration
- **"Backend not running" error**: Start the Django server first before launching desktop app
- **matplotlib backend issues**: Use the provided `launcher.py` which handles dependencies
- **DLL load failed (Windows)**: Install Microsoft Visual C++ 2015-2022 Redistributable

---

## 🚀 Quick Start (Windows)

The project includes batch files for easy setup and execution:

### First Time Setup
```bash
# 1. Setup backend
run setup_backend.bat

# 2. Setup web frontend
run setup_web.bat

# 3. Setup desktop frontend
run setup_desktop.bat
```

### Running the Application
```bash
# 1. Start backend server
run run_backend.bat

# 2. Start desktop app (in new terminal)
run run_desktop.bat

# OR start web app (in new terminal)
run run_web.bat
```

### Interactive Setup
```bash
# Run the interactive menu
run START_HERE.bat
```

## 🚀 Deployment Considerations

### Backend (Production)
- Use PostgreSQL instead of SQLite
- Set `DEBUG = False` in settings.py
- Configure proper SECRET_KEY
- Use gunicorn or uwsgi
- Set up proper ALLOWED_HOSTS
- Use environment variables for secrets
- Configure static file serving

### Web Frontend (Production)
- Run `npm run build`
- Serve static files with nginx or Apache
- Configure proper API URL (not localhost)
- Enable HTTPS

### Desktop Application (Distribution)
- Use PyInstaller to create executables
- Bundle required dependencies
- Create installers for different OS (NSIS, .dmg, .deb)

---

## 👥 About This Project

This project was developed as an **intern screening task** demonstrating:
- ✅ Full-stack development skills (Backend + Web + Desktop)
- ✅ RESTful API design and integration
- ✅ Data processing and analytics with Pandas
- ✅ Data visualization (Chart.js + Matplotlib)
- ✅ Multiple frontend technologies (React + PyQt5)
- ✅ Authentication and security
- ✅ PDF report generation
- ✅ Clean code practices and modular architecture
- ✅ Comprehensive documentation
- ✅ Cross-platform compatibility

**Technologies Versions:**
- Django 4.2.7
- Django REST Framework 3.14.0
- React 18.2.0
- PyQt5 5.15.10
- Matplotlib 3.8.2
- Pandas 2.1.3
- ReportLab 4.0.7

---

## 📄 License

This project is developed for educational and evaluation purposes.

---

## 🙏 Acknowledgments

- Django REST Framework documentation
- React.js community
- PyQt5 documentation
- Chart.js and Matplotlib libraries
- Sample chemical equipment data

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API endpoint documentation
3. Check console/terminal for error messages
4. Verify all services are running

---

**Built with ❤️ for Chemical Equipment Analysis**

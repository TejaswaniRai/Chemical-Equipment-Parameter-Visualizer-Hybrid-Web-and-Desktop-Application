# Chemical Equipment Parameter Visualizer
## Hybrid Web + Desktop Application

A comprehensive hybrid application for visualizing and analyzing chemical equipment parameters. Built with Django backend, React web frontend, and PyQt5 desktop application.

---

## 🎯 Project Overview

This application allows users to:
- 🔐 **Secure Authentication** - User registration and login with token-based auth
- 📤 **Upload CSV** files containing chemical equipment data
- 📊 **View Analytics** - Detailed summary statistics and visualizations
- 🔄 **Real-Time Monitoring** - Auto-refresh every 5 seconds
- 👤 **User Isolation** - Each user sees only their own uploaded datasets
- 📈 **Interactive Charts** - Beautiful visualizations with Chart.js and Matplotlib
- 📄 **Generate PDF Reports** - Professional formatted analysis reports
- 💻 **Dual Interface** - Access through both web browser and desktop application
- 🕐 **History Management** - Track last 5 uploaded datasets per user

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

### 🔐 Authentication & Security
- User registration with validation (minimum 6 characters password)
- Secure login with token-based authentication
- User-specific data isolation (users only see their own uploads)
- Encrypted password storage
- Clear error messages and validation feedback
- Mandatory backend connectivity checks

### 📤 CSV Upload & Processing
- Upload CSV files with equipment data
- Automatic validation of required columns
- Server-side processing with Pandas
- Real-time file validation and error handling

### 📊 Data Analytics
- Calculate summary statistics (averages, totals, counts)
- Equipment type distribution analysis
- Parameter comparisons across equipment
- Real-time data processing

### 📈 Advanced Visualizations

**Web Application (Chart.js):**
- 🥧 Pie chart for equipment type distribution
- 📊 Bar chart for equipment type counts
- 📉 Line chart for parameter trends
- Interactive charts with hover details

**Desktop Application (Matplotlib):**
- 🥧 Enhanced pie chart with gradient colors and exploded slices
- 📊 Horizontal bar chart for better label readability
- 🎨 Professional styling with grid lines and legends
- 🔍 Limited to 10 items for clarity (with indicator if more exist)
- 📏 Auto-scaling and proper spacing
- 💾 High-quality vector graphics

### 🔄 Real-Time Monitoring
- **Auto-refresh every 5 seconds** for both web and desktop
- Toggle button to pause/resume auto-refresh
- Visual indicators showing last update timestamp
- Background updates without disrupting user workflow
- Live dataset count updates

### 👥 User Isolation
- Each user has a private workspace
- Datasets filtered by authenticated user
- No cross-user data visibility
- Separate upload history per user
- Secure data segregation at database level

### 🕐 History Management
- Stores last 5 uploaded datasets **per user**
- View previous analyses with full details
- Click to switch between datasets
- Shows upload timestamp and username
- Empty state with helpful guidance

### 📄 PDF Report Generation
- Professional formatted reports with ReportLab
- Includes summary statistics table
- Equipment type distribution breakdown
- Complete detailed equipment listings
- Downloadable from both web and desktop interfaces
- Custom naming based on dataset

### 🎨 Modern UI/UX

**Desktop Application:**
- Gradient stat cards with large, clear numbers
- Scrollable charts tab for better organization
- Improved spacing and layout
- Styled data table with alternating row colors
- Color-coded toggle buttons (Green = ON, Red = OFF)
- Group boxes with clear section headers

**Web Application:**
- Clean, modern gradient design
- Responsive layout for all screen sizes
- Smooth animations and transitions
- Status indicators with emojis
- Color-coded refresh button (Green = ON, Pink = OFF)

---

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user

### Datasets
- `GET /api/datasets/` - List last 5 datasets **for current user** (requires authentication)
- `POST /api/datasets/upload_csv/` - Upload CSV file (requires authentication)
- `GET /api/datasets/{id}/` - Get dataset details with full equipment list (requires authentication)
- `GET /api/datasets/{id}/summary/` - Get summary statistics (requires authentication)
- `GET /api/datasets/{id}/generate_report/` - Download PDF report (requires authentication)

**Note:** 
- All dataset endpoints require `Authorization: Token <your-token>` header
- Datasets are filtered by authenticated user (user isolation)
- Each user only sees their own uploaded datasets

---

## 📝 CSV File Format

The CSV file should have the following columns:
**Required Columns:**
- `Equipment Name` - Name/ID of the equipment
- `Type` - Type/category of equipment
- `Flowrate` - Flow rate value
- `Pressure` - Pressure value
- `Temperature` - Temperature value

A sample file (`sample_equipment_data.csv`) is provided for testing.

---

## 🧪 Testing

### Automated Test Scripts

Run these scripts to verify functionality:

```bash
# Test authentication security
cd frontend-desktop
python test_auth.py

# Test user isolation
python ..\test_user_isolation.py
```

### Manual Test with Sample Data

1. **Start backend server**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Start desktop OR web app** (in new terminal)
   
   Desktop:
   ```bash
   cd frontend-desktop
   python launcher.py
   ```
   
   Web:
   ```bash
   cd frontend-web
   npm start
   ```

3. **Register User 1**
   - Username: `user1`, Password: `password123`
   - Upload `sample_equipment_data.csv` (15 equipment items)
   - Note: You see 1 dataset in history

4. **Register User 2** (new window/browser tab)
   - Username: `user2`, Password: `password456`
   - Upload the same or different CSV file
   - Note: You see 1 dataset in history (only user2's upload)

5. **Verify User Isolation**
   - User1 sees ONLY user1's data ✅
   - User2 sees ONLY user2's data ✅
   - No cross-user data visible ✅

6. **Test Real-Time Monitoring**
   - Open two app instances (user1 and user2)
   - Upload in one window
   - Watch auto-refresh update within 5 seconds ✅
   - Other user's window doesn't show the upload ✅

7. **View Statistics** for sample data:
   - Total: 15 items
   - Avg Flowrate: 119.80 L/min
   - Avg Pressure: 6.05 bar
   - Avg Temperature: 117.53°C

8. **Test UI Features**
   - View improved horizontal bar charts in Charts tab
   - Scroll through charts for better viewing
   - Click auto-refresh toggle (Green ↔ Red/Pink)
   - Check timestamp updates
   - View styled data table with alternating colors
   - Check gradient stat cards in Summary tab

9. **Download PDF report**
10. **Check history tab** - shows only your uploads

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
- 🎨 Modern gradient design with purple/blue theme
- 📱 Fully responsive layout for all screen sizes
- 📊 Interactive charts with Chart.js (hover for details)
- 🔄 Real-time auto-refresh with toggle (every 5 seconds)
- ⏰ Last update timestamp display
- 🎬 Smooth animations and transitions
- 🟢 Color-coded status indicators (Green = ON, Pink = OFF)
- ✨ Clean, card-based layout

### Desktop Application
- 🖥️ Native Qt look and feel with Fusion style
- 📑 Tabbed interface (Summary, Charts, Data Table, History)
- 📊 High-quality matplotlib visualizations with:
  - Horizontal bar charts for better readability
  - Gradient pie charts with exploded slices
  - Professional grid lines and legends
  - Auto-scaling for optimal display
- 📜 Scrollable charts tab for better organization
- 💳 Gradient stat cards with large, clear numbers
- 🎨 Styled data table with alternating row colors
- 📂 File dialogs for CSV upload and PDF save
- 🔐 Polished authentication window with login/register
- ✅ Clear status messages with emoji indicators
- ⚠️ Detailed error handling and validation feedback
- 🔄 Auto-refresh toggle with visual feedback
- 🛡️ Mandatory backend connectivity check (no bypass)

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
- **"Backend not running" error**: The launcher now requires backend - start Django server first
- **matplotlib backend issues**: Use the provided `launcher.py` which handles dependencies
- **DLL load failed (Windows)**: Install Microsoft Visual C++ 2015-2022 Redistributable
- **Charts not displaying properly**: Charts now use horizontal bars and scrollable layout - scroll down to see all charts
- **Auto-refresh not working**: Check that backend is running and toggle button shows "ON" (green)

### Authentication Issues
- **"Invalid credentials"**: User doesn't exist - register first or check username/password
- **"Username already taken"**: Choose a different username
- **Can't register/login**: Ensure backend server is running at `http://localhost:8000`
- **Token expired**: Logout and login again to get a new token

### User Isolation Issues
- **Seeing other users' data**: Restart backend server to load updated code
- **History shows wrong data**: Each user now sees only their own uploads - this is correct behavior
- **Empty history after login**: Upload a CSV file to populate your personal history

---

## 📄 License

This project is developed for educational and evaluation purposes.

---
## 👨‍💻 Developer

**Tejaswani Rai**
- GitHub: [@TejaswaniRai](https://github.com/TejaswaniRai)
- Linkedin: [@Tejaswani Rai](https://www.linkedin.com/in/tejaswani-rai/)
- Repository: [Chemical-Equipment-Parameter-Visualizer](https://github.com/TejaswaniRai/Chemical-Equipment-Parameter-Visualizer-Hybrid-Web-and-Desktop-Application)

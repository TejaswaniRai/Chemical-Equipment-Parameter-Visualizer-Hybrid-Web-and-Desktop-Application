# Project Architecture & Features Documentation

## 🏗️ Architecture Overview

### System Design
```
┌─────────────────────────────────────────────────────────────┐
│                         Clients                              │
│  ┌──────────────────────┐    ┌──────────────────────┐      │
│  │   React Web App      │    │  PyQt5 Desktop App   │      │
│  │  (Chart.js Charts)   │    │ (Matplotlib Charts)  │      │
│  └──────────────────────┘    └──────────────────────┘      │
│            │                           │                     │
│            └───────────┬───────────────┘                     │
│                        │                                     │
│                   HTTP/REST API                              │
│                        │                                     │
└────────────────────────┼─────────────────────────────────────┘
                         │
         ┌───────────────▼────────────────┐
         │    Django Backend (Port 8000)  │
         │  ┌──────────────────────────┐  │
         │  │  Django REST Framework   │  │
         │  │  - Authentication        │  │
         │  │  - API Endpoints         │  │
         │  │  - Serializers           │  │
         │  └──────────────────────────┘  │
         │  ┌──────────────────────────┐  │
         │  │  Business Logic Layer    │  │
         │  │  - CSV Processing        │  │
         │  │  - Data Analytics        │  │
         │  │  - PDF Generation        │  │
         │  └──────────────────────────┘  │
         │  ┌──────────────────────────┐  │
         │  │  Data Layer (SQLite)     │  │
         │  │  - Dataset Model         │  │
         │  │  - Equipment Model       │  │
         │  │  - User Model            │  │
         │  └──────────────────────────┘  │
         └────────────────────────────────┘
```

---

## 🔄 Data Flow

### CSV Upload Flow
```
1. User selects CSV file (Web or Desktop)
2. File sent to backend via POST /api/datasets/upload_csv/
3. Backend validates file format and columns
4. Pandas processes CSV and extracts data
5. Summary statistics calculated
6. Dataset and Equipment records created in database
7. Old datasets pruned (keep last 5)
8. Response sent back with complete dataset info
9. Frontend updates charts and tables
```

### Authentication Flow
```
1. User enters credentials
2. POST to /api/auth/login/ or /api/auth/register/
3. Backend validates credentials
4. Token generated and returned
5. Frontend stores token (localStorage/memory)
6. Token included in all subsequent API requests
7. Backend validates token for each request
```

---

## 📊 Feature Implementation Details

### 1. CSV Upload & Processing

**Frontend (Web - React)**
```javascript
- File input component
- FormData API for file upload
- Axios for HTTP request
- Error handling and validation
```

**Frontend (Desktop - PyQt5)**
```python
- QFileDialog for file selection
- requests library for HTTP
- File reading and sending
```

**Backend (Django)**
```python
- DRF APIView with @action decorator
- File validation (type, size)
- Pandas DataFrame processing
- Model creation (Dataset, Equipment)
- Transaction handling
```

### 2. Data Visualization

**Web (Chart.js)**
- Pie chart for equipment type distribution
- Bar chart for type counts
- Line chart for multi-parameter comparison
- Responsive design
- Interactive tooltips

**Desktop (Matplotlib)**
- Figure and canvas integration with PyQt5
- Pie chart with autopct formatting
- Multi-bar chart with grouped bars
- Custom colors and styling
- Export capability

### 3. Authentication & Security

**Implementation**
- Token-based authentication (DRF TokenAuthentication)
- Password hashing (Django's built-in)
- CORS headers for cross-origin requests
- CSRF protection
- SQL injection prevention (ORM)

**Token Management**
- Web: localStorage
- Desktop: in-memory storage
- Automatic inclusion in API headers
- Logout clears tokens

### 4. PDF Report Generation

**Technology**: ReportLab

**Report Sections**
1. Title page with dataset info
2. Summary statistics table
3. Equipment type distribution table
4. Detailed equipment listing (paginated)
5. Professional styling with colors

**Features**
- Custom page layout
- Tables with styling
- Dynamic content
- PDF download via browser/file dialog

### 5. History Management

**Database Strategy**
- Store all datasets with timestamps
- Query last 5 ordered by upload time
- Cascade delete for related equipment
- Automatic pruning on new upload

**UI Display**
- List view with summary info
- Click to load full dataset
- Visual indication of active dataset
- Timestamp formatting

---

## 🔐 API Specification

### Authentication Endpoints

#### POST /api/auth/register/
**Request**
```json
{
  "username": "string",
  "password": "string",
  "email": "string (optional)"
}
```

**Response (201)**
```json
{
  "token": "string",
  "user_id": integer,
  "username": "string"
}
```

#### POST /api/auth/login/
**Request**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200)**
```json
{
  "token": "string",
  "user_id": integer,
  "username": "string"
}
```

### Dataset Endpoints

#### GET /api/datasets/
**Headers**: `Authorization: Token <token>`

**Response (200)**
```json
[
  {
    "id": integer,
    "name": "string",
    "uploaded_at": "datetime",
    "uploaded_by_username": "string",
    "total_count": integer,
    "avg_flowrate": float,
    "avg_pressure": float,
    "avg_temperature": float,
    "equipment_types": {
      "Type1": count,
      "Type2": count
    }
  }
]
```

#### POST /api/datasets/upload_csv/
**Headers**: 
- `Authorization: Token <token>`
- `Content-Type: multipart/form-data`

**Request**: FormData with 'file' field

**Response (201)**
```json
{
  "id": integer,
  "name": "string",
  "uploaded_at": "datetime",
  "total_count": integer,
  "avg_flowrate": float,
  "avg_pressure": float,
  "avg_temperature": float,
  "equipment_types": {},
  "equipment_items": [
    {
      "id": integer,
      "equipment_name": "string",
      "equipment_type": "string",
      "flowrate": float,
      "pressure": float,
      "temperature": float
    }
  ]
}
```

#### GET /api/datasets/{id}/
**Headers**: `Authorization: Token <token>`

**Response**: Same as upload response

#### GET /api/datasets/{id}/generate_report/
**Headers**: `Authorization: Token <token>`

**Response**: PDF file (application/pdf)

---

## 🗄️ Database Schema

### Dataset Table
```sql
CREATE TABLE dataset (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    uploaded_at DATETIME,
    uploaded_by_id INTEGER REFERENCES auth_user(id),
    file_path VARCHAR(500),
    total_count INTEGER,
    avg_flowrate REAL,
    avg_pressure REAL,
    avg_temperature REAL,
    equipment_types TEXT (JSON)
);
```

### Equipment Table
```sql
CREATE TABLE equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id INTEGER REFERENCES dataset(id) ON DELETE CASCADE,
    equipment_name VARCHAR(255),
    equipment_type VARCHAR(100),
    flowrate REAL,
    pressure REAL,
    temperature REAL
);
```

---

## 🎨 UI/UX Design Principles

### Web Application
- **Color Scheme**: Purple gradient (#667eea → #764ba2)
- **Layout**: Card-based, responsive grid
- **Typography**: System fonts, clear hierarchy
- **Interactions**: Hover effects, smooth transitions
- **Feedback**: Toast messages, loading states

### Desktop Application
- **Style**: Fusion (Qt style)
- **Layout**: Tabbed interface for organization
- **Components**: Native Qt widgets
- **Colors**: Matching web app theme
- **Dialogs**: Standard file/message dialogs

---

## 🧪 Testing Strategy

### Manual Testing Checklist
- [ ] User registration works
- [ ] User login works
- [ ] CSV upload validates file type
- [ ] CSV upload validates columns
- [ ] Summary statistics calculated correctly
- [ ] Charts render properly
- [ ] Data table displays all rows
- [ ] PDF report generates successfully
- [ ] History shows last 5 datasets
- [ ] Switching datasets updates UI
- [ ] Token authentication works
- [ ] Logout clears session

### Test Data
- Use `sample_equipment_data.csv` provided
- 15 equipment items
- 6 different types
- Valid numeric values

---

## 🚀 Performance Considerations

### Backend Optimization
- Database indexing on foreign keys
- Efficient QuerySet usage
- JSON field for equipment_types (avoid joins)
- Limit history to 5 datasets

### Frontend Optimization
- React component memoization
- Chart.js lazy loading
- Conditional rendering
- Efficient state management

### Desktop Optimization
- PyQt5 event-driven architecture
- Matplotlib figure reuse
- Efficient table updates
- Background thread for API calls (if needed)

---

## 🔧 Customization Guide

### Adding New Parameters
1. Update CSV columns
2. Add fields to Equipment model
3. Run migrations
4. Update serializers
5. Modify analytics calculations
6. Update chart components

### Changing Retention Count
```python
# In views.py, change:
if all_datasets.count() > 5:  # Change 5 to desired count
```

### Customizing Charts
**Web**: Modify chart options in App.js
**Desktop**: Modify plot functions in main.py

---

## 📚 Technology References

- **Django**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **React**: https://react.dev/
- **Chart.js**: https://www.chartjs.org/
- **PyQt5**: https://www.riverbankcomputing.com/static/Docs/PyQt5/
- **Matplotlib**: https://matplotlib.org/
- **Pandas**: https://pandas.pydata.org/
- **ReportLab**: https://www.reportlab.com/documentation/

---

**Last Updated**: November 2025

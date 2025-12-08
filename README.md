# 🐾 StudyPack

**A Collaborative Learning Platform for Students, Tutors, and Teaching Staff**

---

## 📖 About StudyPack

StudyPack consolidates study resources, facilitates peer collaboration, and streamlines coordination between students, peer tutors, teaching assistants, and professors at Northeastern University.

**The Problem**: Students struggle with scattered resources across multiple platforms, difficult study session coordination, and fragmented communication with teaching staff.

**Our Solution**: One centralized platform for discovering study sessions, accessing course materials, requesting help, and managing academic resources.

---

##  Team: Pawgrammers

- **Alayna Schwarzer** - schwarzer.a@northeastern.edu
- **Nancy Guan** - guan.na@northeastern.edu
- **Liya Liju** - liju.l@northeastern.edu
- **Ananya Krishnamurthy** - krishnamurthy.an@northeastern.edu

---

##  Quick Start

### Prerequisites
- Docker Desktop
- Git

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/aschwarzer101/25F-Study-Pack-Project.git
cd 25F-Study-Pack-Project
```

2. **Create `.env` file** in project root:
```env
SECRET_KEY=your_secret_key_here
DB_USER=root
MYSQL_ROOT_PASSWORD=your_password_here
DB_HOST=mysql_db
DB_PORT=3306
DB_NAME=StudyPack
```

3. **Start the application**
```bash
docker compose up -d
```

4. **Access the application**
- **Streamlit UI**: http://localhost:8501
- **REST API**: http://localhost:4000
- **Database**: localhost:3200

### Rebuilding After Changes

```bash
docker compose down -v
docker compose up -d
```

---

## Key Features by User Role

###  Professor
- Upload and manage course materials
- Track student study patterns by topic
- Create courses and update resources
- View student engagement analytics

###  TA Admin
- Manage student enrollments and course sections
- Approve/reject study session requests
- Assign TAs to study sessions
- Manage study locations
- Consolidate duplicate request tags
- Post announcements

###  Student
- Find and join active study sessions
- Create help requests
- Upload and access course materials
- Contact TAs and peer tutors
- Search courses and resources

###  Peer Tutor
- View sessions requesting tutors
- Filter sessions by course/topic
- Access course materials
- Upload study resources
- Organize group tutoring sessions

---

## API Structure

Our REST API is organized into **5 blueprints** with **46 total routes**:

### Blueprints

1. **Student Management** (`/sm`) - Student CRUD, peer tutor operations
2. **Course Resources** (`/cr`) - Courses, enrollments, materials, topics
3. **Session Info** (`/si`) - Study sessions and locations
4. **Requests & Tags** (`/rt`) - Session requests and tag management
5. **Personnel Assignment** (`/pa`) - TAs, admins, and assignments

### Example Endpoints

```bash
# Students
GET    /sm/students
POST   /sm/students
PUT    /sm/students/{nuID}
DELETE /sm/students/{nuID}

# Session Requests
GET    /rt/session_requests?status=Pending
POST   /rt/session_requests
PUT    /rt/session_requests/{requestID}
DELETE /rt/session_requests/{requestID}

# Study Sessions
GET    /si/study_sessions
POST   /si/study_sessions
PUT    /si/study_sessions/{sessionID}
DELETE /si/study_sessions/{sessionID}
```

See full API documentation in the code comments within each blueprint file.

---

##  Database

**Database Name**: StudyPack  
**Tables**: 15+ tables including Student, Course, StudySession, Resource, SessionRequest, and more  
**Sample Data**: Generated using Mockaroo with realistic test data

For complete schema details, see our Phase 2 ER diagrams and DDL documentation.

---

## Streamlit Pages

### Structure
- **Main Home**: User role selection (Professor, TA Admin, Student, Tutor)
- **4 Home Pages**: One for each user role
- **12+ Feature Pages**: 3 per user role covering core functionality

### TA Admin Pages
- Student & TA Management
- Session Requests Dashboard  
- Location Management

### Student Pages
- Study Session Finder
- Course Materials Browser
- Create Session Request

### Additional Pages
- Professor: Topic Analytics, Resource Management
- Tutor: Available Sessions, Materials Access

---

##  Testing

### Test API
```bash
# Test connection
curl http://localhost:4000/

# Get all students
curl http://localhost:4000/sm/students

# Get pending requests
curl http://localhost:4000/rt/session_requests?status=Pending
```

### Test Database
```bash
# Connect to MySQL
docker exec -it <mysql-container-name> mysql -u root -p

# Verify data
USE StudyPack;
SHOW TABLES;
SELECT * FROM Student LIMIT 5;
```

---

##  Common Issues

**Containers won't start**: Check Docker Desktop is running, try `docker compose build`

**Database connection failed**: Verify `.env` has `DB_NAME=StudyPack` and `DB_HOST=mysql_db`

**API returns 404**: Check blueprint is registered in `rest_entry.py` with correct prefix

**Changes not reflecting**: Recreate containers with `docker compose down -v && docker compose up -d`

---

##  Demo Video

[Link to be added after recording]

---

##  Project Documentation

This project was developed in three phases:
- **Phase 1**: User personas, stories, and wireframes
- **Phase 2**: ER diagrams, database design, and SQL implementation
- **Phase 3**: REST API, Streamlit UI, and full-stack integration

---

##  Acknowledgments

**CS 3200 - Database Design**  
**Fall 2025**  
**Northeastern University Khoury College of Computer Sciences**

Special thanks to Professor Mark Fontenot and the CS 3200 teaching staff.

---

**Built with ❤️ by Team Pawgrammers** 🐾

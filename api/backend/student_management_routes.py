import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(layout='wide')

SideBarLinks()

st.title('📚 Available Study Sessions')

st.write("## All Upcoming Study Sessions")

if st.button("Load All Sessions", type="primary", use_container_width=True):
    try:
        url = "http://web-api:4000/sessions"
        response = requests.get(url)
        sessions = response.json()
        
        if sessions and len(sessions) > 0:
            st.success(f"Found {len(sessions)} study sessions!")
            df = pd.DataFrame(sessions)
            
            # Format datetime columns for better display
            if 'startTime' in df.columns:
                df['startTime'] = pd.to_datetime(df['startTime']).dt.strftime('%I:%M %p')
            if 'endTime' in df.columns:
                df['endTime'] = pd.to_datetime(df['endTime']).dt.strftime('%I:%M %p')
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No study sessions found.")
    except Exception as e:
        st.error(f"Error loading sessions: {e}")

st.write("---")


st.write("## 🔍 Search by Location")

col1, col2 = st.columns(2)

with col1:
    building = st.selectbox("Select building:", 
                           ["All Buildings", "Snell Library", "Curry Student Center", 
                            "Forsyth Building", "Ryder Hall"])

with col2:
    room = st.text_input("Room number (optional):", "")

if st.button("Search by Location", use_container_width=True):
    try:
        building_param = "" if building == "All Buildings" else building
        url = f"http://web-api:4000/sessions/location?building={building_param}&room={room}"
        results = requests.get(url).json()
        
        if results and len(results) > 0:
            st.success(f"Found {len(results)} sessions!")
            df = pd.DataFrame(results)
            
            # Format times
            if 'startTime' in df.columns:
                df['startTime'] = pd.to_datetime(df['startTime']).dt.strftime('%I:%M %p')
            if 'endTime' in df.columns:
                df['endTime'] = pd.to_datetime(df['endTime']).dt.strftime('%I:%M %p')
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No sessions found for this location.")
    except Exception as e:
        st.error(f"Error: {e}")

st.write("---")


st.write("## 📅 Search by Date")

session_date = st.date_input("Select date:", datetime.now())

if st.button("Search by Date", use_container_width=True):
    try:
        url = f"http://web-api:4000/sessions/date/{session_date}"
        results = requests.get(url).json()
        
        if results and len(results) > 0:
            st.success(f"Found {len(results)} sessions on {session_date}")
            df = pd.DataFrame(results)
            
            if 'startTime' in df.columns:
                df['startTime'] = pd.to_datetime(df['startTime']).dt.strftime('%I:%M %p')
            if 'endTime' in df.columns:
                df['endTime'] = pd.to_datetime(df['endTime']).dt.strftime('%I:%M %p')
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No sessions found for this date.")
    except Exception as e:
        st.error(f"Error: {e}")

st.write("---")


st.write("## 📋 View Session Details")

session_id = st.number_input("Enter Session ID:", min_value=1000, max_value=1100, value=1001, step=1)

col1, col2 = st.columns(2)

with col1:
    if st.button("Get Session Details", use_container_width=True):
        try:
            # Get session basic info
            url = f"http://web-api:4000/sessions/{session_id}"
            response = requests.get(url)
            
            if response.status_code == 200:
                session = response.json()
                
                if session and 'sessionID' in session:
                    st.success("Session found!")
                    
                    # Display session info in columns
                    info_col1, info_col2, info_col3 = st.columns(3)
                    
                    with info_col1:
                        st.write("**📅 Session Information:**")
                        st.write(f"Date: {session.get('date', 'N/A')}")
                        start_time = pd.to_datetime(session.get('startTime')).strftime('%I:%M %p') if session.get('startTime') else 'N/A'
                        end_time = pd.to_datetime(session.get('endTime')).strftime('%I:%M %p') if session.get('endTime') else 'N/A'
                        st.write(f"Time: {start_time} - {end_time}")
                    
                    with info_col2:
                        st.write("**🏢 Location:**")
                        st.write(f"Building: {session.get('building', 'N/A')}")
                        st.write(f"Room: {session.get('room', 'N/A')}")
                        st.write(f"Capacity: {session.get('capacity', 'N/A')}")
                    
                    with info_col3:
                        st.write("**📊 Status:**")
                        status = "✅ Available" if session.get('status') == 1 else "❌ Unavailable"
                        st.write(status)
                    
                    st.write("---")
                    
                    # Get topics covered
                    st.write("**📚 Topics Covered:**")
                    try:
                        topics_url = f"http://web-api:4000/sessions/{session_id}/topics"
                        topics_response = requests.get(topics_url)
                        
                        if topics_response.status_code == 200:
                            topics = topics_response.json()
                            
                            if topics and len(topics) > 0:
                                for topic in topics:
                                    course_info = f"{topic.get('department', '')} {topic.get('courseName', '')}" if 'department' in topic else ""
                                    st.write(f"• {topic.get('name', 'Unknown topic')} ({course_info})")
                            else:
                                st.info("No topics listed for this session")
                        else:
                            st.info("Topics information unavailable")
                    except Exception as e:
                        st.warning(f"Could not load topics: {e}")
                    
                    # Get attending TAs
                    st.write("**👨‍🏫 Teaching Assistants:**")
                    try:
                        tas_url = f"http://web-api:4000/sessions/{session_id}/tas"
                        tas_response = requests.get(tas_url)
                        
                        if tas_response.status_code == 200:
                            tas = tas_response.json()
                            
                            if tas and len(tas) > 0:
                                for ta in tas:
                                    st.write(f"• {ta.get('firstName', '')} {ta.get('lastName', '')} - {ta.get('email', '')}")
                            else:
                                st.info("No TAs assigned yet")
                        else:
                            st.info("TA information unavailable")
                    except Exception as e:
                        st.warning(f"Could not load TAs: {e}")
                    
                    # Get students enrolled
                    st.write("**👥 Students Enrolled:**")
                    try:
                        students_url = f"http://web-api:4000/sessions/{session_id}/students"
                        students_response = requests.get(students_url)
                        
                        if students_response.status_code == 200:
                            students = students_response.json()
                            
                            if students and len(students) > 0:
                                st.write(f"Total students: {len(students)}")
                                with st.expander("View student list"):
                                    for student in students:
                                        st.write(f"• {student.get('firstName', '')} {student.get('lastName', '')} ({student.get('majorOne', 'N/A')})")
                            else:
                                st.info("No students enrolled yet")
                        else:
                            st.info("Student information unavailable")
                    except Exception as e:
                        st.warning(f"Could not load students: {e}")
                else:
                    st.warning("Session not found.")
            elif response.status_code == 404:
                st.error("Session not found.")
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")

with col2:
    # Join/Leave session functionality
    st.write("**Join or Leave Session:**")
    
    student_nuid = st.number_input("Enter your NUID:", min_value=100000000, max_value=999999999, value=2345678, step=1)
    
    join_col, leave_col = st.columns(2)
    
    with join_col:
        if st.button("Join Session", type="primary", use_container_width=True):
            try:
                url = f"http://web-api:4000/sessions/{session_id}/join"
                data = {"nuID": student_nuid}
                response = requests.post(url, json=data)
                
                if response.status_code == 201:
                    st.success("Successfully joined the session!")
                elif response.status_code == 400:
                    st.warning(response.json().get('error', 'Already enrolled or invalid request'))
                elif response.status_code == 404:
                    st.error(response.json().get('error', 'Session or student not found'))
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    with leave_col:
        if st.button("Leave Session", use_container_width=True):
            try:
                url = f"http://web-api:4000/sessions/{session_id}/leave"
                data = {"nuID": student_nuid}
                response = requests.delete(url, json=data)
                
                if response.status_code == 200:
                    st.success("Successfully left the session!")
                elif response.status_code == 404:
                    st.warning("Not enrolled in this session or session not found")
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {e}")

st.write("---")

# GET - Return all students [TA-1]
@student_management.route("/students", methods=["GET"])
def get_all_students():
   """Get all students"""
   try:
       current_app.logger.info('Getting all students')
       cursor = db.get_db().cursor()
       
       query = """
           SELECT nuID, firstName, lastName, email, gradYear,
                  classYear, majorOne, majorTwo, minor
           FROM Student
           ORDER BY lastName, firstName
       """
       cursor.execute(query)
       
       students = cursor.fetchall()
       cursor.close()
       
       current_app.logger.info(f'Retrieved {len(students)} students')
       return jsonify(students), 200
   except Error as e:
       current_app.logger.error(f'Database error: {str(e)}')
       return jsonify({"error": str(e)}), 500

# POST - Add a new student [TA-1]
@student_management.route("/students", methods=["POST"])
def create_student():
   """Create a new student"""
   try:
       current_app.logger.info('Creating new student')
       data = request.get_json()
       
       required_fields = ["nuID", "firstName", "lastName", "email", "gradYear", "majorOne"]
       for field in required_fields:
           if field not in data:
               return jsonify({"error": f"Missing required field: {field}"}), 400
       
       cursor = db.get_db().cursor()
       
       query = """
           INSERT INTO Student (nuID, firstName, lastName, email, gradYear, majorOne, majorTwo, minor)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
       """
       cursor.execute(query, (
           data["nuID"],
           data["firstName"],
           data["lastName"],
           data["email"],
           data["gradYear"],
           data["majorOne"],
           data.get("majorTwo"),
           data.get("minor")
       ))
       
       db.get_db().commit()
       cursor.close()
       
       current_app.logger.info(f'Created student with nuID: {data["nuID"]}')
       return jsonify({
           "message": "Student created successfully",
           "nuID": data["nuID"]
       }), 201
   except Error as e:
       current_app.logger.error(f'Database error: {str(e)}')
       return jsonify({"error": str(e)}), 500

# GET - Return a student's information [Student-6] [Tutor-4]
@student_management.route("/student/<int:nuid>", methods=["GET"])
def get_student_info(nuid):
   """Get information about a specific student"""
   try:
       current_app.logger.info(f'Getting student info for nuID: {nuid}')
       cursor = db.get_db().cursor()
      
       query = """
           SELECT nuID, firstName, lastName, email, gradYear,
                  classYear, majorOne, majorTwo, minor
           FROM Student
           WHERE nuID = %s
       """
       cursor.execute(query, (nuid,))
       student = cursor.fetchone()
      
       if not student:
           return jsonify({"error": "Student not found"}), 404
      
       cursor.close()
       current_app.logger.info(f'Successfully retrieved student: {nuid}')
       return jsonify(student), 200
   except Error as e:
       current_app.logger.error(f'Database error: {str(e)}')
       return jsonify({"error": str(e)}), 500

# PUT - Update student information [Student-6] [TA-3]
@student_management.route("/student/<int:nuid>", methods=["PUT"])
def update_student_info(nuid):
   """Update a student's information"""
   try:
       data = request.get_json()
       cursor = db.get_db().cursor()
      
       cursor.execute("SELECT * FROM Student WHERE nuID = %s", (nuid,))
       if not cursor.fetchone():
           return jsonify({"error": "Student not found"}), 404
      
       update_fields = []
       params = []
       allowed_fields = ["firstName", "lastName", "email", "majorOne", "majorTwo", "minor"]
      
       for field in allowed_fields:
           if field in data:
               update_fields.append(f"{field} = %s")
               params.append(data[field])
      
       if not update_fields:
           return jsonify({"error": "No valid fields to update"}), 400
      
       params.append(nuid)
       query = f"UPDATE Student SET {', '.join(update_fields)} WHERE nuID = %s"
      
       cursor.execute(query, params)
       db.get_db().commit()
       cursor.close()
       return jsonify({"message": "Student information updated successfully"}), 200
   except Error as e:
       return jsonify({"error": str(e)}), 500

# DELETE - Remove a student [TA-1]
@student_management.route("/students/<int:nuid>", methods=["DELETE"])
def delete_student(nuid):
   """Delete a student from the system"""
   try:
       current_app.logger.info(f'Deleting student with nuID: {nuid}')
       cursor = db.get_db().cursor()
       
       cursor.execute("SELECT * FROM Student WHERE nuID = %s", (nuid,))
       if not cursor.fetchone():
           return jsonify({"error": "Student not found"}), 404
       
       cursor.execute("DELETE FROM Student WHERE nuID = %s", (nuid,))
       db.get_db().commit()
       cursor.close()
       
       current_app.logger.info(f'Successfully deleted student: {nuid}')
       return jsonify({"message": "Student deleted successfully"}), 200
   except Error as e:
       current_app.logger.error(f'Database error: {str(e)}')
       return jsonify({"error": str(e)}), 500

# POST - Convert student to peer tutor [TA-1]
@student_management.route("/peer_tutors/<int:nuid>", methods=["POST"])
def create_peer_tutor(nuid):
   """Convert a student to a peer tutor"""
   try:
       current_app.logger.info(f'Creating peer tutor from student: {nuid}')
       cursor = db.get_db().cursor()
       
       cursor.execute("SELECT firstName, lastName FROM Student WHERE nuID = %s", (nuid,))
       student = cursor.fetchone()
       
       if not student:
           return jsonify({"error": "Student not found"}), 404
       
       cursor.execute("SELECT * FROM PeerTutor WHERE nuID = %s", (nuid,))
       if cursor.fetchone():
           return jsonify({"error": "Student is already a peer tutor"}), 400
       
       query = """
           INSERT INTO PeerTutor (nuID, firstName, lastName)
           VALUES (%s, %s, %s)
       """
       cursor.execute(query, (nuid, student["firstName"], student["lastName"]))
       
       db.get_db().commit()
       cursor.close()
       
       current_app.logger.info(f'Successfully created peer tutor: {nuid}')
       return jsonify({
           "message": "Peer tutor created successfully",
           "nuID": nuid
       }), 201
   except Error as e:
       current_app.logger.error(f'Database error: {str(e)}')
       return jsonify({"error": str(e)}), 500
#>>>>>>> 0414d4bea87b7ab6a83fd9e0710380b51a9ef70c
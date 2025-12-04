
# NO LONGER IMPLEMENTING GROUP PROJECT

# # GET - Return members in a group and their details [Student-6]
# @students.route("/project_group/<int:team_id>/members", methods=["GET"])
# def get_project_group_members(team_id):
#    """Get all members of a project group with their contact information"""
#    try:
#        crn = request.args.get("crn")
      
#        if not crn:
#            return jsonify({"error": "Missing required parameter: crn"}), 400
      
#        cursor = db.get_db().cursor()
      
#        # Check if project group exists
#        cursor.execute("""
#            SELECT * FROM ProjectGroup
#            WHERE teamID = %s AND CRN = %s
#        """, (team_id, crn))
      
#        if not cursor.fetchone():
#            return jsonify({"error": "Project group not found"}), 404
      
#        # Get group members with contact info
#        query = """
#            SELECT pgs.firstName, pgs.lastName, s.email, s.nuID
#            FROM ProjectGroup_Student pgs
#            JOIN Student s ON pgs.nuID = s.nuID
#            WHERE pgs.teamID = %s AND pgs.CRN = %s
#        """
      
#        cursor.execute(query, (team_id, crn))
#        members = cursor.fetchall()
#        cursor.close()
      
#        return jsonify(members), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500




# # GET - Get all project groups for a course
# @students.route("/project_group", methods=["GET"])
# def get_project_groups():
#    """Get all project groups, optionally filtered by course CRN"""
#    try:
#        crn = request.args.get("crn")
      
#        cursor = db.get_db().cursor()
      
#        if crn:
#            query = """
#                SELECT teamID, CRN, teamName
#                FROM ProjectGroup
#                WHERE CRN = %s
#            """
#            cursor.execute(query, (crn,))
#        else:
#            query = "SELECT teamID, CRN, teamName FROM ProjectGroup"
#            cursor.execute(query)
      
#        groups = cursor.fetchall()
#        cursor.close()
      
#        return jsonify(groups), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500




# # POST - Create a project group [Student-6]
# @students.route("/project_group", methods=["POST"])
# def create_project_group():
#    """Create a new project group"""
#    try:
#        data = request.get_json()
      
#        # Validate required fields
#        required_fields = ["teamID", "CRN", "teamName"]
#        for field in required_fields:
#            if field not in data:
#                return jsonify({"error": f"Missing required field: {field}"}), 400
      
#        cursor = db.get_db().cursor()
      
#        query = """
#            INSERT INTO ProjectGroup (teamID, CRN, teamName)
#            VALUES (%s, %s, %s)
#        """
      
#        cursor.execute(query, (
#            data["teamID"],
#            data["CRN"],
#            data["teamName"]
#        ))
      
#        db.get_db().commit()
#        cursor.close()
      
#        return jsonify({
#            "message": "Project group created successfully",
#            "teamID": data["teamID"]
#        }), 201
#    except Error as e:
#        return jsonify({"error": str(e)}), 500




# # PUT - Edit a project group [Student-6]
# @students.route("/project_group/<int:team_id>", methods=["PUT"])
# def update_project_group(team_id):
#    """Update a project group's information"""
#    try:
#        data = request.get_json()
#        crn = request.args.get("crn")
      
#        if not crn:
#            return jsonify({"error": "Missing required parameter: crn"}), 400
      
#        cursor = db.get_db().cursor()
      
#        # Check if project group exists
#        cursor.execute("""
#            SELECT * FROM ProjectGroup
#            WHERE teamID = %s AND CRN = %s
#        """, (team_id, crn))
      
#        if not cursor.fetchone():
#            return jsonify({"error": "Project group not found"}), 404
      
#        # Only teamName can be updated
#        if "teamName" not in data:
#            return jsonify({"error": "No valid fields to update"}), 400
      
#        query = """
#            UPDATE ProjectGroup
#            SET teamName = %s
#            WHERE teamID = %s AND CRN = %s
#        """
      
#        cursor.execute(query, (data["teamName"], team_id, crn))
#        db.get_db().commit()
#        cursor.close()
      
#        return jsonify({"message": "Project group updated successfully"}), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500




# # DELETE - Delete a project group [Student-6]
# @students.route("/project_group/<int:team_id>", methods=["DELETE"])
# def delete_project_group(team_id):
#    """Delete a project group"""
#    try:
#        crn = request.args.get("crn")
      
#        if not crn:
#            return jsonify({"error": "Missing required parameter: crn"}), 400
      
#        cursor = db.get_db().cursor()
      
#        # Check if project group exists
#        cursor.execute("""
#            SELECT * FROM ProjectGroup
#            WHERE teamID = %s AND CRN = %s
#        """, (team_id, crn))
      
#        if not cursor.fetchone():
#            return jsonify({"error": "Project group not found"}), 404
      
#        cursor.execute("""
#            DELETE FROM ProjectGroup
#            WHERE teamID = %s AND CRN = %s
#        """, (team_id, crn))
      
#        db.get_db().commit()
#        cursor.close()
      
#        return jsonify({"message": "Project group deleted successfully"}), 200
#    except Error as e:
#        return jsonify({"error": str(e)}), 500



# Remote library imports
from flask import Flask, request, make_response, session, jsonify
from flask_restful import Resource, Api
from datetime import datetime

# Local imports
from config import app, db, api

# Import Models 
from models import User, Project, Task, Comment

@app.route("/")
def index():
    return "<h1>ProjectHub</h1>"


                            ################################# User Authentication #################################


class Signup(Resource): 
    def post(self):
        try:
            data = request.get_json()
            user = User(
                username=data.get("username"),
                email=data.get("email"), 
            )
            user.password_hash = data.get("password")
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            return make_response(user.to_dict(), 201)
        except ValueError as e:
            return make_response({"error": f"{e}"}, 400)
        

class SignIn(Resource):
    def post(self):
        username = request.get_json()["username"]
        password = request.get_json()["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.authenticate(password):
            session["user_id"] = user.id
            return user.to_dict(), 200
        session.clear()
        return {"error": "Incorrect username or password"}, 401


class SignOut(Resource):
    def delete(self):
        session.clear()
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user = User.query.get(session.get("user_id"))
        if user:
            return user.to_dict(), 200
        else:
            return {}, 401
        
        
                             ################################# User #################################
                             
     
class UserResource(Resource):
    def get(self):
        try:
            return make_response([user.to_dict() for user in User.query.all()], 200)
        except Exception as e:
            return make_response({"Error": "Could not get data"}, 400)
        

class UsersById(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user:
            return make_response(user.to_dict(), 200)
        return make_response({"error": "User not found"}, 404)
    
    
                              ################################# Project #################################
                              
    
class Projects(Resource):
    def get(self):
        projects = [project.to_dict() for project in Project.query.all()]
        if not projects:
            return make_response({"error": "No projects found."}, 404)
        return make_response(jsonify(projects), 200)
    
    
    def post(self):
        try:
            data = request.get_json()

            start_date = data.get("startDate")
            end_date = data.get("endDate")

            if start_date is None or end_date is None:
                return make_response({"error": "Missing start_date or end_date."}, 400)

            # Checked if the user exists by using the user ID from the session
            user = User.query.get(session.get("user_id"))
            if user is None:
                return make_response({"error": "User not found."}, 404)

            new_project = Project(
                user_id=data.get("user_id"),
                title=data.get("title"),               
                description=data.get("description"),
                status=data.get("status"),
                start_date=datetime.strptime(start_date, "%Y-%m-%d"),
                end_date=datetime.strptime(end_date, "%Y-%m-%d"),
            )
            db.session.add(new_project)
            db.session.commit()
            return make_response(new_project.to_dict(), 201)
        except ValueError as e:
            return make_response({"error": e.__str__()}, 400)
        except KeyError:
            return make_response({"error": "Missing required data."}, 400)
        
        
class ProjectId(Resource):
    def get(self, id):
        project = Project.query.get(id)
        if project:
            return make_response(project.to_dict(), 200)
        return make_response({"error": "Project not found."}, 404)
    
    
    def patch(self, id):
        project = Project.query.get(id)
        if not project:
            return make_response({"error": "Project not found."}, 404)
        else:
            data = request.get_json()
            try:    
                for attr, value in data.items():
                    if hasattr(project, attr):
                        setattr(project, attr, value)

                db.session.add(project)
                db.session.commit()

                return make_response(project.to_dict(), 202)
            except ValueError as e:
                return make_response({"error": e.__str__()}, 400)
            
            
    def delete(self, id):
        project = Project.query.get(id)
        if not project:
            return make_response({"error": "Project not found."}, 404)
        else:
            db.session.delete(project)
            db.session.commit()
            return make_response({"message": "Project deleted successfully."}, 204)
        
        
                                    ################################# Task #################################
        
        
class Tasks(Resource):
    def get(self):
        tasks = [task.to_dict() for task in Task.query.all()]
        if not tasks:
            return make_response({"error": "No tasks found."}, 404)
        return make_response(jsonify(tasks), 200)
 
     
    def post(self):
        try:
            data = request.get_json()
            
            due_date = data.get("dueDate")

            if due_date is None:
                return make_response({"error": "Missing due date."}, 400)
            
            # Checked if the user exists by using the user ID from the session
            user = User.query.get(session.get("user_id"))
            if user is None:
                return make_response({"error": "User not found."}, 404)

            new_task = Task(
                user_id=data.get("user_id"),
                description=data.get("description"),
                due_date=datetime.strptime( due_date, "%Y-%m-%d"),
                priority=data.get("priority"),
                status=data.get("status"),
            )
            db.session.add(new_task)
            db.session.commit()
            return make_response(new_task.to_dict(), 201)
        except ValueError as e:
            return make_response({"error": e.__str__()}, 400)
        except KeyError:
            return make_response({"error": "Missing required data."}, 400)
        
        

class TaskId(Resource):
    def get(self, id):
        task = Task.query.get(id)
        if task:
            return make_response(task.to_dict(), 200)
        return make_response({"error": "Task not found."}, 404)
    
    
    def patch(self, id):
        task = Task.query.get(id)
        if not task:
            return make_response({"error": "Task not found."}, 404)
        else:
            data = request.get_json()
            data["due_date"] = datetime.strptime(data["due_date"], "%Y-%m-%d")
            try:
                for attr, value in data.items():
                    if hasattr(task, attr):
                        setattr(task, attr, value)

                db.session.add(task)
                db.session.commit()

                return make_response(task.to_dict(), 202)
            except ValueError as e:
                return make_response({"error": e.__str__()}, 400)
            
            
    def delete(self, id):
        task = Task.query.get(id)
        if not task:
            return make_response({"error": "Task not found."}, 404)
        else:
            db.session.delete(task)
            db.session.commit()
            return make_response({"message": "Task deleted successfully."}, 204)
        
        
                                ################################# Comment #################################


class Comments(Resource):
    def get(self):
        comments = [comment.to_dict() for comment in Comment.query.all()]
        if not comments:
            return make_response({"error": "No comments found."}, 404)
        return make_response(jsonify(comments), 200)
    
 
    def post(self):
        try:
            data = request.get_json()
            user = User.query.get(session.get("user_id"))
            
            # Checked if the user exists by using the user ID from the session
            if user is None:
                return make_response({"error": "User not found."}, 404)
            
            new_comment = Comment(
                user_id=data.get("user_id"),
                task_id=data.get("task_id"),
                text=data.get("text"),
            )
            db.session.add(new_comment)
            db.session.commit()
            return make_response(new_comment.to_dict(), 201)
        except ValueError as e:
            return make_response({"error": e.__str__()}, 400)
        except KeyError:
            return make_response({"error": "Missing required data."}, 400)
        

class CommentId(Resource):
    def get(self, id):
        comment = Comment.query.get(id)
        if comment:
            return make_response(comment.to_dict(), 200)
        return make_response({"error": "Comment not found."}, 404)
    
        
    def patch(self, id):
        comment = Comment.query.get(id)
        if not comment:
            return make_response({"error": "Comment not found"}, 404)
        data = request.get_json()
        try:
            for attr, value in data.items():
                if hasattr(comment, attr):
                    setattr(comment, attr, value)
                
            db.session.add(comment)
            db.session.commit()
            return make_response(comment.to_dict(), 202)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
            
            
    def delete(self, id):
        comment = Comment.query.get(id)
        if not comment:
            return make_response({"error": "Comment not found."}, 404)
        else:
            db.session.delete(comment)
            db.session.commit()
            return make_response({"message": "Comment deleted successfully."}, 204)  
        
        
                                        ################################# User_Project #################################


class UserProjects(Resource):
    def get(self):
        user = User.query.first() 
        return [project.title for project in user.projects]  # print the titles of all projects associated with this user

class ProjectUsers(Resource):
    def get(self):
        project = Project.query.first()  
        return [user.username for user in project.users]  # print the usernames of all users associated with this project

        

        
        
api.add_resource(Signup, "/sign_up")
api.add_resource(SignIn, "/signIn")
api.add_resource(SignOut, "/signOut")
api.add_resource(CheckSession, "/check_session")
api.add_resource(UserResource, "/user")
api.add_resource(UsersById, "/user/<int:id>")
api.add_resource(Projects, "/projects")
api.add_resource(ProjectId, "/projects/<int:id>")
api.add_resource(Tasks, "/tasks")
api.add_resource(TaskId, "/tasks/<int:id>")
api.add_resource(Comments, "/comments")
api.add_resource(CommentId, "/comments/<int:id>")
api.add_resource(UserProjects, "/user_projects")
api.add_resource(ProjectUsers, "/project_users")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
    
    

   
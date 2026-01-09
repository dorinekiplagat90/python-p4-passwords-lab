from flask import request, session
from flask_restful import Resource
from config import app, api
from models import db, User


class Signup(Resource):
    def post(self):
        data = request.get_json()

        user = User(
            username=data["username"]
        )
        user.password_hash = data["password"]

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        return user.to_dict(), 201


class Login(Resource):
    def post(self):
        data = request.get_json()

        user = User.query.filter_by(username=data["username"]).first()

        if user and user.authenticate(data["password"]):
            session["user_id"] = user.id
            return user.to_dict(), 200

        return {"error": "Invalid username or password"}, 401


class Logout(Resource):
    def delete(self):
        session.pop("user_id", None)
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")

        if user_id:
            user = User.query.get(user_id)
            return user.to_dict(), 200

        return {}, 204


api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")


if __name__ == "__main__":
    app.run(port=5555, debug=True)

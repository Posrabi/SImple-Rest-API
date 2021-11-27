from flask import Flask
from flask_restful import Api, Resource, marshal_with, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)  # wrap the app with an API
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name ={self.name}, views ={self.views}, likes = {self.likes})"


video_put_args = reqparse.RequestParser()

video_put_args.add_argument(
    "name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument(
    "views", type=str, help="Views of the video", required=True)
video_put_args.add_argument(
    "likes", type=str, help="Likes of the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument(
    "name", type=str, help="Name of the video is required")
video_update_args.add_argument(
    "views", type=str, help="Views of the video")  # update base on what the user wants
video_update_args.add_argument(
    "likes", type=str, help="Likes of the video")

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)  # serialize the return using the fields
    def get(self, video_id):
        # look for a row, col in videomodel that has id
        # gives an instance of the video model
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Not available")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video taken")
        video = VideoModel(
            id=video_id, name=args["name"], views=args["views"], likes=args["likes"])
        db.session.add(video)
        db.session.commit()
        return video, 201

    def delete(self, video_id):

        return "", 204

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Not found")

        if args['name']:
            result.name = args['name']
        if args["views"]:
            result.views = args['views']
        if args["likes"]:
            result.likes = args['likes']

        db.session.commit()
        return result


api.add_resource(Video, "/video/<int:video_id>")


if __name__ == '__main__':
    app.run(debug=True)  # only use in development environment

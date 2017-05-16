from google.appengine.api import users
import cgi

from handlers.base import BaseHandler
from utils.decorators import validate_csrf
from models.comment import Comment
from models.topic import Topic


class CommentAddHandler(BaseHandler):
    @validate_csrf
    def post(self, topic_id):
        user = users.get_current_user()
        if not user:
            return self.write("You're not logged in.")
        comment = cgi.escape(self.request.get("comment"))
        topic = Topic.get_by_id(int(topic_id))
        new_comment = Comment(content=comment, author_email=user.email(), topic_id=topic.key.id())
        new_comment.put()

        return self.redirect_to("topic-details", topic_id=topic.key.id())

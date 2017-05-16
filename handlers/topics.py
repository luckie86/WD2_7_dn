import cgi
from google.appengine.api import users

from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment
from utils.decorators import validate_csrf


class TopicAddHandler(BaseHandler):
    def get(self):
        return self.render_template_with_csrf("topic_add.html")

    @validate_csrf
    def post(self):
        user = users.get_current_user()
        if not user:
            return self.write("You're not logged in.")
        title = cgi.escape(self.request.get("title"))
        text = cgi.escape(self.request.get("text"))
        new_topic = Topic(title=title, content=text, author_email=user.email())
        new_topic.put()
        return self.redirect_to("topic-details", topic_id = new_topic.key.id())


class TopicDetailsHandler(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.query(Comment.topic_id == topic.key.id(), Comment.deleted == False).fetch()
        params = {"topic": topic, "comments": comments}
        return self.render_template_with_csrf("topic_details.html", params=params)
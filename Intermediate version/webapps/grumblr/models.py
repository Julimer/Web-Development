from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Max

class Post(models.Model):
    text = models.CharField(max_length=42)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return self.text

    @staticmethod
    def get_max_time():
        if Post.objects.all():
            return Post.objects.all().aggregate(Max('time'))['time__max'].isoformat() or "1970-01-01T00:00+00:00"
        else:
            return "1970-01-01T00:00+00:00"

    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00"):
        return Post.objects.filter(time__gt=time).distinct()

    @property
    def html(self):
        html1 = "<div id='post-{0}' class='well post-container'>" \
               "<a href='{{% url 'profile' {1} %}}' class='post-photo'>" \
               "<img src='{2}' class='img-circle' alt='personal icon' width='50' height='50'>" \
               "</a>" \
               "<div class='post-name'><label>{3}</label></div>" \
               "<div class='post-time'><p>{4}</p></div>" \
               "<div class='post-content'><p>{5}</p></div>".format(self.id, self.user.id, self.user.profile.picture.url, self.user.username, self.time, self.text)
        html2 = " <div class='comments-container'>" \
                "<input type='hidden' id='comment-of' value='{0}'>" \
                "<br>" \
                "<div class='col-sm-9'><input type='text' id='comment-input-{1}' name='content' maxlength='200' placeholder='Add a comment...' class='form-control' required/>" \
                "</div><input type='submit' id='comment-btn-{2}' class='btn btn-primary btn-comment' value='Comment'>" \
                "<ol id='comments-list-{3}' class='comments-list'></ol><br></div></div>".format(self.id, self.id, self.id, self.id)
        return html1+html2

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comment_by')
    post = models.ForeignKey(Post, related_name='comment_of')
    content = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return self.content

    @property
    def html(self):
        return "<li id='comment-{0}' class='comment'><div class='row'>" \
               "<div id='comment-userprofile' class='col-sm-1'>" \
               "<a href='{{% url 'profile' {1} %}}' class='comment-photo'>" \
               "<img src='{2}' class='img-rounded' alt='personal icon' width='30' height='30'>" \
               "</a></div><div class='col-sm-10 comment-text'>" \
               "<span><label id='comment-username'>{3}</label></span>" \
               "<span><label id='comment-time'>{4}</label></span>" \
               "<p id='comment-content'>{5}</p></div>" \
               "</div></li>".format(self.id, self.user.id, self.user.profile.picture.url, self.user.username, self.time, self.content)

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    age = models.IntegerField(default=0,blank=True)
    bio = models.CharField(max_length=420, default='0',blank=True)
    picture = models.ImageField(upload_to="user-photos/",default='no-img.jpg',blank=True)
    follows = models.ManyToManyField('Profile', related_name='followed_by', symmetrical=False)

    def __unicode__(self):
        return self.owner_id

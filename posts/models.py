from django.db import models

from general.models import BaseModel
from accounts.models import User


class Post(BaseModel):
    caption = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        db_table = 'posts_post'
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.user)
    

class PostMedia(BaseModel):
    media = models.FileField(upload_to="posts/posts/")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')

    class Meta:
        db_table = 'posts_post_media'
        verbose_name = 'post_media'
        verbose_name_plural = 'post_media'
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.post)
    

REACTION_CHOICES = (
    ('like','Like'),
    ('funny','Funny'),
    ('disgusting','Disgusting'),
    ('amazing','Amazing'),
    ('interesting','interesting'),
)


class PostReaction(BaseModel):
    reaction = models.CharField(max_length=128,choices=REACTION_CHOICES,default='like')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='reactions')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post_reactions')

    class Meta:
        db_table = 'posts_post_reaction'
        verbose_name = 'post_reaction'
        verbose_name_plural = 'post_reactions'
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.post)
    

class Comment(BaseModel):
    comment_text = models.TextField()
    comment = models.ForeignKey("posts.Comment",on_delete=models.CASCADE, related_name="reply",null=True, blank=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="post_comments")

    class Meta:
        db_table = 'posts_comment'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.user)
    

class CommentReaction(BaseModel):
    reaction = models.CharField(max_length=128,choices=REACTION_CHOICES,default='like')
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comment_reactions')

    class Meta:
        db_table = 'posts_comment_reaction'
        verbose_name = 'comment_reaction'
        verbose_name_plural = 'comment_reactions'
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.user)
    

class PostReach(BaseModel):
    visitor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='visited_posts')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='visits')

    class Meta:
        db_table = 'posts_post_reach'
        verbose_name = 'post_reach'
        verbose_name_plural = 'post_reaches'
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.visitor)
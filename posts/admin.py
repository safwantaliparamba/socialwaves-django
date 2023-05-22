from django.contrib import admin

from posts.models import Post, PostMedia, PostReaction, Comment, CommentReaction, PostReach


class PostMediaAdmin(admin.TabularInline):
    model = PostMedia

class PostReactionAdmin(admin.TabularInline):
    model = PostReaction

class PostReachAdmin(admin.TabularInline):
    model = PostReach


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'caption']
    list_filter = ['date_added', 'date_updated']
    list_display_links = ['id']
    inlines = [PostMediaAdmin,PostReactionAdmin,PostReachAdmin]

class CommentReactionAdmin(admin.TabularInline):
    model = CommentReaction


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post','user','comment_text','comment']
    list_filter = ['date_added','date_updated']
    inlines = [CommentReactionAdmin]
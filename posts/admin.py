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
    actions = ['temp_delete']

    def temp_delete(self, request, queryset):
        # Implement your custom action logic here
        queryset.update(is_deleted=True)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects processed.')

    temp_delete.short_description = 'Delete temporarily'

class CommentReactionAdmin(admin.TabularInline):
    model = CommentReaction


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post','user','comment_text','comment']
    list_filter = ['date_added','date_updated']
    inlines = [CommentReactionAdmin]
    actions = ['temp_delete']

    def temp_delete(self, request, queryset):
        # Implement your custom action logic here
        queryset.update(is_deleted=True)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects processed.')

    temp_delete.short_description = 'Delete temporarily'
from django.contrib import admin

from posts.models import Post, PostMedia, PostReaction, Comment, CommentReaction, PostReach


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ["id"]

@admin.register(PostReaction)
class PostReactionAdmin(admin.ModelAdmin):
    list_display = ["id"]

@admin.register(PostReach)
class PostReachAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'caption']
    list_filter = ['date_added', 'date_updated']
    list_display_links = ['id']
    # inlines = [PostMediaAdmin,PostReactionAdmin,PostReachAdmin]
    actions = ['temp_delete','undo_delete']

    def temp_delete(self, request, queryset):
        # Implement your custom action logic here
        queryset.update(is_deleted=True)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects processed.')

    def undo_delete(self, request, queryset):
        queryset.update(is_deleted=False)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects undo deleted.')

    temp_delete.short_description = 'Delete temporarily'
    undo_delete.short_description = 'Undo delete'

class CommentReactionAdmin(admin.TabularInline):
    model = CommentReaction


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post','user','comment_text','comment']
    list_filter = ['date_added','date_updated']
    inlines = [CommentReactionAdmin]
    actions = ['temp_delete','undo_delete']

    def temp_delete(self, request, queryset):
        # Implement your custom action logic here
        queryset.update(is_deleted=True)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects processed.')

    def undo_delete(self, request, queryset):
        queryset.update(is_deleted=False)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects undo deleted.')

    temp_delete.short_description = 'Delete temporarily'
    undo_delete.short_description = 'Undo delete'
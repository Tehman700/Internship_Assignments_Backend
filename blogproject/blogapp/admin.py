from django.contrib import admin
from blogapp.Models.BlogComment import BlogComment
from blogapp.Models.BlogCommentReaction import BlogCommentReaction
from blogapp.Models.BlogPost import BlogPost
from blogapp.Models.BlogReaction import BlogReaction


admin.site.register(BlogComment)
admin.site.register(BlogPost)
admin.site.register(BlogCommentReaction)
admin.site.register(BlogReaction)
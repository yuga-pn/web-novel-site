from django.contrib import admin
from django.utils.html import format_html
from web_novel.models import Novel, OriginalWork, Tag

# Register your models here.

# admin画面のタイトルをカスタマイズ
admin.site.site_header = "📖 ウェブ小説管理システム"
admin.site.site_title = "小説管理"
admin.site.index_title = "管理メニュー"

@admin.register(OriginalWork)
class OriginalWorkAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'novel_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'author']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('基本情報', {
            'fields': ('name', 'author')
        }),
        ('詳細', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('システム情報', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def novel_count(self, obj):
        count = obj.novel_set.count()
        return format_html(
            '<span style="color: #2196F3; font-weight: bold;">{} 作品</span>',
            count
        )
    novel_count.short_description = "登録作品数"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_preview', 'novel_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('基本情報', {
            'fields': ('name', 'color')
        }),
        ('詳細', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('システム情報', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px; display: inline-block;"></div>',
            obj.color
        )
    color_preview.short_description = "色"
    
    def novel_count(self, obj):
        count = obj.novel_set.count()
        return format_html(
            '<span style="color: #4CAF50; font-weight: bold;">{} 作品</span>',
            count
        )
    novel_count.short_description = "使用作品数"

@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_work_display', 'tag_list', 'get_word_display', 'created_at']
    list_filter = ['original_work', 'tags', 'created_at']
    search_fields = ['title', 'summary']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['tags']
    
    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'original_work', 'linked')
        }),
        ('内容', {
            'fields': ('summary', 'word_count')
        }),
        ('分類', {
            'fields': ('tags',),
            'description': 'この小説に適用するタグを選択してください。複数選択可能です。'
        }),
        ('システム情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_work_display(self, obj):
        if obj.original_work:
            return format_html(
                '<span style="color: #2196F3; font-weight: bold;">{}</span>',
                obj.original_work.name
            )
        return format_html(
            '<span style="color: #757575;">{}</span>',
            obj.work_name or "未設定"
        )
    get_work_display.short_description = "原作"
    
    def get_word_display(self, obj):
        if obj.word_count:
            return format_html(
                '<span style="color: #4CAF50; font-weight: bold;">{:,} 文字</span>',
                obj.word_count
            )
        return format_html(
            '<span style="color: #757575;">{}</span>',
            obj.word_num or "未設定"
        )
    get_word_display.short_description = "文字数"
    
    def tag_list(self, obj):
        tags = obj.tags.all()
        if tags:
            tag_html = []
            for tag in tags:
                tag_html.append(
                    format_html(
                        '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px; margin-right: 2px;">{}</span>',
                        tag.color,
                        tag.name
                    )
                )
            return format_html(''.join(tag_html))
        elif obj.tag:
            return format_html(
                '<span style="color: #757575; font-style: italic;">{}</span>',
                obj.tag
            )
        return "タグなし"
    tag_list.short_description = "タグ"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('original_work').prefetch_related('tags')
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

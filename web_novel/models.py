from django.db import models

# Create your models here.

class OriginalWork(models.Model):
    """原作作品のモデル"""
    name = models.CharField(max_length=100, unique=True, verbose_name="原作名")
    author = models.CharField(max_length=50, blank=True, verbose_name="原作者")
    description = models.TextField(blank=True, verbose_name="原作の説明")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    
    class Meta:
        verbose_name = "原作"
        verbose_name_plural = "原作一覧"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    """タグのモデル"""
    name = models.CharField(max_length=30, unique=True, verbose_name="タグ名")
    description = models.TextField(blank=True, verbose_name="タグの説明")
    color = models.CharField(max_length=7, default="#3498db", verbose_name="表示色")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    
    class Meta:
        verbose_name = "タグ"
        verbose_name_plural = "タグ一覧"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Novel(models.Model):
    """小説のモデル"""
    title = models.CharField(max_length=100, verbose_name="タイトル")
    
    # 既存フィールド（下位互換性のため保持）
    work_name = models.CharField(max_length=50, verbose_name="原作名（従来）")
    tag = models.TextField(verbose_name="タグ（従来）")
    summry = models.TextField(verbose_name="あらすじ（従来）")
    word_num = models.TextField(null=True, verbose_name="文字数（従来）")
    
    # 新しいフィールド（オプション）
    original_work = models.ForeignKey(
        OriginalWork, 
        on_delete=models.CASCADE, 
        verbose_name="原作",
        null=True, 
        blank=True,
        help_text="この小説の原作を選択してください"
    )
    tags = models.ManyToManyField(
        Tag, 
        blank=True, 
        verbose_name="タグ",
        help_text="この小説に適用するタグを選択してください"
    )
    linked = models.URLField(verbose_name="小説のURL")
    summary = models.TextField(blank=True, verbose_name="あらすじ（新）")
    word_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="文字数（新）", help_text="半角数字で入力")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時", null=True, blank=True)
    
    # 新しいフィールドと従来フィールドの統合プロパティ
    def get_work_name(self):
        """原作名を取得（新→従来の順で優先）"""
        if self.original_work:
            return self.original_work.name
        return self.work_name
    
    def get_tag_display(self):
        """タグ表示用（新→従来の順で優先）"""
        new_tags = self.tags.all()
        if new_tags:
            return ", ".join([tag.name for tag in new_tags])
        return self.tag
    
    def get_summary(self):
        """あらすじを取得（新→従来の順で優先）"""
        return self.summary if self.summary else self.summry
    
    def get_word_count(self):
        """文字数を取得（新→従来の順で優先）"""
        if self.word_count:
            return str(self.word_count)
        return self.word_num or "0"
    
    class Meta:
        verbose_name = "小説"
        verbose_name_plural = "小説一覧"
        ordering = ['-created_at']
    
    def __str__(self):
        work_name = self.original_work.name if self.original_work else self.work_name
        return f"{self.title} ({work_name})"
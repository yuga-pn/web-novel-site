from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db import models
from web_novel.models import Novel
# Create your views here.

class NovelList(ListView):
    model=Novel
    context_object_name="novels"
    template_name="web_novel/novel_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get("query", "")
        return context
    
    def get_queryset(self):
        query = self.request.GET.get("query")
        if query and query.strip():
            query = query.strip()
            # 従来フィールドでの検索（既存データとの互換性）
            q_objects = models.Q()
            
            # タイトル検索
            q_objects |= models.Q(title__icontains=query)
            
            # 従来の原作名検索
            q_objects |= models.Q(work_name__icontains=query)
            
            # 従来のタグ検索
            q_objects |= models.Q(tag__icontains=query)
            
            # 新しい原作検索（Noneチェック）
            q_objects |= models.Q(original_work__name__icontains=query)
            
            # 新しいタグ検索
            q_objects |= models.Q(tags__name__icontains=query)
            
            # あらすじ検索も追加
            q_objects |= models.Q(summry__icontains=query)
            q_objects |= models.Q(summary__icontains=query)
            
            nov_list = Novel.objects.filter(q_objects).distinct().select_related('original_work').prefetch_related('tags')
        else:
            nov_list = Novel.objects.all().select_related('original_work').prefetch_related('tags')
        return nov_list
    
    def relative_list(self,keywords):
        nov_list=Novel.objects.filter(work_name__icontains=keywords) | Novel.objects.filter(tag__icontains=keywords)| Novel.objects.filter(title__icontains=keywords)
        return nov_list
    
class NovelDetail(DetailView):
    model=Novel
    context_object_name="novel"
    template_name="web_novel/novel_detail.html"
    
    def get_related_novels(self, current_novel):
        related_novels = []
        
        # 1. 同じ原作の他の小説（最高優先度）
        # 新しいフィールドと従来フィールドの両方を考慮
        if current_novel.original_work:
            same_work = Novel.objects.filter(
                original_work=current_novel.original_work
            ).exclude(pk=current_novel.pk)[:3]
        else:
            same_work = Novel.objects.filter(
                work_name__iexact=current_novel.work_name
            ).exclude(pk=current_novel.pk)[:3]
        related_novels.extend(same_work)
        
        # 2. 共通タグを持つ小説（中優先度）
        if len(related_novels) < 5:
            current_tags = current_novel.tags.all()
            if current_tags:
                tag_related = Novel.objects.filter(
                    tags__in=current_tags
                ).exclude(pk=current_novel.pk).exclude(
                    pk__in=[novel.pk for novel in related_novels]
                ).distinct()[:3]
            elif current_novel.tag:
                # 従来のタグフィールドでの検索
                tag_related = Novel.objects.filter(
                    tag__icontains=current_novel.tag.split(',')[0] if current_novel.tag else ''
                ).exclude(pk=current_novel.pk).exclude(
                    pk__in=[novel.pk for novel in related_novels]
                )[:3]
            else:
                tag_related = []
            related_novels.extend(tag_related)
        
        # 3. タイトルキーワード関連（低優先度）
        if len(related_novels) < 5:
            title_words = current_novel.title.split()[:2]  # 最初の2語を使用
            for word in title_words:
                if len(word) > 1:  # 1文字は除外
                    title_related = Novel.objects.filter(
                        title__icontains=word
                    ).exclude(pk=current_novel.pk).exclude(
                        pk__in=[novel.pk for novel in related_novels]
                    )[:2]
                    related_novels.extend(title_related)
                    if len(related_novels) >= 5:
                        break
        
        return related_novels[:5]  # 最大5件
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_novels'] = self.get_related_novels(self.object)
        return context
    
    
    
class TitleList(ListView):
    model=Novel
    context_object_name="titles"
    template_name="web_novel/title_list.html"
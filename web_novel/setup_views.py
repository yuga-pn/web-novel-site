from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def create_admin_user(request):
    """一時的なadminユーザー作成エンドポイント（使用後は削除推奨）"""
    if request.method == 'POST':
        try:
            # 既存のsuperuserをチェック
            if User.objects.filter(is_superuser=True).exists():
                return HttpResponse('Admin user already exists', status=400)
            
            # adminユーザーを作成
            User.objects.create_superuser(
                username='admin',
                email='admin@webnovel.com',
                password='WebNovel2024!'
            )
            
            return HttpResponse('Admin user created successfully!')
            
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}', status=500)
    
    return HttpResponse('Send POST request to create admin user')

def setup_initial_data(request):
    """初期データをセットアップ"""
    from web_novel.models import OriginalWork, Tag
    
    try:
        # 原作を作成
        works = [
            {'name': 'ようこそ実力主義の教室へ', 'author': '衣笠彰梧'},
            {'name': 'ソードアート・オンライン', 'author': '川原礫'},
            {'name': '推しの子', 'author': 'aka'},
        ]
        
        for work_data in works:
            OriginalWork.objects.get_or_create(**work_data)
        
        # タグを作成
        tags = [
            {'name': '学園', 'color': '#2196F3'},
            {'name': '恋愛', 'color': '#E91E63'},
            {'name': 'ファンタジー', 'color': '#9C27B0'},
            {'name': 'SF', 'color': '#00BCD4'},
            {'name': 'アクション', 'color': '#FF5722'},
        ]
        
        for tag_data in tags:
            Tag.objects.get_or_create(**tag_data)
        
        return HttpResponse('Initial data created successfully!')
        
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)
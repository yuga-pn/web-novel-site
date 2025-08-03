from web_novel.models import OriginalWork

def original_works(request):
    """
    全ページで利用可能な原作一覧を提供するコンテキストプロセッサ
    """
    works = OriginalWork.objects.all().order_by('name')
    return {
        'original_works': works
    }
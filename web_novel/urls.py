from django.urls import path
from web_novel.views import NovelList,NovelDetail,TitleList
from web_novel.setup_views import create_admin_user, setup_initial_data

urlpatterns = [
    path("",NovelList.as_view(),name="novel_list"),
    path("novel/<int:pk>/",NovelDetail.as_view(),name="novel_detail"),
    # 初期セットアップ用（本番では削除推奨）
    path("setup/admin/", create_admin_user, name="create_admin"),
    path("setup/data/", setup_initial_data, name="setup_data"),
]

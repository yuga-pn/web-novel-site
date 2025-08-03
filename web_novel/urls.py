from django.urls import path
from web_novel.views import NovelList,NovelDetail,TitleList

urlpatterns = [
    path("",NovelList.as_view(),name="novel_list"),
    path("novel/<int:pk>/",NovelDetail.as_view(),name="novel_detail")
]

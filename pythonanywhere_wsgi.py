"""
PythonAnywhere用のWSGI設定ファイル

このファイルはPythonAnywhereのWeb appタブで使用します。
/var/www/yourusername_pythonanywhere_com_wsgi.py として配置してください。
"""

import os
import sys

# プロジェクトのパスを追加
path = '/home/yourusername/web_novel/config'  # あなたのユーザー名に変更してください
if path not in sys.path:
    sys.path.insert(0, path)

# Django設定モジュールを指定
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Djangoアプリケーションをロード
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
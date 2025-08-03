# PythonAnywhereデプロイガイド

このガイドでは、DjangoアプリケーションをPythonAnywhereにデプロイする手順を説明します。

## 前提条件

- PythonAnywhereアカウントが作成済み
- Gitリポジトリが準備済み（推奨）

## デプロイ手順

### 1. PythonAnywhereでのファイルアップロード

#### 方法A: Gitを使用（推奨）
```bash
# PythonAnywhereのBashコンソールで実行
cd ~
git clone [あなたのリポジトリURL]
cd web_novel/config
```

#### 方法B: ファイル直接アップロード
- Files タブからファイルをアップロード
- `/home/yourusername/web_novel/` ディレクトリに配置

### 2. 仮想環境の作成と依存関係のインストール

```bash
# PythonAnywhereのBashコンソールで実行
cd ~/web_novel/config
python3.10 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 3. データベースの設定

```bash
# マイグレーションの実行
python manage.py makemigrations
python manage.py migrate

# 管理者ユーザーの作成
python manage.py createsuperuser

# 静的ファイルの収集
python manage.py collectstatic --noinput
```

### 4. Webアプリケーションの設定

1. **Web** タブに移動
2. **Add a new web app** をクリック
3. **Manual configuration** を選択
4. **Python 3.10** を選択

#### 4.1 Code セクションの設定
- **Source code**: `/home/yourusername/web_novel/config`
- **Working directory**: `/home/yourusername/web_novel/config`

#### 4.2 WSGI設定ファイルの編集
1. **WSGI configuration file** のリンクをクリック
2. ファイルの内容を以下に置き換え：

```python
import os
import sys

# プロジェクトのパスを追加（yourusernameを実際のユーザー名に変更）
path = '/home/yourusername/web_novel/config'
if path not in sys.path:
    sys.path.insert(0, path)

# Django設定モジュールを指定
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# 仮想環境の設定
os.environ['VIRTUAL_ENV'] = '/home/yourusername/web_novel/config/env'

# Djangoアプリケーションをロード
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### 4.3 仮想環境の設定
- **Virtualenv**: `/home/yourusername/web_novel/config/env`

#### 4.4 静的ファイルの設定
**Static files** セクションで以下を設定：
- **URL**: `/static/`
- **Directory**: `/home/yourusername/web_novel/config/staticfiles`

### 5. 環境変数の設定（オプション）

**Files** タブで `.env` ファイルを作成し、以下を設定：

```
DEBUG=False
SECRET_KEY=あなたの秘密鍵
DATABASE_URL=sqlite:////home/yourusername/web_novel/config/db.sqlite3
```

### 6. アプリケーションの起動

1. **Web** タブで **Reload** ボタンをクリック
2. アプリケーションのURLにアクセスして動作確認

## トラブルシューティング

### よくある問題と解決策

1. **ImportError が発生する場合**
   - パスの設定を確認
   - 仮想環境が正しく設定されているか確認

2. **静的ファイルが表示されない場合**
   - `python manage.py collectstatic` を再実行
   - 静的ファイルのパス設定を確認

3. **データベースエラーが発生する場合**
   - マイグレーションが実行されているか確認
   - データベースファイルの権限を確認

### ログの確認方法

- **Web** タブの **Log files** セクションでエラーログを確認
- **error.log** と **server.log** をチェック

## 更新時の手順

```bash
# コードの更新
cd ~/web_novel/config
git pull  # Gitを使用している場合

# 依存関係の更新（必要に応じて）
source env/bin/activate
pip install -r requirements.txt

# データベースの更新（必要に応じて）
python manage.py migrate

# 静的ファイルの更新
python manage.py collectstatic --noinput
```

**Web** タブで **Reload** をクリックして変更を反映させてください。

## 注意事項

- `yourusername` は実際のPythonAnywhereユーザー名に置き換えてください
- 本番環境では `DEBUG=False` に設定することを推奨します
- データベースのバックアップを定期的に取ることを推奨します
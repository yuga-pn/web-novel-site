#!/usr/bin/env python
"""
デプロイ時にadminユーザーを確実に作成するスクリプト
"""
import os
import django

# Django設定の初期化
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    """Adminユーザーを作成"""
    username = 'admin'
    email = 'admin@webnovel.com'
    password = 'admin123'  # シンプルなパスワード
    
    try:
        # 既存のsuperuserをチェック
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Superuser already exists")
            existing_user = User.objects.filter(is_superuser=True).first()
            print(f"   Username: {existing_user.username}")
            return existing_user.username
        
        # adminユーザーを作成
        admin_user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        print(f"✅ Admin user created successfully!")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print(f"   Email: {email}")
        
        return username
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return None

if __name__ == "__main__":
    create_admin_user()
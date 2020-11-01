from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tag(models.Model):
    tag = models.CharField('タグ名', max_length=50)

    def __str__(self):
        return self.tag


class Post(models.Model):
   title = models.CharField('タイトル', max_length=50)
   text = models.TextField('本文')
   image = models.ImageField('画像', upload_to = 'images', blank=True)
   created_at = models.DateTimeField('投稿日', default=timezone.now)
   tag = models.ForeignKey(Tag, verbose_name = 'タグ', on_delete=models.PROTECT)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   like = models.ManyToManyField(User, related_name='like', blank=True)
   def __str__(self):
       return self.title


# class Post(models.Model):
#    title = models.CharField('タイトル', max_length=35)
#    # このモデル関数は上記でimportしたモデル関数
#
#    text = models.TextField('本文')
#    image = models.ImageField('画像', upload_to = 'images', blank=True)
#
#    upload_to = 'images'
#    # upload_to で画像を投稿したら自動的にimagesディレクトリが作成されその中に画像が保存される
#
#    created_at = models.DateTimeField('投稿日', default=timezone.now)
#    tag = models.ForeignKey(Tag, verbose_name='タグ', on_delete=models.PROTECT)
#
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    # on_delete = models.CASCADEは、もしユーザーが削除された場合、そのユーザーの記事も一緒に削除する
#
#    def __str__(self):
#        return self.title

   # ForeignKey（外部キー）は他のモデル（Postなど）と紐付けるときに使用します。（紐付け方法は複数あります）
   # ForeignKeyの第一引数は、紐付けたいモデル名を記述し、第二引数に管理者画面で表示させたい名前（'タグ')
   # そして第三引数の設定（on_delete = models.PROTECT）は記事を削除したときに
   # 紐付いているタグも一緒に削除するかどうかの設定です。
   # 今回はPROTECTなのでタグは一緒に削除されません。


class Comment(models.Model):
   text = models.TextField('コメント')
   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   # user_image = models.ForeignKey(User, on_delete=models.CASCADE)
   created_at = models.DateTimeField('投稿日', default=timezone.now)
   def __str__(self):
       return self.text


# class Review(models.Model):
#
#
#     def __str__(self):
#         return self.review


# クラスベースビューって何だ??
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating = 0
        rating += self.post_set.aggregate(Sum('likes'))['likes__sum'] * 3
        rating += self.user.comment_set.aggregate(Sum('likes'))['likes__sum']
        for post in self.post_set.all():
            rating += post.comment_set.aggregate(Sum('likes'))['likes__sum']
        self.rating = rating
        self.save()

        # rating = 0
        # posts = Post.objects.filter(author=self.pk)
        # comments = Comment.objects.filter(user=self.pk).aggregate(Sum('likes'))['likes__sum']
        # for post in posts:
        #     rating += Comment.objects.filter(post=post.pk).aggregate(Sum('likes'))['likes__sum']
        # self.rating = rating + comments + posts.aggregate(Sum('likes'))['likes__sum'] * 3
        # self.save()

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ["user"]
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    category = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ["category"]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    new = 'New'
    article = 'Arc'
    KINDS = ((new, 'Новость'),
             (article, 'Статья'),
             )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_post = models.CharField(choices=KINDS, max_length=3, default='Arc')
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    header = models.CharField(max_length=128)
    content = models.TextField(default='Тут пока ничего нет')
    likes = models.IntegerField(default=0)

    def like(self):
        rating = 0
        rating += self.likes
        rating += 1
        self.likes = rating
        self.save()

    def dislike(self):
        rating = 0
        rating += self.likes
        rating -= 1
        self.likes = rating
        self.save()

    def preview(self):
        return f'{self.content[0:123]}...'

    def __str__(self):
        return f"Время публикации: {self.time_in.strftime('%d.%m.%Y %H:%M')}" \
               f", Заголовок: {self.header}" \
               f", Содержание: {self.content}"

    def get_absolute_url(self):
        #return reverse('post', args=[str(self.pk)])
        return reverse('posts_list')

    class Meta:
        ordering = ["-time_in"]
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def like(self):
        rating = 0
        rating += self.likes
        rating += 1
        self.likes = rating
        self.save()

    def dislike(self):
        rating = 0
        rating += self.likes
        rating -= 1
        self.likes = rating
        self.save()

    def __str__(self):
        return f"{self.post}-{self.content}"

    class Meta:
        ordering = ["-post"]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='sub_category')


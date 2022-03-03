from django.db import models
from django.urls import reverse 

# Create your models here.

class Video(models.Model):
    name = models.CharField(max_length=255, verbose_name="Video name")
    describtion = models.TextField(verbose_name="Describtion", blank=True)
    videofile = models.FileField(verbose_name="Video file")
    created_datetime = models.DateTimeField(auto_now_add=True)

    GAME_CATEGORY = "Game"
    FILM_CATEGORY = "Film"
    DOTA_CATEGORY = "Dota"
    category = models.CharField(
        max_length=10,
        verbose_name="Video category",
        choices=[
            (GAME_CATEGORY, "Games"),
            (FILM_CATEGORY, "Films"),
            (DOTA_CATEGORY, "Dota"),
        ],
    )
    NO_RESTRICTION = "NO"
    VIOLATION_RESTRICTION = "VIOLATION"
    SHADOW_BAN_RESTRICTION = "SHADOW"
    BAN_RESTRICTION = "BAN"
    restrctions = models.CharField(
        max_length=10,
        verbose_name="Restrictions",
        choices=[
            (NO_RESTRICTION, "No restriction"),
            (VIOLATION_RESTRICTION, "Violation"),
            (BAN_RESTRICTION, "Ban"),
            (SHADOW_BAN_RESTRICTION, "Shadow ban")
        ],
        default=NO_RESTRICTION
    )

    created_by = models.ForeignKey(
        "auth.user", verbose_name="Author", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.id}|{self.name} ({self.describtion[0:20]}...)"

    def get_absolute_url(self):
        return reverse('video', kwargs={'id': self.id})

    @property
    def likes(self):
        return self.like_set.filter(value__gt=0).count()

    @property
    def dislikes(self):
        return self.like_set.filter(value__lt=0).count()

    class Meta:
        verbose_name = "VIDEO"
        verbose_name_plural = "VIDEOS"


class Like(models.Model):
    video_id = models.ForeignKey(Video, verbose_name="Video",
                                 on_delete=models.SET_NULL,
                                 null=True)
    user_id = models.ForeignKey("auth.User",
                                on_delete=models.SET_NULL,
                                null=True)
    value = models.IntegerField(verbose_name="Like(1), Dislike(-1)", default=0)

    class Meta:
        verbose_name = "Like/Dislike"
        verbose_name_plural = "Likes/Dislikes"


class Comment(models.Model):
    text = models.TextField(verbose_name="Comment text")
    user = models.ManyToManyField("auth.User")
    video_id = models.ForeignKey(Video,
                                 on_delete=models.SET_NULL,
                                 null=True)
    created_datetime = models.DateTimeField(
        verbose_name="Created time", auto_now_add=True
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
from django.db import models

class Tag(models.Models):
    class Meta:
        db_table = "Tag"
    tag_name = models.CharField(max_length=30)
    score = models.PositiveIntegerField()
    attached_meme = models.ForeignKey(
        Meme, on_delete=models.CASCADE, related_name="tags"
    )


class Meme(models.Models):
    class Meta:
        db_table = "Meme"
    image = models.ImageField()


class Mi(models.Model):
    class Meta:
        db_table = "Mi"
    keyword = models.CharField(max_length=50)
    favorite_meme = models.ManyToMany(
        Meme, related_name="liked_by"
        )


class Evalutation(models.Models):
    class Meta:
        db_table = "Evaluation"
    evaluated_score = models.IntegerField()
    evaluated_meme = models.ForeignKey(
        Meme, on_delete=models.CASCADE, related_name="evaluations"
        )
    setter = models.ForeignKey(
        Mi, on_delete=models.CASCADE, related_name="evaluations"
        )
    set_tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name="evaluations"
        )


class TagList(models.Models):
    class Meta:
        db_table = "TagList"
    tag_names = models.CharField(max_length=30)

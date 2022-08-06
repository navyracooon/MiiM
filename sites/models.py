from django.db import models

# db_table: change name of table stored in a database
# on_delete: decide what will happen when parent object is deleted
# related_name: used when dereference is needed

class Meme(models.Models):
    class Meta:
        db_table = "Meme"
    image = models.ImageField()


class Tag(models.Models):
    class Meta:
        db_table = "Tag"
    tag_name = models.CharField(max_length=30)
    score = models.PositiveIntegerField()
    attached_meme = models.ForeignKey(
        Meme, on_delete=models.CASCADE, related_name="tags"
    )


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
    evaluation_diff = models.IntegerField()
    evaluated_time = models.DateTimeField(auto_now_add=True)
    evaluator = models.ForeignKey(
        Mi, on_delete=models.CASCADE, related_name="evaluations"
        )
    evaluated_meme = models.ForeignKey(
        Meme, on_delete=models.CASCADE, related_name="evaluations"
        )
    evaluated_tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name="evaluations"
        )


class TagList(models.Models):
    class Meta:
        db_table = "TagList"
    tag_names = models.CharField(max_length=30)

from django.db import models

# db_table: change name of table stored in a database
# on_delete: decide what will happen when parent object is deleted
# related_name: used when dereference is needed

class Meme(models.Model):
    class Meta:
        db_table = "Meme"
    image_url = models.URLField()
    uploaded_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Meme {}".format(self.id)


class Tag(models.Model):
    class Meta:
        db_table = "Tag"
    tag_name = models.CharField(max_length=30)
    score = models.IntegerField(default=0)
    attached_meme = models.ForeignKey(
        Meme, on_delete=models.CASCADE, related_name="tags"
    )

    def __str__(self):
        return "{}: {}".format(
            self.attached_meme, self.tag_name)


class Language(models.Model):
    class Meta:
        db_table = "Language"
    lang_name = models.CharField(max_length=30)
    possibility = models.IntegerField(default=0)
    attached_meme = models.ForeignKey(
        Meme, on_delete=models.CASCADE, related_name="languages"
    )

    def __str__(self):
        return "{}: {}".format(
            self.attached_meme, self.lang_name)


class Mi(models.Model):
    class Meta:
        db_table = "Mi"
    keyword = models.CharField(max_length=50)
    favorite_memes = models.ManyToManyField(
        Meme, related_name="liked_by", blank=True
        )

    def __str__(self):
        return self.keyword 


class Evaluation(models.Model):
    class Meta:
        db_table = "Evaluation"
    evaluation_diff = models.IntegerField()
    evaluated_time = models.DateTimeField(auto_now_add=True)
    evaluator = models.ForeignKey(
        Mi, on_delete=models.CASCADE, related_name="evaluations"
        )
    evaluated_tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name="evaluations"
        )

    def __str__(self):
        return "{}: ({}) -> {}".format(
            self.evaluator, self.evaluated_tag, self.evaluation_diff)


class TagList(models.Model):
    class Meta:
        db_table = "TagList"
    tag_names = models.CharField(max_length=30)

    def __str__(self):
        return self.tag_names 

import datetime

from django.test import TestCase

from sites.models import Meme, Tag, Language, Mi, Evaluation, TagList


class MemeModelTests(TestCase):
    sample_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
    utc = datetime.timezone.utc

    def test_is_empty(self):
        saved_memes = Meme.objects.all()
        self.assertEqual(saved_memes.count(), 0)
    
    def test_is_count_one(self):
        meme = Meme(image_url=self.sample_url)
        meme.save()
        saved_memes = Meme.objects.all()
        self.assertEqual(saved_memes.count(), 1)

    def test_saving_and_retrieving_meme_url(self):
        meme = Meme()
        image_url = self.sample_url
        uploaded_time = datetime.datetime.now(tz=self.utc)
        meme.image_url = image_url
        meme.uploaded_time = uploaded_time
        meme.save()
        saved_memes = Meme.objects.all()
        test_meme = saved_memes[0]
        self.assertEqual(test_meme.image_url, self.sample_url)
        self.assertAlmostEqual(
                test_meme.uploaded_time, 
                uploaded_time,
                delta=datetime.timedelta(seconds=1))

    def test_auto_now_add(self):
        meme = Meme(image_url=self.sample_url)
        meme.save()
        saved_memes = Meme.objects.all()
        test_meme = saved_memes[0]
        self.assertAlmostEqual(
                test_meme.uploaded_time,
                datetime.datetime.now(tz=self.utc),
                delta=datetime.timedelta(seconds=1))



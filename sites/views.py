from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from .models import (
        Meme, Tag, Language, Mi, Evaluation, TagList)


class IndexView(TemplateView):
    template_name = "sites/index.html"

    def get_recent_tag_names(self, evaluations_by_mi):
        # tag_nameの重複を確認する都合上、tag_nameのリストを渡している
        # ※ tagのリストを作ってしまうと重複をはじくことができない
        recent_tag_names = []
        for evaluation in evaluations_by_mi:
            if len(recent_tag_names) >= 6:
                break
            tag_name_to_add = evaluation.evaluated_tag.tag_name
            if tag_name_to_add not in recent_tag_names:
                recent_tag_names.append(tag_name_to_add)
        return recent_tag_names

    def get_recent_memes(self):
        recent_memes_ins = Meme.objects.all().order_by("-uploaded_time")[:10]
        # tagsはクエリオブジェクトなので注意
        recent_memes = [
                {"image": recent_meme_ins.image, 
                 "tags": recent_meme_ins.tags.all()} 
                for recent_meme_ins in recent_memes_ins]
        return recent_memes

    def get_trend_memes(self, evaluations):
        trend_memes_ins = []
        for evaluation in evaluations:
            if len(trend_memes_ins) >= 10:
                break
            meme_to_add = evaluation.evaluated_tag.attached_meme
            if meme_to_add not in trend_memes_ins:
                trend_memes_ins.append(meme_to_add)
        trend_memes = [
                {"image": trend_meme_ins.image,
                 "tags": trend_meme_ins.tags.all()}
                for trend_meme_ins in trend_memes_ins]
        return trend_memes

    def get_favorite_memes(self, mi):
        favorite_memes_ins = mi.favorite_memes.all()[:10]
        favorite_memes = [
                {"image": favorite_meme_ins.image,
                 "tags": favorite_meme_ins.tags.all()}
                for favorite_meme_ins in favorite_memes_ins]
        return favorite_memes

    def get_related_memes(self, mi):
        favorite_memes = self.get_favorite_memes(mi)
        related_memes_ins = []
        for memes in mi.favorite_memes.all():
            if len(related_memes_ins) >= 10:
                break
            for user in memes.liked_by.all():
                if len(related_memes_ins) >= 10:
                    break
                for meme in user.favorite_memes.all():
                    if len(related_memes_ins) >= 10:
                        break
                    if (meme not in related_memes_ins and
                            meme not in mi.favorite_memes.all()):
                        related_memes_ins.append(meme)
        related_memes = [
                {"image": related_meme_ins.image,
                 "tags": related_meme_ins.tags.all()}
                for related_meme_ins in related_memes_ins]
        return related_memes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # クエリパラメーターを引っ張ってくる
        keyword = self.request.GET.get("mi")

        # Miインスタンス作成
        if keyword:
            try:
                mi = Mi.objects.get(keyword=keyword)
            except ObjectDoesNotExist:
                mi = Mi.objects.create(keyword=keyword)
        else:
            # "ゲスト"はデフォルトのユーザー
            mi = Mi.objects.get(keyword="ゲスト")

        # Evaluationインスタンス作成
        # 全MiのEvaluationとログイン中のMiのEvaluationの両方を作成
        evaluations = Evaluation.objects.order_by("-evaluated_time")
        evaluations_by_mi = evaluations.filter(evaluator=mi)

        context = {
                "mi": mi,
                "recent_tag_names": self.get_recent_tag_names(evaluations_by_mi),
                "recent_memes": self.get_recent_memes(),
                "trend_memes": self.get_trend_memes(evaluations),
                "favorite_memes": self.get_favorite_memes(mi),
                "related_memes": self.get_related_memes(mi),
                }
        return context



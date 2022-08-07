from django.views.generic import (TemplateView)
from django.core.exceptions import ObjectDoesNotExist

from .models import (
    Meme, Tag, Language, Mi, Evaluation, TagList
    )

class IndexView(TemplateView):
    template_name = "sites/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get("mi")
        if keyword:
            # キーワードが既に使用されていればそれを、無ければMi作成
            try:
                mi = Mi.objects.get(keyword=keyword)
            except ObjectDoesNotExist:
                mi = Mi.objects.create(keyword=keyword)
        else:
            # 本当は言語によって切り替えたい
            mi = Mi.objects.get(keyword="ゲスト")

        evaluations = Evaluation.objects.order_by("-evaluated_time")
        evaluations_by_mi = evaluations.filter(evaluator=mi)
        # tag_nameの重複を確認する都合上、tag_nameのリストを渡している
        # ※ tagのリストを作ってしまうと重複をはじくことができない
        recent_tag_names = []
        for evaluation in evaluations_by_mi:
            if len(recent_tag_names) >= 6:
                break
            tag_name_to_add = evaluation.evaluated_tag.tag_name
            if tag_name_to_add not in recent_tag_names:
                recent_tag_names.append(tag_name_to_add)

        recent_memes_obj = Meme.objects.all().order_by("-uploaded_time")[:10]
        # 画像とタグをひとまとめにしてわたす
        recent_memes = []
        for recent_meme_obj in recent_memes_obj:
            recent_memes.append({
                # recent_memes.imageは画像
                # recent_memes.tagsはクエリオブジェクト
                "image": recent_meme_obj.image,
                "tags": recent_meme_obj.tags.all()
                })

        trend_memes_obj = []
        for evaluation in evaluations:
            if len(trend_memes_obj) >= 10:
                break
            meme_to_add = evaluation.evaluated_tag.attached_meme
            if meme_to_add not in trend_memes_obj:
                trend_memes_obj.append(meme_to_add)
        # 画像とタグをひとまとめにしてわたす
        trend_memes = []
        for trend_meme_obj in trend_memes_obj:
            trend_memes.append({
                "image": trend_meme_obj.image,
                "tags": trend_meme_obj.tags.all()
                })

        favorite_memes_obj = mi.favorite_memes.all()[:10]
        # 画像とタグをひとまとめにしてわたす
        favorite_memes = []
        for favorite_meme_obj in favorite_memes_obj:
            favorite_memes.append({
                "image": favorite_meme_obj.image,
                "tags": favorite_meme_obj.tags.all()
                })

        related_memes_obj = []
        for memes in mi.favorite_memes.all():
            if len(related_memes_obj) >= 10:
                break
            for user in memes.liked_by.all():
                if len(related_memes_obj) >= 10:
                    break
                for meme in user.favorite_memes.all():
                    if len(related_memes_obj) >= 10:
                        break
                    if (meme not in related_memes_obj and
                        meme not in mi.favorite_memes.all()):
                        related_memes_obj.append(meme)
        # 画像とタグをひとまとめにしてわたす
        related_memes = []
        for related_meme_obj in related_memes_obj:
            related_memes.append({
                "image": related_meme_obj.image,
                "tags": related_meme_obj.tags.all()
                })

        context = {
            "mi": mi,
            "recent_tag_names": recent_tag_names,
            "recent_memes": recent_memes,
            "trend_memes": trend_memes,
            "favorite_memes": favorite_memes,
            "related_memes": related_memes,
        }
        return context



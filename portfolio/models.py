from django.db import models
from user.models import User
from core.models import Comment, Images
from django.shortcuts import get_object_or_404


# for view_count
from django.utils import timezone
from core.models import Images

# for hashtag
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

# TODO 전체참여자를 participant로 넣고 중계 모델 만들기
# TODO class Participants portfolio 1개 participant 1명


class TaggedPortfolio(TaggedItemBase):
    content_object = models.ForeignKey(
        'Portfolio', on_delete=models.CASCADE)
    tags = models.ForeignKey(
        'core.Tag', related_name='tagged_portfolios', on_delete=models.CASCADE, null=True)


class Portfolio(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="portfolios", on_delete=models.CASCADE)
    thumbnail = models.ForeignKey(Images, related_name="portfolio_thumbnail",
                                  on_delete=models.CASCADE, blank=True, null=True, default=None)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    desc = models.TextField()

    # MTM fields
    like_users = models.ManyToManyField(
        User, related_name='likes', through='PortfolioLike')
    bookmark_users = models.ManyToManyField(
        User, related_name='bookmarks', through='PortfolioBookmark')
    tags = TaggableManager(
        verbose_name='tags', help_text='해시태그를 입력해주세요', blank=True, through='TaggedPortfolio')
    participants = models.ManyToManyField(User, through='Participants')
    comments = models.ManyToManyField(Comment, through='PortfolioComment')
    images = models.ManyToManyField(Images, through='PortfolioImages')

    def classname(self):
        return self.__class__.__name__


class PortfolioLike(models.Model):
    user = models.ForeignKey(
        User, related_name='portfolio_like_users', on_delete=models.CASCADE)
    portfolio = models.ForeignKey(
        Portfolio, related_name='like_portfolios', on_delete=models.CASCADE)


class PortfolioBookmark(models.Model):
    user = models.ForeignKey(
        User, related_name='portfolio_bookmark_users', on_delete=models.CASCADE)
    Portfolio = models.ForeignKey(
        Portfolio, related_name='bookmark_portfolios', on_delete=models.CASCADE)


class Participants(models.Model):
    portfolio = models.ForeignKey(
        to=Portfolio, related_name='portfolio_participants', on_delete=models.CASCADE)
    participant = models.ForeignKey(
        to=User, related_name='participants', on_delete=models.CASCADE)


class PortfolioComment(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='portfolio_comments', blank=True, null=True)
    portfolio = models.ForeignKey(
        Portfolio, related_name='comment_portfolios', on_delete=models.CASCADE)

    @classmethod
    def get_comments(cls, target):
        try:
            comments = PortfolioComment.objects.filter(portfolio=target)
        except:
            comments = None
        finally:
            return comments


class PortfolioImages(models.Model):
    image = models.ForeignKey(
        Images, related_name='portfolio_images', on_delete=models.CASCADE)
    portfolio = models.ForeignKey(to=Portfolio, null=True, blank=True,
                                  related_name='portfolio_images', on_delete=models.CASCADE)


# class PortfolioInformation(models.Model):
#     portfolio = models.OneToOneField(Portfolio, on_delete=models.CASCADE)
#     information = models.OneToOneField(
#         Information, related_name='portfolioInformations', on_delete=models.CASCADE)

# class PortfolioParticipant(models.Model):
#     portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
#     participant = models.ForeignKey(User, on_delete=models.CASCADE)

from datetime import date
from django.db import models
from django.conf import settings
import statistics


class Game(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    GAME_GENRES = [
        ('F', 'First-person shooter'),  # Wert und lesbare Form
        ('R', 'Role playing'),
        ('P', 'Puzzle'),
        ('I', 'Indie'),
        ('M', 'MMO (multi man online)'),
        ('V', 'Voxel'),
        ('A', 'Arcade'),
        ('J', 'Jump n Run')
    ]

    FSK_TYPES = [
        ('0', 'ab 0'),  # Wert und lesbare Form
        ('1', 'ab 6'),
        ('2', 'ab 12'),
        ('3', 'ab 16'),
        ('4', 'ab 18')
    ]

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500,
                                blank=True)
    date_published = models.DateField(blank=True,
                                      default=date.today,
                                      )
    genre = models.CharField(max_length=1,
                            choices=GAME_GENRES,
                            )
    fsk = models.CharField(max_length=1,
                        choices=FSK_TYPES,
                        )

    price = models.PositiveIntegerField()

    pdf = models.FileField(upload_to='uploaded_files/', blank=True, null=True)

    picture = models.ImageField(upload_to='uploaded_files/', blank=True, null=True)

    class Meta:
        ordering = ['name', '-genre']
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def get_full_name(self):
        return_string = self.name
        return return_string

    def get_rating(self):
        comments = Comment.objects.filter(game__id=self.id)
        rating = -1
        if len(comments)>0:
            ratings=[]
            for c in comments:
                c.rating=int(c.rating)
                crating = c.rating or 0
                ratings.append(int(crating))
            return round(statistics.mean(ratings))
        else:
            return -1

    def str(self):
        return self.name

    def repr(self):
        return self.get_full_name() + ' / ' + self.genre

class Comment(models.Model):
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField()
    reported = models.BooleanField(default=False, null=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def get_comment_prefix(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text

    def get_upvotes(self):
        upvotes = Vote.objects.filter(up_or_down='U',
                                      comment=self)
        return upvotes

    def get_upvotes_count(self):
        return len(self.get_upvotes())

    def get_downvotes(self):
        downvotes = Vote.objects.filter(up_or_down='D',
                                        comment=self)
        return downvotes

    def get_downvotes_count(self):
        return len(self.get_downvotes())

    def vote(self, user, up_or_down):
        U_or_D = 'U'
        if up_or_down == 'down':
            U_or_D = 'D'
        if Vote.objects.filter(user=user, comment=self, up_or_down=U_or_D).exists():
            Vote.objects.filter(user=user, comment=self, up_or_down=U_or_D).delete()
        else:
            Vote.objects.filter(user=user, comment=self).delete()
            vote = Vote.objects.create(up_or_down=U_or_D,
                                       user=user,
                                       comment=self
                                       )
    def get_rating(self):
        return int(self.rating)

    def __str__(self):
        return self.get_comment_prefix() + ' (' + self.user.username + ')'

    def __repr__(self):
        return self.get_comment_prefix() + ' (' + self.user.username + ' / ' + str(self.timestamp) + ')'


class Vote(models.Model):
    VOTE_TYPES = [
        ('U', 'up'),
        ('D', 'down'),
    ]

    up_or_down = models.CharField(max_length=1,
                                  choices=VOTE_TYPES,
                                 )
    timestamp = models.DateTimeField(auto_now_add=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'

    def __str__(self):
        return self.up_or_down + ' on "' + self.comment.name + '" by ' + self.user.username

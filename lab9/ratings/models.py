from django.db import models

# Create your models here.

class BookRating(models.Model):
    RATING_CHOICES = (
            ('good', 'Good'),
            ('satisfactory', 'Satisfactory'),
            ('bad', 'Bad'),
        )
    rating = models.CharField(max_length=12, choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_percentages(cls):
        total_votes = cls.objects.count()
        if total_votes == 0:
            return {'good': 0, 'satisfactory': 0, 'bad': 0}
        good_count = cls.objects.filter(rating='good').count()
        satisfactory_count = cls.objects.filter(rating='satisfactory').count()
        bad_count = cls.objects.filter(rating='bad').count()
        return {
            'good': int((good_count / total_votes) * 100),
            'satisfactory': int((satisfactory_count / total_votes) * 100),
            'bad': int((bad_count / total_votes) * 100),
        }
    
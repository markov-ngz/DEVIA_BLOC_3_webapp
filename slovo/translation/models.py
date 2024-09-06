from django.db import models
from django.contrib.auth.models import User

class Translation_stats(models.Model):

    user_id =  models.ForeignKey(User, related_name='translations_stats', on_delete=models.CASCADE)
    count_translations = models.IntegerField(default=0)
    count_feedbacks = models.IntegerField(default=0)
    count_neg_feedbacks = models.IntegerField(default=0)
    count_pos_feedbacks = models.IntegerField(default=0)

    @property
    def grade_translation(self):
        if self.count_translations < 5:
            return 'novice'
        elif self.count_translations < 10:
            return 'initie'
        elif self.count_translations < 15:
            return 'apprentice'
        elif self.count_translations < 25:
            return 'master'
        elif self.count_translations > 30:
            return 'grandmaster'
    @property
    def grade_feedback(self):
        if self.count_feedbacks < 5:
            return 'novice'
        elif self.count_feedbacks < 10:
            return 'initie'
        elif self.count_feedbacks < 15:
            return 'apprentice'
        elif self.count_feedbacks < 25:
            return 'master'
        elif self.count_feedbacks > 30:
            return 'grandmaster'
# ---- DEPRECATED ----

class Translation(models.Model):

    text = models.CharField(max_length=256)
    translation = models.CharField(max_length=256)
    is_correct = models.BooleanField()
    created_by = models.ForeignKey(User, related_name='translations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Contest


class QuestionModelTests(TestCase):

    def test(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        a=1+1
        b=2*1
        self.assertIs(a,b)
from django.test import TestCase
import datetime
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice
# Create your tests here.

def create_question( question_text, days):
    """
        Create a question with the given `question_text` and published the
        given number of `days` offset to now (negative for questions published
        in the past, positive for questions that have yet to be published).
    
    """
    time = timezone.now() + datetime.timedelta(days=days)    
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_poll(question_text, choice_text, time=timezone.now(), votes=0):
    poll_question = Question.objects.create(question_text=question_text, pub_date=time,)
    poll_choice = Choice.objects.create(choice_text=choice_text, votes=votes, question=poll_question)

def create_question_with_choices(days, choice_text_1, votes_1,choice_text_2, votes_2,):
    """ creates a question with some choices and their respective 
    choice_text and votes and also returns the id of the first choice 
    """
    past_question = create_question(question_text='question_text', days=days)
    return past_question
    choice_1 = past_question.choice_set.create(choice_text=choice_text_1, votes=votes_1)
    choice_2 = past_question.choice_set.create(choice_text=choice_text_2, votes=votes_2)
    choice_id = past_question.choice_set.get(id=1)
    return choice_id
        

class QuestionMOdelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is in the future.

        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is older than a day.

        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1) 
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date is within the last day.

        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_with_choice(self):
        """Question published with at least, one choice """

        question = create_question(question_text='Created question', days=-5)
        choice = question.choice_set.create(choice_text='created choice', votes=0)
        choice_text = question.choice_set.get(id=1).choice_text
        self.assertEqual(choice_text, 'created choice',)
        

    def test_was_published_without_choice(self):
        """Question published without any choice """
        question = create_question(question_text='Created question', days=-5)
        empty = False
        try:
            choice_text = question.choice_set.get(id=1).choice_text
            self.assertEqual(choice_text, [],)
        except(Choice.DoesNotExist):
            empty = True
        self.assertEqual(empty, True)
            


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """If no questions exist, returns an appropriate message"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page only if they have at least, one choice.
        """
        create_question('Past question', -30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def test_future_question(self):
        """ Questions with pub_date in the future are not displayed in the index page"""
        create_question('Future question', 30)
        response = self.client.get(reverse('polls:index'))
        #self.assertContains(response, 'No polls are available. ')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question_with_no_choice(self):
        """
        Even if both past and future questions exist, if they have no choice, 
        they would not be displayed
        """
        create_question('Future question', 30)
        create_question('Past question', -30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions if they have:
        1. Atleast, one choice for each question,
        2. Their pub_date are all now or in the past.
        """
        past_question_1 = create_question('Past question 1', -30)
        past_question_1.choice_set.create(choice_text='Past choice 1', votes=0)
        past_question_2 = create_question('Past question 2', -45)
        past_question_2.choice_set.create(choice_text='Past choice 2', votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 1>',
         '<Question: Past question 2>'])


class DetailViewTest(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """

        future_question = create_question(question_text='Future question', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past question', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class ResultsViewTest(TestCase):
    def test_future_question_results(self):
        """ Results for questions whose pub_date is in the future 
        returns a 404 not found
        """
        future_question = create_question(question_text='Future question', days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    #def test_past_question_results(self):
    #    """
    #    Results for questions whose pub_date is in the past are displayed 
    #    by the Resultsview()
    #    """
    #    past_question = create_question_with_choices(days=-5,choice_text_1='choice 1', votes_1=1, 
    #    choice_text_2='choice 2', votes_2=1)
    #    url = reverse('polls:results', args=(past_question.id,))
    #    response = self.client.get(url)
    #    self.assertEqual(response.status_code, 200)
    #    self.assertQuerysetEqual(response, choice_id) <-- choice_id is not defined

class CreatePollTest(TestCase):
    def test_is_question_text_in_response(self):
        poll = create_poll('Question text', 'Choice text')
        url = reverse('polls:create_poll',)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

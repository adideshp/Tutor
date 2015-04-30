from django.db import models
from django.contrib.auth.models import User

class User_Profile(models.Model):
    user = models.OneToOneField(User)
    score = models.IntegerField(default=0)
    user_type = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='profile_images', blank=True)



class Subject(models.Model):
    name = models.CharField(max_length=50)
    creation_time = models.DateTimeField(auto_now=True)


class Topic(models.Model):
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject)
    creation_time = models.DateTimeField(auto_now=True)


class Question(models.Model):
    question_text = models.CharField(max_length=300)
    explanation = models.CharField(max_length=100)
    options = models.CharField(max_length=200)
    owner = models.ForeignKey(User_Profile)
    hint = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    #target_exam = models.IntegerField()
    #subject = models.ForeignKey(Subject)
    #topic = models.ForeignKey(Topic)
    #permissions = models.IntegerField()
    points = models.IntegerField()
    creation_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):              # __unicode__ on Python 2
        return self.question_text


class Class(models.Model):
    instructor = models.ForeignKey(User_Profile, related_name = "User_Profile_Instructor")
    name = models.CharField(max_length=100)
    students =  models.ManyToManyField(User_Profile, related_name = "User_Profile_Students")
    creation_time = models.DateTimeField(auto_now=True)



class Test(models.Model):
    test_name = models.CharField(max_length=50)
    questions =  models.ManyToManyField(Question)
    owner = models.ForeignKey(User_Profile)
    assoicated_class = models.ForeignKey(Class, related_name="Class_Test")
    #target_exam = models.IntegerField()
    #subject = models.ForeignKey(Subject)
    #topic = models.ForeignKey(Topic)
    pass_criteria = models.IntegerField()
    total_time = models.IntegerField(default=0)
    ##difficulty_level = models.IntegerField()
    #instructions = models.CharField(max_length=550)
    #timed = models.BooleanField(default=True)
    #negetive_marking = models.BooleanField()
    #permissions = models.IntegerField()
    creation_time = models.DateTimeField(auto_now=True)


    def __str__(self):              # __unicode__ on Python 2
        return self.test_name


class Test_Summary(models.Model):
    test = models.ForeignKey(Test, related_name="Test_Solved_Summary")
    user = models.ForeignKey(User_Profile, related_name="User_Test_Summary")
    total_time = models.IntegerField(default=0)
    end_time = models.DateTimeField(auto_now=True)
    marks_scored = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    solved_count = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)
    unsolved_count  = models.IntegerField(default=0)


class Question_Summary(models.Model):
    question = models.ForeignKey(Question, related_name="Question_Solved_Summary")
    user = models.ForeignKey(User_Profile, related_name="User_Question_Summary")
    test_summary = models.ForeignKey(Test_Summary, related_name="Questions")
    time_taken = models.IntegerField(default=0)
    attempted = models.BooleanField(default=False)
    correct = models.BooleanField(default=False)


class Test_Report(models.Model):
    test = models.ForeignKey(Test, related_name="Test_Report")
    topper = models.ForeignKey(User_Profile, related_name="Topper")
    test_summary = models.ForeignKey(Test_Summary,related_name="Summary_Test_Report")



class Free_Radicals(models.Model):
    email = models.CharField(max_length=30)
    class_associated = models.ForeignKey(Class)
    creation_time = models.DateTimeField(auto_now=True)




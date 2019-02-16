import datetime

from django.db import models
from django.utils import timezone


class Group(models.Model):
    group_name = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.group_name

# 실제 db.sqlite3 파일에는 chatbot_User, chatbot_Mail 등과 같은 이름으로 테이블이 생성 된다.


class User(models.Model):
    user_name = models.CharField(max_length=30, default=None, null=True)
    user_key = models.CharField(max_length=30, primary_key=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, default=None)
    mail_check = models.BooleanField(default=False)
    state = models.CharField(max_length=20, default='home')

    def get_or_create(user_key):
        try:
            return User.objects.get(user_key=user_key)
        except:
            User.objects.create(user_key=user_key)
            return User.objects.get(user_key=user_key)

    def set_mail_check(self, mail_checked):
        self.mail_check = mail_checked
        self.save()

    def set_name(self, name):
        self.user_name = name
        self.save()

    def __str__(self):
        return self.user_key + '|' + str(self.user_name)


class Mail(models.Model):
    # 만약 여기서 참조하는 User의 데이터가 지워지면 CASCADE 옵션에 의해 같이 삭제
    # ForeignKey는 해당 인스턴스를 파라메터로 넘겨주어야 함
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mail_set_sender')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mail_set_receiver')
    message = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.user_name + '|' + self.message


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_message = models.TextField(null=True)
    bot_message = models.TextField(null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    delay = models.FloatField(null=True)

    def __str__(self):
        return self.user.user_name + '(' + self.user.user_key + ')' + '|' + self.user_message.replace('\n', '') + '|' + self.bot_message.replace('\n', '')

    def write(user, user_message, bot_message, delay=None):
        Log.objects.create(user=user, user_message=user_message,
                           bot_message=bot_message, delay=delay)


class Lazylet_Set(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lazylet_Term(models.Model):
    lazylet_set = models.ForeignKey(Lazylet_Set, on_delete=models.CASCADE)
    term = models.TextField()
    definition = models.TextField()
    image_url = models.CharField(max_length=200)

    def __str__(self):
        return self.term + '|' + self.definition

    class Meta:
        ordering = ['id']


class WordChain_Match(models.Model):
    round = models.IntegerField(default=1)
    last_word = models.OneToOneField(
        'WordChain_Word',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return "%d %s" % (self.round, str(self.wordchain_player_set.all()))


class WordChain_Player(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    match = models.ForeignKey(
        WordChain_Match, on_delete=models.SET_NULL, blank=True, null=True)
    win = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    last_played = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.user_name


class WordChain_Word(models.Model):
    match = models.ForeignKey(WordChain_Match, on_delete=models.CASCADE)
    word = models.CharField(max_length=200)
    player = models.ForeignKey(
        WordChain_Player, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.word

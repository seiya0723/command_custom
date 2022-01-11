from django.db import models
from django.utils import timezone

from django.core.validators import RegexValidator

class History(models.Model):

    dt      = models.DateTimeField(verbose_name="実行日時",default=timezone.now)

    #禁止する特殊文字( & | > < ; ` )。 ?!.*() の括弧内に指定した文字を含まない文字列。
    command_regex   = RegexValidator(regex=r"^(?!.*(\&|\||\>|\<|\;|\`)).*$")
    command         = models.CharField(verbose_name="実行したコマンド",max_length=300,validators=[command_regex])

    def __str__(self):
        return self.command


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone






class toode(models.Model):
    tootekood = models.IntegerField(unique=True)
    nimi = models.CharField(max_length=150)
    kirjeldus = models.TextField()
    #pdf voi pilt
    
    def __str__(self):
        return f"Kood: {str(self.tootekood)}, Nimi: {self.nimi} "





class projektid(models.Model):
    # Define status choices as a tuple of tuples
    NOT_STARTED = 'Not Started'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (NOT_STARTED, 'Not Started'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]

    projekt = models.CharField(max_length=30)
    staatus = models.CharField(
        max_length=150,
        choices=STATUS_CHOICES,  # Limit the status field to these choices
        default=NOT_STARTED,  # Set default status to "Not Started"
    )

    def __str__(self):
        return f"Projekt: {self.projekt}, Staatus: {self.staatus}"


#varvitabel

class mainvarvitabel(models.Model):
    projekt = models.ForeignKey('projektid', on_delete=models.DO_NOTHING)
    tootekood = models.ForeignKey('toode', on_delete=models.DO_NOTHING)
    #nimetus
    #kogus
    #varvikood
    #tahtaeg
    #ajakulu
    #staatus
    #ID

    #varvikood
    #staatus
    #tahtaeg
    def __str__(self):
        return f"Projekt: {self.projekt}, Toode Kood: {self.tootekood}, tootenim: {toode.tootekood}"



class task(models.Model):
    #task ehk id?
    taskcreator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='creator')
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsible')
    createdon = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Task {self.id}"



class komplekteeri(models.Model):
    taskid = models.ForeignKey('task', on_delete=models.DO_NOTHING, related_name='komplekteeri')
    toode = models.ForeignKey('toode', on_delete=models.DO_NOTHING)
    kogus = models.IntegerField(null=True)
    komplekteeritudkogus = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.taskid}"
    
class projektivaade(models.Model):
    projekt1 = models.ForeignKey('projektid', on_delete=models.DO_NOTHING, related_name='projektid1')
    toode = models.ForeignKey('toode', on_delete=models.DO_NOTHING)
    checkbox = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.projekt1}"


from djongo import models

def comparison_validator(function):
    def wrapper(instance, other_instance):
        if not isinstance(other_instance, models.Model):
            return False

        if instance._meta.concrete_model != other_instance._meta.concrete_model:
            return False
        
        if instance.pk is None:
            return instance is other_instance
        return function(instance, other_instance)

    return wrapper


class EmailAuth(models.Model):
    email = models.EmailField(max_length=100, blank=False, unique=True)

    def __srt__(self):
        return self.email


class Assignments(models.Model):
    name = models.TextField(blank=True, null=True)
    account_name = models.TextField(blank=True, null=True)
    start = models.DateField(blank=True, null=True)
    p1_end = models.DateField(blank=True, null=True)
    p2_end = models.DateField(blank=True, null=True)
    p3_end = models.DateField(blank=True, null=True)
    utilisation = models.FloatField(blank=True, null=True)

class Bio(models.Model):
#kimble information
    name = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=100, default='')
    url = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=50, default='')
    email = models.TextField(blank=True, null=True)
    assignments = models.ArrayReferenceField(
        to=Assignments,
        on_delete=models.DO_NOTHING, 
        blank=True, 
        null=True
    )
#bio Information
    profile = models.TextField(blank=True, null=True)
    technical_skills = models.TextField(blank=True, null=True) 
    skills = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{0},{1}'.format(self.name, self.title)


    @comparison_validator
    def __lt__(self, other):
        return self.name < other.name


    @comparison_validator
    def __gt__(self, other):
        return self.name > other.name

class Rosters(models.Model):
    nameR = models.CharField(max_length=100, default='')
    ownerR = models.CharField(max_length=100, default='')
    bio = models.ArrayReferenceField(
        to=Bio,
        on_delete=models.DO_NOTHING, 
        blank=True, 
        null=True
    )  


class Projects(models.Model):
    name = models.CharField(max_length=100, default='')
    rosters = models.ArrayReferenceField(
        to=Rosters,
        on_delete=models.DO_NOTHING, 
        blank=True, 
        null=True
    )    


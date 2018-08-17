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

class Profile(models.Model):
    profile = models.TextField()

     def __str__(self):
        return self.profile

    @comparison_validator
    def __lt__(self, other):
        return self.profile < other.profile

    @comparison_validator
    def __gt__(self, other):
        return self.profile > other.profile

    class Meta:
        abstract = True

class Skill(models.Model):
    skill = models.TextField()

    def __str__(self):
        return self.skill

    @comparison_validator
    def __lt__(self, other):
        return self.skill < other.skill

    @comparison_validator
    def __gt__(self, other):
        return self.skill > other.skill

    class Meta:
        abstract = True

class Technical(models.Model):
    technical = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.technical

    @comparison_validator
    def __lt__(self, other):
        return self.technical < other.technical

    @comparison_validator
    def __gt__(self, other):
        return self.technical > other.technical

class Education(models.Model):
    education = models.TextField()

    class Meta:
        abstract = True

class Bio(models.Model):
    # TODO: skills, experience array fields: cannot create as empty as of now
    nameAndTitle = models.CharField(max_length=100)
    profile = models.TextField(blank=True, null=True)
    #skills = models.ArrayModelField(model_container=Skill, blank=True, null=True)
    technical_skills = models.ArrayReferenceField(
        to=Technical,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    education = models.TextField(blank=True, null=True)
    #experience = models.ArrayModelField(model_container=Experience, blank=True, null=True)
    capabilities = models.ArrayReferenceField(
        to=CapabilityExpertise,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nameAndTitle

    @comparison_validator
    def __lt__(self, other):
        return self.nameAndTitle < other.nameAndTitle

    @comparison_validator
    def __gt__(self, other):
        return self.nameAndTitle > other.nameAndTitle

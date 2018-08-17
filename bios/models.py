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

class Skill(models.Model):
    description = models.TextField()

    class Meta:
        abstract = True

class Technical(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    @comparison_validator
    def __lt__(self, other):
        return self.name < other.name

    @comparison_validator
    def __gt__(self, other):
        return self.name > other.name

class Experience(models.Model):
    company = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        abstract = True

class Capability(models.Model):
    group = models.CharField(max_length=20)
    name = models.CharField(max_length=255)

    def __str__(self):
        return '{0}: {1}'.format(self.group, self.name)

class CapabilityExpertise(models.Model):
    capability = models.EmbeddedModelField(model_container=Capability)
    rating = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('capability', 'rating')

class Bio(models.Model):
    # TODO: skills, experience array fields: cannot create as empty as of now
    name_and_title = models.CharField(max_length=100)
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

    skills = models.ArrayReferenceField(
        to=Skill,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    def __str__(self):
        return '{0}, {1}'.format(self.name, self.title)

    @comparison_validator
    def __lt__(self, other):
        return self.name < other.name

    @comparison_validator
    def __gt__(self, other):
        return self.name > other.name

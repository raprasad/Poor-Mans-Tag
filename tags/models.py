from django.db import models
from django.template.defaultfilters import slugify

class Tag(models.Model):
    """Used in other Django projects to "tag" content.
    
    For example both a NewsStory and FacultyMember may have an M2M relationship to Tag
        class NewsStory(models.Model):
            ...
            tags = models.ManytoManyField(Tag)

        class FacultyMember(models.Model):
            ...
            tags = models.ManytoManyField(Tag)
            
    In this example, the sharing of tags allows a NewsStory to be loosely linked to a FacultyMember as well as other models, etc.

     """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, blank=True)
    visible = models.BooleanField(default=True)
    note = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name

    def save(self):
        self.slug = slugify(self.name)
        super(Tag, self).save()

    class Meta:
        ordering = ('name',)
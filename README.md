Used in other Django projects to "tag" content.

For example both a NewsStory and FacultyMember may have an M2M relationship to Tag:

```python    
    class NewsStory(models.Model):
        ...
        tags = models.ManytoManyField(Tag, null=True, blank=True)   # optional


    class FacultyMember(models.Model):
        ...
        tags = models.ManytoManyField(Tag, null=True, blank=True)   # optional

```
        
In this example, the sharing of tags allows a NewsStory to be loosely linked to a FacultyMember as well as other models, etc.  Or the tags only used within a single model may be used for classification.


(Why a separate "repository"?  Don't ask.) 


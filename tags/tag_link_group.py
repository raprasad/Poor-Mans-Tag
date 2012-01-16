from tags.models import Tag            
            

class TagLinkGroup:
    """Used to help render objects that use the Tag model in an M2M field
    e.g.
        - if a "Page" object has an attribute, similar to:
            tags = models.ManyToManyField(Tag, blank=True, null=True) 
       

        - start with a "obj_with_tag" instance that has a 'tags' attribute
        - build an array of related_objects that have the same tag by using the "_set" notation to call "ManyRelatedManager" objects
        - exclude the "obj_with_tag" from the array of "related_objects"
        - sort the related objects by name
    """
    def __init__(self, tag, obj_with_tag):
        self.obj_with_tag = obj_with_tag
        self.tag = tag
        self.related_objects = []
        self.load_related_objects()
        self.sort_related_objects()
        
    def get_related_object_cnt(self):
        if self.related_objects is None:
            return 0
        return len(self.related_objects)
        
    def sort_related_objects(self):
        self.related_objects.sort(key=lambda x: str(x))
        
    def is_related_obj_same_class(self, related_obj):
        if related_obj is None:
            return False
        
        # check if related_obj and obj_with_tag classes have same name
        if related_obj.__class__.__name__ == self.obj_with_tag.__class__.__name__:
            return True
        
        # check if 'subclass' attribute is same as the obj_with_tag class name
        if related_obj.__dict__.get('subclass_name', None) == self.obj_with_tag.__class__.__name__:
            return True
        
        return False
                
        
    def load_related_objects(self):
        # For the "self.tag":
        #   - iterate through each tag manager as in node_set, fooditem_set, knowledgeitem_set, etc. 
        #   - iterate through related objects in each manager
        #       - add each related object, excluding the "obj_with_tag" 
        #
        if self.tag is None:
            return
            
        # assume manager names end with '__set'
        manager_names = filter(lambda x: str(x).endswith('_set'), dir(self.tag))
        for tag_manager in manager_names:
            for related_obj in eval('self.tag.%s.all()' % tag_manager):
                if self.is_related_obj_same_class(related_obj) and related_obj.id == self.obj_with_tag.id:
                    continue    # this is the selected item, we don't want to list it
                self.related_objects.append(related_obj)                
        self.related_links_count = len(self.related_objects)


class TagLinkGroupManager:
    """Used to assist with an object that implements a 'tags' M2M attribute as in:
        tags = models.ManyToManyField(Tag, blank=True, null=True) 
        * blank=True, null=True aren't necessary to use this class
        
    ex/ usage:
        class FoodItem(models.Model):
            name =  models.CharField(max_length=255, unique=True)
            ...
            tags = models.ManyToManyField(Tag, blank=True, null=True)
            ...
        
        fi = FoodItem.objects.get(name='ketchup')
        tag_manager = TagLinkGroupManager(fi)
        see 'tag_manager' used in templates/tag_related_links.html
    """
    def __init__(self, obj):
        self.object_with_tags = obj
        self.tag_groups = []
        self.total_related_obj_cnt = 0
        self.create_tag_link_groups()
    
    def get_tag_groups(self):
        return self.tag_groups
        
    def get_tag_group_cnt(self):
        if self.tag_groups is None:
            return 0
        return len(self.tag_groups)
        
    def create_tag_link_groups(self):
        """
        Pull all related tag links.  Structure for use in templates.
        """
        if self.object_with_tags is None:
            return None

        if not 'tags' in dir(self.object_with_tags) or not self.object_with_tags.tags.__class__.__name__ == 'ManyRelatedManager':
            return None

        self.tag_groups = []
        self.total_related_obj_cnt = 0

        for tag in self.object_with_tags.tags.all():
            tg = TagLinkGroup(tag, self.object_with_tags)
            self.tag_groups.append(tg)
            self.total_related_obj_cnt += tg.get_related_object_cnt()
            
        


import datetime
from haystack import indexes
from models import Instance


class ModuleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    slug = indexes.CharField(model_attr='slug')
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Instance

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

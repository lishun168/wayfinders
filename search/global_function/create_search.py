from ..models import SearchObject, SearchTags

def create_search_tag(string, url, reference_type, description):
    search_object = SearchObject()
    search_tag = SearchTags()

    search_object.url = url
    search_object.reference_type = reference_type
    search_object.description = description
    search_object.save()

    search_tag.search_object = search_object
    search_tag.tag = string
    search_tag.save()
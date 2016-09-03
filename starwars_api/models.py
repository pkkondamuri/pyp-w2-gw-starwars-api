from starwars_api.client import SWAPIClient
from starwars_api.exceptions import SWAPIClientError
import requests
api_client = SWAPIClient()


class BaseModel(object):

    def __init__(self, json_data):
        """
        Dynamically assign all attributes in `json_data` as instance
        attributes of the Model.
        """
        self.data = json_data
        keys = self.data.keys()
        #print ("keys are "+ str(keys))
        for key in keys:
            setattr(self, key, self.data[key])
        #print ("this is the name " + self.name)
        
    @classmethod
    def get(cls, resource_id):
        """
        Returns an object of current Model requesting data to SWAPI using
        the api_client.
        """
        method_name = "get_"+cls.RESOURCE_NAME
        method = getattr(api_client,method_name)
        #print ("PRINTING method")
        #print (method)
        getitem = method(resource_id)
        
        #print ("PRINTING GETITEM:")
        #print (getitem)
        return cls(getitem)
    
    @classmethod
    def all(cls):
        """
        Returns an iterable QuerySet of current Model. The QuerySet will be
        later in charge of performing requests to SWAPI for each of the
        pages while looping.
        """
        
        contenttype = cls.RESOURCE_NAME
        """
        if contenttype == 'people':
            return PeopleQuerySet()
        else:
            return FilmsQuerySet()
        """
        Model = eval(contenttype.title()+"QuerySet")
        return Model()

class People(BaseModel):
    """Representing a single person"""
    RESOURCE_NAME = 'people'

    def __init__(self, json_data):
        super(People, self).__init__(json_data)

    def __repr__(self):
        return 'Person: {0}'.format(self.name)
        


class Films(BaseModel):
    RESOURCE_NAME = 'films'

    def __init__(self, json_data):
        super(Films, self).__init__(json_data)

    def __repr__(self):
        return 'Film: {0}'.format(self.title)


class BaseQuerySet(object):

    def __init__(self):
        
        self.data = api_client._get_swapi('/api/'+self.RESOURCE_NAME)
        
        #print ("this is content " + str(self.data))
        self.total = 0
        self.index = 0
        self.page = 1
        
        
    def __iter__(self):
        
        self.total = 0
        self.index = 0
        self.page = 1
        
        return self
        
        
    
    def __next__(self):
        """
        Must handle requests to next pages in SWAPI when objects in the current
        page were all consumed.
        """
        
        if self.total == self.data["count"]:
            raise StopIteration()
        if self.index == len(self.data['results']): 
            self.page += 1
            self.index = 0
            self.data = api_client._get_swapi('/api/people',page=self.page)
        
        data = self.data['results'][self.index]
        self.index += 1
        self.total += 1
        """
        if self.RESOURCE_NAME == 'people':
            return People(data)
        else:
            return Films(data)
        """
        Model = eval(self.RESOURCE_NAME.title())
        return Model(data)

    next = __next__

    def count(self):
        """
        Returns the total count of objects of current model.
        If the counter is not persisted as a QuerySet instance attr,
        a new request is performed to the API in order to get it.
        """
        
    
        count_val = 0
        for elem in self:
            count_val += 1
        return count_val
        
        
        

class PeopleQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'people'

    def __init__(self):
        super(PeopleQuerySet, self).__init__()

    def __repr__(self):
        return 'PeopleQuerySet: {0} objects'.format(str(len(self.objects)))


class FilmsQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'films'

    def __init__(self):
        super(FilmsQuerySet, self).__init__()

    def __repr__(self):
        return 'FilmsQuerySet: {0} objects'.format(str(len(self.objects)))

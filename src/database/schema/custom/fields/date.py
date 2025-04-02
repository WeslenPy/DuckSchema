
from marshmallow import fields
from datetime import datetime


class DateTime(fields.Field):
    
    def _serialize(self, value:datetime, attr, obj, **kwargs):
        if value is None:
            return datetime.now()
        
        return value.isoformat()

    def _deserialize(self, value:datetime, attr, data, **kwargs):
        
        date =datetime.fromisoformat(value)
        return date

  
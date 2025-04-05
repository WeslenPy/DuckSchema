
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from marshmallow import fields,validate

class SQLAlchemyAutoSchemaMix(SQLAlchemyAutoSchema):
    
    
    created_at = fields.DateTime(format="iso")
    update_at = fields.DateTime(format="iso")
    status = fields.Boolean(default=True)
 
    def __init__(self, *args, **kwargs):
        from diskrecuperar.database.config.conn import Session
        with Session() as session:
            kwargs["session"] = session
            super().__init__(*args, **kwargs)
    
import logging

from sqlalchemy import text

logger = logging.getLogger(__name__)

def ins_query(req, db):
    query = """
                INSERT INTO TEST(name, age) values(:name, :age)
            """
    
    bind_params = {
            "name" : req.name,
            "age" : req.age
        }
            
    logger.info(query)
    logger.info(bind_params)
    
    db.execute(
        text(query),
        bind_params
    )
        
def sel_query(req, db):
    query = """
                SELECT ID, NAME, AGE FROM TEST WHERE id = :id
            """
            
    bind_params = {
                    "id" : req.id
                }
            
    logger.info(query)
    logger.info(bind_params)
    
    result = db.execute(
            text(query),
            bind_params
        )
    
    rows = [dict(row) for row in result.mappings().all()]
    
    logger.info(f"rows : {rows}")
    
    return rows

def put_query(req, db):
    query = """
                UPDATE TEST SET name = :name, age = :age WHERE id = :id
            """
    
    bind_params = {
                    "id" : req.id,
                    "name" : req.name,
                    "age" : req.age
                }
    
    logger.info(query)
    logger.info(bind_params)
    
    db.execute(
            text(query),
            bind_params
        )
    
# def patch_query(req, db):
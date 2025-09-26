from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, insert,Enum, select, update, delete
from task import Task 

class TaskDB :
        def __init__(self):

            self.engine = create_engine('postgresql://postgres:kaoutar2002@localhost:5432/to_do_list_db')
            metadata = MetaData()

            self.tasks = Table(
                "tasks", metadata,
                Column("id", Integer, primary_key=True),
                Column("title", String, nullable=False),
                Column("done", Boolean, default=False) , 
                # Column("status", Enum('Pending', 'EnCours', 'Done', name="task_status"), default='Pending', nullable=False),
                # Column("priority", Enum('P0', 'P1', 'P2', 'P3', name="task_priority"), default='P3', nullable=False)

            )
            
            metadata.create_all(self.engine)

        def add_task(self , title_value):
              
              query = self.tasks.insert().values( title = title_value , done = False)
              with self.engine.begin() as conn :
                    conn.execute(query)
                    conn.commit()
        def get_all(self):
              with self.engine.begin() as conn : 
                    data = conn.execute(select(self.tasks).group_by(self.tasks.c.done , self.tasks.c.id))
                    conn.commit()
              return [Task(x.id , x.title , x.done) for x in data]
        
        def delete_by_id( self , task_id):
              
              query = delete(self.tasks).where(self.tasks.c.id == task_id)
              
              with self.engine.begin() as conn :
                    conn.execute( query )
                    conn.commit()

        def delete_all( self):
              
              query = delete(self.tasks)
              
              with self.engine.begin() as conn :
                    conn.execute( query )
                    conn.commit()
        # this is for updating the status ( done)
        def update_status(self , task : Task) :
              
              query = update(self.tasks).where(self.tasks.c.id == task.id ).values( done = task.done)
              
              with self.engine.begin() as conn : 
                    conn.execute( query )
                    conn.commit()
                        
# taskDB = TaskDB()
# taskDB.delete_all()
# print(taskDB)


# for task in taskDB.get_all() :
#     print( "id = " , task.id , "title = " , task.title , "status = " , task.done)

# taskDB.add_task("this is the fisrt task")
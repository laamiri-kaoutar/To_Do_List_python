class Task :
    
    # def __init__(self , id , title , done = False ):
    def __init__(self , id , title ,  status='Pending', priority='P3' ):

        self.id = id
        self.title = title
        # self.done = done
        self.status = status
        self.priority = priority

    
    def toggle_status(self):
        self.done = not self.done


class User():
    def __init__(self, uid, last_entrace):
        self.uid = uid

    def set_last_entrace(self):
        last_entrace = datetime.today()
        rows = session.query(Users).filter(Users.uid == self.uid).update({'last_entrace': last_entrace})
        session.commit()
        self.last_entrace = last_entrace

    def set_pushups(self, pushups):
        self.pushups = pushups


    def set_pushups(self, lunges):
        self.lunges = lunges


    def u_trainings(self):
        # autor = self.uid
        # return session.query(Workouts.name).filter(Workouts.ex_id == Exercises.id, Workouts.autor == self.uid).all()
        pass

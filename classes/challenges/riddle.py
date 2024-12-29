class Riddle:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer.lower()
        self.solved = False
        self.active = False
        self.user_input = ""

    def try_solve(self, answer):
        if answer.lower().strip() == self.answer:
            self.solved = True
            self.active = False
            return True
        return False
        
    def reset(self):
        """Reset the riddle state"""
        self.solved = False
        self.active = False
        self.user_input = ""
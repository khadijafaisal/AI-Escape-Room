class QuoteChallenge:
    def __init__(self, quote, missing_word):
        self.quote = quote
        self.missing_word = missing_word.lower()
        self.solved = False
        self.active = False
        self.user_input = ""

    def try_solve(self, answer):
        if answer.lower().strip() == self.missing_word:
            self.solved = True
            self.active = False
            return True
        return False
        
    def reset(self):
        """Reset the quote challenge state"""
        self.solved = False
        self.active = False
        self.user_input = ""
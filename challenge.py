class Challenge:
    def __init__(self, difficulty: int):
        self.difficulty = difficulty
        self.time_limit = 60 * difficulty
        self.points = 100 * difficulty
        self.completed = False
        
    def check_solution(self, attempt: str) -> bool:
        raise NotImplementedError
        
    def get_hint(self) -> str:
        raise NotImplementedError
        
    def calculate_score(self, time_taken: int) -> int:
        if not self.completed:
            return 0
        time_bonus = max(0, self.time_limit - time_taken)
        return self.points + time_bonus
class OptimizationHistory:
    def __init__(self):
        # Stores all iteration data
        self.history = []

    def log(self, iteration_data):
        # Add one iteration's data
        self.history.append(iteration_data)

    def get_history(self):
        # Return full optimization history
        return self.history
    
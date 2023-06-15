from problem import Problem, Eight_puzzle
from typing import Type
import random

class Problem_solver:
    def __init__(self): pass

    def train(self): pass

    def solve(self): pass
    
class Local_beam_search_solver(Problem_solver):
    def __init__(self):
        Problem_solver.__init__(self)

    def train(self, problem: Type[Problem], evaluate_func, r_func, n_func):
        self.problem = problem
        self.evaluate_func = evaluate_func
        self.r_func = r_func
        self.n_func = n_func

    def solve(self, beam_size, max_iter, max_restart):
        Problem_solver.solve(self)
        return self.__search(beam_size, max_iter, max_restart)

    def __search(self, beam_size, max_iter, max_restart):
        init_states = list(self.r_func(self.problem.get_state()))
        for _ in range(max_restart):
            beam_states = []
            # Khởi tạo các trạng thái ban đầu
            for _ in range(beam_size):
                state = random.choice(init_states)
                beam_states.append(state)
                init_states.remove(state)

            for _ in range(max_iter):
                successors = []
                # Tạo ra các trạng thái con
                for state in beam_states:
                    if state == self.problem.goal:
                        return state
                    successors.extend(list(self.n_func(state)))
                # Sắp xếp các trạng thái con theo hàm đánh giá
                successors_sort = sorted(successors, key = lambda x: self.evaluate_func(x))
                # Chọn ra các trạng thái tốt nhất
                beam_states = successors_sort[:beam_size]
        return None
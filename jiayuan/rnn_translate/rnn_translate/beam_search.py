
import numpy as np


class BeamSearch(object):
    def __init__(self, beam_size):
        assert beam_size >= 1
        self.beam_size = beam_size

        self.cum_values = [[0.0]*self.beam_size]
        self.tokens = [[-1]*self.beam_size]
        self.paths = [[0]*self.beam_size]

    def get_final_token_paths(self):
        max_step = len(self.paths) - 1
        beam_size = self.beam_size if self.beam_size < len(self.paths[max_step]) else len(self.paths[max_step])
        final_token_paths = []
        for hypo_idx in range(beam_size):
            print(self.cum_values[max_step][hypo_idx])
            tokens = self.get_token_path(hypo_idx=hypo_idx, step=max_step)
            final_token_paths.append(tokens)
        return final_token_paths

    def get_token_path(self, hypo_idx, step):
        token_list = []
        for step_idx in range(step, 0, -1):
            token_list = [self.tokens[step_idx][hypo_idx]] + token_list
            hypo_idx = self.paths[step_idx][hypo_idx]
        return token_list

    def get_path(self, hypo_idx, step):
        path_list = []
        for step_idx in range(step, 0, -1):
            path_list = [self.paths[step_idx][hypo_idx]] + path_list
            hypo_idx = self.paths[step_idx][hypo_idx]
        return path_list

    def _run_per_step(self, step, cal_function):
        beam_size = self.beam_size
        hypo_size = beam_size
        if step == 1:
            hypo_size = 1
        value_pool = np.array([])
        token_pool = np.array([], dtype=np.int)
        from_hypo_idx_pool = np.array([], dtype=np.int)
        for hypo_idx in range(hypo_size):
            cum_value = self.cum_values[step-1][hypo_idx]
            token_list = self.get_token_path(hypo_idx=hypo_idx, step=step-1)
            np.shape(token_list)

            cur_values = cal_function(token_list, step)
            topn_idxs = cur_values.argsort()[-beam_size:]
            #print(token_pool)
            #print(topn_idxs.tolist())
            token_pool = np.concatenate([token_pool, topn_idxs.tolist()])
            value_pool = np.concatenate([value_pool, [cum_value+v for v in cur_values[topn_idxs]]])
            from_hypo_idx_pool = np.concatenate([from_hypo_idx_pool, [hypo_idx] * len(topn_idxs)])

        topn_idxs = value_pool.argsort()[-beam_size:][::-1] # the first one is the best one
        self.cum_values.append(value_pool[topn_idxs].tolist())
        self.paths.append(from_hypo_idx_pool[topn_idxs].tolist())
        self.tokens.append(token_pool[topn_idxs].tolist())

    def run(self, max_step, cal_function):
        for step in range(1, max_step+1):
            self._run_per_step(step=step, cal_function=cal_function)
            #self.__str__()

    def __str__(self):
        max_step = len(self.paths) - 1
        beam_size = self.beam_size if self.beam_size < len(self.paths[max_step]) else len(self.paths[max_step])
        for hypo_idx in range(beam_size):
            print(self.cum_values[max_step][hypo_idx])
            path = self.get_path(hypo_idx=hypo_idx, step=max_step)
            tokens = self.get_token_path(hypo_idx=hypo_idx, step=max_step)
            print(path)
            print(tokens)


if __name__ == '__main__':
    def cal_function(useless, step):
        a = np.random.normal(loc=1, scale=2, size=3)
        print(a)
        return a

    beam_search = BeamSearch(beam_size=3)
    beam_search.run(max_step=5, cal_function=cal_function)

from utils import truncated_norm_dist_rv


class Station:
    def __init__(self) -> None:
        self.processing_time_min = None
        self.processing_time_max = None
        self.processing_time_mean = None
        self.processing_time_sd = None
        self.queue = []

    def get_processing_time(self):
        return truncated_norm_dist_rv(self.processing_time_min, self.processing_time_max,
                                      self.processing_time_mean, self.processing_time_sd)

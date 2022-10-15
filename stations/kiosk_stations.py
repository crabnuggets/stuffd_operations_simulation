from stations.base_station import Station


class WrapToastingStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 8
        self.processing_time_max = 12
        self.processing_time_mean = 10
        self.processing_time_sd = 2
        self.capacity = 1


class SaladBaseStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 2
        self.processing_time_max = 6
        self.processing_time_mean = 4
        self.processing_time_sd = 2
        self.capacity = 1


class SauceStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 1
        self.processing_time_max = 3
        self.processing_time_mean = 2
        self.processing_time_sd = 0.5
        self.capacity = 1


class DailyBowlToppingsStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 3
        self.processing_time_max = 7
        self.processing_time_mean = 5
        self.processing_time_sd = 1
        self.capacity = 1


class MeatStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 1.5
        self.processing_time_max = 3
        self.processing_time_mean = 2
        self.processing_time_sd = 0.5
        self.capacity = 1


class AdditionalToppingsStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 2
        self.processing_time_max = 5
        self.processing_time_mean = 3.5
        self.processing_time_sd = 1
        self.capacity = 1


class WrappingStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 3.5
        self.processing_time_max = 5
        self.processing_time_mean = 4
        self.processing_time_sd = 1.5
        self.capacity = 1


class ProductToastingStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 8
        self.processing_time_max = 15
        self.processing_time_mean = 12
        self.processing_time_sd = 3
        self.capacity = 3


class KioskOrderingStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 15
        self.processing_time_max = 35
        self.processing_time_mean = 18
        self.processing_time_sd = 6
        self.capacity = 1

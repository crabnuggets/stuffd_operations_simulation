from stations.base_station import Station


class IRLWrapToastingStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 8
        self.processing_time_max = 12
        self.processing_time_mean = 10
        self.processing_time_sd = 2


class IRLSaladBaseStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 3
        self.processing_time_max = 18
        self.processing_time_mean = 12
        self.processing_time_sd = 5


class IRLSauceStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 3
        self.processing_time_max = 7
        self.processing_time_mean = 5
        self.processing_time_sd = 2


class IRLDailyBowlToppingsStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 5
        self.processing_time_max = 20
        self.processing_time_mean = 13
        self.processing_time_sd = 5


class IRLMeatStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 1.5
        self.processing_time_max = 5
        self.processing_time_mean = 3
        self.processing_time_sd = 1


class IRLAdditionalToppingsStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 5
        self.processing_time_max = 18
        self.processing_time_mean = 13
        self.processing_time_sd = 3


class IRLWrappingStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 3.5
        self.processing_time_max = 5
        self.processing_time_mean = 4
        self.processing_time_sd = 1.5


class IRLProductToastingStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 8
        self.processing_time_max = 15
        self.processing_time_mean = 12
        self.processing_time_sd = 3


class IRLPaymentStation(Station):
    def __init__(self) -> None:
        super().__init__()
        self.processing_time_min = 15
        self.processing_time_max = 35
        self.processing_time_mean = 18
        self.processing_time_sd = 6

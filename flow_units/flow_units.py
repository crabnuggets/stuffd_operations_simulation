from flow_units.base_flow_unit import FlowUnit


class Kebab(FlowUnit):
    def __init__(self) -> None:
        super().__init__()
        self.recipe = ['WrapToastingStation', 'SaladBaseStation', 'SauceStation',
                       'MeatStation', 'WrappingStation', 'ProductToastingStation']


class Burrito(FlowUnit):
    def __init__(self) -> None:
        super().__init__()
        self.recipe = ['WrapToastingStation', 'SaladBaseStation', 'SauceStation', 'MeatStation',
                       'AdditionalToppingsStation', 'WrappingStation', 'ProductToastingStation']


class DailyBowl(FlowUnit):
    def __init__(self) -> None:
        super().__init__()
        self.recipe = ['SaladBaseStation', 'SauceStation', 'DailyBowlToppingsStation', 'MeatStation']

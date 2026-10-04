'''
演示类的封装
私有属性不能直接调用，可以通过类提供的公有方法来访问和修改私有属性
'''
class Car:
    def __init__(self, name, color):
        self.__name = name  # 私有属性
        self.__color = color  # 私有属性

    # 公有方法，获取私有属性name
    def get_name(self):
        return self.__name

    # 公有方法，设置私有属性name
    def set_name(self, name):
        self.__name = name

    # 公有方法，获取私有属性color
    def get_color(self):
        return self.__color

    # 公有方法，设置私有属性color
    def set_color(self, color):
        self.__color = color


# 定义一个继承自Car的子类Fuelcar
class Fuelcar(Car):
    def __init__(self, name, color, fuel_type):
        super().__init__(name, color)
        self.__fuel_type = fuel_type  # 私有属性

    # 公有方法，获取私有属性fuel_type
    def get_fuel_type(self):
        return self.__fuel_type

    # 公有方法，设置私有属性fuel_type
    def set_fuel_type(self, fuel_type):
        self.__fuel_type = fuel_type

class Electriccar(Car):
    def __init__(self, name, color, battery_capacity):
        super().__init__(name, color)
        self.__battery_capacity = battery_capacity  # 私有属性

    # 公有方法，获取私有属性battery_capacity
    def get_battery_capacity(self):
        return self.__battery_capacity

    # 公有方法，设置私有属性battery_capacity
    def set_battery_capacity(self, battery_capacity):
        self.__battery_capacity = battery_capacity


def main():
    # 创建一个燃油车对象
    fuel_car = Fuelcar("Toyota", "Red", "Gasoline")
    print(f"Fuel Car: {fuel_car.get_name()}, Color: {fuel_car.get_color()}, Fuel Type: {fuel_car.get_fuel_type()}")

    # 修改燃油车的属性
    fuel_car.set_name("Honda")
    fuel_car.set_color("Blue")
    fuel_car.set_fuel_type("Diesel")
    print(f"Updated Fuel Car: {fuel_car.get_name()}, Color: {fuel_car.get_color()}, Fuel Type: {fuel_car.get_fuel_type()}")

    # 创建一个电动车对象
    electric_car = Electriccar("Tesla", "White", 100)
    print(f"Electric Car: {electric_car.get_name()}, Color: {electric_car.get_color()}, Battery Capacity: {electric_car.get_battery_capacity()} kWh")

    # 修改电动车的属性
    electric_car.set_name("Nissan")
    electric_car.set_color("Black")
    electric_car.set_battery_capacity(80)
    print(f"Updated Electric Car: {electric_car.get_name()}, Color: {electric_car.get_color()}, Battery Capacity: {electric_car.get_battery_capacity()} kWh")

    # 多态演示
    cars = [fuel_car, electric_car]
    for car in cars:
        print(f"Car: {car.get_name()}, Color: {car.get_color()}")
        if isinstance(car, Fuelcar):
            print(f"Fuel Type: {car.get_fuel_type()}")
        elif isinstance(car, Electriccar):
            print(f"Battery Capacity: {car.get_battery_capacity()} kWh")
    


if __name__ == "__main__":
    main()
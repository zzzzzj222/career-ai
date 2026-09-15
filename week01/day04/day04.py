
'''
类的定义和使用示例
'''
class student:
    def __init__(self, name, chinese, math, english):
        self.name = name
        self.chinese = chinese
        self.math = math
        self.english = english

    def display(self):
        print(f"Name: {self.name}")
        print(f"Chinese: {self.chinese}")
        print(f"Math: {self.math}")
        print(f"English: {self.english}")

    def update_score(self, chinese=None, math=None, english=None):
        if chinese is not None:
            self.chinese = chinese
        if math is not None:
            self.math = math
        if english is not None:
            self.english = english
        else:
            print("Invalid subject")

if __name__ == '__main__':
    student1 = student("Alice", 90, 85, 92)
    student1.display()

    student1.update_score(chinese=95, math=88)
    student1.display()
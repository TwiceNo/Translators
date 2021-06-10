from stage2 import priority


class Stack:
    def __init__(self):
        self.stack = []
        self.counters = []
        self.last_bracket = None
        self.last_type = None

    def polska(self, item):
        if item in ["r2", "r3"]:
            return self.brackets(item)
        elif item in ["r5", "r6"]:
            return self.indexing(item)
        elif item == "r1":
            return self.comma()
        elif not self.stack or priority[item] > priority[self.stack[-1]]:
            self.stack.append(item)
            self.last_type = item[0]
        else:
            output = []
            while self.stack and priority[self.stack[-1]] <= priority[item]:
                output.append(self.stack.pop())
            self.last_type = item[0]
            return output

    def brackets(self, item):
        if self.last_type in ["i", "w"]:
            return self.function(item)
        if item == "r2":
            self.stack.append(item)
            self.last_bracket = item
            self.last_type = item[0]
        else:
            output = []
            stack_item = self.stack.pop()
            while self.stack and stack_item != "r2":
                output.append(stack_item)
                stack_item = self.stack.pop()
            self.last_bracket = None
            self.last_type = item[0]
            return output

    def indexing(self, item):
        if item == "r5":
            self.stack.append("INDEXING")
            self.counters.append(2)
            self.last_bracket = item
            self.last_type = item[0]
        else:
            output = []
            stack_item = self.stack.pop()
            while self.stack and stack_item != "INDEXING":
                output.append(stack_item)
                stack_item = self.stack.pop()
            output.append(self.counters.pop())
            output.append(self.stack.pop())
            self.last_bracket = None
            self.last_type = item[0]
            return output

    def function(self, item):
        if item == "r2":
            self.stack.append("FUNCTION")
            self.counters.append(1)
            self.last_bracket = item
            self.last_type = item[0]
        else:
            output = []
            stack_item = self.stack.pop()
            while self.stack and stack_item != "FUNCTION":
                output.append(stack_item)
                stack_item = self.stack.pop()
            output.append(self.counters.pop())
            output.append(self.stack.pop())
            self.last_bracket = None
            self.last_type = item[0]
            return output

    def comma(self):
        if self.last_bracket:
            if self.last_bracket == "r2":
                operation = "FUNCTION"
            else:
                operation = "INDEXING"
            output = []
            stack_item = self.stack.pop()
            while self.stack and stack_item != operation:
                output.append(stack_item)
                stack_item = self.stack.pop()
            self.counters[-1] += 1
            return output

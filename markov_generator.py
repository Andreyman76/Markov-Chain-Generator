import random


class MarkovNode:
    def __init__(self):
        self.postfixes = {}
        self.sum = 0

    def add_postfix(self, lexeme):
        if lexeme in self.postfixes.keys():
            self.postfixes[lexeme] += 1
        else:
            self.postfixes[lexeme] = 1

        self.sum += 1
        pass

    def select_random_postfix(self):
        intervals = {}
        left = 0.0

        for p in self.postfixes.keys():
            intervals[p] = [0.0, 0.0]
            intervals[p][0] = left
            left += (self.postfixes[p] / self.sum)
            intervals[p][1] = left

        num = random.random()
        for p in intervals.keys():
            if intervals[p][0] <= num < intervals[p][1]:
                return p

        raise KeyError(f'Key not found')

    def __str__(self):
        return '{' + f'sum: {self.sum}, postfixes: {self.postfixes}' + '}'


class MarkovGenerator:
    def __init__(self):
        self.__nodes = {'[START]': MarkovNode()}
        pass

    def add_sentence(self, sentence):
        """Add text (lexeme set) for analysis"""
        previous = '[START]'
        for lexeme in sentence:
            if not isinstance(lexeme, tuple):
                lexeme = tuple([lexeme])

            if lexeme not in self.__nodes.keys():
                self.__nodes[lexeme] = MarkovNode()
            self.__nodes[previous].add_postfix(lexeme)
            previous = lexeme

        self.__nodes[previous].add_postfix('[END]')
        pass

    def generate(self):
        """Generate text based on available data"""
        result = []

        lexeme = self.__nodes['[START]'].select_random_postfix()
        while lexeme != '[END]':
            if isinstance(lexeme, tuple):
                for i in lexeme:
                    result.append(i)
            else:
                result.append(lexeme)
            lexeme = self.__nodes[lexeme].select_random_postfix()

        return result

    def most_likely_continuation(self, starting_lexeme):
        """Select most likely postfix except [END]"""
        result = None

        if not isinstance(starting_lexeme, tuple):
            starting_lexeme = tuple([starting_lexeme])

        if starting_lexeme in self.__nodes.keys():
            postfixes = self.__nodes[starting_lexeme].postfixes
            max_sum = 0

            for postfix in postfixes:
                if postfix == '[END]':
                    continue

                if postfixes[postfix] > max_sum:
                    max_sum = postfixes[postfix]
                    result = postfix

        return result

    def print_nodes(self):
        """Print generator nodes to console"""
        for key in self.__nodes.keys():
            print(f'{key}: {self.__nodes[key]}')
        pass

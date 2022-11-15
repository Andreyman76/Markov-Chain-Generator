from markov_generator import MarkovGenerator


def get_syllables(string: str):
    """Get a list of syllables of a word"""
    string = string.replace('th', 'Θ')
    vowels = 'аеёиоуыэюяАЕЁИОУЫЭЮЯaeiouyAEIOUY'
    other = 'ъьЪь'
    parsed = []
    vowels_indexes = []
    result = []

    # Find the positions of the vowels, these are the syllables
    for i in range(len(string)):
        if string[i] in vowels:
            vowels_indexes.append(i)
            result.append(string[i])
            parsed.append(True)
        else:
            parsed.append(False)

    vowels_iterator = range(len(vowels_indexes))
    # Add one consonant to the left of the syllable, if possible
    for i in vowels_iterator:
        j = vowels_indexes[i]
        if j - 1 >= 0 and not parsed[j - 1] and string[j - 1] not in other:
            parsed[j - 1] = True
            result[i] = string[j - 1] + result[i]

    # Add all remaining letters to the right
    for i in vowels_iterator:
        j = vowels_indexes[i] + 1
        while j < len(string):
            if parsed[j]:
                break
            parsed[j] = True
            result[i] += string[j]
            j += 1

    # Add all remaining letters to the left
    for i in vowels_iterator:
        j = vowels_indexes[i] - 2
        while j >= 0:
            if parsed[j]:
                break
            parsed[j] = True
            result[i] = string[j] + result[i]
            j -= 1

    result = [i.replace('Θ', 'th') for i in result]
    return result


def group_by(elements: list, max_group_length: int):
    """Group elements by given group length"""
    result = []
    groups = []
    count = len(elements)

    for i in range(max_group_length):
        group = elements[0:i]
        if len(group) > 0:
            groups.append(tuple(group))
            group = []

        for j in range(i, count):
            group.append(elements[j])

            if len(group) == max_group_length:
                groups.append(tuple(group))
                group = []

        if len(group) > 0:
            groups.append(tuple(group))

        result.append(tuple(groups))
        groups = []

    return result


def run_examples():
    """Examples of using"""
    # Syllable example
    print('<Syllable example>')
    word = 'Programming'
    print(f'Word: {word}')
    syllables = get_syllables(word)
    print(f'Syllables: {syllables}')
    print('=' * 20)

    # Grouping example
    print('<Grouping example>')
    print(f'Elements: {syllables}')
    group_length = 2
    print(f'Groups with wax length {group_length}:')
    groups = group_by(syllables, group_length)
    for group in groups:
        print(group)
    print('=' * 20)

    # This example generates 5 unique names
    print('<Name generation example>')
    with open('FantasyMaleNames.txt', 'r', encoding='utf-8') as file:
        names = [name.replace('\n', '') for name in file.readlines()]

    generator = MarkovGenerator()

    # Loading the Generator with Examples
    for name in names:
        syllables = get_syllables(name)  # Got a list of syllables of a name
        generator.add_sentence(syllables)  # Adding syllables to generator as sentence

    # Generating 5 unique names
    count = len(names)
    while len(names) < count + 5:
        name = ''.join(generator.generate())
        if name not in names:  # Uniqueness check
            print(name)
            names.append(name)

    print('=' * 20)

    # Sentences generation example
    print('<Sentences generation example>')
    with open('HarryPotterText.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    replaces = {
        '!': '.',
        '?': '.',
        '...': '.',
        ';': '',
        '”': '',
        '“': '',
        ':': '',
        '\n': '',
        '\r': '',
        ', ': ' ',
        '(': '',
        ')': ''
    }

    for key, value in replaces.items():
        text = text.replace(key, value)

    sentences = text.split('.')
    generator = MarkovGenerator()

    for sentence in sentences:
        words = [word.lower() for word in sentence.split(' ')]
        while '' in words:
            words.remove('')

        generator.add_sentence(words)  # Add words to the generator as sentences
        groups = group_by(words, 2)
        for group in groups:
            generator.add_sentence(group)  # Add word groups to the generator as sentences

    # Generate 5 random sentences
    for i in range(5):
        print(' '.join(generator.generate()))

    print('=' * 20)

    # Example of automatic text continuation
    print('<Text auto-continuation example> (print [END] for exit)')
    while True:
        phrase = input('Input some word or phrase: ')
        if phrase == '[END]':
            break

        words = tuple(phrase.split(' ')) if ' ' in phrase else phrase
        generated = generator.most_likely_continuation(words)
        generated = ' '.join(generated) if isinstance(generated, tuple) else generated
        print(f'{phrase} {generated}')
    pass


if __name__ == '__main__':
    run_examples()

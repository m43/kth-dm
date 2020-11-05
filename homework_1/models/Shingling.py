import re
import hashlib


class Shingling:
    """
    Represents a text document using an ordered set of unique k-shingles; k is defined in the constructor.
    """

    def __init__(self, document_path, k, hash_function, universe, encoding='UTF-8'):
        """
        Constructs a Shingling object given a text document location and parameter k.

        :param document_path: Path to text document.
        :param k: The shingle size/length.
        :param hash_function: The hashing function to be used.
        :param universe: An array in which we save found hashed k-shingles to be used in later.
        :param encoding: The encoding used for reading the text document the path was given for.
        """

        # save arguments in object
        self.path = document_path
        self.k = k
        self.hash_function = hash_function
        self.universe = universe
        self.encoding = encoding

        # get all unique k_shingles
        k_shingles = set()
        with open(document_path, 'r', encoding=encoding) as f:
            previous = ''  # used to remember the last k characters of previous line to get shingles between two lines
            for line in f:
                line = previous + ' ' + line  # add previous characters for shingling
                line = ' '.join(line.split())  # remove all extra separators
                line = re.sub(r'[^a-zA-Z0-9]+', ' ', line)  # remove special characters (excluding spaces)
                line = line.lower()  # lowercase the whole thing
                if len(line) < k:
                    # current line is not long enough to generate k-sized shingles, read next line and remember this one
                    previous = line
                    continue
                # generate all k-shingles from current line
                for i in range(0, len(line) - k + 1):
                    k_shingles.add(line[i:i + k])
                previous = line[-k + 1:]

        # hash all the unique k-shingles and save them in the object
        hash_brownies = set()
        for k_shingle in k_shingles:
            hashed_shingle = hash_function(k_shingle)
            hash_brownies.add(hashed_shingle)
            universe.add(hashed_shingle)
        self.hash_brownies = hash_brownies

    def return_hashed_shingles(self):
        """
        Returns the set of hashed k-shingles.

        :return: The set of hashed k-shingles.
        """

        return self.hash_brownies

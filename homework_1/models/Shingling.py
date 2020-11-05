import re


class Shingling:
    """
    Represents a text document using an ordered set of unique k-shingles; k is defined in the constructor.
    """

    def __init__(self, readable_file_document, k, hash_function, universe):
        """
        Constructs a Shingling object given a text document location and parameter k.

        :param readable_file_document: A readable file document.
        :param k: The shingle size/length.
        :param hash_function: The hashing function to be used.
        :param universe: An array in which we save found hashed k-shingles to be used in later.
        """

        # get all unique k_shingles
        k_shingles = set()
        previous = ''  # used to remember the last k characters of previous line to get shingles between two lines
        for line in readable_file_document:
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
        hash_brownies = set([hash_function(x) for x in k_shingles])
        universe.update(hash_brownies)
        self.hash_brownies = hash_brownies

    def return_hashed_shingles(self):
        """
        Returns the set of hashed k-shingles.

        :return: The set of hashed k-shingles.
        """

        return self.hash_brownies

# -*- coding: utf-8 -*-
u"""
# -*- coding: utf-8 -*-
(c) 2009 Ryszard Szopa <ryszard.szopa@gmail.com>

This work ‘as-is’ we provide.
No warranty, express or implied.
We’ve done our best,
to debug and test.
Liability for damages denied.

Permission is granted hereby,
to copy, share, and modify.
Use as is fit,
free or for profit.
On this notice these rights rely.

This library provides two classes: Ngrams, which treats words as tokens

    >>> Ngrams(u"This is a very small donkey.") * Ngrams(u"This animal is a very small donkey.") #doctest:+ELLIPSIS
    0.771516749810...

and CharNgrams, which treats single characters as tokens:

    >>> CharNgrams('supercalifragilistic')*CharNgrams('supercalifragislislistic') #doctest:+ELLIPSIS
    0.973025545134...

If none of these fits your definition of `token' all you have to do is
subclass Ngrams and define you own tokenize method.

When creating an Ngrams object you can provide a second argument as
the value of n (the default being 3). You can compare only n-grams
with the same value of n.

    >>> Ngrams('ala ma kota', 3) * Ngrams('ala ma kota', 2)
    Traceback (most recent call last):
      ...
    WrongN

"""
import re
import math

class Ngrams(object):
    """
    Compare strings using an n-grams model and cosine similarity. This
    class uses words as tokens. See module docs.


    >>> print Ngrams('''Compare strings using an n-grams model and cosine similarity. This class uses words as tokens. See module docs.''').d
    """
    class WrongN(Exception):
        """Error to raise when two ngrams of different n's are being
        compared."""
        pass

    def __init__(self, text, n=3):
        self.n = n
        self.text = text
        self.d = self.text_to_ngrams(self.text, self.n)

    def __getitem__(self, word):
        return self.d[word]

    def __contains__(self, word):
        return word in self.d

    def __iter__(self):
        return iter(self.d)

    def __mul__(self, other):
        """
        Returns the similarity between self and other as a float in
        (0;1).
        """
        if self.n != other.n:
            raise self.WrongN
        if self.text == other.text:
            return 1.0
        return sum(self[k]*other[k] for k in self if k in other)

    def __repr__(self):
        return "Ngrams(%s, %s)" % (repr(self.text), repr(self.n))

    def __str__(self):
        return self.text

    def tokenize(self, text):
        """
        # -*- coding: utf-8 -*-
        Return an iterator of tokens of which the n-grams will
        consist. You can overwrite this method in subclasses.

        >>> list(Ngrams('').tokenize(chr(10).join([u"This work 'as-is' we provide.",\
        u'No warranty, express or implied.', \
        u"We've done our best,", \
        u'to debug and test.',\
        u'Liability for damages denied.'])))[:5]
        [u'this work asis', u'work asis we', u'asis we provide', u'we provide no', u'provide no warranty']

        """

        words = re.compile(u'[^\w\n ]|\xe2', re.UNICODE).sub('', text).lower().split()
        return (' '.join(words[i:i+self.n]) for i in range(len(words)))

    def text_to_ngrams(self, text, n=3):
        d = {}
        for ngram in self.tokenize(text):
            try: d[ngram] += 1
            except KeyError: d[ngram] = 1

        norm = math.sqrt(sum(x**2 for x in d.values()))
        for k, v in d.iteritems():
            d[k] = v/norm
        return d

class CharNgrams(Ngrams):

    """
    Ngrams comparison using single characters as tokens.

    >>> CharNgrams("ala ma kota")*CharNgrams("ala ma kota")
    1.0

    >>> CharNgrams("Warszawska")*CharNgrams("Warszawa") > CharNgrams("Warszawa")*CharNgrams("Wawa")
    True

    """
    def tokenize(self, st):
        """
        >>> ''.join(CharNgrams('').tokenize('ala ma kota!'))
        'alamakota'
        """
        return (c for c in st if c.isalnum())

class CharNgramSpaces(CharNgrams):
    '''Like CharNgrams, except it keeps whitespace as one space in
    the process of tokenization. This should be useful for analyzing
    texts longer than words, where places at which word boundaries
    occur may be important.'''
    def tokenize(self, st):
        return super(CharNgramSpaces, self).tokenize(re.sub(r'\s+', ' ', st))


if __name__=="__main__":
    import doctest
    doctest.testmod()


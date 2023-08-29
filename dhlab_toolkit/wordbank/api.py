import requests
from dhlab_toolkit.constants import BASE_URL

def word_variant(word: str, form: str, lang: str = "nob") -> list:
    """Find alternative ``form`` for a given ``word`` form.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint ``/variant_form``

    Example: ``word_variant('spiste', 'pres-part')``

    :param str word: any word string
    :param str form: a morphological feature tag from the Norwegian wordbank
        `"Orbanken" <https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-5/>`_.
    :param str lang: either "nob" or "nno"
    """
    r = requests.get(
        f"{BASE_URL}/variant_form", params={"word": word, "form": form, "lang": lang}
    )
    return r.json()


def word_paradigm(word: str, lang: str = "nob") -> list:
    """Find paradigms for a given ``word`` form.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint ``/paradigm``

    Example:

    .. code-block:: python

        word_paradigm('spiste')
        # [['adj', ['spisende', 'spist', 'spiste']],
        # ['verb', ['spis', 'spise', 'spiser', 'spises', 'spist', 'spiste']]]

    :param str word: any word string
    :param str lang: either "nob" or "nno"
    """
    r = requests.get(f"{BASE_URL}/paradigm", params={"word": word, "lang": lang})
    return r.json()


def word_paradigm_many(wordlist: list, lang: str = "nob") -> list:
    """Find alternative forms for a list of words."""
    r = requests.post(f"{BASE_URL}/paradigms", json={"words": wordlist, "lang": lang})
    return r.json()


def word_form(word: str, lang: str = "nob") -> list:
    """Look up the morphological feature specification of a ``word`` form."""
    r = requests.get(f"{BASE_URL}/word_form", params={"word": word, "lang": lang})
    return r.json()


def word_form_many(wordlist: list, lang: str = "nob") -> list:
    """Look up the morphological feature specifications for word forms in a ``wordlist``."""
    r = requests.post(f"{BASE_URL}/word_forms", json={"words": wordlist, "lang": lang})
    return r.json()


def word_lemma(word: str, lang: str = "nob") -> list:
    """Find the list of possible lemmas for a given ``word`` form."""
    r = requests.get(f"{BASE_URL}/word_lemma", params={"word": word, "lang": lang})
    return r.json()


def word_lemma_many(wordlist, lang="nob"):
    """Find lemmas for a list of given word forms."""
    r = requests.post(f"{BASE_URL}/word_lemmas", json={"words": wordlist, "lang": lang})
    return r.json()
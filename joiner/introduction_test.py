import json
import pytest

from .extractor import Name, Namespace, Signal, SignalName
from .introduction import IntroductionExtractor


def test_empty_input():
    extractor = IntroductionExtractor([])
    assert extractor.extract() == {}


def test_extract_years():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "bar",
                "year_of_introduction": 1903
            },
            {
                "name": "baz",
                "year_of_introduction": 2023
            }
        ]
    }
    """)
    extractor = IntroductionExtractor([pedigree])

    assert sorted(extractor.extract()) == sorted({
        Name("bar", Namespace.PEDIGREE): [
            Signal(SignalName.YEAR_OF_INTRODUCTION, 1903),
        ],
        Name("baz", Namespace.PEDIGREE): [
            Signal(SignalName.YEAR_OF_INTRODUCTION, 2023),
        ],
    })


def test_dedupe():
    pedigree1 = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "bar",
                "year_of_introduction": 1903
            },
            {
                "name": "baz",
                "year_of_introduction": 2023
            }
        ]
    }
    """)
    pedigree2 = json.loads("""
    {
        "name": "woo",
        "parentage": [
            {
                "name": "bar",
                "year_of_introduction": 1903
            },
            {
                "name": "yay",
                "year_of_introduction": 1979
            }
        ]
    }
    """)
    extractor = IntroductionExtractor([pedigree1, pedigree2])

    assert sorted(extractor.extract()) == sorted({
        Name("bar", Namespace.PEDIGREE): [
            Signal(SignalName.YEAR_OF_INTRODUCTION, 1903),
        ],
        Name("baz", Namespace.PEDIGREE): [
            Signal(SignalName.YEAR_OF_INTRODUCTION, 2023),
        ],
        Name("yay", Namespace.PEDIGREE): [
            Signal(SignalName.YEAR_OF_INTRODUCTION, 1979),
        ]
    })



def test_parentage_not_present():
    pedigree = json.loads("""
    {
        "name": "foo"
    }
    """)
    extractor = IntroductionExtractor([pedigree])

    assert extractor.extract() == {}


def test_parentage_empty():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": []
    }
    """)
    extractor = IntroductionExtractor([pedigree])


def test_parentage_has_no_year():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "bar"
            }
        ]
    }
    """)
    extractor = IntroductionExtractor([pedigree])

    assert extractor.extract() == {}


def test_parentage_has_no_name():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "year_of_introduction": 1999
            }
        ]
    }
    """)
    extractor = IntroductionExtractor([pedigree])

    assert extractor.extract() == {}


def test_year_is_not_int():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "bar",
                "year_of_introduction": "1999"
            }
        ]
    }
    """)
    extractor = IntroductionExtractor([pedigree])

    assert extractor.extract() == {}
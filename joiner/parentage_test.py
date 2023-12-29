import json
import pytest

from .extractor import Signal, SignalName
from .parentage import ParentageExtractor


def test_empty_input():
    extractor = ParentageExtractor([])
    assert extractor.extract() == {}

def test_reconstruct_tree():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "foo",
                "coordinates": [
                    0, 95, 40, 105
                ]
            },
            {
                "name": "woo",
                "coordinates": [
                    100, 45, 140, 55
                ]
            },
            {
                "name": "yay",
                "coordinates": [
                    100, 145, 140, 155
                ]
            },
            {
                "name": "houpla",
                "coordinates": [
                    200, 20, 240, 30
                ]
            },
            {
                "name": "panowie",
                "coordinates": [
                    200, 70, 240, 80
                ]
            },
            {
                "name": "moo",
                "coordinates": [
                    200, 120, 240, 130
                ]
            },
            {
                "name": "baa",
                "coordinates": [
                    200, 170, 240, 180
                ]
            }
        ]
    }
    """)
    extractor = ParentageExtractor([pedigree])

    assert sorted(extractor.extract()) == sorted({
        "foo": [
            Signal(SignalName.CHILD_OF, "woo"),
            Signal(SignalName.CHILD_OF, "yay")
        ],
        "woo": [
            Signal(SignalName.PARENT_OF, "foo"),
            Signal(SignalName.CHILD_OF, "houpla"),
            Signal(SignalName.CHILD_OF, "panowie")
        ],
        "houpla": [
            Signal(SignalName.PARENT_OF, "woo")
        ],
        "panowie": [
            Signal(SignalName.PARENT_OF, "woo")
        ],
        "yay": [
            Signal(SignalName.PARENT_OF, "foo"),
            Signal(SignalName.CHILD_OF, "moo"),
            Signal(SignalName.CHILD_OF, "baa")
        ],
        "moo": [
            Signal(SignalName.PARENT_OF, "yay")
        ],
        "baa": [
            Signal(SignalName.PARENT_OF, "yay")
        ],
    })


def test_dedupe_results():
    pedigree1 = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "foo",
                "coordinates": [
                    0, 95, 40, 105
                ]
            },
            {
                "name": "woo",
                "coordinates": [
                    100, 45, 140, 55
                ]
            },
            {
                "name": "houpla",
                "coordinates": [
                    200, 20, 240, 30
                ]
            }
        ]
    }
    """)
    pedigree2 = json.loads("""
    {
        "name": "woo",
        "parentage": [
            {
                "name": "woo",
                "coordinates": [
                    0, 95, 40, 105
                ]
            },
            {
                "name": "houpla",
                "coordinates": [
                    100, 45, 140, 55
                ]
            },
            {
                "name": "yay",
                "coordinates": [
                    200, 20, 240, 30
                ]
            }
        ]
    }
    """)
    extractor = ParentageExtractor([pedigree1, pedigree2])

    assert sorted(extractor.extract()) == sorted({
        "foo": [
            Signal(SignalName.CHILD_OF, "woo"),
        ],
        "woo": [
            Signal(SignalName.PARENT_OF, "foo"),
            Signal(SignalName.CHILD_OF, "houpla")
        ],
        "houpla": [
            Signal(SignalName.PARENT_OF, "woo"),
            Signal(SignalName.CHILD_OF, "yay")
        ],
        "yay": [
            Signal(SignalName.PARENT_OF, "houpla")
        ],
    })


def test_skip_no_parentage():
    pedigree = json.loads("""
    {
        "name": "foo"
    }
    """)
    extractor = ParentageExtractor([pedigree])

    assert extractor.extract() == {}


def test_skip_empty_parentage():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": []
    }
    """)
    extractor = ParentageExtractor([pedigree])

    assert extractor.extract() == {}


def test_skip_one_parentage():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "foo",
                "coordinates": [
                    0, 95, 40, 105
                ]
            }
        ]
    }
    """)
    extractor = ParentageExtractor([pedigree])

    assert extractor.extract() == {}


def test_skip_first_parentage_has_no_coords():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "foo"
            },
            {
                "name": "bar",
                "coordinates": [
                    100, 45, 140, 55
                ]
            }
        ]
    }
    """)
    extractor = ParentageExtractor([pedigree])

    assert extractor.extract() == {}


def test_skip_second_parentage_has_no_coords():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "foo",
                "coordinates": [
                    0, 95, 40, 105
                ]
            },
            {
                "name": "bar"
            }
        ]
    }
    """)
    extractor = ParentageExtractor([pedigree])

    assert extractor.extract() == {}


def test_skip_first_parentage_has_three_coords():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "foo",
                "coordinates": [
                    0, 95, 40
                ]

            },
            {
                "name": "bar",
                "coordinates": [
                    100, 45, 140, 55
                ]
            }
        ]
    }
    """)
    extractor = ParentageExtractor([pedigree])

    assert extractor.extract() == {}


def test_skip_second_parentage_has_three_coords():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "foo",
                "coordinates": [
                    0, 95, 40, 105
                ]
            },
            {
                "name": "bar",
                "coordinates": [
                    100, 45, 140
                ]
            }
        ]
    }
    """)
    extractor = ParentageExtractor([pedigree])

    assert extractor.extract() == {}


def test_skip_first_parentage_has_five_coords():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "foo",
                "coordinates": [
                    0, 95, 40, 105, 99
                ]
            },
            {
                "name": "bar",
                "coordinates": [
                    100, 45, 140, 55
                ]
            }
        ]
    }
    """)
    extractor = ParentageExtractor([pedigree])

    assert extractor.extract() == {}


def test_skip_second_parentage_has_five_coords():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "foo",
                "coordinates": [
                    0, 95, 40, 105
                ]
            },
            {
                "name": "bar",
                "coordinates": [
                    100, 45, 140, 55, 98
                ]
            }
        ]
    }
    """)
    extractor = ParentageExtractor([pedigree])

    assert extractor.extract() == {}


def test_skip_unknown_parent():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "foo",
                "coordinates": [
                    0, 95, 40, 105
                ]
            },
            {
                "name": "unknown",
                "coordinates": [
                    100, 45, 140, 55
                ]
            }
        ]
    }
    """)
    extractor = ParentageExtractor([pedigree])

    assert extractor.extract() == {}


def test_ignore_entry_with_3_coords():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "foo",
                "coordinates": [
                    0, 95, 40, 105
                ]
            },
            {
                "name": "woo",
                "coordinates": [
                    100, 45, 140, 55
                ]
            },
            {
                "name": "houpla",
                "coordinates": [
                    200, 20, 240
                ]
            }
        ]
    }
    """)
    extractor = ParentageExtractor([pedigree])

    assert sorted(extractor.extract()) == sorted({
        "foo": [
            Signal(SignalName.CHILD_OF, "woo"),
        ],
        "woo": [
            Signal(SignalName.PARENT_OF, "foo"),
        ],
    })


def test_ignore_entry_with_5_coords():
    pedigree = json.loads("""
    {
        "name": "foo",
        "parentage": [
            {
                "name": "foo",
                "coordinates": [
                    0, 95, 40, 105
                ]
            },
            {
                "name": "woo",
                "coordinates": [
                    100, 45, 140, 55
                ]
            },
            {
                "name": "houpla",
                "coordinates": [
                    200, 20, 240, 30, 97
                ]
            }
        ]
    }
    """)
    extractor = ParentageExtractor([pedigree])

    assert sorted(extractor.extract()) == sorted({
        "foo": [
            Signal(SignalName.CHILD_OF, "woo"),
        ],
        "woo": [
            Signal(SignalName.PARENT_OF, "foo"),
        ],
    })
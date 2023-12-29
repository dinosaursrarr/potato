import json
import pytest

from .extractor import Signal, SignalName
from .name import EuropotatoPedigreeNameExtractor, PedigreeNameExtractor

def test_pedigree_name_empty_input():
    extractor = PedigreeNameExtractor([])
    assert extractor.extract() == {}


def test_pedigree_names():
    pedigree1 = json.loads('{"name": "foo"}')
    pedigree2 = json.loads('{"name": "bar"}')
    extractor = PedigreeNameExtractor([pedigree1, pedigree2])
    assert sorted(extractor.extract()) == sorted({
        "foo": [Signal(SignalName.PEDIGREE_NAME, "foo")],
        "bar": [Signal(SignalName.PEDIGREE_NAME, "bar")],
    })


def test_skip_missing_pedigree_name():
    pedigree1 = json.loads('{"year_of_introduction": 1987}')
    extractor = PedigreeNameExtractor([pedigree1])
    assert extractor.extract() == {}


def test_europotato_pedigree_names_empty_input():
    name_map = {"1": "foo", "2003": "bar"}
    extractor = EuropotatoPedigreeNameExtractor({}, name_map)
    assert extractor.extract() == {}


def test_europotato_pedigree_names_empty_name_map():
    pedigrees = {
        "1.json": {"name": "woo"},
        "2003.json": {"name": "yay"}
    }
    name_map = {"1": "foo", "2003": "bar"}
    extractor = EuropotatoPedigreeNameExtractor(pedigrees, {})
    assert extractor.extract() == {}


def test_europotato_pedigree_names_success():
    pedigrees = {
        "1.json": {"name": "woo"},
        "2003.json": {"name": "yay"}
    }
    name_map = {"1": "foo", "2003": "bar"}
    extractor = EuropotatoPedigreeNameExtractor(pedigrees, name_map)
    assert sorted(extractor.extract()) == sorted({
        "woo": [Signal(SignalName.EUROPOTATO_NAME, "foo")],
        "yay": [Signal(SignalName.EUROPOTATO_NAME, "bar")],
    })


def test_europotato_pedigree_names_ignore_pedigree_not_in_name_map():
    pedigrees = {
        "2.json": {"name": "woo"}
    }
    name_map = {"1": "foo", "2003": "bar"}
    extractor = EuropotatoPedigreeNameExtractor(pedigrees, name_map)
    assert extractor.extract() == {}


def test_europotato_pedigree_names_ignore_pedigree_not_ending_in_json():
    pedigrees = {
        "1": {"name": "woo"}
    }
    name_map = {"1": "foo", "2003": "bar"}
    extractor = EuropotatoPedigreeNameExtractor(pedigrees, name_map)
    assert extractor.extract() == {}


def test_europotato_pedigree_names_ignore_pedigree_without_name():
    pedigrees = {
        "1.json": {"year_of_introduction": 1977}
    }
    name_map = {"1": "foo", "2003": "bar"}
    extractor = EuropotatoPedigreeNameExtractor(pedigrees, name_map)
    assert extractor.extract() == {}


def test_europotato_pedigree_names_ignore_empty_name_map_entry():
    pedigrees = {
        "1.json": {"name": "foo"}
    }
    name_map = {"1": "", "2003": "bar"}
    extractor = EuropotatoPedigreeNameExtractor(pedigrees, name_map)
    assert extractor.extract() == {}
import json
import pytest

from .loader import JsonLoader

# no such directory
# no .json files
# load all with no filter
# filter when filter applied
# non-json in file

def test_no_such_directory(tmp_path):
    l = JsonLoader(tmp_path / "foo", lambda j,n: n)
    with pytest.raises(FileNotFoundError, match='foo'):
        l.load()

def test_no_json_files_in_directory(tmp_path):
    d = tmp_path / "bar"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("hello")
    l = JsonLoader(d, lambda j,n: n)
    assert l.load() == {}

def test_load_all_json_files(tmp_path):
    d = tmp_path / "baz"
    d.mkdir()
    (d / "abc.json").write_text('{"foo": "bar", "baz": [1, 2, 3]}')
    (d / "def.json").write_text('{"foo": "woo", "baz": [7, 8, 9]}')
    l = JsonLoader(d, lambda j,n: n[:-5])

    assert l.load() == {
        "abc": {"foo": "bar", "baz": [1, 2, 3]},
        "def": {"foo": "woo", "baz": [7, 8, 9]}
    }

def test_key_fn_on_json(tmp_path):
    d = tmp_path / "baz"
    d.mkdir()
    (d / "abc.json").write_text('{"foo": "bar", "baz": [1, 2, 3]}')
    (d / "def.json").write_text('{"foo": "woo", "baz": [7, 8, 9]}')
    l = JsonLoader(d, lambda j,n: j["foo"])

    assert l.load() == {
        "bar": {"foo": "bar", "baz": [1, 2, 3]},
        "woo": {"foo": "woo", "baz": [7, 8, 9]}
    }

def test_filter_filenames(tmp_path):
    d = tmp_path / "baz"
    d.mkdir()
    (d / "abc.json").write_text('{"foo": "bar", "baz": [1, 2, 3]}')
    (d / "def.json").write_text('{"foo": "woo", "baz": [7, 8, 9]}')
    l = JsonLoader(d, lambda j,n: n[:-5], lambda x: x[0] == 'a')

    assert l.load() == {
        "abc": {"foo": "bar", "baz": [1, 2, 3]}
    }

def test_non_json_content(tmp_path):
    d = tmp_path / "baz"
    d.mkdir()
    (d / "abc.json").write_text('hello my baby hello my honey')
    l = JsonLoader(d, lambda j,n: n)
    with pytest.raises(json.decoder.JSONDecodeError):
        l.load()
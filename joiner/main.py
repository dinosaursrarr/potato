import json
import pathlib

from absl import app
from absl import flags
from enum import Enum

from joiner.introduction import IntroductionExtractor
from joiner.loader import JsonLoader
from joiner.name import EuropotatoPedigreeNameExtractor, PedigreeNameExtractor
from joiner.parentage import ParentageExtractor

FLAGS = flags.FLAGS

flags.DEFINE_string('europotato_root', '', 'Path to read europotato crawler json output from.')
flags.DEFINE_string('pedigree_root', '', 'Path to read potato pedigree crawler json output from.')
flags.DEFINE_string('output_root', '', 'Path to write output files under.')


def main(argv):
    if not FLAGS.europotato_root:
        raise ValueError('europotato_root must be provided')
    if not FLAGS.pedigree_root:
        raise ValueError('pedigree_root must be provided')
    if not FLAGS.output_root:
        raise ValueError('Output root must be provided')
    europotato_root = pathlib.Path(FLAGS.europotato_root)
    pedigree_root = pathlib.Path(FLAGS.pedigree_root)
    output_root = pathlib.Path(FLAGS.output_root)

    # europotato_e = JsonLoader(europotato_root, lambda j,n: j["name"], lambda x: x[-7:-5] == '-E').load()
    # europotato_p = JsonLoader(europotato_root, lambda j,n: j["name"], lambda x: x[-7:-5] == '-P').load()
    pedigree = JsonLoader(pedigree_root, lambda j,n: n[:-5], lambda x: x[:-5].isnumeric()).load()
    name_map = json.load(open(pedigree_root / 'europotato_names.json'))

    extractors = [
        ParentageExtractor(pedigree.values()),
        IntroductionExtractor(pedigree.values()),
        PedigreeNameExtractor(pedigree.values()),
        EuropotatoPedigreeNameExtractor(pedigree, name_map)
    ]
    for extractor in extractors:
        signals = extractor.extract()


if __name__ == '__main__':
    app.run(main)

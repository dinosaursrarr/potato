import json
import pathlib

from absl import app
from absl import flags

from joiner.loader import JsonLoader

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

    europotato_e = JsonLoader(europotato_root, lambda j,n: j["name"], lambda x: x[-2:] == '-E').load()
    europotato_p = JsonLoader(europotato_root, lambda j,n: j["name"], lambda x: x[-2:] == '-P').load()
    pedigree = JsonLoader(pedigree_root, lambda j,n: j["name"], lambda x: x.isnumeric()).load()
    name_map = json.load(open(pedigree_root / 'europotato_names.json'))

if __name__ == '__main__':
    app.run(main)

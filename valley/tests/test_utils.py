import json
import unittest

from valley.tests.examples.example_schemas import durham
from valley.utils import import_util
from valley.utils.json_utils import (ValleyEncoder, ValleyDecoder)


class UtilTest(unittest.TestCase):
    json_string = '{"dogs": [{"breed": {"name": "Cocker Spaniel",' \
                  ' "_type": "valley.tests.examples.example_schemas.Breed"},' \
                  ' "name": "Bruno", "_type": "valley.tests.examples.' \
                  'example_schemas.Dog"}, {"breed": {"name": "Cockapoo", ' \
                  '"_type": "valley.tests.examples.example_schemas.Breed"}' \
                  ', "name": "Blitz", "_type": ' \
                  '"valley.tests.examples.example_schemas.Dog"}], ' \
                  '"primary_breed": {"name": "Cocker Spaniel", ' \
                  '"_type": "valley.tests.examples.example_schemas.Breed"}, ' \
                  '"name": "Durham", "_type": ' \
                  '"valley.tests.examples.example_schemas.Troop"}'

    def test_import_util(self):
        klass = import_util('valley.properties.SlugProperty')
        self.assertEqual('SlugProperty', klass.__name__)

    def test_json_encoder(self):
        self.assertEqual(json.dumps(durham, cls=ValleyEncoder), self.json_string)

    def test_json_decoder(self):
        new_troop = json.loads(self.json_string, cls=ValleyDecoder)
        self.assertEqual(new_troop.name, durham.name)
        self.assertEqual(new_troop.primary_breed.name, durham.primary_breed.name)
        self.assertEqual(new_troop.dogs[0].name, durham.dogs[0].name)
        self.assertEqual(new_troop.dogs[1].name, durham.dogs[1].name)

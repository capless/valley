import unittest
import json

from valley.utils import import_util
from valley.utils.json_utils import (ValleyEncoder,ValleyDecoder,
                                     ValleyEncoderNoType)
from valley.tests.examples.schemas import durham


class UtilTest(unittest.TestCase):

    json_string = '{"dogs": [{"breed": {"name": "Cocker Spaniel",' \
                      ' "_type": "valley.tests.examples.schemas.Breed"},' \
                      ' "name": "Bruno", "_type": "valley.tests.examples.' \
                      'schemas.Dog"}, {"breed": {"name": "Cockapoo", ' \
                      '"_type": "valley.tests.examples.schemas.Breed"}' \
                      ', "name": "Blitz", "_type": ' \
                      '"valley.tests.examples.schemas.Dog"}], ' \
                      '"primary_breed": {"name": "Cocker Spaniel", ' \
                      '"_type": "valley.tests.examples.schemas.Breed"}, ' \
                      '"name": "Durham", "_type": ' \
                      '"valley.tests.examples.schemas.Troop"}'

    def test_import_util(self):
        klass = import_util('valley.mixins.VariableMixin')
        self.assertEqual('VariableMixin', klass.__name__)

    def test_json_encoder(self):
        self.assertEqual(json.dumps(durham,cls=ValleyEncoder),self.json_string)

    def test_json_decoder(self):
        new_troop = json.loads(self.json_string, cls=ValleyDecoder)
        self.assertEqual(new_troop.name,durham.name)
        self.assertEqual(new_troop.primary_breed.name, durham.primary_breed.name)
        self.assertEqual(new_troop.dogs[0].name, durham.dogs[0].name)
        self.assertEqual(new_troop.dogs[1].name, durham.dogs[1].name)

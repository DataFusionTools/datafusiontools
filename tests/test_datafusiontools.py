from machine_learning.mpl import MPL

import setup as s
import pytest
import json
from core.data_input import Data, Variable, Geometry
from core.data_input import Geometry, Data, Variable
from tests.utils import TestUtils
import numpy as np
from core.utils import CreateInputsML, AggregateMethod
import machine_learning.enumeration_classes as class_enums

np.random.seed(1)


class TestDataFusionTools:
    @pytest.mark.skip(reason="__version__ should now be import from setup.cfg")
    @pytest.mark.acceptancey
    def test_version(self):
        pass

    @pytest.mark.acceptance
    def test_neural_net(self):
        # read result json of OURS and create data
        input_files = TestUtils.get_test_files_from_local_test_dir("", "results.json")
        with open(str(input_files[0])) as f:
            scenario_data = json.load(f)
        # each scenario is is a separate Data class
        data_list = []
        geometry = Geometry(x=0, y=0, z=0)
        for key, value in scenario_data.items():
            data_for_input = []
            for name_attribute, list_values in value["data"].items():
                if not (name_attribute == "Depth"):
                    data_for_input.append(
                        Variable(label=name_attribute, value=np.array(list_values))
                    )
            data_list.append(
                Data(
                    location=geometry,
                    independent_variable=Variable(
                        label="depth", value=np.array(value["data"]["Depth"])
                    ),
                    variables=data_for_input,
                )
            )
        assert len(data_list) == 11
        # create features from data
        create_features = CreateInputsML()
        for data in data_list:
            create_features.add_features(
                data, ["E", "v", "rho"], use_location_as_input=(False, False, False)
            )
            create_features.add_targets(data, ["Lithology"])
        assert create_features.get_all_features(flatten=False).shape == (32, 4)
        assert create_features.get_all_targets(flatten=False).shape == (32, 1)
        # Create neural net based on this input
        nn = MPL(
            classification=True,
            nb_hidden_layers=3,
            nb_neurons=[28, 28, 14],
            activation_fct=class_enums.ActivationFunctions.sigmoid,
            optimizer=class_enums.Optimizer.Adam,
            loss=class_enums.LossFunctions.binary_crossentropy,
            epochs=2,
            batch=1,
            regularisation=0,
        )
        # Train with flat shape
        nn.train(
            create_features.get_all_features(flatten=False),
            create_features.get_all_targets(flatten=False),
        )
        nn.predict(create_features.get_all_features(flatten=False))
        assert nn.prediction[0]
        assert nn.accuracy

    @pytest.mark.acceptance
    def test_two_datasets(self):
        class CPT:
            def __init__(self):
                self.qc = [1, 2, 3, 2, 2]
                self.depth = [0, 0.1, 0.2, 0.3, 0.4]
                self.friction = [0.5, 0.6, 0.5, 0.3, 0.2]
                self.pwp = [0.1, 0.2, 0.3, 0.2, 0.2]
                self.label = ["1", "1", "2", "2", "3"]
                self.coordinates = [100, 200, -0.5]

        class insar:
            def __init__(self):
                self.time = [0, 10, 20, 50]
                self.disp = [[0, -0.01, -0.02, -0.02], [0, -0.01, -0.02, -0.02]]
                self.coordinates = [[100, 200], [120, 220]]

        cpt1 = CPT()
        cpt2 = CPT()
        cpt2.coordinates = [200, 300, -0.5]
        cpts = [cpt1, cpt2]
        set = insar()

        data_list_cpt = []
        for c in cpts:
            data_for_input = []
            for att in c.__dict__.keys():
                if not (att == "depth") and not (att == "coordinates"):
                    data_for_input.append(
                        Variable(label=att, value=np.array(getattr(c, att)))
                    )

            data_list_cpt.append(
                Data(
                    location=Geometry(
                        x=c.coordinates[0], y=c.coordinates[1], z=c.coordinates[2]
                    ),
                    independent_variable=Variable(
                        label="depth", value=np.array(c.depth)
                    ),
                    variables=data_for_input,
                )
            )

        data_list_insar = []
        for i, val in enumerate(set.coordinates):

            data_list_insar.append(
                Data(
                    location=Geometry(x=val[0], y=val[1], z=0),
                    independent_variable=Variable(
                        label="time", value=np.array(set.time)
                    ),
                    variables=[
                        Variable(label="displacement", value=np.array(set.disp[i]))
                    ],
                )
            )
        create_features = CreateInputsML()
        aggregated_features = create_features.find_closer_points(
            input_data=data_list_cpt,
            combined_data=data_list_insar,
            aggregate_method=AggregateMethod.MAX,
            interpolate_on_independent_variable=False,
            aggregate_variable="displacement",
            number_of_points=1,
        )
        for data in aggregated_features:
            create_features.add_features(
                data,
                ["qc", "friction", "pwp", "displacement"],
                use_independent_variable=True,
            )
            create_features.add_targets(data, ["label"])

        features = create_features.get_all_features(flatten=False)
        targets = create_features.get_all_targets(flatten=False)
        assert features.shape == (10, 5)
        nn = MPL(
            classification=True,
            nb_hidden_layers=3,
            nb_neurons=[28, 28, 14],
            activation_fct=class_enums.ActivationFunctions.sigmoid,
            optimizer=class_enums.Optimizer.Adam,
            loss=class_enums.LossFunctions.binary_crossentropy,
            epochs=2,
            batch=1,
            regularisation=0,
        )
        # Train with flat shape
        nn.train(
            features,
            targets,
        )
        nn.predict(features)
        assert nn.prediction[0] == "1"

The data were stored in a :download:`pickle <../_static/test_case_DF.pickle>` file.

.. code-block:: python

    
    def get_input_data():
        input_files = "test_case_DF.pickle"
        with open(input_files, "rb") as f:
            (cpts, resistivity, insar) = pickle.load(f)
        # create List[Data]
        cpts_list = []
        for name, item in cpts.items():
            location = Geometry(x=item["coordinates"][0], y=item["coordinates"][1], z=0)
            cpts_list.append(
                Data(
                    location=location,
                    independent_variable=Variable(value=item["NAP"], label="NAP"),
                    variables=[
                        Variable(value=item["water"], label="water"),
                        Variable(value=item["tip"], label="tip"),
                        Variable(value=item["IC"], label="IC"),
                        Variable(value=item["friction"], label="friction"),
                    ],
                )
            )
        resistivity_list = []
        for name, item in resistivity.items():
            location = Geometry(x=item["coordinates"][0], y=item["coordinates"][1], z=0)
            resistivity_list.append(
                Data(
                    location=location,
                    independent_variable=Variable(value=item["NAP"], label="NAP"),
                    variables=[
                        Variable(value=item["resistivity"], label="resistivity")
                    ],
                )
            )
        insar_list = []
        for counter, coordinates in enumerate(insar["coordinates"]):
            location = Geometry(x=coordinates[0], y=coordinates[1], z=0)
            insar_list.append(
                Data(
                    location=location,
                    independent_variable=Variable(value=insar["time"], label="time"),
                    variables=[
                        Variable(
                            value=insar["displacement"][counter], label="displacement"
                        )
                    ],
                )
            )
        create_features = CreateInputsML()
        aggregated_features = create_features.find_closer_points(
            input_data=cpts_list,
            combined_data=insar_list,
            aggregate_method=AggregateMethod.SUM,
            interpolate_on_independent_variable=False,
            aggregate_variable="displacement",
            number_of_points=10,
        )
        aggregated_features = create_features.find_closer_points(
            input_data=aggregated_features,
            combined_data=resistivity_list,
            aggregate_method=AggregateMethod.MEAN,
            aggregate_variable="resistivity",
            interpolate_on_independent_variable=True,
            number_of_points=10,
        )
        assert len(aggregated_features) != 0
        for aggregated_feature in aggregated_features:
            create_features.add_features(
                aggregated_feature,
                ["tip", "displacement", "resistivity"],
                use_independent_variable=True,
                use_location_as_input=(True, True, False),
            )
            create_features.add_targets(aggregated_feature, ["IC"])
        create_features.split_train_test_data()
        training_data = create_features.get_features_train(flatten=False)
        target_data = create_features.get_targets_train(flatten=False)
        validation_training = create_features.get_features_test(flatten=False)
        validation_target = create_features.get_targets_test(flatten=False)
        return training_data, target_data, validation_training, validation_target, create_features.get_feature_names()
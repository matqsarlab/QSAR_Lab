#!/usr/bin/env python3.11

from QSAR_Lab.Misvik_Bayeas_model.models import CoreModel


class Selector(CoreModel):
    def __init__(self, model, train, test, toxic, perm_num=2) -> None:
        super().__init__(model, train, test, toxic, perm_num)
        self.__allNMs = (
            train.index.tolist() + test.index.tolist() + toxic.index.tolist()
        )

    def create_data_set(self):
        c = 1
        datasets = {}

        for name in self.__allNMs:
            train_c = self.train.copy()
            test_c = self.test.copy()
            toxic_c = self.toxic.copy()

            if name in self.train.index:
                external = train_c.loc[name]
                train_c.drop(name, inplace=True)
                datasets[f"set_{c}"] = (train_c, test_c, toxic_c, external)
            elif name in self.test.index:
                external = test_c.loc[name]
                test_c.drop(name, inplace=True)
                datasets[f"set_{c}"] = (train_c, test_c, toxic_c, external)
            else:
                external = toxic_c.loc[name]
                toxic_c.drop(name, inplace=True)
                datasets[f"set_{c}"] = (train_c, test_c, toxic_c, external)
            c += 1
        return datasets

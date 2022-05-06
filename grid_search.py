import itertools
import time
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_predict
from QSAR_Lab.smogn_maker import synth_smoth
from QSAR_Lab.spliter import split_x_to_n
from sklearn.ensemble import AdaBoostRegressor


def adbr():
    """
    AdaBoostRegressor - method with random creator hyperparameters
    """
    rs = np.random.randint(0, 1000)
    n_est = np.random.randint(1, 100)
    lr = np.random.uniform(0.1, 2)
    return AdaBoostRegressor(random_state=rs, n_estimators=n_est, learning_rate=lr)



class Modeling:
    """
        @ Metoda 'modeling', przyjmuje zbiory X_train/test, y_train/test oraz liczbe deskryptorow

        @ Wymagana jest lista z instancjami modeli

        @ Liczba deskrytporow definiuje ilu elementowy zbior ma powstac ze zbioru pierwotnego
          Oznacza to, ze jezeli pierwotne dane zawieraly N deskryptorow to po przez kombinacje
          bez powtorzen powstanie S n-elementowych zbiorow z n deskryptorami

                 Data = 10 deskrytporow
               + n = 3
                --------------------------
               = 120 zbiorow 3-elementowych 

        @ Metoda 'save' sluzy do zapisywania. przyjmuje nastepujace argumenty:
          
          * output = "nazwa pliku bez rozszerzenia"
          * sort_by = "nazwa kolumny po ktorej maja byc sortowane wartosci"

      """

    def __init__(self, X, y, n_desc):
        self.n = n_desc
        self.X = X
        self.y = y
        self.table = pd.DataFrame()

    def __comb__(self, n, descriptors=None):

        """
        Create all n-elemental combinations of descriptors
        """

        if descriptors ==  None:
            descriptors = self.X.columns
            descriptors = descriptors[1:]
        else:
            descriptors = self.X[descriptors]

        comb = itertools.combinations(descriptors, n)
        X_copy = self.X.copy()
        y_ = self.y.copy()

        for c in comb:
            X_ = X_copy[list(c)]
            data = pd.concat([X_, y_], axis=1)
            yield data

    def save(self, output="output", **kwargs):
        """
          * output = "nazwa pliku bez rozszerzenia"
          * sort_by = "nazwa kolumny po ktorej maja byc sortowane wartosci"
        """

        if kwargs:
            self.table.sort_values(by=kwargs["sort_by"], inplace=True, ascending=False)


        return self.table.to_excel(f"{output}.xlsx")

    def modeling(self, models, logfile="log", delta_time=1., descriptors=None, const_descr=None):
        """
        models: List with names of methods
                * AdaBoostRegressor

        logfile: Name of logfile
        delta_time: Process time [h]
        descriptors: List with interesting descriptors name 
        const_descr: Constantly descriptors which we want to use in model
        smogn_number: Amount of smogn set 
        rel_coef: See in SMOGN documentation
        """

        models_ = models                                            # List with models
        desc_gen = self.__comb__(self.n, descriptors)               # Generator with all combinations of Descriptors 
        desc_gen = itertools.cycle(desc_gen)

        r2_train_ = []
        r2_test_ = []
        cv_r2_ = []
        set_= []
        metoda = []
        counter = 0

        dict_model = {"AdaBoostRegressor": adbr}   # Dict with machine-learning methods

        ## Timer
        open(f"{logfile}.log", "w").close()     # Create new *.log file

        pt = 0                                  # Timer set on 0
        while pt/3600 < delta_time:             # Statment: process_time[h] < delta time[h]
            pt = time.process_time()            # Process time start

            result = []

            data = next(desc_gen)

            if const_descr:
                data = pd.concat([data, self.X[const_descr]],axis=1)

            result.append(data)

            data = pd.concat(result)
            data.dropna(axis=1, inplace=True)
            data.drop_duplicates(inplace=True)
            data.sort_values(by=[self.y.name], axis=0, inplace=True)

            ## Create X, y variables
            y_ = data[self.y.name]
            X_ = data.drop(self.y.name, axis=1)
            
            # Spliter
            X_train, X_test, y_train, y_test = split_x_to_n(X_, y_)

            # Standard Scaler
            scaler = StandardScaler()
            scaler.fit(X_train)
            X_train = pd.DataFrame(
                scaler.transform(X_train), index=X_train.index, columns=X_train.columns
            )
            X_test = pd.DataFrame(
                scaler.transform(X_test), index=X_test.index, columns=X_test.columns
            )

            for m_ in models_:
                model = dict_model[m_]()
                model.fit(X_train, y_train)

                r2_train = model.score(X_train, y_train)
                r2_test = model.score(X_test, y_test)

                cv_train = cross_val_predict(estimator=model, X=X_train, y=y_train, cv=len(X_train))
                cv_train_r2 = r2_score(y_train, cv_train)

                # Model score
                if r2_train > -0.6 and r2_train <= 0.99 and r2_test > -0.6 and cv_train_r2 >  -0.5:

                    r2_train_.append(r2_train)
                    r2_test_.append(r2_test)
                    cv_r2_.append(cv_train_r2)
                    set_.append(list(X_train.columns))
                    metoda.append(model)

                    with open(f"{logfile}.log", "a") as f:
                        f.write(str(model)+"\n")
                        f.write(str(r2_train)+"\n")
                        f.write(str(r2_test)+"\n")
                        f.write(str(cv_train_r2)+"\n")
                        f.write(str(X_train.columns)+"\n")
                        f.write(str(data)+"\n")
                        f.write("-- "*25 + "\n")

                    data.to_excel(f"{logfile}_data-{counter}.xlsx")
                    counter += 1

        d = {'method': metoda, 'R^2': r2_train_, 'Q^2': r2_test_, 'CV':cv_r2_, 'descriptors': set_}
        d = pd.DataFrame(d)

        self.table = d.copy()
        return d



## ----------------- Modeling_and_SMOGN Class -------------------------
class Modeling_with_SMOGN:
    """
        @ Metoda 'modeling', przyjmuje zbiory X_train/test, y_train/test oraz liczbe deskryptorow

        @ Wymagana jest lista z instancjami modeli

        @ Liczba deskrytporow definiuje ilu elementowy zbior ma powstac ze zbioru pierwotnego
          Oznacza to, ze jezeli pierwotne dane zawieraly N deskryptorow to po przez kombinacje
          bez powtorzen powstanie S n-elementowych zbiorow z n deskryptorami

                 Data = 10 deskrytporow
               + n = 3
                --------------------------
               = 120 zbiorow 3-elementowych 

        @ Metoda 'save' sluzy do zapisywania. przyjmuje nastepujace argumenty:
          
          * output = "nazwa pliku bez rozszerzenia"
          * sort_by = "nazwa kolumny po ktorej maja byc sortowane wartosci"

      """

    def __init__(self, X, y, n_desc):
        self.n = n_desc
        self.X = X
        self.y = y
        self.table = pd.DataFrame()

    def __comb__(self, n, descriptors=None):

        """
        Create all n-elemental combinations of descriptors
        """

        if descriptors ==  None:
            descriptors = self.X.columns
            descriptors = descriptors[1:]
        else:
            descriptors = self.X[descriptors]

        comb = itertools.combinations(descriptors, n)
        X_copy = self.X.copy()
        y_ = self.y.copy()

        for c in comb:
            X_ = X_copy[list(c)]
            data = pd.concat([X_, y_], axis=1)
            yield data

    def save(self, output="output", **kwargs):
        """
          * output = "nazwa pliku bez rozszerzenia"
          * sort_by = "nazwa kolumny po ktorej maja byc sortowane wartosci"
        """

        if kwargs:
            self.table.sort_values(by=kwargs["sort_by"], inplace=True, ascending=False)


        return self.table.to_excel(f"{output}.xlsx")

    def modeling_smogn(self, models, logfile="log", delta_time=1., descriptors=None, const_descr=None, smogn_number=1, rel_coef=1.5):
        """
        models: List with names of methods
                * AdaBoostRegressor

        logfile: Name of logfile
        delta_time: Process time [h]
        descriptors: List with interesting descriptors name 
        const_descr: Constans descriptors which we want use in model
        smogn_number: Amount of smogn set 
        rel_coef: See in SMOGN documentation
        """

        models_ = models                                            # List with models
        desc_gen = self.__comb__(self.n, descriptors)               # Generator with all combinations of Descriptors 
        desc_gen = itertools.cycle(desc_gen)

        r2_train_ = []
        r2_test_ = []
        cv_r2_ = []
        set_= []
        metoda = []
        counter = 0

        dict_model = {"AdaBoostRegressor": adbr}   # Dict with machine-learning methods

        ## Timer
        open(f"{logfile}.log", "w").close()     # Create new *.log file

        pt = 0                                  # Timer set on 0
        while pt/3600 < delta_time:             # Statment: process_time[h] < delta time[h]
            pt = time.process_time()            # Process time start

            smogn_set = []
            result = []
            for i in range(smogn_number):
                sm = synth_smoth(self.X, self.y.name, rel_coef=rel_coef)
                smogn_set.append(sm)

            data = next(desc_gen)

            if const_descr:
                data = pd.concat([data, self.X[const_descr]],axis=1)

            result.append(data)

            for i in smogn_set:
                result.append(i)

            data = pd.concat(result)
            data.dropna(axis=1, inplace=True)
            data.drop_duplicates(inplace=True)
            data.sort_values(by=[self.y.name], axis=0, inplace=True)

            ## Create X, y variables
            y_ = data[self.y.name]
            X_ = data.drop(self.y.name, axis=1)
            
            # Spliter
            X_train, X_test, y_train, y_test = split_x_to_n(X_, y_)

            # Standard Scaler
            scaler = StandardScaler()
            scaler.fit(X_train)
            X_train = pd.DataFrame(
                scaler.transform(X_train), index=X_train.index, columns=X_train.columns
            )
            X_test = pd.DataFrame(
                scaler.transform(X_test), index=X_test.index, columns=X_test.columns
            )

            for m_ in models_:
                model = dict_model[m_]()
                model.fit(X_train, y_train)

                r2_train = model.score(X_train, y_train)
                r2_test = model.score(X_test, y_test)

                cv_train = cross_val_predict(estimator=model, X=X_train, y=y_train, cv=len(X_train))
                cv_train_r2 = r2_score(y_train, cv_train)

                # Model score
                if r2_train > -0.6 and r2_train <= 0.99 and r2_test > -0.6 and cv_train_r2 >  -0.5:

                    r2_train_.append(r2_train)
                    r2_test_.append(r2_test)
                    cv_r2_.append(cv_train_r2)
                    set_.append(list(X_train.columns))
                    metoda.append(model)

                    with open(f"{logfile}.log", "a") as f:
                        f.write(str(model)+"\n")
                        f.write(str(r2_train)+"\n")
                        f.write(str(r2_test)+"\n")
                        f.write(str(cv_train_r2)+"\n")
                        f.write(str(X_train.columns)+"\n")
                        f.write(str(data)+"\n")
                        f.write("-- "*25 + "\n")

                    data.to_excel(f"{logfile}_data-{counter}.xlsx")
                    counter += 1

        d = {'method': metoda, 'R^2': r2_train_, 'Q^2': r2_test_, 'CV':cv_r2_, 'descriptors': set_}
        d = pd.DataFrame(d)

        self.table = d.copy()
        return d



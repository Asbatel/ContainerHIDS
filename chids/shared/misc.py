import itertools
import os
from pathlib import Path
import pickle
import numpy as np
from chids.shared.constants import *
from rich.console import Console



def _format_input(inputs, TRAINING_MODE=True):

    if TRAINING_MODE:
        inputs = list(itertools.chain.from_iterable(inputs))

    inputs = [x for x in inputs if x]
    ready_anomaly_vectors = np.array(inputs)
    return ready_anomaly_vectors

def save_file(training_elements, model, output_folder):
    console = Console()

    try:
        path = os.getcwd() + "/" + output_folder
        if not Path(path).is_dir():
            os.mkdir(os.getcwd() + "/" + output_folder)

        model.save(path+'/'+'model.h5')
        console.print('model' + ' -------->  saved successfully in {}'.format(output_folder), style='green bold')

        for _, ele in enumerate(training_elements):
            with open(output_folder + "/" + OUTPUT_FILES_NAMES[_] + ".pkl", 'wb') as f:
                pickle.dump(ele, f)

            console.print(OUTPUT_FILES_NAMES[_] + ' -------->  saved successfully in {}'.format(output_folder), style='green bold')


    except OSError:
        print("Creation of the directory %s failed" % os.getcwd())


def prepare_scaps(scaps_dir):
    scaps = []
    for scap in os.listdir(scaps_dir):
        scaps.append(''.join(os.path.join(scaps_dir, scap)))
    return scaps


def load_pickled_file(file):
    with open(file, 'rb') as f:
        output = pickle.load(f)
    return output

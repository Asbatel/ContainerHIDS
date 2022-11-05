from baseline import Baseline
import typer
from rich import print
from rich.table import Table
from rich.console import Console

from chids.conf.config import *
from chids.shared.constants import *
from chids.ML.test_model import Testing
from chids.utils.anomaly_vector import AnomalyVector
from chids.shared.misc import *

console = Console()
app = typer.Typer(pretty_exceptions_short=False)

@app.command()
def evaluate(seen_syscalls: str = typer.Option(..., "--ss"), seen_args:str  = typer.Option(..., "--sa"), freq_max:str = typer.Option(..., "--fm"),
             trained_model:str=typer.Option(..., "--tm"), thresh_list:str = typer.Option(..., "--tl"), normal_dir:str=typer.Option(..., "--ns"),
             exploit_dir:str=typer.Option(..., "--ms")):
    console.print(EVALUATION_INITIALIZER, style=STYLE, soft_wrap=False)

    detection_rate = []
    false_positive_rate = []

    results_normal_scaps = _get_evaluation_results(normal_dir, seen_syscalls, seen_args, freq_max, trained_model, thresh_list)
    results_exploit_scaps = _get_evaluation_results(exploit_dir, seen_syscalls, seen_args, freq_max, trained_model, thresh_list)

    for _, i in enumerate(zip(*results_normal_scaps)):
        false_positive_rate.append(i.count(True)/len(i))

    for _, i in enumerate(zip(*results_exploit_scaps)):
        detection_rate.append(i.count(True)/len(i))

    _print_results(detection_rate, false_positive_rate)



@app.command()
def baseline(input_dir_path: str = typer.Option(..., "--td"), output_dir_name: str = typer.Option(..., "--od")):
    console.print(TRAINING_INITIALIZER, style=STYLE, soft_wrap=False)
    scaps = prepare_scaps(input_dir_path)
    seen_syscalls, seen_args, max_freq, model, thresh_list = Baseline(scaps).get_training_elements()

    output_table = Table(title=TRAINING_HEADERS)
    output_table.add_column("Number of training scaps", style="magenta")
    output_table.add_column("previously seen syscalls", style="magenta")
    output_table.add_column("previously seen arguments", style="magenta")
    output_table.add_column("Thresholds", style="magenta")
    output_table.add_row(str(len(scaps)), str(seen_syscalls)[1:-1], str(seen_args)[1:-1], str(thresh_list)[1:-1])

    print(output_table)
    save_file([seen_syscalls, seen_args, max_freq, thresh_list], model, output_dir_name)


def _get_evaluation_results(_dir, seen_syscalls, seen_args, freq_max, trained_model, thresh_list):
    seen_syscalls = load_pickled_file(seen_syscalls)
    seen_args = load_pickled_file(seen_args)
    freq_max = load_pickled_file(freq_max)
    thresh_list = load_pickled_file(thresh_list)

    scaps = prepare_scaps(_dir)
    baseline_obj = Baseline(scaps)
    scaps_dfs = baseline_obj._scaps_to_dfs()
    traces = baseline_obj._get_scaps_traces(scaps_dfs)
    scaps_anomaly_vectors = AnomalyVector(traces, seen_syscalls, seen_args, freq_max).get_anomaly_vectors()
    results = Testing(trained_model, thresh_list).get_classifications(scaps_anomaly_vectors)

    return results

def _print_results(detection_rate, false_positive_rate):
    output_table = Table(title=EVALUATION_HEADER)
    output_table.add_column("Theta", style="magenta")
    output_table.add_column("Detection Rate", style="magenta")
    output_table.add_column("False Alarm Rate", style="magenta")

    zipped_result = zip(THETA_VALUES, detection_rate, false_positive_rate)

    for i in zipped_result:
        output_table.add_row(str(i[0]), str(i[1]), str(i[2]))

    print(output_table)





if __name__== "__main__" :
    app()
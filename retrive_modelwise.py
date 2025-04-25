import os
import json

from collections import defaultdict
import argparse

def wrap(d,name='parameters'):
        return {name: d}
    
def retrive_main():
    models = ["mlp", "resnet", "transformer"]
    suffix = ["-l", "-lr", "-t", "-t-l", "-t-lr", "-lrlr", "-t-lrlr"]

    best_params = defaultdict(dict)
    merged_params = defaultdict(dict)

    for basemodel in models:
        for suf in suffix:
            model = basemodel + suf
            model_path = os.path.join("exp", model)
            if os.path.isdir(model_path):
                for dataset in os.listdir(model_path):
                    print("Processing dataset.model:", dataset, model_path)
                    dataset_path = os.path.join(model_path, dataset)
                    report_file_path = os.path.join(dataset_path, "0_evaluation", "0", "report.json")
                    if os.path.isfile(report_file_path):
                        with open(report_file_path, "r") as report_file:
                            report_data = json.load(report_file)
                            if "config" in report_data and "model" in report_data["config"]:
                                best_params[dataset][model] = report_data["config"]["model"][basemodel]
                                best_params[dataset][model]['num_bins'] = report_data["config"]["model"]["d_num_embedding"]
                                best_params[dataset][model]['learning_rate'] = report_data["config"]["training"]["lr"]
                    

    output_file_raw = "rtdl_best_params_modelwise.json"
    with open(output_file_raw, "w") as f:
        json.dump(wrap(best_params), f, indent=4)

        
if __name__ == "__main__":
    retrive_main()


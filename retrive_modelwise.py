import os
import json

from collections import defaultdict
import argparse

def wrap(d,name='parameters'):
        return {name: d}
    
def retrive_main():
    models = ["mlp", "resnet"] #, "transformer"]
    suffix = ["", "-lr", "-t", "-t-lr", "-lrlr", "-t-lrlr"]

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
                    
                    if suf == "":
                        merged_params[dataset][basemodel] = best_params[dataset][basemodel]
                        merged_params[dataset][basemodel]['num_bins'] = {}
                    elif suf == "-lr" or suf == "-t-lr" or suf == "-lrlr" or suf == "-t-lrlr":
                        merged_params[dataset][basemodel]['num_bins'][suf] = best_params[dataset][model]['num_bins']
                    else:
                        pass


    output_file_raw = "rtdl_best_params_raw.json"
    output_file = "rtdl_best_params.json"
    output_sample = "rtdl_best_params_sample.json"
    with open(output_file_raw, "w") as f:
        json.dump(wrap(best_params), f, indent=4)
    with open(output_file, "w") as f:
        json.dump(wrap(merged_params), f, indent=4)
    with open(output_sample, "w") as f:
        json.dump(wrap(wrap(best_params['gesture'],'gesture')), f, indent=4)

        
if __name__ == "__main__":
    retrive_main()


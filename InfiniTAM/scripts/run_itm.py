import sys
from _run import * 
from systemsettings import *
from datasets import *
import numpy as np 
from subprocess import call

class InfiniTAM(SLAMAlgorithm):

    def __init__(self, bin_path):
        SLAMAlgorithm.__init__(self, bin_path)

        #self.ate_remove_offset = True
        #self.ate_align = True

    def reset_evaluation(self):
        pass

    def _calculate_ate_for_scale(self):
        self.evalATE.calculate_for_scale()

    def _setup_from_dataset(self, dataset):
        if dataset.quat:
            self.quat = dataset.quat

        if dataset.init_pose:
            self.init_pose = dataset.init_pose

        self.camera = dataset.camera
        #self.ate_associate_identity = dataset.ate_associate_identity

    def _generate_run_command(self, camera_calib_path, dataset_path, results_path):
        rgb = dataset_path + 'rgb_qvga_ppm/%04i.ppm'
        depth = dataset_path + 'depth_qvga_pgm/%04i.pgm'
        call(["touch", results_path])
        arguments = '{} {} {} 2> {}'.format(str(dataset_path + "calib_half.txt"), rgb, depth, results_path) 
        return self.bin_path + 'Apps/InfiniTAM_cli/InfiniTAM_cli ' + arguments

    def _store_variables(self, res):

        return res


results_dir = gen_results_dir(RESULTS_PATH)
algorithm = InfiniTAM(BIN_PATH)
algorithm.ate_associate_identity = False
algorithm.ate_remove_offset = False
algorithm.ate_align = True

run_results = {}
# for mu in [0.1, 0.05]:
run_counter = 0
for sequence in [TUM_RGB_FR2_DESK, TUM_RGB_FR3_DESK]:
    kernel_data = []
    res = algorithm.run(sequence)
    res['sequence'] = sequence.descr
    res['noise_factor'] = 0.075
    run_results[run_counter] = res
    run_counter += 1
    kernel_data.append(res)
print run_results 


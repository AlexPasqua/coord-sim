import argparse
import simpy
import random
from coordsim.simulation.flowsimulator import FlowSimulator
from coordsim.reader import networkreader
from coordsim.metrics import metrics
import coordsim.network.scheduler as scheduler
from coordsim.simulation.simulatorparams import SimulatorParams
import logging
import time
log = logging.getLogger(__name__)


def main():
    # Initialize logger

    args = parse_args()
    metrics.reset()
    start_time = time.time()
    logging.basicConfig(level=logging.INFO)
    # Create a SimPy environment
    env = simpy.Environment()
    # Initialize environment (random seed and simpy.)
    seed = args.seed
    random.seed(seed)

    network = networkreader.read_network(args.network, node_cap=10, link_cap=10)

    # Getting current placement of VNF's
    sf_placement, sfc_list, sf_list = networkreader.network_update(args.placement, network)
    log.info("Total of {} nodes have VNF's placed in them\n".format(len(sf_placement)))

    # Obtain flow datarate and size params
    flow_dr_mean = args.flow_dr_mean
    flow_dr_stdev = args.flow_dr_stdev
    flow_size_shape = args.flow_size_shape

    # Obtain flow inter arrival mean
    inter_arr_mean = args.inter_arr_mean

    schedule = scheduler.flow_schedule()
    # Simulation duration
    duration = args.duration
    params = SimulatorParams(network, sf_placement, sfc_list, sf_list, seed, schedule, inter_arr_mean=inter_arr_mean,
                             flow_dr_mean=flow_dr_mean, flow_dr_stdev=flow_dr_stdev, flow_size_shape=flow_size_shape)
    simulator = FlowSimulator(env, params)
    simulator.start_simulator()
    env.run(until=duration)
    end_time = time.time()
    metrics.running_time(start_time, end_time)


def parse_args():
    default_seed = 9999
    # Read CLI arguments
    parser = argparse.ArgumentParser(description="Coordination-Simulation tool")
    parser.add_argument('-d', '--duration', required=True, default=None, dest="duration", type=int)
    parser.add_argument('-r', '--rate', required=False, default=None, dest="rate")
    parser.add_argument('-s', '--seed', required=False, default=default_seed, dest="seed", type=int)
    parser.add_argument('-n', '--network', required=True, dest='network')
    parser.add_argument('-iam', '--inter_arr_mean', required=False, default=1.0, dest="inter_arr_mean", type=float)
    parser.add_argument('-p', '--placement', required=True, default=None, dest="placement")
    parser.add_argument('-fdm', '--flow_dr_mean', required=False, default=1.0, dest="flow_dr_mean", type=float)
    parser.add_argument('-fds', '--flow_dr_stdev', required=False, default=1.0, dest="flow_dr_stdev", type=float)
    parser.add_argument('-fss', '--flow_size_shape', required=False, default=1.0, dest="flow_size_shape", type=float)
    return parser.parse_args()


if __name__ == '__main__':
    main()
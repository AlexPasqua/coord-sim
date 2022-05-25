# Summary of main characteristics

## Conceptual characteristics
- **Discrete**-event **flow-based** simulator
- Relatively close to reality accuracy
- <u>Simulator's params can be changed **mid-simulation**</u> (by the calling coordination algorithm)

## Implementation details
- Python3.6
- Based on **SymPy**
### Modules:
Location: `src/coordsim/`
- **Simulation module:** contains
  - **FlowSimulator:** main simulator (imports and utilizes other modules)
  - **SimulatorParams:** class used to hold the simulator's parameters, that can be changed mid-simulation
- **Network module:** contains FLow descriptor class holding the properties of the flow (e.g. data rate)
- **Reader module:** parses YAML (for SFs/SFCs) and GraphML (for the network) files
- **Simulation module:** main flow simulator

## Operation flow
The user (coordination algorithm or CLI) provides 2 inputs:
- network file (GraphML): contains network's nodes and edges
- VNF file (YAML): includes the list of SFCs and the list of SFs under each SFC in an ordered manner
### Procedure:
1. **Parsing and start:**
   - GraphML and YAML files are parsed producing:
     - NetworkX obj containing list of nodes and edges
     - Dicts containing SFCs and SF
     - List of ingress nodes
     - This params are passed to a SimulatorParams obj
   - **Start:** calling `start()` in FLowSimulator obj
2. At each ingress node, the function `generate_flow()` is called
3. Once the flow is generated, `init_flow()` initializes the handling of the flow within the simulator
4. In `process_flow()`, the processing delay for that particular SF is generated (given mean a std dev of a normal distribution taken from the YAML file)
    - The simulator checks then node's remaining capacity
      - If there isn't enough capacity, the flow is dropped
5. Once the flow was processed completely at each SF, depart_flow() is called to register the flow’s departure from the network
    - If the flow still has other SFs to be processed at in the network, process_flow() calls pass_flow() again in a mutually recursive manner. This allows the flow to stay in the SF for processing, while the parts of the flow that were processed already to be sent to the next SF.
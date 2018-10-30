import networkx as nx


class GraphHandler:
    """
        This class is used for graph handling operations only
    """
    def get_trace_graph(self, th, traces):
            
        trace_graph = {}

        for trace in traces:
            # th is available as an injected dependency
            utc_timestamp = th.convert_to_utc(trace['time'])

            # Check if Graph present
            if trace['trace_id'] in trace_graph:
                # Since the graph already exists, Use the existing object
                dgObj = trace_graph[trace['trace_id']]

                # Check if the node does not exists
                if trace['span_id'] not in dgObj.nodes:
                    dgObj.add_node(trace['span_id'])
                    dgObj.node[trace['span_id']]['node'] = False

                dgObj.add_node(utc_timestamp)
                dgObj.node[utc_timestamp]['app'] = trace['app']
                dgObj.node[utc_timestamp]['component'] = trace['component']
                dgObj.node[utc_timestamp]['msg'] = trace['msg']
                dgObj.node[utc_timestamp]['time'] = trace['time']

                # Link this created follower node and the main node
                dgObj.add_edge(utc_timestamp, trace['span_id'], weight=utc_timestamp)

                # Does this span has a parent?
                if 'parent_span_id' in trace:
                    # Is the parent node already present
                    if trace['parent_span_id'] in dgObj.nodes:
                        # Update the edge/link between this main node and its parent node
                        # with least utc_timestamp value, so as to sort
                        edge = dgObj.get_edge_data(trace['span_id'], trace['parent_span_id'])
                        if edge is not None:
                            if utc_timestamp < edge['weight']:
                                dgObj.add_edge(trace['span_id'], trace['parent_span_id'], weight=utc_timestamp)
                        else:
                            # Edge does not exist, so create it
                            dgObj.add_edge(trace['span_id'], trace['parent_span_id'], weight=utc_timestamp)
                    else:
                        # Need to create a parent node
                        dgObj.add_node(trace['parent_span_id'])
                        dgObj.node[trace['parent_span_id']]['is_parent'] = True
                        dgObj.node[trace['parent_span_id']]['node'] = False
                        dgObj.add_edge(trace['span_id'], trace['parent_span_id'], weight=utc_timestamp)

                    # Since this has a parent then this is a child
                    dgObj.node[utc_timestamp]['is_child'] = True

                # We might have encountered the last node for a trace
                if 'error' in trace:
                    dgObj.graph['failed'] = trace['error']

            else:
                # The very beginning of Graph creation
                # We will reuse this object only per trace
                dg = nx.DiGraph()

                # We have encountered the child node first.
                # So create the parent node first and then the child
                if 'parent_span_id' in trace:
                    dg.add_node(trace['parent_span_id'])
                    dg.node[trace['parent_span_id']]['is_parent'] = True
                    dg.node[trace['parent_span_id']]['node'] = False

                dg.add_node(trace['span_id'])
                dg.node[trace['span_id']]['node'] = False

                dg.add_node(utc_timestamp)
                dg.node[utc_timestamp]['app'] = trace['app']
                dg.node[utc_timestamp]['component'] = trace['component']
                dg.node[utc_timestamp]['msg'] = trace['msg']
                dg.node[utc_timestamp]['time'] = trace['time']
                dg.add_edge(utc_timestamp, trace['span_id'], weight=utc_timestamp)

                # Make sure to link the child to the parent
                if 'parent_span_id' in trace:
                    # Add the parent span id property
                    dg.node[trace['span_id']]['parent_span_id'] = trace['parent_span_id']
                    # Now connect the child with the parent
                    dg.add_edge(trace['span_id'], trace['parent_span_id'], weight=utc_timestamp)
                    # Since this has a parent then this is a child
                    dg.node[utc_timestamp]['is_child'] = True

                # We might have encountered the last node for a trace
                if 'error' in trace:
                    dg.graph['failed'] = trace['error']

                trace_graph[trace['trace_id']] = dg

        return trace_graph
        
    def print_trace_graph(self, trace_graph):
            
        if trace_graph is not None:
            i = 0
            for trace_id in trace_graph:
                dg = trace_graph[trace_id]
                if 'failed' in dg.graph and dg.graph['failed'] is True:
                    i = i + 1
                    sorted_nodes = list(nx.lexicographical_topological_sort(dg))
                    all_node_data = dg.nodes.data()
                    for node in sorted_nodes:
                        if 'node' not in all_node_data[node]:
                            print('\n')
                            if 'is_child' in all_node_data[node]:
                                print("     - " + all_node_data[node]['time'] + " " + all_node_data[node]['app'] + " "
                                        + all_node_data[node]['component'] + "" + all_node_data[node]['msg'])
                            else:
                                print("- " + all_node_data[node]['time'] + " " + all_node_data[node]['app'] + " "
                                        + all_node_data[node]['component'] + "" + all_node_data[node]['msg'])

            print('\nTotal failed traces: ', i)
        else:
            raise ValueError

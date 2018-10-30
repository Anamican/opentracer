from handlers.file_handler import FileHandler
from handlers.time_handler import TimeHandler
from handlers.graph_handler import GraphHandler

file_path = 'log-data.json'
fh = FileHandler(file_path)
traces = fh.get_file_contents()

th = TimeHandler()
gh = GraphHandler()

# Inject the dependency of TimeHandler
trace_graph = gh.get_trace_graph(th, traces)
gh.print_trace_graph(trace_graph)

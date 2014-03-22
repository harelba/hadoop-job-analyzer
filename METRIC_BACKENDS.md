## Metric backend plugins
The tool uses a simple plugin mechanism for the metric backend access. A metric backend plugin is just a python module called `hja-<metric-backend-id>.py`, which should implement the following functions:

* `initialize(params)` - The plugin should initialize. `params` contain a map with the parameters passed by the user using the `-P` command line parameter
* `projection_started(proj)` - Sending the metric for a specific projection has started. proj is the projection object itself, and contains metadata about the projection
* `projection_finished(proj)` - Sending the metric for a specific projection has finished
* `add_metric(proj,name,value,timestamp)` - The plugin should add the metric to the list of metrics to send (or it can just send the metric directly...). The projection object is provided here as well, along with the name, value and timestamp of the metric. The name is a string and both the value and the timestamp are floats.
* `done()` - The plugin should do its cleanup, if needed.

The stdout plugin (which resides in hja-stdout.py) can be used as an easy baseline for writing a new plugin.

`NOTE:` The interface to the metric plugins is currently an easy (metric_name,metric_value,timestamp) interface, in which the metric name is an already processed string. In the future, depending on need, a more structured interface will be created, which will allow the plugins more freedom.


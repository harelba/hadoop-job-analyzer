## Usage
### Parameters
The following parameters can be provided:

#### Analysis related parameters
* `-f` - The location of the jobtracker's `history/done` folder. Should be local or some mount to the jobtracker
* `-l` - List all available fields, possibly with sample values from actual jobs. Use -s to control the number of samples
* `-M` - When set, this job name will be analyzed as a map of key-values, separated by "||". Each key/value pair will automatically be available to other parts, as if it was part of the job's information. It will also participate in the output of the -l parameter. The parameter is not mandatory of course.
* `-S` - This can be used to change the job name key-value separator (default is ||).
* `-m` - Maximum length of job name metadata extracted using `-j`. Values longer than this value will be replaced with "toolong". This is a defense mechanism against clutter caused by non compliant job names.
* `-r` - Relaxed mode. In this mode, non compliant jobs and missing fields will not cause the analysis to stop

The `-l` flag is very useful for getting visibility regarding the available fields and their value. Use it in conjunction with `-s` which controls the number of samples to fetch for each of the available fields.

#### Aggregation related parameters
* `-p` - The required aggregations. The aggregations should be separated by a comma. Composite aggregations can be provided, separating the fields by a slash. For example, to aggregate by USER and by the combination of the source host and the job queue use "USER,SOURCE_HOST/JOB_QUEUE". Use -l to get a list of the available fields
* `-t` - The name of the field which will be used to associate a job with a certain time and to aggregate data over time. Defaults to SUBMIT_TIME, and should rarely be changed
* `-i` - The required time interval for aggregation in seconds. This is actually the size of one time bucket. Defaults to 60 - one minute. Please note that when using graphite, you can use the summarize() function in order to perform time aggregations on a per-query basis, so there is no need to change this interval at all.


#### Metric sending related parameters
* `-C` - The type of the metric client. Currently supported types are stdout and graphite. Note that graphite requires the following client parameters: server=X,port=Y.
* `-P` - Parameters to be passed to the metric client. A comma separated list of name=value pairs. For example: server=graphite.domain.com,port=2003
* `-n` - Prefix for all metrics. You can add ${HOSTNAME} in the prefix and it will be replaced with <domain>.<hostname>. For example, "data.hadoop.jobtracker.${HOSTNAME}. Please note that you'd need to use single quotes in the command line so the $ sign will not be parsed by the shell
* `-c` - This flag causes metrics to be cached locally after being sent to the metric backend. Identical metrics which are cached will not be sent again to the metric backend. This flag is useful for reducing the number of metrics being sent in large scale installations. Non-identical (updated) metrics will still be sent to the backend, so there is no risk of losing any information.


## Contact
Any feedback would be much appreciated, as well as pull requests, of course.

Harel Ben-Attia, harelba@gmail.com, @harelba on Twitter


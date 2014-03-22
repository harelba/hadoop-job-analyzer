## Examples
Please note that the basis for the examples is real job files, but they were modified a bit in order not to expose any business related data.

### Getting the list of available fields
The following example shows how to get a list of all fields which are available. The list is dynamic and is based on the actual jobs in the provided folder. In addition to providing the list of the fields, it also provides samples of the data for each field (taken from the job themselves).

		./hadoop-job-analyzer -f example-history-folder/ -l -s 2

This example analyzes the jobs in the example-history-folder folder and lists the fields which are available according to these jobs. In addition, it outputs 2 sample values for each of the fields. If `-s` is not provided, the number of samples will be 3 by default. 

Let's see partial output from this command:

		SOURCE_HOST
			--> hostB_mydomain_com
			--> hostC_mydomain_com
		FINISHED_REDUCES
			--> 52.0
			--> 4.0
		COUNTERS.FileSystemCounters.HDFS_BYTES_READ
			--> 535.0
			--> 51801816991.0
		USER
			--> diana
			--> jeniffer
		LAUNCH_LATENCY
			--> 0.176000118256
			--> 9.75900006294

Looking at this output, you can see that there is an automatic flattening of job counters (in this case the HDFS Bytes read counter). Also, there are also derived fields, in this case the LAUNCH_LATENCY, which is calculated and not part of the job's original data. 

Note that when using `-l`, no metrics are actually being sent anywhere.

### Aggregation
This example shows how to actually perform aggregations. For this example, we'll use the **stdout** metric backend type, so all the metrics would be printed to stdout.

		./hadoop-job-analyzer -f example-history-folder/ -p USER,SOURCE_HOST -n 'data.jobtracker.${HOSTNAME}' -C stdout

There are multiple things to note here in the command line:
* The history folder is the example folder we previously used. 

* The `-p` parameter is "USER,SOURCE_HOST". This means that we requested to get two views - One per user and the other per source host (submitting host name).

* The `-n` parameter defines the prefix which we want for all the metrics that are sent. Note that there's a special value ${HOSTNAME} as part of the prefix. When it is used, the tool replaces it with a <domain>.<host> structure of the current hostname (which will usually be the job tracker machine). This allows to easy handle metrics multiple job trackers on the metric backend side.

* The `-C` parameter just says that we would like to use the **stdout** metric client. The plugin for stdout just spits out all the metrics to the screen, as we'll see in a moment.

Here is some of the output written to the screen after running the command:

		...
		Metric for projection <spec=('USER',)> - name is data.jobtracker.unknown-domain.harel-laptop.USER.alex.ACTUAL_DURATION.value value is 2364.748 timestamp is 1368597540
		Metric for projection <spec=('USER',)> - name is data.jobtracker.unknown-domain.harel-laptop.USER.john.ACTUAL_DURATION.value value is 1177.502 timestamp is 1368598440
		Metric for projection <spec=('USER',)> - name is data.jobtracker.unknown-domain.harel-laptop.USER.jeniffer.ACTUAL_DURATION.value value is 1297.222 timestamp is 1368598380
		...
		Metric for projection <spec=('SOURCE_HOST',)> - name is data.jobtracker.unknown-domain.harel-laptop.SOURCE_HOST.hostA_mydomain_com.ACTUAL_DURATION.value value is 1419.047 timestamp is 1368597900
		Metric for projection <spec=('SOURCE_HOST',)> - name is data.jobtracker.unknown-domain.harel-laptop.SOURCE_HOST.hostC_mydomain_com.ACTUAL_DURATION.value value is 7071.148 timestamp is 1368597900
		Metric for projection <spec=('SOURCE_HOST',)> - name is data.jobtracker.unknown-domain.harel-laptop.SOURCE_HOST.hostB_mydomain_com.ACTUAL_DURATION.value value is 789.681 timestamp is 1368597840
		...

This is actual output from the stdout metric plugin. You can see that the `ACTUAL_DURATION` field is aggregated both on a per `USER` basis (`USER.alex`, `USER.john` etc.) and on a per `SOURCE_HOST` basis (`SOURCE_HOST.hostA`, `SOURCE_HOST.hostC` etc.). The aggregations are separate, providing two separate views of the same data. 

Another thing to look here is that the timestamps are rounded to 1 minute intervals (the default). The tool provides the time aggregation as well, in parallel to the projections (Meaning you get a multiple of "time X projection_values" for each field).

It is important to note that by default, the association of a job with a specific time is done using the `SUBMIT_TIME` field (rounding it to the 1 minute intervals). Both the time field itself and the interval can be modified using the `-t` and `-i` parameters.

And another small thing - Note the "unknown-domain.harel-laptop". This is the value that the tool has replaced instead of the `${HOSTNAME}`. In a real job tracker machine, it would provide the domain and the hostname of the job tracker.

### Sending the metrics to graphite
In this example, we'll just the metrics to graphite. The command line is similar to the one in the aggregation example (which used the **stdout** metric plugin), but now we'll use the graphite plugin.

In contrast to the stdout plugin, the graphite plugin requires parameters in order to work. Specifically, it requires the server and port of the graphite backend. We can pass parameters to the metric plugin by using the `-P` parameter:

		./hadoop-job-analyzer -f example-history-folder/ -p USER,SOURCE_HOST -n 'data.jobtracker.${HOSTNAME}' -C graphite -P server=graphite.domain.com,port=2003

Adding the `-P` parameter allows the plugin to use these parameter when initializing. Note that when running this command, no output will be written to the console (The metrics are sent to graphite).

### Extracting job metadata from the job name
The tool provides a method for treating the job name as a provider for job metadata, adding more fields to each jobs. These "fields" can then be used for aggregation, projection etc.

In order to treat the job name as metadata, use the `-M` parameter. This will cause the tool to parse the job name for a map of key-values in the format "key=value||key=value||...". key-value pairs will automatically become fields in the job (You'll be able to see them in the output of a `-l` command, aggregate by them, etc.).

Let's assume you've run the command as follows:
		./hadoop-job-analyzer -f example-history-folder/ -n 'data.jobtracker.${HOSTNAME}' -C stdout -p SERVICE,DOMAIN,MYDATA -M

Notice that the `-p` parameter (projections required) uses SERVICE and DOMAIN as if they were standard fields of the job.

Now let's assume there are job names with the following values:

	SERVICE=WWW||DOMAIN=calculationA||MYDATA=extrainfo||PRIORITY=1
	SERVICE=PQQ||DOMAIN=calculationB||MYDATA=extrainfo||PRIORITY=1
	SERVICE=PQQ||DOMAIN=calculationA||MYDATA=extrainfo||PRIORITY=2
	...
	SERVICE=PQQ||DOMAIN=calculationC||MYDATA=extrainfo||PRIORITY=1

Running the same command with the `-l` parameter would give us the following (partial) output.

		...
		SERVICE
			--> PQQ
			--> XPA
			--> WWW
		...
		DOMAIN
			--> calculationB
			--> calculationB
			--> calculationC

In order to prevent cluttering of the metric namespace, the tool enforces a limit on the maximum length of a value extracted from the job name. If the extracted value is longer than the maximum, the value will be replaced by `toolong`. The limit can be easily changed using the `-m` parameter.

## Contact
Any feedback would be much appreciated, as well as pull requests, of course.

Harel Ben-Attia, harelba@gmail.com, @harelba on Twitter


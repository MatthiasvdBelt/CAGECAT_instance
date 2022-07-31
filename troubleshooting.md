# Troubleshooting

If a job failed during execution, inspect the generated log file after filling in the job_id:
```
cat /repo/cagecat/jobs/<job_id>/logs/<job_id>.log
```
Next, you can inspect the logs of the worker processes. These workers execute the job and may show somme additional info:
```
cat /process_logs/worker-* | grep -B 50 -A 50 <job_id>
```

## Internal server errors

An error occurred in uWSGI. Inspect the uWSGI log file by
```
tail -n 100 /process_logs/uwsgi.log
```

If you changed a file (i.e. for debugging), you are required to reload all code by running
```
uwsgi --reload /tmp/uwsgi-master.pid
```

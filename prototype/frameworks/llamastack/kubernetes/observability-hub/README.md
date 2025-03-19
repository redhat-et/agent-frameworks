# Llamastack Telemetry

Follow this README to configure an observability stack in OpenShift to visualize Llamastack telemetry and vLLM metrics.

**WIP - Still TODO**

1. Add logging
2. Add vLLM Dashboards


## Hub OpenShift Operators

Operators are available from OperatorHub, or install via kustomize with the command below.

Install operators with:

```bash
oc apply --kustomize ./operators
```

### Operator descriptions

1. **Red Hat Build of OpenTelemetry**: The OpenTelemetry Collector (OTC) is provided from this operator.
Metrics and traces will be distributed from the OTC to various backends. The user-workload monitoring
prometheus instance is utilized as prometheus backend. Tempo is deployed and is the tracing backend.

2. **Tempo Operator**: Provides `TempoStack` Custom Resource. This is the backend for distributed tracing. An S3-compatible storage (Minio) is paired with Tempo.

3. **Grafana Operator**: Provides Grafana APIs including `GrafanaDashboard`, `Grafana`, and `GrafanaDataSource` that will be used to visualize telemetry.

4. **Cluster Observability Operator**: This provides PodMonitor and ServiceMonitor Custom Resources which are necessary for OpenShift user-workload
monitoring's prometheus to scrape workload metrics. Also, the COO provides UIPlugins for viewing telemetry. 

## Create PodMonitor or ServiceMonitor for any AI Workload that exposes a metrics endpoint

This is how to enable collection of user-workload metrics for any workload within OpenShift. You need to create a `PodMonitor` or a `ServiceMonitor`.
The PodMonitor will ensure all metrics from a particular pod will be scraped by the user-workload-monitoring Prometheus, and a ServiceMonitor will
scrape from any pod that runs under a particular service.

* [Example PodMonitor](./podmonitor-example.yaml)
* [Example ServiceMonitor](./servicemonitor-example.yaml)

Upon creation of either, metrics will be scraped and will be visible from the console `Observe -> Metrics` dashboards.

## Create custom resources and configurations for observability hub

Create the observablity hub namespace `observability-hub`. If a different namespace is created, be sure to update the resource yamls accordingly.

```bash
oc create ns observability-hub
```

### Tracing Backend (Tempo with Minio for S3 storage)

```bash
# edit storageclassName & secret as necessary
# secret and storage for testing only
oc apply --kustomize ./tempo
```

### OpenTelemetryCollector deployment

```bash
oc apply --kustomize ./otel-collector
```

### Metrics Backend & Grafana 

This will deploy a Grafana instance, and Prometheus & Tempo DataSources
The Grafana console is configured with `username: rhel, password: rhel`

```bash
cd grafana
./deploy-grafana.sh
```
Upon success, you can explore metrics and traces from Grafana route.

#### GrafanaDashboard to visualize cluster metrics and traces

Check out [github.com/kevchu3/openshift-4-grafana](https://github.com/kevchu3/openshift4-grafana/tree/master/dashboards/crds) for a list of
dashboards to deploy on OpenShift.

Here's an example to download and deploy a GrafanaDashboard for OpenShift 4.16 cluster metrics.
The dashboard is slightly modified from https://github.com/kevchu3/openshift4-grafana/blob/master/dashboards/json_raw/cluster_metrics.ocp416.json

```bash
oc apply -n observability-hub -f cluster-metrics-dashboard/cluster-metrics.yaml 
```

### Cluster Observability Operator Tracing UIPlugin

The Jaeger frontend feature of TempoStack is no longer supported by Red Hat. This has been replaced by the COO UIPlugin. To create the UIPlugin for
Tracing, first ensure the TempoStack described above is created. This is a prerequisite. Then, all that's necessary to view traces from
the OpenShift console at `Observe -> Traces` is to create the following [Tracing UIPlugin resource](./tracing-ui-plugin.yaml). 

```bash
oc apply ./tracing-ui-plugin.yaml
```

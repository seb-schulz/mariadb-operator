{{/*
Expand the name of the chart.
*/}}
{{- define "mariadb.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "mariadb.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "mariadb.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "mariadb.labels" -}}
helm.sh/chart: {{ include "mariadb.chart" . }}
{{ include "mariadb.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "mariadb.selectorLabels" -}}
app.kubernetes.io/name: {{ include "mariadb.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "mariadb.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "mariadb.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the cluster role to use
*/}}
{{- define "mariadb.clusterRoleName" -}}
{{- default (include "mariadb.fullname" .) .Values.clusterRole.name }}
{{- end }}

{{/*
Create the name of the cluster role bind to use
*/}}
{{- define "mariadb.ClusterRoleBindingName" -}}
{{- default (include "mariadb.fullname" .) .Values.ClusterRoleBindingName }}
{{- end }}

{{/*
Create image of containers.
*/}}
{{- define "mariadb.image" -}}
{{- $cur := first . -}}
{{- $appVersion := last . -}}
{{- if $cur.imageOverride -}}
{{- $cur.imageOverride }}
{{- else }}
{{- $cur.image.repository }}{{ ":" }}{{ $cur.image.tag | default $appVersion }}
{{- end }}
{{- end }}

{{/*
Create the name of the persistent volume claim to use
*/}}
{{- define "mariadb.persistentVolumeClaimName" -}}
{{- default (include "mariadb.fullname" .) .Values.persistentVolumeClaim.name }}
{{- end }}

{{/*
Create the name of the persistent volume claim to use
*/}}
{{- define "mariadb.secretName" -}}
{{- default (include "mariadb.fullname" .) .Values.secret.name }}
{{- end }}

{{/*
Create/generate the password
*/}}
{{- define "mariadb.secretPassword" -}}
{{- $cur := first . -}}
{{- $passwd := last . -}}
{{- $len := default 32 $cur.Values.secret.randPassworkdLength|int -}}
{{- default $passwd (randAlphaNum $len) | b64enc | quote }}
{{- end }}
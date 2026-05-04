{{/*
Standard helpers for the HopeUp chart.
*/}}

{{- define "hopeup.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "hopeup.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "hopeup.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels applied to every resource.
*/}}
{{- define "hopeup.labels" -}}
helm.sh/chart: {{ include "hopeup.chart" . }}
{{ include "hopeup.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: hopeup
{{- end -}}

{{- define "hopeup.selectorLabels" -}}
app.kubernetes.io/name: {{ include "hopeup.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Component-specific labels (backend / frontend / worker / beat).
Usage: {{ include "hopeup.componentLabels" (dict "context" . "component" "backend") }}
*/}}
{{- define "hopeup.componentLabels" -}}
{{ include "hopeup.labels" .context }}
app.kubernetes.io/component: {{ .component }}
app: {{ .component }}
tier: {{ .component }}
{{- end -}}

{{- define "hopeup.componentSelector" -}}
{{ include "hopeup.selectorLabels" .context }}
app.kubernetes.io/component: {{ .component }}
app: {{ .component }}
{{- end -}}

{{/*
Standardized image string. Falls back to global.imageRegistry if repository
doesn't already include a registry.
*/}}
{{- define "hopeup.image" -}}
{{- $reg := .global.imageRegistry -}}
{{- $repo := .image.repository -}}
{{- $tag := .image.tag | default .context.Chart.AppVersion -}}
{{- if contains "/" $repo -}}
{{- printf "%s:%s" $repo $tag -}}
{{- else -}}
{{- printf "%s/%s:%s" $reg $repo $tag -}}
{{- end -}}
{{- end -}}

{{/*
Service account name helper.
*/}}
{{- define "hopeup.serviceAccountName" -}}
{{- printf "%s-%s" (include "hopeup.fullname" .context) .component -}}
{{- end -}}

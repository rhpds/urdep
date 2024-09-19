{{/*
Expand the name of the chart.
*/}}
{{- define "urdep.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "urdep.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "urdep.labels" -}}
helm.sh/chart: {{ include "urdep.chart" . }}
{{ include "urdep.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "urdep.selectorLabels" -}}
app.kubernetes.io/name: {{ include "urdep.name" . }}
{{-   if (ne (upper .Release.Name) "RELEASE-NAME") }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{-   end -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "urdep.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "urdep.name" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Create the name of the namespace to use
*/}}
{{- define "urdep.namespaceName" -}}
  {{- default (include "urdep.name" .) .Values.namespace.name }}
{{- end -}}

{{/*
Define the image to deploy
*/}}
{{- define "urdep.image" -}}
  {{- if .Values.image.override -}}
    {{- .Values.image.override -}}
  {{- else -}}
    {{- if eq .Values.image.tagOverride "-" -}}
      {{- .Values.image.repository -}}
    {{- else if .Values.image.tagOverride -}}
      {{- printf "%s:%s" .Values.image.repository .Values.image.tagOverride -}}
    {{- else -}}
      {{- printf "%s:v%s" .Values.image.repository .Chart.AppVersion -}}
    {{- end -}}
  {{- end -}}
{{- end -}}

{{/*
Create the name for the postgresql component
*/}}
{{- define "urdep.postgresqlName" -}}
  {{- .Values.postgresql.name | default (printf "%s-postgresql" (include "urdep.name" .)) -}}
{{- end -}}

{{- define "urdep.postgresqlSelectorLabels" -}}
app.kubernetes.io/name: {{ include "urdep.name" . }}-postgresql
{{-   if (ne (upper .Release.Name) "RELEASE-NAME") }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{-   end -}}
{{- end -}}

{{/*
Image for postgresql
*/}}
{{- define "urdep.postgresqlImage" -}}
  {{- if .Values.postgresql.image.override }}
     {{- .Values.postgresql.image.override }}
  {{- else }}
     {{- .Values.postgresql.image.repository }}:{{ .Values.postgresql.image.tag }}
  {{- end }}
{{- end -}}

// Verification harness for the pinned Coze Studio importer components.
// No service/network request is permitted. This does not launch Coze UI.
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"sort"
	"strings"

	common "github.com/coze-dev/coze-studio/backend/api/model/plugin_develop/common"
	"github.com/coze-dev/coze-studio/backend/crossdomain/plugin/model"
	"github.com/getkin/kin-openapi/openapi3"
	"github.com/getkin/kin-openapi/openapi3filter"
	"github.com/getkin/kin-openapi/routers/legacy"
)

type Result struct {
	File            string            `json:"file"`
	Parse           string            `json:"parse"`
	HostValidate    string            `json:"host_validate"`
	Tools           []string          `json:"tools"`
	RequestMapping  map[string]string `json:"request_mapping"`
	ResponseMapping map[string]string `json:"response_mapping"`
	Checks          map[string]string `json:"checks"`
	Errors          []string          `json:"errors,omitempty"`
}

func fieldPaths(params []*common.APIParameter, prefix string) []string {
	var paths []string
	for _, p := range params {
		name := p.Name
		if name == "[Array Item]" {
			name = "[]"
		}
		path := name
		if prefix != "" {
			if name == "[]" {
				path = prefix + name
			} else {
				path = prefix + "." + name
			}
		}
		paths = append(paths, path)
		paths = append(paths, fieldPaths(p.SubParameters, path)...)
	}
	return paths
}
func assert(row *Result, key string, ok bool, detail string) {
	if ok {
		row.Checks[key] = "PASS: " + detail
	} else {
		row.Checks[key] = "FAIL: " + detail
		row.Errors = append(row.Errors, key+": "+detail)
	}
}
func main() {
	ctx := context.Background()
	results := []Result{}
	// Disable all outgoing HTTP. Parsing/validation must never call a service.
	http.DefaultTransport = blockedTransport{}
	for _, path := range os.Args[1:] {
		row := Result{File: filepath.Base(path), RequestMapping: map[string]string{}, ResponseMapping: map[string]string{}, Checks: map[string]string{}}
		loader := openapi3.NewLoader()
		loader.IsExternalRefsAllowed = false
		doc, err := loader.LoadFromFile(path)
		if err != nil {
			row.Parse = "FAIL"
			row.Errors = append(row.Errors, err.Error())
			results = append(results, row)
			continue
		}
		row.Parse = "PASS"
		coze := model.Openapi3T(*doc)
		if err = coze.Validate(ctx); err != nil {
			row.HostValidate = "FAIL"
			row.Errors = append(row.Errors, err.Error())
		} else {
			row.HostValidate = "PASS"
		}
		service := strings.TrimSuffix(row.File, filepath.Ext(row.File))
		for route, item := range doc.Paths {
			for method, op := range item.Operations() {
				row.Tools = append(row.Tools, op.OperationID)
				tool := model.ToolInfo{Operation: model.NewOpenapi3Operation(op)}
				req, reqerr := tool.ToReqAPIParameter()
				if reqerr != nil {
					row.RequestMapping[op.OperationID] = reqerr.Error()
					row.Errors = append(row.Errors, "request mapping: "+reqerr.Error())
				} else {
					row.RequestMapping[op.OperationID] = fmt.Sprintf("PASS %d top-level fields", len(req))
				}
				resp, resperr := tool.ToRespAPIParameter()
				if resperr != nil {
					row.ResponseMapping[op.OperationID] = resperr.Error()
					row.Errors = append(row.Errors, "response mapping: "+resperr.Error())
				} else {
					row.ResponseMapping[op.OperationID] = fmt.Sprintf("PASS %d top-level fields", len(resp))
				}
				_, maperr := model.NewOpenapi3Operation(op).ToEinoSchemaParameterInfo(ctx)
				assert(&row, op.OperationID+"_agent_schema", maperr == nil, fmt.Sprint(maperr))
				auth := op.Parameters[1].Value
				for _, p := range op.Parameters {
					if p.Value.Name == "Authorization" {
						auth = p.Value
					}
				}
				assert(&row, op.OperationID+"_blank_credential", auth.Name == "Authorization" && auth.Required && auth.In == "header" && auth.Schema.Value.Default == nil && auth.Schema.Value.Example == nil, "required header, no saved default/example")
				// In-memory Reference binding uses only a variable name, never a token.
				auth.Schema.Value.Extensions = map[string]interface{}{"x-variable-ref": "adc_auth"}
				bound, err := tool.ToReqAPIParameter()
				bindingOK := false
				if err == nil {
					for _, p := range bound {
						if p.Name == "Authorization" && p.VariableRef != nil && *p.VariableRef == "adc_auth" && p.GlobalDefault == nil {
							bindingOK = true
						}
					}
				}
				assert(&row, op.OperationID+"_reference_mapping", bindingOK, "official mapper preserves private variable name; no credential value stored")
				auth.Schema.Value.Extensions = nil
				if op.OperationID == "getTaskResults" && resperr == nil {
					paths := fieldPaths(resp, "")
					joined := "|" + strings.Join(paths, "|") + "|"
					media := "response.data[].video_url"
					if service == "seedance" {
						media = "response.data.content.video_url"
					}
					if service == "nano-banana" {
						media = "response.data[].image_url"
					}
					assert(&row, "result_media_mapping", strings.Contains(joined, "|"+media+"|"), media)
					assert(&row, "batch_media_mapping", strings.Contains(joined, "|items[]."+media+"|"), "same media field in batch items")
					assert(&row, "terminal_error_mapping", strings.Contains(joined, "|response.error.message|") || strings.Contains(joined, "|response.error|"), "explicit terminal error field")
				}
				// Real kin-openapi request validation, in memory; no transport is invoked.
				body := map[string]interface{}{"id": "OWNED_TASK_ID_PLACEHOLDER", "action": "retrieve"}
				if op.OperationID != "getTaskResults" {
					switch service {
					case "seedance":
						body = map[string]interface{}{"model": "doubao-seedance-1-0-pro-fast-251015", "content": []interface{}{map[string]interface{}{"type": "text", "text": "A test description; no generation is sent."}}, "async": true}
					case "happyhorse":
						body = map[string]interface{}{"model": "happyhorse-1.1-t2v", "action": "generate", "prompt": "Schema fixture only.", "async": true}
					case "nano-banana":
						body = map[string]interface{}{"model": "nano-banana-2", "action": "generate", "prompt": "Schema fixture only.", "async": true}
					}
				}
				router, err := legacy.NewRouter(doc)
				if err != nil {
					row.Errors = append(row.Errors, err.Error())
					continue
				}
				validate := func(withAuth bool, payload map[string]interface{}) error {
					b, _ := json.Marshal(payload)
					r, _ := http.NewRequest(method, "https://api.acedata.cloud"+route, bytes.NewReader(b))
					r.Header.Set("Content-Type", "application/json")
					if withAuth {
						r.Header.Set("Authorization", "Bearer SCHEMA_ONLY_INVALID_MARKER")
					}
					rt, pp, e := router.FindRoute(r)
					if e != nil {
						return e
					}
					return openapi3filter.ValidateRequest(ctx, &openapi3filter.RequestValidationInput{Request: r, PathParams: pp, Route: rt})
				}
				assert(&row, op.OperationID+"_missing_auth_rejected", validate(false, body) != nil, "no-key request rejected by required-header validation; no API request")
				assert(&row, op.OperationID+"_schema_request_accepted", validate(true, body) == nil, "invalid public marker used only in memory, not sent")
			}
		}
		sort.Strings(row.Tools)
		assert(&row, "two_tools", len(row.Tools) == 2, "exact two-tool import")
		results = append(results, row)
	}
	b, _ := json.MarshalIndent(results, "", "  ")
	fmt.Println(string(b))
	for _, r := range results {
		if len(r.Errors) > 0 {
			os.Exit(1)
		}
	}
}

type blockedTransport struct{}

func (blockedTransport) RoundTrip(*http.Request) (*http.Response, error) {
	return nil, fmt.Errorf("all outgoing HTTP disabled in verification")
}

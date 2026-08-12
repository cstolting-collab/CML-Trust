# Model-tool integration boundary

`cml-trust` includes a narrow, opt-in host wrapper for applications that use
developer-supplied function calling. It is not a hosted service, a generator
integration, or evidence that any model provider has adopted CML.

## Implemented operations

- `cml_plan_seal` compiles one CML source inside a host-configured workspace,
  creates a validated `sealed_plan`, and appends it to the host-owned JSONL
  ledger.
- `cml_status_derive` reads that fixed ledger and derives its current status.

The model cannot select a ledger path, execute a shell command, call arbitrary
Python functions, or read a path outside the configured workspace. Paths are
checked after resolution so symlinks and sibling paths cannot escape the root.

```python
from cml_trust.tool_host import CMLTrustToolHost, tool_definitions

host = CMLTrustToolHost("/safe/project")
tools = tool_definitions()

# After the model requests an allow-listed function:
result = host.execute(tool_name, parsed_json_arguments)
```

The containing application is responsible for sending `tools` to its model
API, parsing the requested function name and JSON arguments, calling
`host.execute`, and returning the structured result to the model.

## Security and concurrency boundary

- The host application, not the model, chooses `allowed_root` and `store_path`.
- Unknown operations and arguments fail closed.
- CML-Trust and adapter error codes remain machine-readable.
- Unexpected exceptions are returned as a generic `INTERNAL_ERROR`; internal
  details are not exposed to the model.
- Writes are serialized across wrapper instances in one Python process.
- The alpha JSONL store has no cross-process lock. A deployment must use one
  writer process or add an external lock before allowing multiple processes to
  share a ledger.

## Claim boundary

Successful use establishes only that a host application called the public CML
tooling and received its structured result. It does not establish that Grok,
Llama, xAI, Meta, or a media generator internally executes, adopts, or endorses
CML.

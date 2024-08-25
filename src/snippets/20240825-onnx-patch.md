# Patching ONNX to expose intermediate output

```python
def patch_onnx(input_filename: str, output_filename: str, inter_layer_names: List[str])->None:
    """
    Main idea: append value_info_proto with name included in inter_layer_names to the
    graph output list
    """
    model = onnx.load(input_filename)
    value_info_protos = []
    for node in model.graph.value_info:
        if node.name in inter_layer_names:
            value_info_protos.append(node)
    assert len(value_info_protos) == len(inter_layer_names)
    model.graph.output.extend(value_info_protos)  
    onnx.checker.check_model(model)
    onnx.save(model, output_filename)
```

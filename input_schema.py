INPUT_SCHEMA = {
    "prompt": {
        'datatype': 'STRING',
        'required': True,
        'shape': [1],
        'example': ["A cat holding a sign that says hello world"]
    },
     "workflow_name": {
        'datatype': 'STRING',
        'required': True,
        'shape': [1],
        'example': ["flux_workflow"]
    }
}

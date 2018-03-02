@title[Introduction]
# Spline
### The pipeline tool

**Source**:
http://github.com/Nachtfeuer/pipeline

**Contact**:
[thomas.lehmann.private@gmail.com](mailto:thomas.lehmann.private@gmail.com)

---
@title[Features]
### Features
matrix, pipeline, stages, task groups,
shell, docker(image), docker(container), python,
parallelizable, filterable (tags), model data,
cleanup hook, Jinja2 templating support,
tasks variables, conditional tasks, dynamic report,
dry run support, schema validation.

---
@title[Quickstart]
### Quickstart
#### Installation:

```shell
pip install spline
```

#### Minimal Pipeline:
```
pipeline:
  - stage(Demo):
      - tasks(ordered):
          - shell:
              script: echo "hello world"
```

---
@title[Task Types]
### Task Types

```yaml
- shell:
    script: echo "hello world"
- python:
    script: print("hello world")
- docker(image):
    name: demo
    tag: "1.0"
    unique: no
    script: from centos:7
- docker(container):
    image: demo:1.0
    script: echo "hello world
```

---

## The End


@title[Introduction]
# Spline
### The pipeline tool

**Source** |
http://github.com/Nachtfeuer/pipeline

**Contact** |
[thomas.lehmann.private@gmail.com](mailto:thomas.lehmann.private@gmail.com)

---
@title[Features]
### Features

**Structural** | **Task Types**   | **Behaviorial**          | **Data**
-------------- | ---------------- | ------------------------ | -----------------
Matrix         | Shell            | Ordered (matrix, tasks)  | Model
Pipeline       | Python           | Parallel (matrix, tasks) | Env. Variables
Stages         | Docker Image     | Filter (matrix, tasks)   | Task Variables
Tasks Groups   | Docker container | Conditional tasks        | Schema Validation
Tasks          |                  | Jinja2 Templating        | Report

also: dry run support

---
@title[Quickstart]
### Quickstart
#### Installation:

```shell
pip install spline
```

#### Minimal Pipeline:
```yaml
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
    script: echo "hello world"
```

---
@title[Jinja2 Templating Support (Part One)]
### Jinja2 Templating Support (Part One)
```yaml
model: {"mmsg": "model message"}
pipeline:
  - env: {"pmsg": "pipeline message"}
  - stage(Demo):
      - env: {"smsg": "stage message"}
      - tasks(ordered):
          - env: {"tmsg": "tasks block message"}
          - shell:
              script: |
                echo "User: {{ env.USER }}"
                echo "Model msg: {{ model.mmsg }}"
                echo "Pipeline msg: {{ env.pmsg }}"
                echo "Stage msg: {{ env.smsg }}"
                echo "Tasks block msg: {{ env.tmsg }}"
```
<small>(env. variables are merged, last ones win, OS env. variables come last)</small>

---
@title[Jinja2 Templating Support (Part Two)]
### Jinja2 Templating Support (Part Two)
#### Nested rendering support

```yaml
model:
  one: "{{ env.USER }}: hello"
  two: "{{ model.one|render(env=env) }} world!"
pipeline:
 - stage(This Is A Demo):
   - tasks(ordered):
     - shell:
         script: echo "{{model.two|render(model=model,env=env)}}"
```
(on my machine: `thomas: "hello world!"`)

---
@title[Task Variables]
### Task Variables
#### Special rules:
- either need to be separated via a tasks block or via an **env** block inbetween in same block
- field **variable** not available for docker(image)

#### Example:
```yaml
pipeline:
  - stage(Demo):
    - tasks(ordered):
      - shell:
          script: git rev-parse --short HEAD
          variable: commit
    - tasks(ordered):
      - shell:
          script: "echo \"commit: {{ variables.commit }}\""
```

---
@title[Conditional Tasks]
### Conditional Tasks

 - field **when** available on all task types
 - `when: "'{{ env.BRANCH_NAME }}' == 'master'"`
 - support for **==**, **<**, **<=**, **>** and **>=**
 - support for lists: `when: "'{{ env.BRANCH_NAME }}' in ['prod', 'preprod']"`
 - negate with **not** like `when: "'not {{ env.BRANCH_NAME }}' == 'master'"`;
   for lists: **not in**.
 - single quotes always required for strings

---
@title[Docker Image]
### Task: docker(image)

```
model:
  base_url: http://download.oracle.com/otn-pub/java/jdk
  rpm: jdk-9.0.4_linux-x64_bin.rpm
  version_url: "9.0.4+11/c2514751926b4512b076cc82f959763f/{{ model.rpm }}"
pipeline:
  - stage(Demo):
    - tasks(ordered):
      - docker(image):
          name: jdk
          tag: "9.0.4"
          unique: no
          script: |
            from centos:7
            run yum -y install wget
            run wget --quiet --no-cookies --no-check-certificate \
                     --header "Cookie: oraclelicense=accept-securebackup-cookie" \
                     {{ model.base_url }}/{{ model.version_url|render(model=model) }}
            run yum -y localinstall {{ model.rpm }}
            run rm -f {{ model.rpm }}
            run java --version
```

---
## The End


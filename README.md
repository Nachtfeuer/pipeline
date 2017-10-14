# Welcome to the pipeline tool

**Work in progress; not yet for use; stay tuned**

# Quick start

Following dependencies are required:

```
pip install pyaml pykwalify
```

Main focus for a quick start is developing on this
project. For **using** this pipeline tool there will
be another section.

```
git clone https://github.com/Nachtfeuer/pipeline.git
cd pipeline
./validate.sh
```

# Some hints

The following code should print the loaded yaml just
basing on pure Python data (dict, list, str and so on).

```
python -c "import yaml;print(yaml.load(open('example.yaml').read()))"
```


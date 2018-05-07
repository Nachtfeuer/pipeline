The include statement
=====================

Basic Usage
-----------
You can use the **!include** statement on maps and lists. You have to ensure that the
final document structure is still a valid spline document. Spline will run the
validation after the include has been done.

```yaml
model: !include library/model.yaml
pipeline:
   - stage(Setup): !include library/setup.yaml
   - stage(Build): !include library/build.yaml
   - stage(Test):
        - !include library/setup-test.yaml
        - !include library/run-test.yaml
        - !include library/teardown-test.yaml
   - stage(Deploy): !include library/deploy.yaml
```

Notes
------
 - The loader is evaluating the **!include** statement for the main document
only (by intention).
 - the specified file has to exist!

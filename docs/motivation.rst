Motivation
==========

Working a longer time with tools like Jenkins and Travis CI you might find out that
you loose a lot of time because of try and error. You change the pipeline on a
feature branch, push it remote and then run the pipeline analyzing the results.
As an example you cannot easily use a Jenkinsfile locally since that Groovy code
does use a so called DSL accessing Jenkins and the plugin infrastructure in a running 
Jenkins instance.

I have been seeking for a better solution where you can do most things already on
your own machine. Basically all concepts like matrix, stages and parallelism
should be available in a simple terminal (console).

Also it allows using this tool in different existing environments like
Jenkins and Travis CI where you can keep the Jenkinsfile (.travis.yml) very
simple and short while your pipeline definition yaml contains all.

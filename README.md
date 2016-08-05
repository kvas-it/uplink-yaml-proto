# Uplink.yaml

`uplink.yaml` is a file that contains the information that is necessary for
building, testing, packaging and deployment of the software. It fully describes
the interaction of the software with the CI system (Uplink).

This document describes the information contained in `uplink.yaml` and the
format of the file. At this moment it's used for prototyping and collecting
feedback and thus everything here is subject to change.

## Content of the file

`uplink.yaml` contains sections that describe the following aspects of the
interaction between software and the CI system:

1. How to produce the build artifacts (environment, what to run and where are
   the artifacts at the end). There could be one or more build configuration,
so that all build configurations together produce all artifacts.
2. How to deploy the artifacts. The deployment processes has access to all
   build artifacts and to the source code of the repository. The deployment
process can produce one or more deployed assemblies (groups of one or more
virtual/real boxes that are working together).
3. How to publish the artifacts. The publishing process has access to any
   necessary build artifacts and to the source code of the repository.
4. How to run the tests. There could be one or more test configurations using
   artifacts and/or deployed assemblies. Each test configuration runs on a
clean environment.

## Examples

This section contains example scenarios. Each scenario consists of the type of
software that we're dealing with, what goes into each section of `uplink.yaml`
and example of `uplink.yaml` (this is not there yet).

### Python library or script

1. Build artifacts: .tgz packages, eggs or wheels, or it could be nothing,
   since we can publish and test directly without building.
2. No deployment section.
3. Publish to pypi (or local devpi server) using devpi client.
4. Run tests using tox, doesn't use any artifacts.

Examples:
- Simple python package using Tox [python-abp-1](python-abp-1.yaml)

### Browser plugin

1. Build artifacts: plugin package(s).
2. Maybe assembly for selenium testing or something like that.
3. Publish to one or more stores.
4. Run local unit tests using node.js and some test runner; maybe run
   functional tests with selenium using the selenium assembly.

### Web site

1. Build artifacts: rendered static content.
2. Production assembly of two boxes: (nginx + static content) + (fcgi
   multiplexer + scripts), test assembly that might be identical or maybe
slightly different.
3. No publishing, we only deploy this.
4. Test the website using the testing assembly and maybe something like
   selenium.

### Deployment of 3rd party software, like Discourse

1. No build.
2. Assembly with production configuration, for example a database box and an
   application box with nginx as a reverse proxy.
3. No publishing.
4. Maybe test the production assembly.

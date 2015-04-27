# reaper

The purpose of the reaper repository is to store the reference
implementation of the scoring system as outlined in the research paper.

## Installation

The projects runs on systems with `python3`. There are a number of python
libraries that the code needs in order to execute. To install them, simply run
`pip -r requirements.txt` (or `pip3` if your system does not have python3 set
as the default.)

## Usage

The `score_repo.py` executable is the main interface that should be used by the
end user. In order to use the tool, however, a few steps need to be taken first.

Another batch script is currently under development, called `batch_score.py`
will can be used to score many different repositories at the same time.

### config.json

This file is responsible for controlling various aspects of the system. There
are two high level keys that can be altered, `options` and `attributes`.

#### `options`

| Key | Values | Description |
| --- |:------:| -----------:|
| `threshold` | Positive Numbers | Defines the threshold by which the system considers a repository to contain a software project. |
| `persistResult` | true or false | Whether the granular results should be saved to the specified datasource. |
| `datasource` | object | Settings for connecting to the GHTorrent database, see description below. |
| `githubTokens` | list | List of GitHub OAuth tokens to be used for authentication for rate limiting purposes. |

##### `datasource`

[GHTorrent](http://ghtorrent.org/) is a research project that aims to collect
and store information produced by the public GitHub events feed. The initial
implementation of `score_repo.py` relies on this information being accessible.

Load a dump of the GHTorrent data set into MySQL or MariaDB (binary compatible
as of this writing), copy the `config.json.sample` file to `config.json` and
edit the appropriate parameters under the `options => datasource` key.

#### `attributes`

The system is designed as a number of plugins that all have a chance to analyze
a given repository (both metadata as well as contents). A number of provided
attributes are apart of the base distribution of the system, but more can easily
be added.

In order for an attribute to be executed, it must be listed under the
`attribtues` key in the configuration file.

An example entry looks like the following:

```json
{
  "name": "architecture",
  "dependencies": [
    "ctags"
  ],
  "enabled": true,
  "weight": 50,
  "options": {
  }
}
```

`name` refers to the name of the attribute as it appears under the `attribute/`
directory. `dependencies` is a list of system utilities that the attribute
implementation relies on in order to function. `enabled` controls whether the
attribute will be considered during the scoring of the repository. `weight`
allows the bias of the attribute to be fine tuned in order to adjust its effect
on the final score. Finally, `options` are specific options for each particular
attribute implementation.

## Attribute Development

In order to add your own attribute plugin to the system, there are few things
that must be done. First, add an attribute entry as described in the above
section that refers to your specific attribute.

Secondly, create the appropriately named directory under `attributes/` along
with a `main.py`. Inside of this, the following function signature should be
used to kickoff the execution of the plugin:

```python
def run(project_id, repo_path, cursor, **options):
  # Implementation goes here.
```

Check the doc block for details on what each parameter provides in terms of
functionality. Attribute implementations should return a tuple of two values:
the binary result of execution and the raw result of execution. The binary
result should be True or False and the raw result should be a real number that
is the raw calculation made by the plugin. In the case of purely binary results,
do something like `return result, int(result)`.

Additionally, there is the option of initializing the plugin. To take advantage
of initialization, add the following function signature to `main.py`:

```python
def init(cursor, **options):
  # Implementation goes here.
```

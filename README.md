# reaper

Reaper is a tool used to assess a GitHub repository in the form of a score. It
considers a number of different *attributes* in order to perform a thorough
assessment.

Together with a database of metadata provided by the [GHTorrent](http://ghtorrent.org/) project, *reaper* considers both contextual information such as commit history as well
as the contents of the repository itself.

## Installation

The projects runs on systems with `python3`. There are a number of python
libraries that the code needs in order to execute. To install them, simply run
`pip install -r requirements.txt` (or `pip3` if your system does not have python3 set
as the default.)

## Interface

The main interface that should be used to run reaper is the Python script called 
`batch_score.py`. This script should be called with a set of parameters that 
specify where the datasource can be found, what projects need to be analyzed,
etc. 

Additionally there is a script called `score_repo.py`, however at the moment it 
is outdated and cannot be used to score repos. 

### Usage

`batch_score.py` can be called as follows: 

`batch_score.py -c <config> -r <repos_path> -m <manifest> -s <sample_file>`

Where:
* `<config>`: Is an instance of `config.json`.
* `<repos_path>`: Is the path to a directory where reaper can check out the 
source files of a project. 
* `<manifest>`: Is an instance of `manifest.json` (which can be found in this 
repository) containing information on what attributes should be executed.
* `<sample_file>`: A list of GHTorrent project ids that should be analyzed, 
newline seperated. 

### config.json

This file is responsible for controlling various aspects of the system. There
are two high level keys that can be altered, `options` and `attributes`.

#### `options`

| Key | Values | Description |
| --- |:------:| -----------:|
| `threshold` | Positive Numbers | Defines the threshold by which the system considers a repository to contain a software project. |
| `persistResult` | true or false | Whether the granular results should be saved to the specified datasource. |
| `datasource` | object | Settings for connecting to the GHTorrent database, see description below. |
| `github_tokens` | list | List of GitHub OAuth tokens to be used for authentication for rate limiting purposes. |

##### `datasource`

[GHTorrent](http://ghtorrent.org/) is a research project that aims to collect
and store information produced by the public GitHub events feed. The initial
implementation of `score_repo.py` relies on this information being accessible.

Load a dump of the GHTorrent data set into MySQL or MariaDB (binary compatible
as of this writing), copy the `config.json.sample` file to `config.json` and
edit the appropriate parameters under the `options => datasource` key.

#### `peristResult`

If persist results is enabled a database table needs to exist to which reaper can 
write results. This table should be named `reaper_results` and should contain at 
least a column for project ids named `project_id`, and a column to store the score 
for a repository named `score`. Additionally, there should be a column for every 
attribute that you want to store.

For instance, to create this table in MySQL the following table create statement
can be used:

```
CREATE TABLE `reaper_results` (
  `project_id` int(11) NOT NULL,
  `architecture` double DEFAULT NULL,
  `community` double DEFAULT NULL,
  `continuous_integration` double DEFAULT NULL,
  `documentation` double DEFAULT NULL,
  `history` double DEFAULT NULL,
  `license` double DEFAULT NULL,
  `management` double DEFAULT NULL,
  `project_size` double DEFAULT NULL,
  `repository_size` double DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `stars` double DEFAULT NULL,
  `unit_test` double DEFAULT NULL,
  `score` double DEFAULT NULL,
  PRIMARY KEY (`project_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
```

#### `attributes`

The system is designed as a number of plugins that all have a chance to analyze
a given repository (both metadata as well as contents). A number of provided
attributes are apart of the base distribution of the system, but more can easily
be added.

In order for an attribute to be executed, it must be listed under the
`attributes` key in the configuration file.

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

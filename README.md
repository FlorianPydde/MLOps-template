# MLOps with Azure

This repository contains the basic structure for machine learning projects based on Azure technologies like Azure ML and Azure DevOps. The folder names and files are chosen based on personal experience and we encourage teams to use their own convention. Nevertheless, we will describe the principles and ideas behind the structure, which we recommend to follow when customizing your own project and MLOps process. Also, we expect users to be familiar with azure machine learning concepts and how to use the technology.

## Data Science Lifecycle Base Repo

The base project structure was inspired by the following [dslp repo](https://github.com/dslp/dslp-repo-template). We readapted it to support minimal MLOps principles.

## TL;DR

Examples of core machine learning scripts like training, scoring, etc are saved in _src_. Examples of scripts to run the core scripts on remote compute, aks clusters, etc are saved in _operation/execution_. To use the scripts on your local machine, the azure ml workspace credentials in a config.json file in the root directory.
We do not provide any concrete implementation of MLOps but only the folder structure and some examples, as the naming convention and logical flow highly depend on the use case.

## Contributing

TBD

## Default Directory Structure

```
├───azure_pipelines     # folder containing all the azure devops pipelines
├── data                # directory is for consistent data placement. contents are gitignored by default.
│   ├── README.md
│   ├── interim         # storing intermediate results (mostly for debugging)
│   ├── processed       # storing transformed data used for reporting, modeling, etc
│   └── raw             # storing raw data to use as inputs to rest of pipeline
├── docs
│   ├── code            # documenting everything in the code directory (could be sphinx project for example)
│   ├── data            # documenting datasets, data profiles, behaviors, column definitions, etc
│   ├── media           # storing images, videos, etc, needed for docs.
│   ├── references      # for collecting and documenting external resources relevant to the project
│   └── solution_architecture.md    # describe and diagram solution design and architecture
├───notebooks           # experimentation folder with notebooks, code and other. The files don't need to be committed
├───operation           # all the code and configuration to execute the source scripts
│   ├───configuration   # any configuration files
│   │   ├───environment_dev
│   │   ├───environment_prod
│   │   └───environment_stage
│   ├───execution       # azure ml scripts to run source script on remote
│   ├───monitoring      # anything related to monitoring, model performance, data drifts, model scoring, etc
│   └───tests           # for testing your code, data, and outputs
│       ├───data_validation     # any data validation scripts
│       ├───integration         # integration tests like training pipeline, scoring script on AKS, etc
│       └───unit                # unit tests
|── src
├── .gitignore
├── README.md
└── setup.py 
```

## MLOps template guidelines

There exists many different MLOps templates and implementation examples. The main challenge that most of them either follow a structure fined-tune to a reduced set of use cases or they constrain too much the experimentation side. As a rule of thumb, there are two questions that assess the quality of your template.

1. How easy is it to debug the code when the CD pipeline fails ?
2. How easy is it to add new functionalities or adapt your code when your environments (stage/prod/...) or use case changes ?

In essence, the first question assess how different is way the data scientist experiments code from the deployment process. The second question ensures that one is not "overfitting" to the use case. Thus, having these two questions in mind, we can try defining a "common denominator" folder structure and process.

Next, we need to acknowledge that there are different levels of MLOps implementation, as for any framework. For instance, lets take the example _Scrum_. When a team or an organization is moving from an _Waterfall_ approach to _Scrum_, the change is implemented step wise. It is rarely the case that a team successfully implements all the guidelines at once. On the other hand, it is worth noting that applying only a few principles will not bring the expected benefits. For instance, only doing "standup meetings" and having a "sprints" will not create a successful scrum team. Hence, we see that there are different levels when it comes to applying a new framework but it is necessary to define the minimum principles to follow to create value and what we strive to, i.e the entire framework implementation, to integrate change (question 2)

Here is an example of a set of minimum (Level 1) MLOps requirements and the full (level 3,4,...) requirements

| Aspects     | Minimum Requirement                                                                                                        | Full Requirement                                                                                                                  |
| ----------- | -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Environment |dev: for experimentation and coding<br> prod (or stage or whatever you fancy): the environment hosting the whole solution | dev/stage/prod and others if required                                                                                             |
|             |                                                                                                                            |                                                                                                                                   |
| Code        | CD integration pipeline for automated training pipeline and scoring service                                                | CI pipeline on Master branch (or other branch)<br>CD pipeline for integration of all parts: training,                             |
|             |                                                                                                                            |                                                                                                                                   |
| Data        | Raw data are centralised and updated automatically                                                                         | Data validation<br>Data drifts detection<br>Feature store for reusability                                                         |
|             |                                                                                                                            |                                                                                                                                   |
| Model       | Model performance logged during training      
# MLOps with Azure

This repository contains the basic structure for machine learning projects based on Azure technologies like Azure ML and Azure DevOps. The folder names and files are chosen based on personal experience and we encourage teams to use their own convention. Nevertheless, we will describe the principles and ideas behind the structure, which we recommend to follow when customizing your own project and MLOps process. Also, we expect users to be familiar with azure machine learning concepts and how to use the technology.

## Data Science Lifecycle Base Repo

The base project structure was inspired by the following [dslp repo](https://github.com/dslp/dslp-repo-template). We readapted it to support minimal MLOps principles.

## TL;DR

Examples of core machine learning scripts like training, scoring, etc are saved in _src_. Examples of scripts that run the core scripts on remote compute, aks clusters, etc are saved in _operation/execution_. To use the scripts on your local machine, add the azure ml workspace credentials in a config.json file in the root directory.
We do not provide any concrete implementation of MLOps but only the folder structure and some examples, as the naming convention and logical flow highly depend on the use case. Nevertheless, you may want to have a look at the utils.py modules which handle the credentials.

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
| Environment |  dev: for experimentation and coding<br> prod (or stage or whatever you fancy): the environment hosting the whole solution | dev/stage/prod and others if required                                                                                             |
|             |                                                                                                                            |                                                                                                                                   |
| Code        | CD integration pipeline for automated training pipeline and scoring service                                                | CI pipeline on Master branch (or other branch)<br>CD pipeline for integration of all parts: training,                             |
|             |                                                                                                                            |                                                                                                                                   |
| Data        | Raw data are centralised and updated automatically                                                                         | Data validation<br>Data drifts detection<br>Feature store for reusability                                                         |
|             |                                                                                                                            |                                                                                                                                   |
| Model       | Model performance logged during training                                                                                   | Automated model validation against holdout set<br>trigger for automated training<br>scored data and results logged<br>A/B Testing |

This template will provide the basic elements to quickly setup a minimal MLOps processes so that the team can move quickly from the basic level to the most advance MLops infrastructure

## Azure Machine Learning

Azure machine learning provides a lot of different APIs and tools to create an optimal MLOps infrastructure. We will review the different tools and provide some recommendation on how to best leverage the latter. We will focus review managing data, training and scoring process and review which credentials are required to access the resources

### Training in Azure

It is important to understand how training is performed in azure. In essence, one writes normal core machine learning scripts like train.py, score.py, etc and another set of separate scripts that will perform environment configuration and execute the core scripts on a remote machine, as for instance a VM or AKS cluster as explained [here](https://docs.microsoft.com/en-us/azure/machine-learning/concept-environments). One can choose to either use python scripts (or R) to execute the remote run or Azure CLI. We do not recommend the later as it constrains too much the experimentation (question 1). 

For simplicity, I will call the set of core script "Core Scripts", that you can find in the **src folder**, and the other set "Ops Scripts", saved in the **operation folder** as they handle the operation. Why is this distinction so important ? Azure has different ways for handling credentials and each set of scripts use different approaches to handle access to the workspace and datasets. We discuss this point in the next section.

### Workspace/Secrets

The central piece of Azure ML is the Workspace. Every process is executed or linked to it Workspace, as for instance when retrieving datasets, uploading models to the registry, running automl, etc. There are 3 main way to retrieve, and a secondary:

1. The most straight forward is through the azure portal. You can download the _config.json_ from your aml resource page. This method is used for Core and Ops scripts when developing on the local machine.
2. Through the _run_ object. This is used in Core Scripts to access the workspace when run on a remote compute. An example can be [found here](https://github.com/Azure/MachineLearningNotebooks/blob/71861278041bfc37557293adb94d844e5e36e60e/how-to-use-azureml/automated-machine-learning/regression-explanation-featurization/train_explainer.py). 

```
run = Run.get_context() 
ws = run.experiment.workspace
```

3. Through a service principal stored as environment variable. This method is used in devops pipelines when performing integration. To generate and use service principals follow [this link](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-setup-authentication)

In the **src** and **operation/execution** folder, one can find the _utils.py_ scripts that shows how the credentials are retrieved.

Now that we know how to get the workspace credentials we can show how to train a model, handle the data, and define a scoring script.

### Training

There are 4 different ways in AML to run a training script. The full explanation can be [found here](https://docs.microsoft.com/en-us/azure/machine-learning/concept-train-machine-learning-model)

1. **Run_config**: this approaches is useful if you want either quickly setup your environment or spend time fine tuning it. Also, it can be used to execute pyspark job on hdinsights.
2. **Estimator**: this is probably the most straightforward method. Azure has a setup of already configured environment that are very useful when using deep learning frameworks like TensorFlow, Pytorch, etc. Of course, it also accepts your conda environment or pip requirement file.
3. **AutoMl**: very simple way to generate automated model training. It doesn't need any Core Scripts. As a side note, if one doesn't like using this service, we recommend testing it as a baseline to your custom model.
4. **Machine Learning Pipeline**: very useful when one needs to run a sequence of scripts or uses a "multi-model" approach as for instance in demand forecasting where one model is trained per product.

All the approaches allow to either can handle the datasets by either passing them as arguments from the Ops Scripts to the Core Scripts or inside the later. We discuss how to manage the data in the next session.

### Data

As stated before, we assume that all the datasets are stored in a single source (the approach is the same if data are in different storages). With AzureML, there are 3 different way to upload,download,load,save data :

1. Using the Datastore/Dataset objects directly from the aml sdk
2. Using the Datastore/Dataset objects passed as arguments to a script and extracted via the _run_ object
3. Using azure storage sdk like [the blob library](https://pypi.org/project/azure-storage-blob/)

**Case (1)**, the datasets are registered in the workspace and thus we need to retrieve the workspace credentials. We already described how to perform that step in the _workspace_ section. Basically, when developing on a local machine, the credentials are retrieved from the portal and stored in a config.json file. When run on a remote machine, the workspace credentials are retrieved from the _run context_.

**Case (2)** is more common when using AML Pipelines as shown in [this example](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-move-data-in-out-of-pipelines)

**Case (3)** is less common but can be leverage when clients do not wish to use the datastore/dataset functionalities due to security concern. The main difference is that the access credentials to the data location is handled either directly through keyvault or through the AML workspace (which uses keyvault under the hood).

### Score/Infer

The scoring part is probably the less trivial to generalize. Indeed, it does not only depend on the training approach but also on the customer's constraints. AML proposes different methods to package the code and model, and also diverse deployment targets. Even though there are multiple ways to deploy a script, the core scoring script keeps most of the time the same structure. You can find an example in the _src_ folder.

For the deployment targets, you can find an exhaustive list of target under [Choose a compute target](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-and-where?tabs=azcli). It is worth noting that all the targets leverage Docker.

We will list here the different approach to package your service:

1. If the data science team manage a production target (AKS, VM, etc), the team can use the **Model Deploy** functionality and all the configuration is taken care of, as explained here [under deploy model](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-and-where?tabs=python).

2. In most companies, the production environment is managed by a dedicated team. For this scenario, one can choose to use the [**aml package**](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-package-models) approach or create a _Flask_ app hosted in a docker. In both cases, the production team receives a docker file to deploy.  
   - **Warning!** when using the aml package functionality, the docker file retrieve a base image from an azure container registry (ACR). This means that the production team has to have access to the ACR
  
   - In the second case, you have two options: either create your fully custom docker file with flask and download the model from the registry, or download the script from within the scoring script which means docker/aks has to have access to the workspace.

### Variable Handling

**!DO NOT ADDED ANY SECRETS OR KEYS IN CONFIGURATION FILES THAT ARE NOT PART OF THE GITIGNORE!**

There are many constants and variables to handle in a data science project, as for instance the datasets name, the model name, model variables, etc. It is important to distinguish between configuration variables and environment variables. Indeed, environment variables only depend on the environment in which a script is run, i.e dev/stage/prod (or whatever the convention). Hence, we recommend to understand what needs to be stored in a config/settings file and what should come from the os environment. It is not necessary to define a specific _.ENV_ files as the variables will be added in the CI/CD pipelines in Azure DevOps (or whatever DevOps tool one uses). Indeed, when developing in dev, we can simply use the default function ```os.getenv('ENV_VARIABLE', 'your-dev-env-variable')```.

For standard configuration variables, there is **one main guideline to follow**: Core Scripts should not contain any hardcoded variables in the code ! All variables must come from the scripts argument and may be hardcoded in the argument as default value as follows ``args.add_argument('--model_name',default='mymodel.pkl', type=str, help='')``. You might ask yourself now: 'what's this strange rule ?'. Well, all variables ought be in configuration files in a single place. This helps quickly adding/removing/updating variables. Ok, but we could still have added them to our Core Scripts. Again, you must remember that these scripts will eventually be run by our Op Scripts. These Op Scripts can easily handle the arguments from a config files to forward them to the Core Scripts. Indeed, the Op Scripts are commonly run in a virtual agent which contains all the project files. Thus, the path to the configuration will always be constant and there is no need to use ``sys.path`` or other cumbersome tricks to find the correct path.

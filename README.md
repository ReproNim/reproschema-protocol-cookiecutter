# reproschema-protocol-cookiecutter
A cookiecutter for ReproSchema protocols.

## Prerequisites

The following are required and recommended tools for using this cookiecutter and the ReproSchema protocol that it generates. This is all a one-time setup, so if you have already done it, skip to the [next section](#creating-a-new-project)!

  * **pipx**
  
    pipx is a tool for managing isolated Python-based applications. It is the recommended way to install Poetry and cruft. To install pipx follow the instructions here: https://pypa.github.io/pipx/installation/

  * **Poetry**
  
    Poetry is a Python project management tool. You will use it in your generated project to manage dependencies and build distribution files. If you have pipx installed you can install Poetry by running: 
     ```shell
     pipx install poetry
     ```
     For other installation methods see: https://python-poetry.org/docs/#installation
  
  * **cruft**

    cruft is a tool for generating projects based on a cookiecutter (like this one!) as well as keeping those projects updated if the original cookiecutter changes. Install it with pipx by running:
    ```shell
    pipx install cruft
    ```
    You may also choose to not have a persistent installation of cruft, in which case you would replace any calls to the `cruft` command below with `pipx run cruft`. 

## Creating a new project

### Step 1: Generate the project files

To generate a new LinkML project run the following:

```bash
cruft create https://github.com/ReproNim/reproschema-protocol-cookiecutter
```

You will be prompted for a few values.  The defaults are fine for most
protocols, but do name your protocol something that makes sense to you!
The interactive session will guide you through the process:

1. `protocol_name`: Name of the protocol, use kebab-case with no spaces.
Suggestions:
    - `reproschema-protocol`
    - `mood-protocol`
    - `media-selection`
    - `mental-health-survey`
2. `github_org`: Your GitHub username or organization name. This is used to construct links to documentation pages.
3. `protocol_description`: Description of the protocol.
    - A single brief sentence is recommended
    - Can easily be modified later
4. `number_of_activities`: How many activities/assessments do you want to create? Choose between 1 and 5; later, it will randomly generate the number of activities of your choice for your protocol.
5. `full_name`: Your name
6. `email`: Your email
7. `license`: Choose a license for the project. If your desired license is not listed, you can update or remove the `LICENSE` file in the generated project.

Then, go to your protocol folder
```bash
cd my-reproschema-protocol  # using the folder example above
```

### Step 2: Create a GitHub project

1. Go to https://github.com/new and follow the instructions, being sure NOT to add a `README` or `.gitignore` file (this cookiecutter template will take care of those files for you)

2. Add the remote to your local git repository

   ```bash
   git remote remove origin
   git remote add origin https://github.com/{github-user-or-organization}/{protocol-name}.git
   git branch -M main
   git push -u origin main
   ```
3. Create the gh-pages branch 
    - Fetch the latest changes from your repository (if any): 
        ```bash 
        git fetch origin 
        ``` 
    - Create and switch to the new gh-pages branch: 
        ```bash 
        git checkout -b gh-pages 
        ``` 
    This branch allows you to deploy your ReproSchema UI publicly. 
    
## Keeping your project up to date

In order to be up-to-date with the template, first check if there is a mismatch
between the project's boilerplate code and the template by running:

```bash
cruft check
```

This indicates if there is a difference between the current project's
boilerplate code and the latest version of the project template. If the project
is up-to-date with the template:

```output
SUCCESS: Good work! Project's cruft is up to date and as clean as possible :).
```

Otherwise, it will indicate that the project's boilerplate code is not
up-to-date by the following:

```output
FAILURE: Project's cruft is out of date! Run `cruft update` to clean this mess up.
```

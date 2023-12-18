# {{cookiecutter.protocol_name}}

{{cookiecutter.protocol_description}}

## Website

[https://{{cookiecutter.github_org}}.github.io/{{cookiecutter.protocol_name}}](https://{{cookiecutter.github_org}}.github.io/{{cookiecutter.protocol_name}})

## Repository Structure

* [{{cookiecutter.__protocol_slug}}/]({{cookiecutter.__protocol_slug}}/) - Contains protocol files
  * [schema]({{cookiecutter.__protocol_slug}}/{{cookiecutter.__protocol_slug}}_schema) - Reproschema protocol schema (edit this file)
  * [README.md]({{cookiecutter.__protocol_slug}}/README.md) - Welcome page of the protocol (edit this file)
* [activities/](activities/) - Contains activity files (edit these files)
* [ui-changes/src/config.js](ui-changes/src/config.js) - Source file for UI setup (edit this file)

## Developer Documentation

<details>
Use the `make` command to generate protocol artefacts:

* `make all`: make everything
* `make deploy`: deploys site
</details>

## Credits

This protocol was made with
[reproschema-protocol-cookiecutter](https://github.com/ReproNim/reproschema-protocol-cookiecutter).

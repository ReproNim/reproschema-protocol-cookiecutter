# {{cookiecutter.protocol_name}}

{{cookiecutter.protocol_description}}

## Website

[https://{{cookiecutter.github_org}}.github.io/{{cookiecutter.protocol_name|slugify}}](https://{{cookiecutter.github_org}}.github.io/{{cookiecutter.protocol_name|slugify}})

## Deployment to GitHub Pages

This repository includes automatic deployment to GitHub Pages. Follow these steps to enable it:

1. **Enable GitHub Pages in your repository:**
   - Go to Settings → Pages
   - Under "Source", select "GitHub Actions"
   - Click Save

2. **The deployment will trigger automatically when:**
   - You push to the `main` branch
   - You push a tag starting with `v` (e.g., `v1.0.0`)
   - You manually trigger the workflow from the Actions tab

3. **Deploy a specific version:**
   - Go to the Actions tab
   - Select "Deploy to GitHub Pages"
   - Click "Run workflow"
   - Enter the branch, tag, or commit SHA you want to deploy
   - Click "Run workflow"

4. **Access your deployed protocol:**
   - Once deployed, visit: `https://{{cookiecutter.github_org}}.github.io/{{cookiecutter.protocol_name|slugify}}`
   - The deployment typically takes 2-5 minutes
   - The deployed version is shown in the banner

## Repository Structure

* [{{cookiecutter.__protocol_slug}}/]({{cookiecutter.__protocol_slug}}/) - Contains protocol files
  * [schema]({{cookiecutter.__protocol_slug}}/{{cookiecutter.__protocol_slug}}_schema) - Reproschema protocol schema (edit this file)
  * [README.md]({{cookiecutter.__protocol_slug}}/README.md) - Welcome page of the protocol (edit this file)
* [activities/](activities/) - Contains activity files (edit these files)
* [ui-changes/src/config.js](ui-changes/src/config.js) - Source file for UI setup (edit this file)

## Credits

This protocol was made with
[reproschema-protocol-cookiecutter](https://github.com/ReproNim/reproschema-protocol-cookiecutter).

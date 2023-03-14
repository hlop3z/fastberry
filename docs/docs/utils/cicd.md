# (**CI/CD**) | **C**ontinuous **I**ntegration & **C**ontinuous **D**eployment

## Configure the **Stages** and **Scripts**

```yaml title=".git-ci.yml"
stages:
  - build
  - test
  - deploy

# Define build stage jobs
build:
  stage: build
  script:
    #- pip install -r requirements.txt
    - echo "Build"

# Define test stage jobs
unit_tests:
  stage: test
  script:
    #- pip install -r requirements.txt
    #- pytest -v tests/unit
    - echo "Unit-Tests"

integration_tests:
  stage: test
  script:
    #- pip install -r requirements.txt
    #- pytest -v tests/integration
    - echo "Integration-Tests"

# Define deploy stage jobs
deploy_to_staging:
  stage: deploy
  script:
    #- pip install -r requirements.txt
    #- deploy-script-for-staging.sh
    - echo "Deploy-To-Staging"

deploy_to_production:
  stage: deploy
  script:
    #- pip install -r requirements.txt
    #- deploy-script-for-production.sh
    - echo "Deploy-To-Production"
```

## **Pythonic** (Pipeline)

```python title="pipelines.py"
import sys
import yaml
import subprocess


def run_commands(commands):
    """Run All Scripts"""
    for command in commands:
        subprocess.call(command, shell=True)


def enforce_list(script):
    """Script(s) as List"""
    script = script or []
    if isinstance(script, str):
        script = [script]
    return script


def collect_jobs_by_stage(file_name: str):
    """Group Jobs By Stage"""

    # Load the pipeline definition from a YAML file
    with open(file_name, "r") as f:
        pipeline = yaml.safe_load(f)
    jobs_by_stage = {}

    # Group the jobs by stage
    for job in pipeline:
        if job != "stages":
            obj = pipeline[job]
            obj["name"] = job
            stage = obj["stage"]
            if stage not in jobs_by_stage:
                jobs_by_stage[stage] = []
            jobs_by_stage[stage].append(obj)
    return jobs_by_stage


def run_pipeline(
    stages: list | None = None, file_name: str = ".git-ci.yml", break_length: int = 45
):
    """CI/CD Pipeline"""

    jobs_by_stage = collect_jobs_by_stage(file_name)

    do_check = False
    if stages:
        do_check = True

    # Loop through each stage and execute the jobs in order
    for stage, jobs in jobs_by_stage.items():
        if do_check and stage not in stages:
            continue
        else:
            stage_text = f"Stage: {stage}"
            print("-" * break_length)
            print(stage_text)
            print("-" * break_length)
            for job in jobs:
                print(f'Executing job: {job["name"]}')
                script = job.get("script", [])
                script = enforce_list(script)
                run_commands(script)
                print(f'Job completed: {job["name"]}', end="\n\n")

    # Done
    print("=" * (break_length))
    print("All jobs completed.")


# Run Command
if len(sys.argv) > 1:
    stages = sys.argv[1]
    stages = list(map(lambda x: x.strip(), stages.split(" ")))
    run_pipeline(stages)
else:
    run_pipeline()
```

## **Run** Pipeline

```sh
python pipelines.py "build test deploy"
```

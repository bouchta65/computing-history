# Create Your First AI Agent with Microsoft Foundry

This repository is a hands-on lab for building, testing, and using your first AI agent with Microsoft Foundry, Visual Studio Code, Python, and a Flask web client.

The project walks you through creating a **Computing History Agent**: an AI assistant that can answer questions about the history of computing, computer pioneers, early machines, programming languages, operating systems, and the evolution of AI.

## What You Will Build

By the end of the lab, you will have:

- Created a Microsoft Foundry project.
- Deployed a generative AI model.
- Built and configured a prompt agent.
- Continued development in Visual Studio Code.
- Connected a Python Flask client app to your published agent.
- Used a dark chatbot interface to send prompts and display agent responses.

## Repository Description

**Create your first AI agent with Microsoft Foundry. Learn how to set up Azure and Foundry resources, deploy a model, create a prompt agent, continue development in Visual Studio Code, and connect the agent to a Python Flask chatbot client.**

Hosted documentation: [https://bouchta65.github.io/computing-history/documentation.html](https://bouchta65.github.io/computing-history/documentation.html)

## Prerequisites

Before starting, make sure you have:

- A Microsoft Azure subscription with permissions to create Foundry resources and deploy models.
- A GitHub account.
- Visual Studio Code installed.
- Python 3.13 or later installed.
- Git installed.
- Azure CLI installed.

## Lab Steps

### 1. Setup

Start with the setup guide:

[Instructions/Labs/00-setup.md](Instructions/Labs/00-setup.md)

In this step, you prepare your environment by checking required tools, Azure access, GitHub access, Python, Git, and Azure CLI.

### 2. Get Started in Microsoft Foundry

Continue with:

[Instructions/Labs/01-get-started-in-foundry.md](Instructions/Labs/01-get-started-in-foundry.md)

In this step, you:

- Create or open a Microsoft Foundry project.
- Deploy a model such as `gpt-4.1-mini`.
- Test the model in the playground.
- Add system instructions.
- Create a computing history agent.
- Publish or prepare the agent for use.

### 3. Continue in Visual Studio Code

Continue with:

[Instructions/Labs/02-continue-in-vscode.md](Instructions/Labs/02-continue-in-vscode.md)

In this step, you:

- Install the Foundry Toolkit extension for Visual Studio Code.
- Connect VS Code to your Foundry project.
- Open and test your agent from VS Code.
- Create a Python environment.
- Write code to call your agent by using the Azure AI Projects SDK and OpenAI Responses API.

### 4. Use Your Agent in a Client Application

Finish with:

[Instructions/Labs/03-use-agent.md](Instructions/Labs/03-use-agent.md)

In this step, you:

- Get the published agent endpoint from Microsoft Foundry.
- Configure the `.env` file in the client app.
- Install the Python dependencies.
- Run the Flask chatbot application.
- Send prompts to your agent from the browser UI.

## Client App

The chatbot client is in:

```text
computer-history-client/
```

Important files:

- `app.py`: Flask application and web routes.
- `agent_client.py`: Python client used to call the Foundry agent.
- `requirements.txt`: Python dependencies.
- `static/style.css`: Chatbot and documentation styling.
- `static/script.js`: Browser chat behavior.
- `.env`: Local configuration for your agent endpoint. This file is ignored by Git.

## Run the Client App Locally

From the repository root:

```powershell
cd computer-history-client
python -m pip install -r requirements.txt
python app.py
```

Then open:

```text
http://localhost:5000
```

If authentication fails, sign in with Azure CLI:

```powershell
az login
```

## Documentation Pages

The repository also includes an in-app documentation landing page:

[documentation.html](documentation.html)

From the chatbot UI, click **Documentation** to view the instruction pages.

## Notes

- The `.env` file should contain your local agent configuration and should not be committed.
- Some Microsoft Foundry screens may change over time because AI tooling evolves quickly.
- The generated agent responses can include mistakes, so verify important answers.

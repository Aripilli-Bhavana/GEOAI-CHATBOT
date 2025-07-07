
A local chatbot web application powered by Ollama's LLM models (e.g., llama3), designed for geospatial data interaction and question-answering. This project demonstrates how to connect a Flask-based chatbot frontend to an Ollama language model server, process user queries, and return context-aware answers based on your dataset.

---

## Table of Contents

- [Project Overview](#project-overview)  
- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Running the Application](#running-the-application)  
- [Connecting to Ollama LLM Server](#connecting-to-ollama-llm-server)  
- [Testing the Chatbot](#testing-the-chatbot)  
- [Project Structure](#project-structure)  
- [Troubleshooting](#troubleshooting)  
- [References](#references)  

---

## Project Overview

The **ollamacheck** project is a Flask-based web app that acts as a chatbot interface using Ollama's locally hosted LLM models like `llama3`. The chatbot answers questions specifically related to your geospatial dataset by querying the LLM server. It serves as a lightweight, modular proof-of-concept for integrating local LLMs into custom applications.

---

## Features

- Connects to Ollama LLM models locally or remotely.
- Provides an API for query processing and response fetching.
- Easily configurable IP and port to point to any Ollama LLM server.
- Context-aware chatbot designed to respond based on dataset content.
- Modular Flask backend with separate route handling.
- Scripts for running with Docker, native Windows PowerShell, or Linux shell.
- Designed for Uttarakhand geospatial data, but adaptable for other datasets.

---

## Prerequisites

- **Ollama** installed and configured on your machine or a reachable server.  
  (https://ollama.com/docs/getting-started)  
- Ollama LLM models downloaded (e.g., `llama3`).  
- Python 3.8 or higher installed.  
- Git (to clone this repo).  
- Optional: Docker installed if you want to run via Docker.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ollamacheck.git
   cd ollamacheck

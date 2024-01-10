# Ask Priya

Ask Priya is an AI chat bot that uses data from the USCIS website to answer questions you might have about immigration relating to the US.
It uses llama-index and Google Vertex AI behind the scenes to avoid many of the common pitfalls of using a large language model like ChatGPT on its own. When you ask it a question it searches through its index of data from the USCIS website and retrieves the most relevant "documents". It then passes along those documents along with your question to a LLM and asks it to answer you without straying outside of the documents given to it.

This reduces hallucination which is the phenomenon of models like ChatGPT making up a piece of information because it sounds like it would be true. Note: this is not a perfect process. Information given by Ask Priya is not legal advice and is not a substitute for a lawyer or official advisor.

[GitHub Page](https://github.com/fadilf/AskPriya)

To set things up your own, follow these steps:
- Clone the repository from GitHub
- Open the project's root directory in your terminal of choice.
- Create a virtual environment by running `python -m venv .venv`
- Install requirements by typing `pip install -r requirements.txt`
- Run the `create_index.ipynb` to create the index used by the application
- You are now ready to run the app!

To run the application:
- Activate the virtual environment by running `.\.venv\Scripts\activate` in the project's root directory
- Run `streamlit run ./app/main.py`

To generate an updated index:
- Create a CSV file using [this Colab notebook](https://colab.research.google.com/drive/1WS4jlYXG8YT4zvyorX4d-UjtsXjhO9ov?usp=sharing)
- Save the new CSV file in the `data`, replacing the old `uscis.csv` file.
- Remake the index using the `create_index.ipynb` file as done in the setup.
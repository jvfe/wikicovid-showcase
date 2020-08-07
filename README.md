# Showcasing COVID-19 data from Wikidata

Just exploring what sort of scientific data about COVID we can get from Wikidata and seeing ways to visualize it, as a way to introduce wikidata to other people. 

#### [Check it out on heroku](https://wikidata-covid.herokuapp.com/)

Or run it yourself:

* Clone the repo

```bash
git clone https://github.com/jvfe/wikicovid-showcase.git
cd wikicovid-showcase
```
* Create enviroment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

* Run app

```bash
streamlit run app.py
```

Most of the SPARQL queries I'm using were made by [Egon Willighagen](https://github.com/egonw/SARS-CoV-2-Queries) so thanks a lot to him.

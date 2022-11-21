# VisRuler: Visual Analytics for Extracting Decision Rules from Bagged and Boosted Decision Trees

This Git repository contains the code that accompanies the research paper "VisRuler: Visual Analytics for Extracting Decision Rules from Bagged and Boosted Decision Trees". The details of the experiments and the research outcome are described in [the paper](https://arxiv.org/abs/2112.00334).

**Note:** VisRuler is optimized to work better for standard resolutions (such as 1440p/QHD (Quad High Definition) and 1080p). Any other resolution might need manual adjustment of your browser's zoom level to work properly.

**Note:** The tag `paper-version` matches the implementation at the time of the paper's publication. The current version might look significantly different depending on how much time has passed since then.

**Note:** This software is based on the Random Forest, Adaptive Boosting, and Randomized Search implementations from [Scikit-learn](https://scikit-learn.org/stable/index.html) library. Although we used RANDOM_SEED = 42, the exact same input data for different systems might generate slightly different outputs due to the use of these libraries, and such differences will propagate to our software.

**Note:** As any other software, the code is not bug free. There might be limitations in the views and functionalities of the tool that could be addressed in a future code update.

# Data Sets #
All publicly available data sets used in the paper are in the `datasets` folder, formatted as comma separated values (csv). 
They are based on the data sets available online from [Kaggle](https://www.kaggle.com/) or the [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/index.php): World Happiness Report 2019, German Credit Data (slightly processed), and Iris Flower.

# Requirements #
For the backend:
- [Python 3](https://www.python.org/downloads/) (Version: 3.8.x)
- [MongoDB](https://www.mongodb.com/try/download/community) (Version: 4.x)
- Other packages: `pymongo`, `Flask`, `Flask-PyMongo`, `flask_cors`, `numpy`, `pandas`, `joblib`, `scikit-learn`, `umap`, and `math`.

One way to install MongoDB in macOS is by using Homebrew:
```
brew tap mongodb/brew
brew install mongodb-community@5.0
```

You can install all the backend requirements for Python with the following command:
```
pip install -r requirements.txt
```

For the frontend:
- [Node.js](https://nodejs.org/en/) (including Webpack; to install it, `npm install webpack-dev-server@3.7.1`)

There is no need to install anything further for the frontend (e.g., D3 and Plotly.js), since all modules are in the repository.

For the reproducibility of the first use case, the Red Wine Quality data set should be inserted to MongoDB by using the commands below:
```
# recommendation: use insertMongo script to add a data set in Mongo database
# for Python3
python3 insertMongo.py
```

# Usage #
Below is an example of how you can get VisRuler running using Python and Node.js for the backend and frontend, respectively. The frontend is written in JavaScript/HTML with the help of Vue.js framework, so it could be hosted in any other web server of your preference. The only hard requirement (currently) is that both frontend and backend must be running on the same machine. 
```
# first terminal: hosting the visualization side (client)
# with Node.js
cd frontend
npm install webpack-dev-server@3.7.1
npm run dev
```

```
# second terminal: hosting the computational side (server)
FLASK_APP=run.py flask run
```

Then, open your browser and point it to `localhost:8080`. We recommend using an up-to-date version of Google Chrome.

# Corresponding Author #
For any questions with regard to the implementation or the paper, feel free to contact [Angelos Chatzimparmpas](mailto:angelos.chatzimparmpas@lnu.se).

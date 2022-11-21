from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

import json
import copy
import warnings
import re
import random
import math  
import pandas as pd 
pd.set_option('use_inf_as_na', True)
import numpy as np
import multiprocessing
from operator import itemgetter
from rulelist import RuleList
import umap

from joblib import Memory
from joblib import Parallel, delayed

from sklearn import preprocessing

from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_predict

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split


from sklearn import metrics
from sklearn.cluster import DBSCAN

# this block of code is for the connection between the server, the database, and the client (plus routing)

# access MongoDB 
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"
mongo = PyMongo(app)

cors = CORS(app, resources={r"/data/*": {"origins": "*"}})

@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/Reset', methods=["GET", "POST"])
def reset():
    global DataRawLength
    global DataResultsRaw
    global previousState
    previousState = []

    global filterActionFinal
    filterActionFinal = ''

    global keySpecInternal
    keySpecInternal = 1

    global RANDOM_SEED
    RANDOM_SEED = 42

    global keyData
    keyData = 0

    global ModelSpaceUMAP
    ModelSpaceUMAP = []

    global keepOriginalFeatures
    keepOriginalFeatures = []

    global XData
    XData = []

    global roundValueSend 
    roundValueSend = 15

    global XDataNorm
    XDataNorm = []

    global yData
    yData = []

    global XDataNoRemoval
    XDataNoRemoval = []

    global XDataNoRemovalOrig
    XDataNoRemovalOrig = []
    
    global finalResultsData
    finalResultsData = []

    global detailsParams
    detailsParams = []

    global algorithmList
    algorithmList = []

    global ClassifierIDsList
    ClassifierIDsList = ''

    global RetrieveModelsList
    RetrieveModelsList = []

    global crossValidation
    crossValidation = 3

    global parametersSelData
    parametersSelData = []

    global target_names
    target_names = []

    global keyFirstTime
    keyFirstTime = True

    global target_namesLoc
    target_namesLoc = []

    global featureCompareData
    featureCompareData = []

    global columnsKeep
    columnsKeep = []

    global columnsNewGen
    columnsNewGen = []

    global columnsNames
    columnsNames = []

    global fileName
    fileName = []

    global results
    results = []

    global scoring
    scoring = {'accuracy': 'accuracy', 'precision_macro': 'precision_macro', 'recall_macro': 'recall_macro'}

    global names_labels
    names_labels = []

    global randomSearchVar
    randomSearchVar = 10

    global paramsRF
    paramsRF = {}
    
    global paramsAB
    paramsAB = {}

    return 'The reset was done!'

# retrieve data from client and select the correct data set
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/ServerRequest', methods=["GET", "POST"])
def retrieveFileName():
    global DataRawLength
    global DataResultsRaw
    global DataResultsRawTest
    global DataRawLengthTest

    global fileName
    fileName = []
    fileName = request.get_data().decode('utf8').replace("'", '"')
    print(fileName)
    global keySpecInternal
    keySpecInternal = 1

    global filterActionFinal
    filterActionFinal = ''

    global dataSpacePointsIDs
    dataSpacePointsIDs = []

    global RANDOM_SEED
    RANDOM_SEED = 42

    global keyData
    keyData = 0

    global ModelSpaceUMAP
    ModelSpaceUMAP = []

    global keepOriginalFeatures
    keepOriginalFeatures = []

    global XData
    XData = []

    global roundValueSend 
    roundValueSend = 15

    global XDataNorm
    XDataNorm = []

    global XDataNoRemoval
    XDataNoRemoval = []

    global XDataNoRemovalOrig
    XDataNoRemovalOrig = []

    global previousState
    previousState = []

    global scoring
    scoring = {'accuracy': 'accuracy', 'precision_macro': 'precision_macro', 'recall_macro': 'recall_macro'}

    global yData
    yData = []

    global finalResultsData
    finalResultsData = []

    global ClassifierIDsList
    ClassifierIDsList = ''

    global algorithmList
    algorithmList = []

    global detailsParams
    detailsParams = []

    # Initializing models

    global RetrieveModelsList
    RetrieveModelsList = []

    global resultsList
    resultsList = []

    global resultsRF
    global resultsAB 

    resultsRF = []
    resultsAB = []

    global crossValidation
    crossValidation = 3

    global parametersSelData
    parametersSelData = []

    global target_names
    
    target_names = []

    global keyFirstTime
    keyFirstTime = True

    global target_namesLoc
    target_namesLoc = []

    global names_labels
    names_labels = []

    global featureCompareData
    featureCompareData = []

    global columnsKeep
    columnsKeep = []

    global columnsNewGen
    columnsNewGen = []

    global columnsNames
    columnsNames = []

    global randomSearchVar
    randomSearchVar = 10

    global paramsRF
    paramsRF = {}
    
    global paramsAB
    paramsAB = {}

    DataRawLength = -1
    DataRawLengthTest = -1
    data = json.loads(fileName)  
    if data['fileName'] == 'HeartC':
        CollectionDB = mongo.db.HeartC.find()
        target_names.append('Healthy')
        target_names.append('Diseased')
    elif data['fileName'] == 'biodegC':
        StanceTest = True
        CollectionDB = mongo.db.biodegC.find()
        CollectionDBTest = mongo.db.biodegCTest.find()
        CollectionDBExternal = mongo.db.biodegCExt.find()
        target_names.append('Non-biodegr.')
        target_names.append('Biodegr.')
    elif data['fileName'] == 'breastC':
        CollectionDB = mongo.db.breastC.find()
        target_names.append('Malignant')
        target_names.append('Benign')
    elif data['fileName'] == 'TitanicC':
        CollectionDB = mongo.db.TitanicC.find()
        target_names.append('Survived')
        target_names.append('Died')
    elif data['fileName'] == 'CreditC':
        CollectionDB = mongo.db.CreditC.find()
        target_names.append('Rejected')
        target_names.append('Accepted')
    elif data['fileName'] == 'HappinessC':
        CollectionDB = mongo.db.HappinessC.find()
        target_names.append('HS-Level-1')
        target_names.append('HS-Level-2')
        target_names.append('HS-Level-3')
    elif data['fileName'] == 'diabetesC':
        CollectionDB = mongo.db.diabetesC.find()
        target_names.append('Positive')
        target_names.append('Negative')
    elif data['fileName'] == 'ContraceptiveC':
        CollectionDB = mongo.db.ContraceptiveC.find()
        target_names.append('Short-term')
        target_names.append('Long-term')
        target_names.append('No-use')
    elif data['fileName'] == 'VehicleC':
        CollectionDB = mongo.db.VehicleC.find()
        target_names.append('Van')
        target_names.append('Car')
        target_names.append('Bus')
    elif data['fileName'] == 'WineC':
        CollectionDB = mongo.db.WineC.find()
        target_names.append('Fine')
        target_names.append('Superior')
        target_names.append('Inferior')
    else:
        CollectionDB = mongo.db.IrisC.find()
    DataResultsRaw = []
    for index, item in enumerate(CollectionDB):
        item['_id'] = str(item['_id'])
        item['InstanceID'] = index
        DataResultsRaw.append(item)
    DataRawLength = len(DataResultsRaw)

    DataResultsRawTest = []

    dataSetSelection()

    return 'Everything is okay'

def dataSetSelection():

    global AllTargets
    global target_names
    global paramsRF
    global paramsAB
    global sendHyperRF
    global sendHyperAB

    target_namesLoc = []

    DataResults = copy.deepcopy(DataResultsRaw)

    for dictionary in DataResultsRaw:
        for key in dictionary.keys():
            if (key.find('*') != -1):
                target = key
                continue
        continue

    DataResultsRaw.sort(key=lambda x: x[target], reverse=True)
    DataResults.sort(key=lambda x: x[target], reverse=True)

    for dictionary in DataResults:
        del dictionary['_id']
        del dictionary['InstanceID']
        del dictionary[target]

    AllTargets = [o[target] for o in DataResultsRaw]
    AllTargetsFloatValues = []

    global fileName
    data = json.loads(fileName) 

    previous = None
    Class = 0
    for i, value in enumerate(AllTargets):
        if (i == 0):
            previous = value
            if (data['fileName'] == 'IrisC' or data['fileName'] == 'BreastC'):
                target_names.append(value)
            else:
                pass
        if (value == previous):
            AllTargetsFloatValues.append(Class)
        else:
            Class = Class + 1
            if (data['fileName'] == 'IrisC' or data['fileName'] == 'BreastC'):
                target_names.append(value)
            else:
                pass
            AllTargetsFloatValues.append(Class)
            previous = value

    ArrayDataResults = pd.DataFrame.from_dict(DataResults)

    global XData, yData, RANDOM_SEED
    XData, yData = ArrayDataResults, AllTargetsFloatValues

    global keepOriginalFeatures

    for col in XData.columns:
        keepOriginalFeatures.append(col)

    warnings.simplefilter('ignore')

    executeSearch()
    
    return 'Everything is okay'

# Initialize every model for each algorithm
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/ServerRequestSelParameters', methods=["GET", "POST"])
def executeSearch():
    
    global fileName
    global crossValidation
    global XData
    global XDataNorm
    global yData
    global RANDOM_SEED
    global target_names
    global keepOriginalFeatures
    global sendHyperRF
    global sendHyperAB
    global paramsRF
    global paramsAB
    global allParametersPerformancePerModel
    allParametersPerformancePerModel = []
    global randomSearchVar
    global X_train
    global Order
    global X_test
    global y_train
    global y_test
    global resultsRF
    global resultsAB 
    global roundValueSend

    resultsRF = []
    resultsAB = []
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(XData)

    x = XData.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    XDataNorm = pd.DataFrame(x_scaled)

    featureNamesLocal = []
    for col in XData.columns:
        featureNamesLocal.append(col+'_minLim')
        
    for col in XData.columns:
        featureNamesLocal.append(col+'_maxLim')

    for ind, value in enumerate(target_names):
        featureNamesLocal.append(str(ind))

    data = json.loads(fileName)  

    if data['fileName'] == 'TitanicC' or data['fileName'] == 'CreditC':
        X_train, X_test, y_train, y_test = train_test_split(XDataNorm, yData, test_size=0.1, stratify=yData, random_state=32)
    else:
        X_train, X_test, y_train, y_test = train_test_split(XDataNorm, yData, test_size=0.1, stratify=yData, random_state=RANDOM_SEED)
    print(X_test)
    X_train = X_train.reset_index(drop=True)
    X_test = X_test.reset_index(drop=True)

    algorithms = ['RF', 'AB']

    X_train.columns = keepOriginalFeatures

    countNumberOfFeatures = 0
    for col in XData.columns:
        countNumberOfFeatures = countNumberOfFeatures + 1
    rootSQ = int(math.sqrt(countNumberOfFeatures))

    paramsRF = {'n_estimators': list(range(2, 21)), 'max_depth': list(range(10, 26)), 'min_samples_leaf': list(range(1,11)), 'max_features':list(range(rootSQ,countNumberOfFeatures)) } # (2,21) (10,26) and (1,11)
    sendHyperRF = paramsRF
    paramsAB = {'n_estimators': list(range(2, 21)), 'base_estimator__max_depth': list(range(10, 26)), 'learning_rate': list(np.arange(0.1,0.4,0.1)), 'base_estimator__min_samples_leaf':list(range(1,11))}
    sendHyperAB = paramsAB

    for eachAlgor in algorithms:
        if (eachAlgor) == 'RF':
            clf = RandomForestClassifier(random_state=RANDOM_SEED)
            AlgorithmsIDsEnd = 0
            resultsLocalRF = randomSearchRF(XData, X_train, y_train, X_test, clf, paramsRF, eachAlgor, AlgorithmsIDsEnd, crossValidation, randomSearchVar, RANDOM_SEED, roundValueSend) 
        else: 
            clf = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(), random_state=RANDOM_SEED)
            AlgorithmsIDsEnd = randomSearchVar
            resultsLocalAB = randomSearchAB(XData, X_train, y_train, X_test, clf, paramsAB, eachAlgor, AlgorithmsIDsEnd, crossValidation, randomSearchVar, RANDOM_SEED, roundValueSend)  
    
    allParametersPerformancePerModel = resultsLocalRF + resultsLocalAB
    jsonFileRF = []
    jsonFileRF = json.loads(allParametersPerformancePerModel[6])
    frameRF = []
    frameRF = pd.read_json(jsonFileRF)

    jsonFileGB = []
    jsonFileGB = json.loads(allParametersPerformancePerModel[23])
    frameGB = pd.DataFrame()
    frameGB = pd.read_json(jsonFileGB)

    predValueRF = []
    predValueRF = json.loads(allParametersPerformancePerModel[10])
    predValueRFRead = pd.DataFrame()
    predValueRFRead = pd.read_json(predValueRF)

    predValueGB = []
    predValueGB = json.loads(allParametersPerformancePerModel[27])
    predValueGBRead = pd.DataFrame()
    predValueGBRead = pd.read_json(predValueGB)

    together = pd.DataFrame()
    together = pd.concat([frameRF, frameGB])
    together = together.reset_index(drop=True)

    togetherPredValue = pd.DataFrame()
    togetherPredValue = pd.concat([predValueRFRead, predValueGBRead])
    togetherPredValue = togetherPredValue.reset_index(drop=True)

    epsilon = 0.3
    minSamples = range(5,51)
    storePosition = -1
    findMax = 0
    for i in minSamples:
        db = DBSCAN(eps=epsilon, min_samples=i, n_jobs=-1).fit(together)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        if ((metrics.adjusted_rand_score(togetherPredValue['predicted_value'], labels)) > findMax):
            findMax = metrics.adjusted_rand_score(togetherPredValue['predicted_value'], labels)
            storePosition = i

    db = DBSCAN(eps=epsilon, min_samples=storePosition, n_jobs=-1).fit(together)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    #n_noise_ = list(labels).count(-1)

    print('Estimated number of clusters: %d' % n_clusters_)
    #print('Estimated number of noise points: %d' % n_noise_)
    print(findMax)

    if (n_clusters_ > 100):
        n_clusters_ = 100
    elif (n_clusters_ == 1):
        n_clusters_ = 2
    else:
        pass

    global ModelSpaceUMAP
    ModelSpaceUMAP = FunUMAP(together, n_clusters_)

    SendEachClassifiersPerformanceToVisualize()

    return 'Everything Okay'

location = './cachedir'
memory = Memory(location, verbose=0)

@memory.cache
def randomSearchRF(XData, X_train, y_train, X_test, clf, params, eachAlgor, AlgorithmsIDsEnd, crossValidation, randomS, RANDOM_SEED, roundValue):
    print('insideRFNow!!!')
    # this is the grid we use to train the models
    randSear = RandomizedSearchCV(    
        estimator=clf, param_distributions=params, n_iter=randomS,
        cv=crossValidation, refit='accuracy', scoring=scoring,
        verbose=0, n_jobs=-1, random_state=RANDOM_SEED)

    # fit and extract the probabilities
    randSear.fit(X_train, y_train)

    # process the results
    cv_results = []
    cv_results.append(randSear.cv_results_)
    df_cv_results = pd.DataFrame.from_dict(cv_results)

    number_of_models = []
    # number of models stored
    number_of_models = len(df_cv_results.iloc[0][0])

    # initialize results per row
    df_cv_results_per_row = []

    modelsIDs = []
    for i in range(number_of_models):
        number = AlgorithmsIDsEnd+i
        modelsIDs.append(eachAlgor+str(number))
        df_cv_results_per_item = []
        for column in df_cv_results.iloc[0]:
            df_cv_results_per_item.append(column[i])
        df_cv_results_per_row.append(df_cv_results_per_item)

    df_cv_results_classifiers = pd.DataFrame()
    # store the results into a pandas dataframe
    df_cv_results_classifiers = pd.DataFrame(data = df_cv_results_per_row, columns= df_cv_results.columns)

    # copy and filter in order to get only the metrics
    metrics = df_cv_results_classifiers.copy()
    metrics = metrics.filter(['mean_test_accuracy', 'mean_test_precision_macro', 'mean_test_recall_macro',]) 

    parametersPerformancePerModel = pd.DataFrame()
    # concat parameters and performance
    parametersPerformancePerModel = pd.DataFrame(df_cv_results_classifiers['params'])
    parametersPerformancePerModel = parametersPerformancePerModel.to_json(double_precision=15)

    parametersLocal = json.loads(parametersPerformancePerModel)['params'].copy()
    Models = []
    for index, items in enumerate(parametersLocal):
        Models.append(str(index))

    parametersLocalNew = [ parametersLocal[your_key] for your_key in Models ]

    perModelProb = []
    confuseFP = []
    confuseFN = []
    featureImp = []
    collectDecisionsPerModel = pd.DataFrame()
    collectDecisions = []
    collectLocationsAll = []
    collectDecisionsMod = []
    collectStatistics = []
    collectStatisticsMod = []
    collectStatisticsPerModel = []
    collectInfoPerModel = []
    yPredictTestList = []
    perModelPrediction = []
    storeTrain = []
    storePredict = []
    
    featureNames = []
    featureNamesDuplicated = []
    
    for col in XData.columns:
        featureNames.append(col)
        featureNamesDuplicated.append(col+'_minLim')
    for col in XData.columns:
        featureNamesDuplicated.append(col+'_maxLim')
    
    counterModels = 1
    for eachModelParameters in parametersLocalNew:
        collectDecisions = []
        collectLocations = []
        collectStatistics = []
        sumRes = 0
        clf.set_params(**eachModelParameters)
        np.random.seed(RANDOM_SEED) # seeds
        clf.fit(X_train, y_train) 
        yPredictTest = clf.predict(X_test)
        yPredictTestList.append(yPredictTest)

        feature_importances = clf.feature_importances_
        feature_importances[np.isnan(feature_importances)] = 0
        featureImp.append(list(feature_importances))

        yPredict = cross_val_predict(clf, X_train, y_train, cv=crossValidation)
        yPredict = np.nan_to_num(yPredict)
        perModelPrediction.append(yPredict)

        yPredictProb = cross_val_predict(clf, X_train, y_train, cv=crossValidation, method='predict_proba')
        yPredictProb = np.nan_to_num(yPredictProb)
        perModelProb.append(yPredictProb.tolist())

        storeTrain.append(y_train)
        storePredict.append(yPredict)
        cnf_matrix = confusion_matrix(y_train, yPredict)
        FP = cnf_matrix.sum(axis=0) - np.diag(cnf_matrix) 
        FN = cnf_matrix.sum(axis=1) - np.diag(cnf_matrix)
        FP = FP.astype(float)
        FN = FN.astype(float)
        confuseFP.append(list(FP))
        confuseFN.append(list(FN))
        for tree_idx, est in enumerate(clf.estimators_):
            decisionPath = extractDecisionInfo(est,counterModels,tree_idx,X_train,y_train,featureNamesDuplicated,eachAlgor,feature_names=featureNames,only_leaves=True)
            if (roundValue == -1):
                pass
            else:
                decisionPath[0] = decisionPath[0].round(roundValue)
            collectDecisions.append(decisionPath[0])
            collectStatistics.append(decisionPath[1])
            sumRes = sumRes + decisionPath[2]
            collectLocations.append(decisionPath[3])
        collectDecisionsMod.append(collectDecisions)
        collectStatisticsMod.append(collectStatistics)
        collectInfoPerModel.append(sumRes)
        collectLocationsAll.append(collectLocations)
        counterModels = counterModels + 1

    collectInfoPerModelPandas = pd.DataFrame(collectInfoPerModel)

    totalfnList = []
    totalfpList = []
    numberClasses = [y_train.index(x) for x in set(y_train)]
    if (len(numberClasses) == 2):
        for index,nList in enumerate(storeTrain):
            fnList = []
            fpList = []
            for ind,el in enumerate(nList):
                if (el==1 and storePredict[index][ind]==0):
                    fnList.append(ind)
                elif (el==0 and storePredict[index][ind]==1):
                    fpList.append(ind)
                else:
                    pass   
            totalfpList.append(fpList)
            totalfnList.append(fnList)
    else:
        for index,nList in enumerate(storeTrain):
            fnList = []
            class0fn = []
            class1fn = []
            class2fn = []
            for ind,el in enumerate(nList):
                if (el==0 and storePredict[index][ind]==1):
                    class0fn.append(ind)
                elif (el==0 and storePredict[index][ind]==2):
                    class0fn.append(ind)
                elif (el==1 and storePredict[index][ind]==0):
                    class1fn.append(ind)
                elif (el==1 and storePredict[index][ind]==2):
                    class1fn.append(ind)
                elif (el==2 and storePredict[index][ind]==0):
                    class2fn.append(ind)
                elif (el==2 and storePredict[index][ind]==1):
                    class2fn.append(ind)
                else:
                    pass  
            fnList.append(class0fn)
            fnList.append(class1fn)
            fnList.append(class2fn)
            totalfnList.append(fnList)
        for index,nList in enumerate(storePredict):
            fpList = []
            class0fp = []
            class1fp = []
            class2fp = []
            for ind,el in enumerate(nList):
                if (el==0 and storeTrain[index][ind]==1):
                    class0fp.append(ind)
                elif (el==0 and storeTrain[index][ind]==2):
                    class0fp.append(ind)
                elif (el==1 and storeTrain[index][ind]==0):
                    class1fp.append(ind)
                elif (el==1 and storeTrain[index][ind]==2):
                    class1fp.append(ind)
                elif (el==2 and storeTrain[index][ind]==0):
                    class2fp.append(ind)
                elif (el==2 and storeTrain[index][ind]==1):
                    class2fp.append(ind)
                else:
                    pass  
            fpList.append(class0fp)
            fpList.append(class1fp)
            fpList.append(class2fp)
            totalfpList.append(fpList)
    
    # for index, nList in enumerate(totalfpList):
    #     if ((index+1) != len(totalfpList)):
    #         confuseFPCommon.append(len(list(set(nList).intersection(totalfpList[index+1]))))
    # for index, nList in enumerate(totalfnList):
    #     if ((index+1) != len(totalfnList)):
    #         confuseFNCommon.append(len(list(set(nList).intersection(totalfnList[index+1]))))

    summarizeResults = []
    summarizeResults = metrics.sum(axis=1)
    summarizeResultsFinal = []
    for el in summarizeResults:
        summarizeResultsFinal.append(round(((el * 100)/3),2))

    indices, L_sorted = zip(*sorted(enumerate(summarizeResultsFinal), key=itemgetter(1)))
    indexList = list(indices)

    collectDecisionsSorted = []
    collectStatisticsSorted = []
    collectLocationsAllSorted = []
    for el in indexList:
        for item in collectDecisionsMod[el]:
            collectDecisionsSorted.append(item)
        for item2 in collectStatisticsMod[el]:
            collectStatisticsSorted.append(item2)
        for item3 in collectLocationsAll[el]:
            collectLocationsAllSorted.append(item3)

    collectDecisionsPerModel = pd.concat(collectDecisionsSorted)
    collectStatisticsPerModel = pd.concat(collectStatisticsSorted)
    collectLocationsAllPerSorted = pd.DataFrame(collectLocationsAllSorted)
    collectDecisionsPerModel = collectDecisionsPerModel.reset_index(drop=True)
    collectStatisticsPerModel = collectStatisticsPerModel.reset_index(drop=True) 
    collectLocationsAllPerSorted = collectLocationsAllPerSorted.reset_index(drop=True) 

    collectDecisionsPerModel = collectDecisionsPerModel.to_json(double_precision=15)
    collectStatisticsPerModel = collectStatisticsPerModel.to_json(double_precision=15)
    collectInfoPerModelPandas = collectInfoPerModelPandas.to_json(double_precision=15)
    collectLocationsAllPerSorted = collectLocationsAllPerSorted.to_json(double_precision=15)

    perModelPredPandas = pd.DataFrame(perModelPrediction)
    perModelPredPandas = perModelPredPandas.to_json(double_precision=15)

    yPredictTestListPandas = pd.DataFrame(yPredictTestList)
    yPredictTestListPandas = yPredictTestListPandas.to_json(double_precision=15)

    perModelProbPandas = pd.DataFrame(perModelProb)
    perModelProbPandas = perModelProbPandas.to_json(double_precision=15)

    metrics = metrics.to_json(double_precision=15)
    # gather the results and send them back
    resultsRF.append(modelsIDs) # 0 
    resultsRF.append(parametersPerformancePerModel) # 1
    resultsRF.append(metrics) # 2
    resultsRF.append(json.dumps(confuseFP)) # 3
    resultsRF.append(json.dumps(confuseFN)) # 4
    resultsRF.append(json.dumps(featureImp)) # 5
    resultsRF.append(json.dumps(collectDecisionsPerModel)) # 6
    resultsRF.append(perModelProbPandas) # 7
    resultsRF.append(json.dumps(perModelPredPandas)) # 8
    resultsRF.append(json.dumps(target_names)) # 9
    resultsRF.append(json.dumps(collectStatisticsPerModel)) # 10
    resultsRF.append(json.dumps(collectInfoPerModelPandas)) # 11
    resultsRF.append(json.dumps(keepOriginalFeatures)) # 12
    resultsRF.append(json.dumps(yPredictTestListPandas)) # 13
    resultsRF.append(json.dumps(collectLocationsAllPerSorted)) # 14
    resultsRF.append(json.dumps(totalfpList)) # 15
    resultsRF.append(json.dumps(totalfnList)) # 16

    return resultsRF

location = './cachedir'
memory = Memory(location, verbose=0)

@memory.cache
def randomSearchAB(XData, X_train, y_train, X_test, clf, params, eachAlgor, AlgorithmsIDsEnd, crossValidation, randomS, RANDOM_SEED, roundValue):
    print('insideABNow!!!')
    # this is the grid we use to train the models
    randSear = RandomizedSearchCV(    
        estimator=clf, param_distributions=params, n_iter=randomS,
        cv=crossValidation, refit='accuracy', scoring=scoring,
        verbose=0, n_jobs=-1, random_state=RANDOM_SEED)

    # fit and extract the probabilities
    randSear.fit(X_train, y_train)

    # process the results
    cv_results = []
    cv_results.append(randSear.cv_results_)
    df_cv_results = pd.DataFrame.from_dict(cv_results)

    number_of_models = []
    # number of models stored
    number_of_models = len(df_cv_results.iloc[0][0])

    # initialize results per row
    df_cv_results_per_row = []

    modelsIDs = []
    for i in range(number_of_models):
        number = AlgorithmsIDsEnd+i
        modelsIDs.append(eachAlgor+str(number))
        df_cv_results_per_item = []
        for column in df_cv_results.iloc[0]:
            df_cv_results_per_item.append(column[i])
        df_cv_results_per_row.append(df_cv_results_per_item)

    df_cv_results_classifiers = pd.DataFrame()
    # store the results into a pandas dataframe
    df_cv_results_classifiers = pd.DataFrame(data = df_cv_results_per_row, columns= df_cv_results.columns)

    # copy and filter in order to get only the metrics
    metrics = df_cv_results_classifiers.copy()
    metrics = metrics.filter(['mean_test_accuracy', 'mean_test_precision_macro', 'mean_test_recall_macro',]) 

    parametersPerformancePerModel = pd.DataFrame()
    # concat parameters and performance
    parametersPerformancePerModel = pd.DataFrame(df_cv_results_classifiers['params'])
    parametersPerformancePerModel = parametersPerformancePerModel.to_json(double_precision=15)

    parametersLocal = json.loads(parametersPerformancePerModel)['params'].copy()
    Models = []
    for index, items in enumerate(parametersLocal):
        Models.append(str(index))

    parametersLocalNew = [ parametersLocal[your_key] for your_key in Models ]

    perModelProb = []
    confuseFP = []
    confuseFN = []
    featureImp = []
    collectDecisionsPerModel = pd.DataFrame()
    collectDecisions = []
    collectDecisionsMod = []
    collectLocationsAll = []
    collectStatistics = []
    collectStatisticsMod = []
    collectStatisticsPerModel = []
    collectInfoPerModel = []
    yPredictTestList = []
    perModelPrediction = []
    storeTrain = []
    storePredict = []
    
    featureNames = []
    featureNamesDuplicated = []
    
    for col in XData.columns:
        featureNames.append(col)
        featureNamesDuplicated.append(col+'_minLim')
    for col in XData.columns:
        featureNamesDuplicated.append(col+'_maxLim')
    
    counterModels = 1
    for eachModelParameters in parametersLocalNew:
        collectDecisions = []
        collectLocations = []
        collectStatistics = []
        sumRes = 0
        clf.set_params(**eachModelParameters)
        np.random.seed(RANDOM_SEED) # seeds
        clf.fit(X_train, y_train) 
        yPredictTest = clf.predict(X_test)
        yPredictTestList.append(yPredictTest)

        feature_importances = clf.feature_importances_
        feature_importances[np.isnan(feature_importances)] = 0
        featureImp.append(list(feature_importances))

        yPredict = cross_val_predict(clf, X_train, y_train, cv=crossValidation)
        yPredict = np.nan_to_num(yPredict)
        perModelPrediction.append(yPredict)

        yPredictProb = cross_val_predict(clf, X_train, y_train, cv=crossValidation, method='predict_proba')
        yPredictProb = np.nan_to_num(yPredictProb)
        perModelProb.append(yPredictProb.tolist())

        storeTrain.append(y_train)
        storePredict.append(yPredict)
        cnf_matrix = confusion_matrix(y_train, yPredict)
        FP = cnf_matrix.sum(axis=0) - np.diag(cnf_matrix) 
        FN = cnf_matrix.sum(axis=1) - np.diag(cnf_matrix)
        FP = FP.astype(float)
        FN = FN.astype(float)
        confuseFP.append(list(FP))
        confuseFN.append(list(FN))
        for tree_idx, est in enumerate(clf.estimators_):
            decisionPath = extractDecisionInfo(est,counterModels,tree_idx,X_train,y_train,featureNamesDuplicated,eachAlgor,feature_names=featureNames,only_leaves=True)
            if (roundValue == -1):
                pass
            else:
                decisionPath[0] = decisionPath[0].round(roundValue)
            collectDecisions.append(decisionPath[0])
            collectStatistics.append(decisionPath[1])
            sumRes = sumRes + decisionPath[2]
            collectLocations.append(decisionPath[3])
        collectDecisionsMod.append(collectDecisions)
        collectStatisticsMod.append(collectStatistics)
        collectInfoPerModel.append(sumRes)
        collectLocationsAll.append(collectLocations)
        counterModels = counterModels + 1

    collectInfoPerModelPandas = pd.DataFrame(collectInfoPerModel)

    totalfnList = []
    totalfpList = []
    numberClasses = [y_train.index(x) for x in set(y_train)]
    if (len(numberClasses) == 2):
        for index,nList in enumerate(storeTrain):
            fnList = []
            fpList = []
            for ind,el in enumerate(nList):
                if (el==1 and storePredict[index][ind]==0):
                    fnList.append(ind)
                elif (el==0 and storePredict[index][ind]==1):
                    fpList.append(ind)
                else:
                    pass   
            totalfpList.append(fpList)
            totalfnList.append(fnList)
    else:
        for index,nList in enumerate(storeTrain):
            fnList = []
            class0fn = []
            class1fn = []
            class2fn = []
            for ind,el in enumerate(nList):
                if (el==0 and storePredict[index][ind]==1):
                    class0fn.append(ind)
                elif (el==0 and storePredict[index][ind]==2):
                    class0fn.append(ind)
                elif (el==1 and storePredict[index][ind]==0):
                    class1fn.append(ind)
                elif (el==1 and storePredict[index][ind]==2):
                    class1fn.append(ind)
                elif (el==2 and storePredict[index][ind]==0):
                    class2fn.append(ind)
                elif (el==2 and storePredict[index][ind]==1):
                    class2fn.append(ind)
                else:
                    pass  
            fnList.append(class0fn)
            fnList.append(class1fn)
            fnList.append(class2fn)
            totalfnList.append(fnList)
        for index,nList in enumerate(storePredict):
            fpList = []
            class0fp = []
            class1fp = []
            class2fp = []
            for ind,el in enumerate(nList):
                if (el==0 and storeTrain[index][ind]==1):
                    class0fp.append(ind)
                elif (el==0 and storeTrain[index][ind]==2):
                    class0fp.append(ind)
                elif (el==1 and storeTrain[index][ind]==0):
                    class1fp.append(ind)
                elif (el==1 and storeTrain[index][ind]==2):
                    class1fp.append(ind)
                elif (el==2 and storeTrain[index][ind]==0):
                    class2fp.append(ind)
                elif (el==2 and storeTrain[index][ind]==1):
                    class2fp.append(ind)
                else:
                    pass  
            fpList.append(class0fp)
            fpList.append(class1fp)
            fpList.append(class2fp)
            totalfpList.append(fpList)
    
    summarizeResults = []
    summarizeResults = metrics.sum(axis=1)
    summarizeResultsFinal = []
    for el in summarizeResults:
        summarizeResultsFinal.append(round(((el * 100)/3),2))

    indices, L_sorted = zip(*sorted(enumerate(summarizeResultsFinal), key=itemgetter(1)))
    indexList = list(indices)

    collectDecisionsSorted = []
    collectStatisticsSorted = []
    collectLocationsAllSorted = []
    for el in indexList:
        for item in collectDecisionsMod[el]:
            collectDecisionsSorted.append(item)
        for item2 in collectStatisticsMod[el]:
            collectStatisticsSorted.append(item2)
        for item3 in collectLocationsAll[el]:
            collectLocationsAllSorted.append(item3)

    collectDecisionsPerModel = pd.concat(collectDecisionsSorted)
    collectStatisticsPerModel = pd.concat(collectStatisticsSorted)
    collectLocationsAllPerSorted = pd.DataFrame(collectLocationsAllSorted)

    collectDecisionsPerModel = collectDecisionsPerModel.reset_index(drop=True)
    collectStatisticsPerModel = collectStatisticsPerModel.reset_index(drop=True) 
    collectLocationsAllPerSorted = collectLocationsAllPerSorted.reset_index(drop=True) 
    collectDecisionsPerModel = collectDecisionsPerModel.to_json(double_precision=15)
    collectStatisticsPerModel = collectStatisticsPerModel.to_json(double_precision=15)
    collectInfoPerModelPandas = collectInfoPerModelPandas.to_json(double_precision=15)
    collectLocationsAllPerSorted = collectLocationsAllPerSorted.to_json(double_precision=15)

    perModelPredPandas = pd.DataFrame(perModelPrediction)
    perModelPredPandas = perModelPredPandas.to_json(double_precision=15)

    yPredictTestListPandas = pd.DataFrame(yPredictTestList)
    yPredictTestListPandas = yPredictTestListPandas.to_json(double_precision=15)

    perModelProbPandas = pd.DataFrame(perModelProb)
    perModelProbPandas = perModelProbPandas.to_json(double_precision=15)

    metrics = metrics.to_json(double_precision=15)
    # gather the results and send them back
    resultsAB.append(modelsIDs) # 0 17
    resultsAB.append(parametersPerformancePerModel) # 1 18
    resultsAB.append(metrics) # 2 19
    resultsAB.append(json.dumps(confuseFP)) # 3 20
    resultsAB.append(json.dumps(confuseFN)) # 4 21
    resultsAB.append(json.dumps(featureImp)) # 5 22
    resultsAB.append(json.dumps(collectDecisionsPerModel)) # 6 23
    resultsAB.append(perModelProbPandas) # 7 24
    resultsAB.append(json.dumps(perModelPredPandas)) # 8 25
    resultsAB.append(json.dumps(target_names)) # 9 26
    resultsAB.append(json.dumps(collectStatisticsPerModel)) # 10 27
    resultsAB.append(json.dumps(collectInfoPerModelPandas)) # 11 28
    resultsAB.append(json.dumps(keepOriginalFeatures)) # 12 29
    resultsAB.append(json.dumps(yPredictTestListPandas)) # 13 30
    resultsAB.append(json.dumps(collectLocationsAllPerSorted)) # 14 31
    resultsAB.append(json.dumps(totalfpList)) # 15 32
    resultsAB.append(json.dumps(totalfnList)) # 16 33

    return resultsAB

def extractDecisionInfo(decision_tree,counterModels,tree_index,X_train,y_train,feature_names_duplicated,eachAlgor,feature_names=None,only_leaves=True):
    '''return dataframe with node info
    '''
    decision_tree.fit(X_train, y_train)
    # extract info from decision_tree
    n_nodes = decision_tree.tree_.node_count
    children_left = decision_tree.tree_.children_left
    children_right = decision_tree.tree_.children_right
    feature = decision_tree.tree_.feature
    threshold = decision_tree.tree_.threshold
    impurity = decision_tree.tree_.impurity
    value = decision_tree.tree_.value
    n_node_samples = decision_tree.tree_.n_node_samples

    whereTheyBelong = decision_tree.apply(X_train)

    # cast X_train as dataframe
    df = pd.DataFrame(X_train)
    if feature_names is not None:
        df.columns = feature_names
    
    # indexes with unique nodes
    idx_list = df.assign(
        leaf_id = lambda df: decision_tree.apply(df)
    )[['leaf_id']].drop_duplicates().index

    # test data for unique nodes
    X_test = df.loc[idx_list,].to_numpy()
    # decision path only for leaves
    dp = decision_tree.decision_path(X_test)
    # final leaves for each data
    leave_id = decision_tree.apply(X_test)
    # values for each data
    leave_predict = decision_tree.predict(X_test)
    # dictionary for leave_id and leave_predict
    dict_leaves = {k:v for k,v in zip(leave_id,leave_predict)}
    
    # create decision path information for all nodes
    dp_idxlist = [[ini, fin] for ini,fin in zip(dp.indptr[:-1],dp.indptr[1:])]
    dict_decisionpath = {}
    for idxs in dp_idxlist:
        dpindices = dp.indices[idxs[0]:idxs[1]]
        for i,node in enumerate(dpindices):
            if node not in dict_decisionpath.keys():
                dict_decisionpath[node] = dpindices[:i+1]
    
    # initialize number of columns and output dataframe
    n_cols = df.shape[-1]
    df_thr_all = pd.DataFrame()

    # predict for samples
    for node, node_index in dict_decisionpath.items():
        l_thresh_max = np.ones(n_cols) * np.nan
        l_thresh_min = np.ones(n_cols) * np.nan
        
        # decision path info for each node
        for i,node_id in enumerate(node_index):
            if node == node_id:
                continue

            if children_left[node_id] == node_index[i+1]: #(X_test[sample_id, feature[node_id]] <= threshold[node_id]):
                l_thresh_max[feature[node_id]] = threshold[node_id]
            else:
                l_thresh_min[feature[node_id]] = threshold[node_id]
        # append info to df_thr_all
        df_thr_all = df_thr_all.append(
            [[thr_min for thr_max,thr_min in zip(l_thresh_max,l_thresh_min)]
             + [thr_max for thr_max,thr_min in zip(l_thresh_max,l_thresh_min)]
             + [
                 node,
                 counterModels,
                 tree_index,
                 np.nan if node not in dict_leaves.keys() else dict_leaves[node],
                 #value[node],
                 impurity[node],
                 n_node_samples[node]
               ]
            ]
        )
    # rename columns and set index
    if feature_names is not None:
        df_thr_all.columns = feature_names_duplicated + ['node','counterModels','tree_index','predicted_value','impurity','samples']
    else:
        df_thr_all.columns = ['X_{}'.format(i) for i in range(n_cols)] + ['node','counterModels','tree_index','predicted_value','impurity','samples']
    #df_thr_all = df_thr_all.set_index('decision')
    #df_thr_all = df_thr_all.reset_index(drop=True)
    if only_leaves:
        df_thr_all = df_thr_all[~df_thr_all['predicted_value'].isnull()]
        df_thr_all['impurity'].loc[df_thr_all['impurity'] < 0] = 0
        # df_thr_all['impurity'].loc[df_thr_all['impurity'] >= 0.5] = 0.8

    # del df_thr_all['decision']
    # del df_thr_all['predicted_value']

    #df_thr_all.reset_index()

    df_thr_all = df_thr_all.replace(np.nan,2) # nan mapped as value 2

    #df_thr_all = df_thr_all.sort_index()
    
    copy_df_thr_all = df_thr_all.copy()

    del df_thr_all['node']
    del df_thr_all['counterModels']
    del df_thr_all['tree_index']
    del df_thr_all['predicted_value']
    del df_thr_all['impurity']
    del df_thr_all['samples']

    copy_df_thr_all = copy_df_thr_all[['node','counterModels','tree_index','predicted_value', 'impurity', 'samples']]
    return [df_thr_all,copy_df_thr_all,len(df_thr_all),whereTheyBelong]

# Sending each model's results to frontend
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/PerformanceForEachModel', methods=["GET", "POST"])
def SendEachClassifiersPerformanceToVisualize():

    loopEmpty = []
    initialStates = []
    for x in range(randomSearchVar*2):
        if (x < (randomSearchVar*2/2)):
            loopEmpty.append(x+1)
        initialStates.append(1)
    response = { 
        'PerformancePerModel': allParametersPerformancePerModel,
        'ModelSpaceUMAPSend': ModelSpaceUMAP,
        'X_train': X_train.to_json(double_precision=15),
        'y_train': y_train,
        'X_test': X_test.to_json(double_precision=15),
        'y_test': y_test,
        'HypRF': sendHyperRF,
        'HypAB': sendHyperAB,
        'NumberOfModels': loopEmpty,
        'States': initialStates
    }
    return jsonify(response)

def FunUMAP (data, neighbors):
    trans = umap.UMAP(n_neighbors=neighbors, min_dist=0.1, random_state=RANDOM_SEED, transform_seed=RANDOM_SEED).fit(data)
    Xpos = trans.embedding_[:, 0].tolist()
    Ypos = trans.embedding_[:, 1].tolist()
    return [Xpos,Ypos]

@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/SearchingAgain', methods=["GET", "POST"])
def requestedNewModels():

    RetrievedModel = request.get_data().decode('utf8').replace("'", '"')
    RetrievedModel = json.loads(RetrievedModel)

    limitationRF = RetrievedModel['RFNewModels']
    limitationAB = RetrievedModel['ABNewModels']
    thresholdMain = RetrievedModel['thresholdMain']

    global paramsRF
    paramsRF = limitationRF

    global paramsAB
    paramsAB = limitationAB

    global randomSearchVar 
    randomSearchVar = thresholdMain

    executeSearch()

    return 'Everything is okay'

@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/updateRounding', methods=["GET", "POST"])
def updateRoundingFun():

    RetrievedModel = request.get_data().decode('utf8').replace("'", '"')
    RetrievedModel = json.loads(RetrievedModel)

    roundingValueLocal = RetrievedModel['roundingValue']

    global roundValueSend
    roundValueSend = roundingValueLocal

    executeSearch()

    return 'Everything is okay'

@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@app.route('/data/askToRemoveAFeature', methods=["GET", "POST"])
def askToRemoveAFeatureFun():

    RetrievedModel = request.get_data().decode('utf8').replace("'", '"')
    RetrievedModel = json.loads(RetrievedModel)

    removingFeature = RetrievedModel['whoWasRemoved']

    global XData
    global keepOriginalFeatures
    keepOriginalFeatures = []

    XData = XData.drop(columns=[removingFeature])
    for col in XData.columns:
        keepOriginalFeatures.append(col)

    executeSearch()

    return 'Everything is okay'
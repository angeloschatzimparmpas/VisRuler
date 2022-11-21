<template>
  <div>
    <table id="tableManual" class="table table-borderless table-sm" style="margin-top: -12px; margin-bottom: -12px">
      <tbody>
      <td>Filter Instances due to Decisions:</td>
      <td><input id="filterDecisions" type="checkbox" @change="triggeredChange" data-toggle="toggle"></td>
      <td>
      <td>
      <td>Local Feature Ranking - Bins:</td>
      <td><b-form-slider ref="basic2" v-model="basicValue2" :min="5" :max="50" :step="5" trigger-change-event @slide-start="slideStartDecLoc" @slide-stop="slideStopDecLoc" style="padding-right: 20px;"></b-form-slider>{{ basicValue2 }}</td>  
      </tbody>
    </table>
    <div id="PCPDataView" class="parcoords"></div>
  </div>
</template>

<script>
import { EventBus } from '../main.js'
import 'parcoord-es/dist/parcoords.css';
import ParCoords from 'parcoord-es';
import * as d3Base from 'd3'
import bFormSlider from 'vue-bootstrap-slider/es/form-slider';
import 'bootstrap-slider/dist/css/bootstrap-slider.css'
import $ from 'jquery'; // <-to import jquery

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

export default {
  name: 'Test',
  data () {
    return {
      basicValue2: 10,
      PCPDataReceived: '',
      activeTestInstancePCP: 0,
      onlyOnce: true,
      EvaluationFinalResults: [],
      generalLimit: [],
      limitFiltering: [],
      flagCheckedFilter: false,
      overlap: [],
      modeCurrent: true,
      firstAll: true,
      firstAllDecisions: [],
      eachFeatureOveralpBins: [],
      resultsFilteringDecisions: [],
      indicRF: [],
      indicGB: [],
      originalLabels: [],
      globalSortingFeatures: [],
      holdFlag: [],
      RetrieveNameTest: '',
    }
  },
  methods: {
      slideStartDecLoc () {
      
      },
      slideStopDecLoc () {
        this.firstAll = true
        this.PCPView()
        //EventBus.$emit('refreshImmediately')
      },
      triggeredChange () {
        this.flagCheckedFilter = document.getElementById("filterDecisions").checked
        this.PCPView()
      },
      PCPView () {

          var originalFeatures = JSON.parse(this.PCPDataReceived[9])
          var colorRange = ["#bebada", "#fdb462", "#fb8072", "#ff00ff"];        
          d3.selectAll("#PCPDataView > *").remove();
          var DataRaw = JSON.parse(this.PCPDataReceived[4])

          var X_testInstance = JSON.parse(this.PCPDataReceived[6])
          var maximum = []
          var minimum = []
          for (let k = 0; k < Object.values(DataRaw).length; k++) {
            maximum.push(Math.max(...Object.values(Object.values(DataRaw)[k])))
            minimum.push(Math.min(...Object.values(Object.values(DataRaw)[k])))
          }

          var RFInstances = JSON.parse(this.EvaluationFinalResults[14])
          var RFInstancesParse = JSON.parse(RFInstances)
          var RFStats = JSON.parse(this.EvaluationFinalResults[10])
          var RFStatsRead = JSON.parse(RFStats)
          var RFLength = Object.values(RFStatsRead.predicted_value).length
          var RFDecisions = JSON.parse(this.EvaluationFinalResults[6])
          var RFDecisionsRead = JSON.parse(RFDecisions)

          var GBInstances = JSON.parse(this.EvaluationFinalResults[31])
          var GBInstancesParse = JSON.parse(GBInstances)
          var GBStats = JSON.parse(this.EvaluationFinalResults[27])
          var GBStatsRead = JSON.parse(GBStats)
          var GBLength = Object.values(GBStatsRead.predicted_value).length
          var GBDecisions = JSON.parse(this.EvaluationFinalResults[23])
          var GBDecisionsRead = JSON.parse(GBDecisions)

          var target_names = this.PCPDataReceived[5]

          var listAllLimits = {}
          var listofObjectsDec = []
          var localList = []
          var loopNormal = 0
          var keepColorRF = []
          var keepColorAB = []

          for (var k = 0; k < Object.values(RFDecisionsRead).length/2; k++) {
            listofObjectsDec = []
            for (var i = 0; i < (RFLength+GBLength); i++) {
              localList = []
              if (this.limitFiltering.length == 0) {
                if (this.generalLimit.length == 0) {
                    if (i >= RFLength) {
                      var reduce = i - RFLength
                        if (Object.values(Object.values(GBDecisionsRead)[k])[reduce] == 2) {
                          localList[0] = minimum[k]
                        } else {
                          localList[0] = Object.values(Object.values(GBDecisionsRead)[k])[reduce]
                        }
                        if (Object.values(Object.values(GBDecisionsRead)[Object.values(RFDecisionsRead).length/2+k])[reduce] == 2) {
                          localList[1] = maximum[k]
                        } else {
                          localList[1] = Object.values(Object.values(GBDecisionsRead)[Object.values(RFDecisionsRead).length/2+k])[reduce]                     
                        }
                    } else {
                        if (Object.values(Object.values(RFDecisionsRead)[k])[i] == 2) {
                          localList[0] = minimum[k]
                        } else {
                          localList[0] = Object.values(Object.values(RFDecisionsRead)[k])[i]
                        }
                        if (Object.values(Object.values(RFDecisionsRead)[Object.values(RFDecisionsRead).length/2+k])[i] == 2) {
                          localList[1] = maximum[k]
                        } else {
                          localList[1] = Object.values(Object.values(RFDecisionsRead)[Object.values(RFDecisionsRead).length/2+k])[i]                     
                        }
                    }
                } else {
                  if (this.generalLimit.includes(i)) {
                    if (i >= RFLength) {
                      var reduce = i - RFLength
                        if (Object.values(Object.values(GBDecisionsRead)[k])[reduce] == 2) {
                          localList[0] = minimum[k]
                        } else {
                          localList[0] = Object.values(Object.values(GBDecisionsRead)[k])[reduce]
                        }
                        if (Object.values(Object.values(GBDecisionsRead)[Object.values(RFDecisionsRead).length/2+k])[reduce] == 2) {
                          localList[1] = maximum[k]
                        } else {
                          localList[1] = Object.values(Object.values(GBDecisionsRead)[Object.values(RFDecisionsRead).length/2+k])[reduce]                     
                        }
                    } else {
                        if (Object.values(Object.values(RFDecisionsRead)[k])[i] == 2) {
                          localList[0] = minimum[k]
                        } else {
                          localList[0] = Object.values(Object.values(RFDecisionsRead)[k])[i]
                        }
                        if (Object.values(Object.values(RFDecisionsRead)[Object.values(RFDecisionsRead).length/2+k])[i] == 2) {
                          localList[1] = maximum[k]
                        } else {
                          localList[1] = Object.values(Object.values(RFDecisionsRead)[Object.values(RFDecisionsRead).length/2+k])[i]                     
                        }
                    }
                  }
                }
              } else {
                if (this.limitFiltering.includes(i)) {
                    if (i >= RFLength) {
                      var reduce = i - RFLength
                        if (Object.values(Object.values(GBDecisionsRead)[k])[reduce] == 2) {
                          localList[0] = minimum[k]
                        } else {
                          localList[0] = Object.values(Object.values(GBDecisionsRead)[k])[reduce]
                        }
                        if (Object.values(Object.values(GBDecisionsRead)[Object.values(RFDecisionsRead).length/2+k])[reduce] == 2) {
                          localList[1] = maximum[k]
                        } else {
                          localList[1] = Object.values(Object.values(GBDecisionsRead)[Object.values(RFDecisionsRead).length/2+k])[reduce]                     
                        }
                    } else {
                        if (Object.values(Object.values(RFDecisionsRead)[k])[i] == 2) {
                          localList[0] = minimum[k]
                        } else {
                          localList[0] = Object.values(Object.values(RFDecisionsRead)[k])[i]
                        }
                        if (Object.values(Object.values(RFDecisionsRead)[Object.values(RFDecisionsRead).length/2+k])[i] == 2) {
                          localList[1] = maximum[k]
                        } else {
                          localList[1] = Object.values(Object.values(RFDecisionsRead)[Object.values(RFDecisionsRead).length/2+k])[i]                     
                        }
                    }
                }     
              }
              if((localList.length != 0)) {
                if (localList[0] > localList[1]) {
                  var tempList = []
                  tempList[0] = localList[1]
                  tempList[1] = localList[0]
                  listofObjectsDec.push(tempList)
                } else {
                  listofObjectsDec.push(localList)
                }
              }
              if (k==0) {
                  if (this.limitFiltering.length == 0) {
                    if (this.generalLimit.length == 0) {
                      if (i >= RFLength) {
                          var reduce = i - RFLength
                          keepColorAB.push(Object.values(Object.values(GBStatsRead.predicted_value))[reduce])
                        } else {
                          keepColorRF.push(Object.values(Object.values(RFStatsRead.predicted_value))[i])
                        }
                    } else {
                        if (this.generalLimit.includes(i)) {
                      if (i >= RFLength) {
                          var reduce = i - RFLength
                          keepColorAB.push(Object.values(Object.values(GBStatsRead.predicted_value))[reduce])
                        } else {
                          keepColorRF.push(Object.values(Object.values(RFStatsRead.predicted_value))[i])
                        }
                      }
                    }
                  } else {
                    if (this.limitFiltering.includes(i)) {
                      if (i >= RFLength) {
                        var reduce = i - RFLength
                        keepColorAB.push(Object.values(Object.values(GBStatsRead.predicted_value))[reduce])
                      } else {
                        keepColorRF.push(Object.values(Object.values(RFStatsRead.predicted_value))[i])
                      }
                  }
                }
              }
            }
            listAllLimits[Object.keys(DataRaw)[loopNormal]] = listofObjectsDec
            loopNormal = loopNormal + 1
          }

          if (this.firstAll) {
            this.eachFeatureOveralpBins = []
            this.firstAll = false
            this.firstAllDecisions = listAllLimits
            var countingBinsAllPer
            var next_step
            var eachStep = (1/this.basicValue2)
            
            // compute here binnarization
            for (var k = 0; k < originalFeatures.length; k++) {
              var countingBinsAll = []
              var j = 0
                while(j < 1) {
                  countingBinsAllPer = 0
                  next_step = j + eachStep
                  if (this.basicValue2 <= 10) {
                    next_step = parseFloat(next_step.toPrecision(1))
                  } else {
                    next_step = parseFloat(next_step.toPrecision(2))
                  }
                  for (var m = 0; m < Object.values(this.firstAllDecisions[originalFeatures[k]]).length; m++) {
                    if ((Object.values(this.firstAllDecisions[originalFeatures[k]])[m][0] <= next_step) && (Object.values(this.firstAllDecisions[originalFeatures[k]])[m][1] >= j)) {
                      countingBinsAllPer = countingBinsAllPer + 1
                    }
                  }
                  j = next_step
                  countingBinsAll.push(countingBinsAllPer/Object.values(this.firstAllDecisions[originalFeatures[k]]).length)
                }
              this.eachFeatureOveralpBins.push(countingBinsAll)
            }
          }

          var eachFeatureOveralpBinsSel = []
          var countingBinsAllPerSel
          var next_stepSel
          var eachStepSel = (1/this.basicValue2)
          
          // compute here binnarization
          for (var k = 0; k < originalFeatures.length; k++) {
            var countingBinsSel = []
            var j = 0
              while(j < 1) {
                countingBinsAllPerSel = 0
                next_stepSel = j + eachStepSel
                if (this.basicValue2 <= 10) {
                  next_stepSel = parseFloat(next_stepSel.toPrecision(1))
                } else {
                  next_stepSel = parseFloat(next_stepSel.toPrecision(2))
                }
                for (var m = 0; m < Object.values(listAllLimits[originalFeatures[k]]).length; m++) {
                  if ((Object.values(listAllLimits[originalFeatures[k]])[m][0] <= next_stepSel) && (Object.values(listAllLimits[originalFeatures[k]])[m][1] >= j)) {
                    countingBinsAllPerSel = countingBinsAllPerSel + 1
                  }
                }
                j = next_stepSel
                countingBinsSel.push(countingBinsAllPerSel/Object.values(listAllLimits[originalFeatures[k]]).length)
              }
            eachFeatureOveralpBinsSel.push(countingBinsSel)
          }

          var sumPerFeature = new Array(originalFeatures.length)
          for (var k = 0; k < originalFeatures.length; k++) {
            var summarizeEachFeature = 0
            for (var x = 0; x < this.eachFeatureOveralpBins[k].length; x++) {
              summarizeEachFeature = summarizeEachFeature + ((this.eachFeatureOveralpBins[k][x]) * (Math.log(eachFeatureOveralpBinsSel[k][x])))
            }
            if (isNaN(summarizeEachFeature)) {
              sumPerFeature[k] = 0
            } else {
              sumPerFeature[k] = Math.abs(summarizeEachFeature * (-1))
            }
          }
          
          function sortWithIndeces(toSort) {
            for (var i = 0; i < toSort.length; i++) {
              toSort[i] = [toSort[i], i];
            }
            toSort.sort(function(left, right) {
              return left[0] < right[0] ? -1 : 1;
            });
            toSort.sortIndices = [];
            for (var j = 0; j < toSort.length; j++) {
              toSort.sortIndices.push(toSort[j][1]);
              toSort[j] = toSort[j][0];
            }
            return toSort;
          }

          if (Object.values(listAllLimits)[0].length == Object.values(this.firstAllDecisions)[0].length) {
            if (this.holdFlag) {
              var sortedInd = this.globalSortingFeatures.reverse()
            } else {
              var sortedInd = this.globalSortingFeatures
            }
            
          } else {
            var sortedInd = sortWithIndeces(sumPerFeature).sortIndices.reverse()
          }

          var DataSetParse = []
          var listOfObjects = []
          var newTest = -1
          for (let l = 0; l <= Object.values(Object.values(DataRaw)[0]).length; l++) {
            listOfObjects = []
            if (l == Object.values(Object.values(DataRaw)[0]).length) {
              newTest = l
              for (let k = 0; k < Object.values(DataRaw).length; k++) {
                listOfObjects[Object.keys(DataRaw)[sortedInd[k]]] = Object.values(Object.values(X_testInstance)[sortedInd[k]])[this.activeTestInstancePCP]
              }
              listOfObjects["Outcome"] = 3
              listOfObjects["ID"] = l
            } else {
              for (let k = 0; k < Object.values(DataRaw).length; k++) {
                listOfObjects[Object.keys(DataRaw)[sortedInd[k]]] = Object.values(Object.values(DataRaw)[sortedInd[k]])[l]
              }
              listOfObjects["Outcome"] = target_names[l]
              listOfObjects["ID"] = l
            }
            DataSetParse.push(listOfObjects)
          }
          var numberEstimRF = JSON.parse(this.EvaluationFinalResults[1]).params
          var numberEstimGB = JSON.parse(this.EvaluationFinalResults[18]).params

          var yValueRF = []
          var yValueGB = []
          
          for (let j = 0; j < this.indicRF.length; j++) {
            yValueRF.push(numberEstimRF[this.indicRF[j]].n_estimators)
          }

          var eachModelLimitsRF = []
          var step = 0
          for (let j = 0; j < yValueRF.length; j++) {
            eachModelLimitsRF.push([0+step,yValueRF[j]+step-1])
            step = step + yValueRF[j]
          }  

          for (let j = 0; j < this.indicGB.length; j++) {
            yValueGB.push(numberEstimGB[this.indicGB[j]].n_estimators)
          } 

          var eachModelLimitsGB = []
          step = 0
          for (let j = 0; j < yValueGB.length; j++) {
            eachModelLimitsGB.push([0+step,yValueGB[j]+step-1])
            step = step + yValueGB[j]
          }  

          var flagForFeatures = new Array(originalFeatures.length)
          var indicesToKeep = []
          if (this.flagCheckedFilter == false) {
            for (var i = 0; i < DataSetParse.length; i++) {
              indicesToKeep.push(i)
            }
          } else {
            for (var i = 0; i < this.resultsFilteringDecisions.length; i++) {
              if (this.resultsFilteringDecisions[i]['model'] == "RF") {  
                var counterCheck = 0
                var indexCurrent = -1
                for (var k = eachModelLimitsRF[this.resultsFilteringDecisions[i]['model_id']-1][0]; k <= eachModelLimitsRF[this.resultsFilteringDecisions[i]['model_id']-1][1]; k++) {
                  if (this.resultsFilteringDecisions[i]['tree_id'] == counterCheck) {
                    indexCurrent = k
                    break;
                  }
                  counterCheck = counterCheck + 1
                }
                for (var j = 0; j < Object.values(RFInstancesParse).length; j++) {
                  if (Object.values(Object.values(RFInstancesParse)[j])[indexCurrent] == this.resultsFilteringDecisions[i]['decision_id']) {
                    indicesToKeep.push(j)
                  }
                }
                indicesToKeep.push(DataSetParse.length-1)
              } else if (this.resultsFilteringDecisions[i]['model'] == "AB") {  
                var counterCheck = 0
                var indexCurrent = -1
                for (var k = eachModelLimitsGB[this.resultsFilteringDecisions[i]['model_id']-1][0]; k <= eachModelLimitsGB[this.resultsFilteringDecisions[i]['model_id']-1][1]; k++) {
                  if (this.resultsFilteringDecisions[i]['tree_id'] == counterCheck) {
                    indexCurrent = k
                    break;
                  }
                  counterCheck = counterCheck + 1
                }
                for (var j = 0; j < Object.values(GBInstancesParse).length; j++) {
                  if (Object.values(Object.values(GBInstancesParse)[j])[indexCurrent] == this.resultsFilteringDecisions[i]['decision_id']) {
                    indicesToKeep.push(j)
                  }
                }
                indicesToKeep.push(DataSetParse.length-1)
              } else {
                // for (var i = 0; i < DataSetParse.length; i++) {
                //   for (var loop = 0; loop < flagForFeatures.length; loop++) {
                //     flagForFeatures[loop] = false
                //   }
                //   for (var m = 0; m < Object.values(listAllLimits[originalFeatures[0]]).length; m++) {
                //     for (var k = 0; k < originalFeatures.length; k++) {
                //       if (Object.values(listAllLimits[originalFeatures[k]])[m][1] == 1) {
                //         if ((DataSetParse[i][originalFeatures[k]] >= Object.values(listAllLimits[originalFeatures[k]])[m][0]) && (DataSetParse[i][originalFeatures[k]] <= Object.values(listAllLimits[originalFeatures[k]])[m][1])) {
                //           flagForFeatures[k] = true
                //         }                     
                //       } else {
                //         if ((DataSetParse[i][originalFeatures[k]] >= Object.values(listAllLimits[originalFeatures[k]])[m][0]) && (DataSetParse[i][originalFeatures[k]] < Object.values(listAllLimits[originalFeatures[k]])[m][1])) {
                //           flagForFeatures[k] = true
                //         }
                //       }

                //     }
                //     var checker = arr => arr.every(v => v === true);
                //     if (checker(flagForFeatures)) {
                //       indicesToKeep.push(i)
                //       break;
                //     } else {
                //     }
                //   }
                // }
              }
            }
          }
          indicesToKeep = indicesToKeep.reduce((a, x) => a.includes(x) ? a : [...a, x], []).sort()
          DataSetParse = DataSetParse.filter((el,i)=>indicesToKeep.some(j => i === j))

          if (this.flagCheckedFilter == false) {
            var frequency = target_names.reduce(function (acc, curr) {
              if (typeof acc[curr] == 'undefined') {
                acc[curr] = 1;
              } else {
                acc[curr] += 1;
              }

              return acc;
            }, {});

            this.originalLabels = Object.keys(frequency)

            var sumAllFrequencies = 0
            var prepareString = ''
            for (let index = 0; index < Object.values(frequency).length; index++) {
              if (index == Object.values(frequency).length-1) {
                prepareString += Object.values(frequency)[index];
              } else {
                prepareString += Object.values(frequency)[index] + "+";
              }
              sumAllFrequencies = sumAllFrequencies + Object.values(frequency)[index]
            }
            EventBus.$emit('sendInstancesSeg', prepareString)
            EventBus.$emit('sendInstancesSum', sumAllFrequencies)
          } else {
            target_names = target_names.filter((el,i)=>indicesToKeep.some(j => i === j))
          
            var frequency = target_names.reduce(function (acc, curr) {
              if (typeof acc[curr] == 'undefined') {
                acc[curr] = 1;
              } else {
                acc[curr] += 1;
              }

              return acc;
            }, {});

            for (let looping = 0; looping < this.originalLabels.length; looping++) {
              if (Object.keys(frequency).includes(looping.toString())) {

              } else {
                frequency[looping] = 0
              }
            }

            var sumAllFrequencies = 0
            var prepareString = ''
            for (let index = 0; index < Object.values(frequency).length; index++) {
              if (index == Object.values(frequency).length-1) {
                prepareString += Object.values(frequency)[index];
              } else {
                prepareString += Object.values(frequency)[index] + "+";
              }
              sumAllFrequencies = sumAllFrequencies + Object.values(frequency)[index]
            }
            EventBus.$emit('sendInstancesSeg', prepareString)
            EventBus.$emit('sendInstancesSum', sumAllFrequencies)
          }

          EventBus.$emit('ExtractResults', listAllLimits)
          // check that again! There is a bug here!
          var keepColorFinal = keepColorRF.concat(keepColorAB)
          EventBus.$emit('manualDecisions', keepColorFinal)

          var lengthOverlap = this.overlap.length

          if (lengthOverlap == 0) {

          } else {
            if (this.modeCurrent) {
              var storeMaxs = new Array(originalFeatures.length)
              var storeMins = new Array(originalFeatures.length)
              storeMaxs.fill(1)
              storeMins.fill(0)
              for (var k = 0; k < originalFeatures.length; k++) {
                for (var m = 0; m < Object.values(listAllLimits[originalFeatures[k]]).length; m++) {
                  if (Object.values(listAllLimits[originalFeatures[k]])[m][1] < storeMaxs[k]) {
                    storeMaxs[k] = Object.values(listAllLimits[originalFeatures[k]])[m][1]
                  }
                  if (Object.values(listAllLimits[originalFeatures[k]])[m][0] > storeMins[k]) {
                    storeMins[k] = Object.values(listAllLimits[originalFeatures[k]])[m][0]
                  }
                }
                Object.values(listAllLimits[originalFeatures[k]])[0][0] = storeMins[k]
                Object.values(listAllLimits[originalFeatures[k]])[0][1] = storeMaxs[k]
                listAllLimits[originalFeatures[k]] = Object.values(listAllLimits[originalFeatures[k]]).slice(0,1)
              }
            } else {
                var storeMaxs = new Array(originalFeatures.length)
                var storeMins = new Array(originalFeatures.length)
                storeMaxs.fill(1)
                storeMins.fill(0)
                var storeMinimums = new Array(originalFeatures.length)
                var storeMaximums = new Array(originalFeatures.length)
                storeMaximums.fill(0)
                storeMinimums.fill(1)
                for (var k = 0; k < originalFeatures.length; k++) {
                  for (var m = 0; m < Object.values(listAllLimits[originalFeatures[k]]).length; m++) {
                    if (Object.values(listAllLimits[originalFeatures[k]])[m][1] < storeMaxs[k]) {
                      storeMaxs[k] = Object.values(listAllLimits[originalFeatures[k]])[m][1]
                    }
                    if (Object.values(listAllLimits[originalFeatures[k]])[m][0] > storeMins[k]) {
                      storeMins[k] = Object.values(listAllLimits[originalFeatures[k]])[m][0]
                    }
                    if (Object.values(listAllLimits[originalFeatures[k]])[m][1] > storeMaximums[k]) {
                      storeMaximums[k] = Object.values(listAllLimits[originalFeatures[k]])[m][1]
                    }
                    if (Object.values(listAllLimits[originalFeatures[k]])[m][0] < storeMinimums[k]) {
                      storeMinimums[k] = Object.values(listAllLimits[originalFeatures[k]])[m][0]
                    }
                  }
                  Object.values(listAllLimits[originalFeatures[k]])[0][0] = storeMinimums[k]
                  Object.values(listAllLimits[originalFeatures[k]])[0][1] = storeMins[k]
                  Object.values(listAllLimits[originalFeatures[k]])[1][0] = storeMaxs[k]
                  Object.values(listAllLimits[originalFeatures[k]])[1][1] = storeMaximums[k]
                  if (Object.values(listAllLimits[originalFeatures[k]])[0][0] == Object.values(listAllLimits[originalFeatures[k]])[0][1] && Object.values(listAllLimits[originalFeatures[k]])[1][0] == Object.values(listAllLimits[originalFeatures[k]])[1][1]) {
                    listAllLimits[originalFeatures[k]] = Object.values(listAllLimits[originalFeatures[k]]).slice(0,0)
                  }
                  else if (Object.values(listAllLimits[originalFeatures[k]])[0][0] == Object.values(listAllLimits[originalFeatures[k]])[0][1]) {
                    listAllLimits[originalFeatures[k]] = Object.values(listAllLimits[originalFeatures[k]]).slice(1,2)
                  } else if (Object.values(listAllLimits[originalFeatures[k]])[1][0] == Object.values(listAllLimits[originalFeatures[k]])[1][1]) {
                    listAllLimits[originalFeatures[k]] = Object.values(listAllLimits[originalFeatures[k]]).slice(0,1)
                  } else {
                    listAllLimits[originalFeatures[k]] = Object.values(listAllLimits[originalFeatures[k]]).slice(0,2)
                  }    
                }   
              }
          }

          var leftMargin = -40

          if (this.RetrieveNameTest == 'IrisC') {
            var width = Object.values(listAllLimits)[0].length * 13.5 // 13.5 iris, 27 diabetes, 29 breast cancer // titanic and happiness decrease to 20 // german credit bank 29
          } else if (this.RetrieveNameTest == 'CreditC') {
            var width = Object.values(listAllLimits)[0].length * 29 // 13.5 iris, 27 diabetes, 29 breast cancer // titanic and happiness decrease to 20 // german credit bank 29
          } else {
            var width = Object.values(listAllLimits)[0].length * 20 // 13.5 iris, 27 diabetes, 29 breast cancer // titanic and happiness decrease to 20 // german credit bank 29
          }

          if (width <= 750) {
            width = 750 
            leftMargin = 10
          }
          var height = 780

          var colors = ["#bebada", "#fdb462", "#fb8072", "#000000", "#fb807200"];

          var highlighted = []
          highlighted.push(DataSetParse[DataSetParse.length-1])

          listOfObjects = []
          for (let k = 0; k < Object.values(DataRaw).length; k++) {
            listOfObjects[Object.keys(DataRaw)[sortedInd[k]]] = 0
          }
          listOfObjects["Outcome"] = 4
          listOfObjects["ID"] = DataSetParse.length
          DataSetParse.push(listOfObjects)
       
          listOfObjects = []
          for (let k = 0; k < Object.values(DataRaw).length; k++) {
            listOfObjects[Object.keys(DataRaw)[sortedInd[k]]] = 1
          }
          listOfObjects["Outcome"] = 4
          listOfObjects["ID"] = DataSetParse.length
          DataSetParse.push(listOfObjects)

          var pc = ParCoords()("#PCPDataView")
              .data(DataSetParse)
              .width(width)
              .height(height)
              .margin({ top: 20, left: leftMargin, bottom: 20, right: ((width/Object.keys(DataRaw).length)-60) })
              .color(function(d, i) { return colors[d.Outcome] })
              //.bundlingStrength(1) // set bundling strength
              .smoothness(0)
              //.bundleDimension("sepal_w")
              .showControlPoints(false)
              .hideAxis(["Outcome","ID"])
              .render()
              .highlight(highlighted)
              .alphaOnBrushed(0.75)
              .brushMode('1D-axes-multi')
              .brushExtents(listAllLimits);

          //var scaleDecisions = d3.scaleLinear().domain([this.totalDecisionsTest, 1]).range([3, 3]); 
          
          if (this.generalLimit.length != 0) {
            var current = this.generalLimit.length
          }
          if (this.limitFiltering.length != 0) {
            var current = this.limitFiltering.length
          }


          var dimension = document.getElementsByClassName('dimension')
          var counter = 0
          dimension.forEach(element => {
            counter = counter + 1
            var ticks = element.getElementsByClassName('tick')
            ticks.forEach(tickOne => {
              tickOne.getElementsByTagName("text")[0].style.transform = "rotate(-90deg) translate(15px,-15px)";
            });
            var labels = element.getElementsByClassName('label')[0]
            if (counter > Object.values(RFDecisionsRead).length/2) {

            } else {
              labels.style.transform = "translate(30px, -5px)";
              labels.style.fontSize = "16px";
              var group = element.getElementsByClassName('brush-group')[0]
              var classGroup = group.getElementsByClassName('brush')
              classGroup.forEach((el, ind) => {
                var splittingProcess = el.id
                var separateParts = splittingProcess.split("-")
                var currentNumber = parseInt(separateParts[2])
                if (ind == 0) {

                } else {
                  var styleOver = el.getElementsByClassName('overlay')[0]
                  var styleSel = el.getElementsByClassName('selection')[0]
                  var styleHan1 = el.getElementsByClassName('handle')[0]
                  var styleHan2 = el.getElementsByClassName('handle')[1]
                  styleOver.style.x = currentNumber*3+"px"
                  styleSel.style.x =  currentNumber*3+"px"
                  styleOver.style.width = 3+"px"
                  styleSel.style.width = 3+"px"
                  if (lengthOverlap) {
                    styleSel.style["fill"] = colorRange[3]
                  } else {
                    styleSel.style["fill"] = colorRange[keepColorFinal[currentNumber]]
                  }
                  styleSel.style.position = "relative"
                  styleSel.style["fill-opacity"] = 0.5
                  styleSel.style.stroke = "#000"
                  styleSel.style["stroke-width"] = 0.5
                  styleOver.style.zIndex = "-1"
                  styleSel.style.zIndex = "-1"
                  styleOver.style.display = "none";
                  styleHan1.style.display = "none";
                  styleHan2.style.display = "none";

                }
              });
            }
          });
        },
      reset () {
        d3.selectAll("#PCPDataView > *").remove();
        this.basicValue1 = -1
      },
    },
  mounted () {

    $(function() {
      $(".parcoords").on('mousewheel', function(event) {
        if (event.originalEvent.wheelDelta > 0 || event.originalEvent.detail < 0) {
          event.currentTarget.scrollLeft -= (0.2 * 50); //need a value to speed up the change
        }
        else {
          event.currentTarget.scrollLeft += (0.2 * 50); //need a value to speed up the change
        }
        event.preventDefault();
      });
    });

    EventBus.$on('SendToServerDataSetBasicConfirm', data => { this.RetrieveNameTest = data })

    EventBus.$on('firstAllTrue', data => {
      this.firstAll = data})

    EventBus.$on('onHold', data => {
      this.holdFlag = data})

    EventBus.$on('indicesRFSend', data => {
      this.indicRF = data})
    EventBus.$on('indicesGBSend', data => {
      this.indicGB = data})

    EventBus.$on('TrueFlag', data => { this.onlyOnce = data })
    EventBus.$on('selectDecisionsTestLimitation', data => {
      this.generalLimit = data})
    EventBus.$on('selectDecisions', data => {
      this.limitFiltering = data})
    EventBus.$on('emittedEventCallingTrainingResults', data => {
      this.EvaluationFinalResults = data})
    EventBus.$on('emittedEventCallingResult', data => { this.PCPDataReceived = data })
    EventBus.$on('emittedEventCallingTestingView', data => { this.limitFiltering = data })
    EventBus.$on('emittedEventCallingTestingView', this.PCPView)
    //EventBus.$on('emittedEventCallingEvaluation', this.PCPView)
    EventBus.$on('CallFromSpace', data => { this.activeTestInstancePCP = data })
    //EventBus.$on('CallFromSpace', this.PCPView)

    EventBus.$on('sendAnchoredPoints', data => { this.overlap = data })
    EventBus.$on('activeMode', data => { this.modeCurrent = data })
    EventBus.$on('activeMode', this.PCPView)

    EventBus.$on('sendDecisionsFiltered', data => { this.resultsFilteringDecisions = data })

    EventBus.$on('flagtoTrue', data => { this.firstAll = data })

    EventBus.$on('globalSortingFeatures', data => { this.globalSortingFeatures = data })

    EventBus.$on('reset', this.reset)
  }
}
</script>

<style>
#PCPDataView {
  transform: translate(-2.3%, 0%) rotate(90deg);
  z-index: 0;
  margin-bottom: 0px;
  margin-left: 35px;
  overflow-x: scroll;
}

#tableManual {
  z-index: 1;
}

.parcoords svg {
  position: relative !important;
  z-index: 1;
}

</style>
<template>
<div>
  <div style = "border: 1px solid black; margin-bottom:4px"> 
  <button style="float: center; margin-top: 4px" class="btn-outline-dark"
  id="know"
  v-on:click="knowClass">
  <font-awesome-icon icon="file-export" />
  {{ valueKnowE }}
  </button>
  <div class="switch-toggle switch-3 switch-candy" style="margin-top: 4px; margin-bottom: 4px; margin-left: 4px; margin-right: 4px">

    <input id="all" name="un" type="radio"/>
    <label for="all" @click="clickedAll()">= All</label>

    <input id="unan" name="un" type="radio"/>
    <label for="unan" @click="clickedUNAN()">≠ Unanimous</label>

    <input id="maj" name="un" type="radio" checked="checked"/>
    <label for="maj" @click="clickedMAJ()">≠ Majority</label>

    <a></a>
  </div>
  <b-row style="margin-top: 4px;">
  <b-col cols="2">
  <button class="btn-outline-dark"
  id="leftID"
  v-on:click="left">
  <font-awesome-icon icon="arrow-circle-left" />
  </button>
  </b-col>
  <b-col cols="8" style="margin-top:3px">
  {{ whichActive }}
  </b-col>
  <b-col cols="2">
  <button class="btn-outline-dark"
  id="rightID"
  v-on:click="right">
  <font-awesome-icon icon="arrow-circle-right" />
  </button>
  </b-col>
  </b-row>
  <div id='finalDecision' style="min-height: 160px"></div>
  </div>
  <div style = "border: 1px solid black;"> 
  <div id='chart' class="parcoords" style="min-height: 228px"></div>
  <div id='chart2' class="parcoords" style="min-height: 228px"></div>
  <b-row>
    <div class="col-lg-4" style="margin-top:2px; margin-bottom:-25px; margin-left: 0px"><p>Search for New Models</p></div>
    <div class="col-lg-8" style="margin-top:-8px; margin-left: -12px"><div id="thres"></div></div>
  </b-row>
  </div>
</div>
</template>

<script>

import * as Plotly from 'plotly.js'
import { EventBus } from '../main.js'
import 'parcoord-es/dist/parcoords.css';
import ParCoords from 'parcoord-es';
import * as d3Base from 'd3'
import slider from 'd3slider';
// attach all d3 plugins to the d3v5 library
const d3v5 = Object.assign(d3Base, {slider})
import * as _ from 'lodash'   

export default {
  name: 'Rules',
  data () {
    return {
      threshold: 0,
      whichActive: 'No test instance selected',
      descriptiveRules: [],
      resultsFinal: [],
      activeInstance: 0,
      manualDecisions: [],
      gotAssocRules: [],
      valueKnowE: 'Extract Manual Decisions (MD)',
      states: [],
      activeMode: 1,
      totalPerformRF: 0,
      totalPerformAB: 0,
      HyperParamsAll: '',
      RFSort: [],
      GBSort: [],
    }
  },
  methods: {
      InitSlider () {  

      d3.selectAll("#thres > *").remove();

      var sliderStepPos = d3v5.slider('#thres', {
              domain: [0, 10],
              playButton: false,
              interval: 1,
              tickInterval: 1,
              value: this.threshold,
              height: 55,
              width: 250,
              loop: false,
              size: 9,
              color: '#000000',
              onDrag: function(val){
                EventBus.$emit('CorrThres', val)
                if (val != 0) {
                  EventBus.$emit('CallNewModels')
                }
              }
            });	

    },
    clickedAll () {
      this.activeMode = 0
    },
    clickedMAJ () {
      this.activeMode = 1
    },
    clickedUNAN () {
      this.activeMode = 2
    },
    knowClass () {
      EventBus.$emit('OpenModal')
    },
    left () {
      EventBus.$emit('onHold', false)
      EventBus.$emit('flagtoTrue', true)
      var RFPredictions = JSON.parse(this.resultsFinal[0])
      var GBPredictions = JSON.parse(this.resultsFinal[1])
      var y_test = this.resultsFinal[2]     
      var target_names = this.resultsFinal[3]

      var splitStatesRF = []
      var splitStatesAB = []
      for (let i = 0; i < this.states.length; i++) {
        if (i%2 == 0) {
          splitStatesRF.push(this.states[i])
        } else {
          splitStatesAB.push(this.states[i])
        }
      }

      var countLenRF = 0;
      for(var i = 0; i < splitStatesRF.length; ++i){
          if(splitStatesRF[i] == 1)
              countLenRF++;
      }

      var countLenAB = 0;
      for(var i = 0; i < splitStatesAB.length; ++i){
          if(splitStatesAB[i] == 1)
              countLenAB++;
      }

      var counterLooping = 0

      while (counterLooping < y_test.length) {

        if ((this.activeInstance - 1) < 0) {
          this.activeInstance = (this.resultsFinal[2].length - 1)
        } else {
          this.activeInstance = this.activeInstance - 1
        }

        EventBus.$emit('activeTestInstance', this.activeInstance)

        var tempResults = 0

        var countRF = new Array(target_names.length).fill(0);

        for (var k = 0; k < Object.values(RFPredictions[this.activeInstance]).length; k++) {
          if (splitStatesRF[k] == 1) {
            if (Object.values(RFPredictions[this.activeInstance])[this.RFSort[k]] == 0) {
              countRF[0] = countRF[0] + 1
            } else if (Object.values(RFPredictions[this.activeInstance])[this.RFSort[k]] == 1) {
              countRF[1] = countRF[1] + 1
            } else {
              countRF[2] = countRF[2] + 1
            }
          }
        }

        for (var m = 0; m < countRF.length; m++) {
          countRF[m] = (countRF[m] / countLenRF) * 100
        }

        var countGB = new Array(target_names.length).fill(0);

        for (var k = 0; k < Object.values(GBPredictions[this.activeInstance]).length; k++) {
          if (splitStatesAB[k] == 1) {
            if (Object.values(GBPredictions[this.activeInstance])[this.GBSort[k]] == 0) {
              countGB[0] = countGB[0] + 1
            } else if (Object.values(GBPredictions[this.activeInstance])[this.GBSort[k]] == 1) {
              countGB[1] = countGB[1] + 1
            } else {
              countGB[2] = countGB[2] + 1
            }
          }
        }
        for (var m = 0; m < countGB.length; m++) {
          countGB[m] = (countGB[m] / countLenAB) * 100
        }

        for (var i = 0; i < target_names.length; i++) {
          if (i == y_test[this.activeInstance]) {
            tempResults = countRF[i] + countGB[i]
          }
        }

        tempResults = tempResults / 2
        
        if (this.activeMode == 0) {
          break
        } else if (this.activeMode == 1) {
          if (Number.parseInt(tempResults) < 51) {
            break
          }

        } else {
          if (Number.parseInt(tempResults) != 100) {
            break
          }
          if (counterLooping == y_test.length) {
            break
          }
        }
        counterLooping++
      }
      this.finalDecisionView()
    },
    right () {
      EventBus.$emit('onHold', false)
      EventBus.$emit('flagtoTrue', true)
      var RFPredictions = JSON.parse(this.resultsFinal[0])
      var GBPredictions = JSON.parse(this.resultsFinal[1])
      var y_test = this.resultsFinal[2]     
      var target_names = this.resultsFinal[3]

      var splitStatesRF = []
      var splitStatesAB = []
      for (let i = 0; i < this.states.length; i++) {
        if (i%2 == 0) {
          splitStatesRF.push(this.states[i])
        } else {
          splitStatesAB.push(this.states[i])
        }
      }

      var countLenRF = 0;
      for(var i = 0; i < splitStatesRF.length; ++i){
          if(splitStatesRF[i] == 1)
              countLenRF++;
      }

      var countLenAB = 0;
      for(var i = 0; i < splitStatesAB.length; ++i){
          if(splitStatesAB[i] == 1)
              countLenAB++;
      }

      var counterLooping = 0

      while (counterLooping < y_test.length) {

        if ((this.activeInstance + 1) > (this.resultsFinal[2].length - 1)) {
          this.activeInstance = 0
        } else {
          this.activeInstance = this.activeInstance + 1
        }

        EventBus.$emit('activeTestInstance', this.activeInstance)

        var tempResults = 0

        var countRF = new Array(target_names.length).fill(0);

        for (var k = 0; k < Object.values(RFPredictions[this.activeInstance]).length; k++) {
          if (splitStatesRF[k] == 1) {
            if (Object.values(RFPredictions[this.activeInstance])[this.RFSort[k]] == 0) {
              countRF[0] = countRF[0] + 1
            } else if (Object.values(RFPredictions[this.activeInstance])[this.RFSort[k]] == 1) {
              countRF[1] = countRF[1] + 1
            } else {
              countRF[2] = countRF[2] + 1
            }
          }
        }

        for (var m = 0; m < countRF.length; m++) {
          countRF[m] = (countRF[m] / countLenRF) * 100
        }

        var countGB = new Array(target_names.length).fill(0);

        for (var k = 0; k < Object.values(GBPredictions[this.activeInstance]).length; k++) {
          if (splitStatesAB[k] == 1) {
            if (Object.values(GBPredictions[this.activeInstance])[this.GBSort[k]] == 0) {
              countGB[0] = countGB[0] + 1
            } else if (Object.values(GBPredictions[this.activeInstance])[this.GBSort[k]] == 1) {
              countGB[1] = countGB[1] + 1
            } else {
              countGB[2] = countGB[2] + 1
            }
          }
        }
        for (var m = 0; m < countGB.length; m++) {
          countGB[m] = (countGB[m] / countLenAB) * 100
        }

        for (var i = 0; i < target_names.length; i++) {
          if (i == y_test[this.activeInstance]) {
            tempResults = countRF[i] + countGB[i]
          }
        }

        tempResults = tempResults / 2

        if (this.activeMode == 0) {
          break
        } else if (this.activeMode == 1) {
          if (Number.parseInt(tempResults) < 51) {
            break
          }

        } else {
          if (Number.parseInt(tempResults) != 100) {
            break
          }
          if (counterLooping == y_test.length) {
            break
          }
        }
        counterLooping++
      }
      this.finalDecisionView()
    },
    finalDecisionView () {

      var splitStatesRF = []
      var splitStatesAB = []
      for (let i = 0; i < this.states.length; i++) {
        if (i%2 == 0) {
          splitStatesRF.push(this.states[i])
        } else {
          splitStatesAB.push(this.states[i])
        }
      }

      var countLenRF = 0;
      for(var i = 0; i < splitStatesRF.length; ++i){
          if(splitStatesRF[i] == 1)
              countLenRF++;
      }

      var countLenAB = 0;
      for(var i = 0; i < splitStatesAB.length; ++i){
          if(splitStatesAB[i] == 1)
              countLenAB++;
      }

      var RFPredictions = JSON.parse(this.resultsFinal[0])
      var GBPredictions = JSON.parse(this.resultsFinal[1])

      var target_names = this.resultsFinal[3]

      var manual = this.manualDecisions
      var countManual = new Array(target_names.length).fill(0);

      for (var loopM = 0; loopM < manual.length; loopM++) {
        if (manual[loopM] == 0) {
          countManual[0] = countManual[0] + 1
        } else if (manual[loopM] == 1) {
          countManual[1] = countManual[1] + 1
        } else {
          countManual[2] = countManual[2] + 1
        }
      }
      
      for (var looping = 0; looping < countManual.length; looping++) {
        countManual[looping] = (countManual[looping] / manual.length) * 100
      }

      var countRF = new Array(target_names.length).fill(0);

      for (var k = 0; k < Object.values(RFPredictions[this.activeInstance]).length; k++) {
        if (splitStatesRF[k] == 1) {
          if (Object.values(RFPredictions[this.activeInstance])[this.RFSort[k]] == 0) {
            countRF[0] = countRF[0] + 1
          } else if (Object.values(RFPredictions[this.activeInstance])[this.RFSort[k]] == 1) {
            countRF[1] = countRF[1] + 1
          } else {
            countRF[2] = countRF[2] + 1
          }
        }
      }

      for (var m = 0; m < countRF.length; m++) {
        countRF[m] = (countRF[m] / countLenRF) * 100
      }

      var countGB = new Array(target_names.length).fill(0);

      for (var k = 0; k < Object.values(GBPredictions[this.activeInstance]).length; k++) {
        if (splitStatesAB[k] == 1) {
          if (Object.values(GBPredictions[this.activeInstance])[this.GBSort[k]] == 0) {
            countGB[0] = countGB[0] + 1
          } else if (Object.values(GBPredictions[this.activeInstance])[this.GBSort[k]] == 1) {
            countGB[1] = countGB[1] + 1
          } else {
            countGB[2] = countGB[2] + 1
          }
        }
      }
      for (var m = 0; m < countGB.length; m++) {
        countGB[m] = (countGB[m] / countLenAB) * 100
      }

      var y_test = this.resultsFinal[2]     

      this.whichActive = 'test instance #' + (this.activeInstance+1) + ' (out of ' + y_test.length + ')'
      var groupResults = []
      for (var i = 0; i < target_names.length; i++) {
        var tempResults = []
        tempResults.push(countManual[i]) // manual
        tempResults.push(countRF[i])
        tempResults.push(countGB[i])
        if (i == y_test[this.activeInstance]) {
          tempResults.push(100)
        } else {
          tempResults.push(0)
        }
        groupResults.push(tempResults)
      }

      Plotly.purge('finalDecision')

      if (target_names.length == 2) {
        var trace1 = {
          x: groupResults[0],
          y: ['MD', 'RF', 'AB', '<b>GT</b>'],
          name: 'Class1',
          orientation: 'h',
          marker: {
            color: 'rgba(190, 186, 218, 1.0)',
            width: 1,
            line: {
              color: 'rgba(0,0,0,1.0)',
              width: 1
            }
          },
          type: 'bar'
        };

        var trace2 = {
          x: groupResults[1],
          y: ['MD', 'RF', 'AB', '<b>GT</b>'],
          name: 'Class2',
          orientation: 'h',
          type: 'bar',
          marker: {
            color: 'rgba(253, 180, 98, 1.0)',
            width: 1,
            line: {
              color: 'rgba(0,0,0,1.0)',
              width: 1
            }
          }
        };

        var data = [trace1, trace2];
      } else {
        var trace1 = {
          x: groupResults[0],
          y: ['MD', 'RF', 'AB', '<b>GT</b>'],
          name: 'Class1',
          orientation: 'h',
          marker: {
            color: 'rgba(190, 186, 218, 1.0)',
            width: 1,
            line: {
              color: 'rgba(0,0,0,1.0)',
              width: 1
            }
          },
          type: 'bar'
        };

        var trace2 = {
          x: groupResults[1],
          y: ['MD', 'RF', 'AB', '<b>GT</b>'],
          name: 'Class2',
          orientation: 'h',
          type: 'bar',
          marker: {
            color: 'rgba(253, 180, 98, 1.0)',
            width: 1,
            line: {
              color: 'rgba(0,0,0,1.0)',
              width: 1
            }
          }
        };

        var trace3 = {
          x: groupResults[2],
          y: ['MD', 'RF', 'AB', '<b>GT</b>'],
          name: 'Class3',
          orientation: 'h',
          type: 'bar',
          marker: {
            color: 'rgba(251, 128, 114, 1.0)',
            width: 1,
            line: {
              color: 'rgba(0,0,0,1.0)',
              width: 1
            }
          }
        };

        var data = [trace1, trace2, trace3];
      }

      var width = 370
      var height = 160

      var layout = {
        barmode: 'stack',
        font: { family: 'Helvetica', size: 14, color: '#000000' },
          autosize: false,
          width: width,
          height: height,
          showlegend: false,
          yaxis:{
              autorange:'reversed',
          },
          xaxis: {
            title: 'Class Agreement (%)'
          },
          margin: {
            l: 30,
            r: 0,
            b: 40,
            t: 5,
            pad: 0
          },
      };

      Plotly.newPlot('finalDecision', data, layout, {staticPlot: true});
    },
    clean(obj) {
      var propNames = Object.getOwnPropertyNames(obj);
      for (var i = 0; i < propNames.length; i++) {
        var propName = propNames[i];
        if (obj[propName] === null || obj[propName] === undefined) {
          delete obj[propName];
        }
      }
    },
    chartView() {

      var splitStatesRF = []
      var splitStatesAB = []
      for (let i = 0; i < this.states.length; i++) {
        if (i%2 == 0) {
          splitStatesRF.push(this.states[i])
        } else {
          splitStatesAB.push(this.states[i])
        }
      }

      var RFHyper = this.descriptiveRules[7]
      var ABHyper = this.descriptiveRules[8]

      var outcomeRF = this.totalPerformRF
      var outcomeAB = this.totalPerformAB

      var maxRF = Math.max(...outcomeRF)
      var minRF = Math.min(...outcomeRF)
      var maxAB = Math.max(...outcomeAB)
      var minAB = Math.min(...outcomeAB)

      var parametersLocRF = JSON.parse(this.HyperParamsAll[1])
      var parametersRF = parametersLocRF.params
      var parametersLocAB = JSON.parse(this.HyperParamsAll[18])
      var parametersAB = parametersLocAB.params

      var stringParametersRF = []
      for (let j = 0; j < this.RFSort.length; j++) {
        stringParametersRF.push(Object.values(parametersRF)[this.RFSort[j]])
      }

      var stringParametersAB = []
      for (let j = 0; j < this.GBSort.length; j++) {
        stringParametersAB.push(Object.values(parametersAB)[this.GBSort[j]])
      }

      var colors = ["#33a02c", "#1f78b4", "#a65628", "#ffffff"];

      var DataSetParseRF = []
      var listOfObjectsRF = []
      // max
      listOfObjectsRF["ID"] = -1
      listOfObjectsRF["Ov. Score (%)"] = maxRF
      listOfObjectsRF["n_estimators"] = Math.max(...RFHyper.n_estimators)
      listOfObjectsRF["max_depth"] = Math.max(...RFHyper.max_depth)
      listOfObjectsRF["min_samples_leaf"] = Math.max(...RFHyper.min_samples_leaf)
      listOfObjectsRF["max_features"] = Math.max(...RFHyper.max_features)
      listOfObjectsRF["color"] = 3
      DataSetParseRF.push(listOfObjectsRF)

      listOfObjectsRF = []
      // min
      listOfObjectsRF["ID"] = -2
      listOfObjectsRF["Ov. Score (%)"] = minRF
      listOfObjectsRF["n_estimators"] = Math.min(...RFHyper.n_estimators)
      listOfObjectsRF["max_depth"] = Math.min(...RFHyper.max_depth)
      listOfObjectsRF["min_samples_leaf"] = Math.min(...RFHyper.min_samples_leaf)
      listOfObjectsRF["max_features"] = Math.min(...RFHyper.max_features)
      listOfObjectsRF["color"] = 3
      DataSetParseRF.push(listOfObjectsRF)
        
      for (var loopRF = 0; loopRF < splitStatesRF.length; loopRF++) {
        listOfObjectsRF = []
        listOfObjectsRF["ID"] = loopRF
        listOfObjectsRF["Ov. Score (%)"] = parseFloat(outcomeRF[loopRF])
        listOfObjectsRF[Object.keys(stringParametersRF[loopRF])[0]] = Object.values(stringParametersRF[loopRF])[0]
        listOfObjectsRF[Object.keys(stringParametersRF[loopRF])[3]] = Object.values(stringParametersRF[loopRF])[3]
        listOfObjectsRF[Object.keys(stringParametersRF[loopRF])[1]] = Object.values(stringParametersRF[loopRF])[1]
        listOfObjectsRF[Object.keys(stringParametersRF[loopRF])[2]] = Object.values(stringParametersRF[loopRF])[2]
        if (splitStatesRF[loopRF] == 1) {
          listOfObjectsRF["color"] = 0
        } else {
          listOfObjectsRF["color"] = 2
        }
        DataSetParseRF.push(listOfObjectsRF)
      }

      var DataSetParseAB = []
      var listOfObjectsAB = []

      // max
      listOfObjectsAB["ID"] = -1
      listOfObjectsAB["Ov. Score (%)"] = maxAB
      listOfObjectsAB["n_estimators"] = Math.max(...ABHyper.n_estimators)
      listOfObjectsAB["max_depth"] = Math.max(...ABHyper.base_estimator__max_depth)
      listOfObjectsAB["min_samples_leaf"] = Math.max(...ABHyper.base_estimator__min_samples_leaf)
      listOfObjectsAB["learning_rate"] = Math.max(...ABHyper.learning_rate)
      listOfObjectsAB["color"] = 3
      DataSetParseAB.push(listOfObjectsAB)

      listOfObjectsAB = []
      // min
      listOfObjectsAB["ID"] = -2
      listOfObjectsAB["Ov. Score (%)"] = minAB
      listOfObjectsAB["n_estimators"] = Math.min(...ABHyper.n_estimators)
      listOfObjectsAB["max_depth"] = Math.min(...ABHyper.base_estimator__max_depth)
      listOfObjectsAB["min_samples_leaf"] = Math.min(...ABHyper.base_estimator__min_samples_leaf)
      listOfObjectsAB["learning_rate"] = Math.min(...ABHyper.learning_rate)
      listOfObjectsAB["color"] = 3
      DataSetParseAB.push(listOfObjectsAB)

      for (var loopAB = 0; loopAB < splitStatesAB.length; loopAB++) {
        listOfObjectsAB = []
        listOfObjectsAB["ID"] = loopAB
        listOfObjectsAB["Ov. Score (%)"] = parseFloat(outcomeAB[loopAB])
        listOfObjectsAB[Object.keys(stringParametersAB[loopAB])[0]] = Object.values(stringParametersAB[loopAB])[0]
        listOfObjectsAB["max_depth"] = Object.values(stringParametersAB[loopAB])[3]
        listOfObjectsAB["min_samples_leaf"] = Object.values(stringParametersAB[loopAB])[2]
        listOfObjectsAB[Object.keys(stringParametersAB[loopAB])[1]] = Object.values(stringParametersAB[loopAB])[1]
        if (splitStatesAB[loopAB] == 1) {
          listOfObjectsAB["color"] = 1
        } else {
          listOfObjectsAB["color"] = 2
        }
        DataSetParseAB.push(listOfObjectsAB)
      }

      var width = 375
      var height = 223

      d3.selectAll("#chart > *").remove();
      d3.selectAll("#chart2 > *").remove();

        var togetherOutside = []
        togetherOutside.push('n_estimators')
        togetherOutside.push(RFHyper.n_estimators)
        EventBus.$emit('updateRFNewModels', togetherOutside)
        togetherOutside = []
        togetherOutside.push('max_depth')
        togetherOutside.push(RFHyper.max_depth)
        EventBus.$emit('updateRFNewModels', togetherOutside)
        togetherOutside = []
        togetherOutside.push('min_samples_leaf')
        togetherOutside.push(RFHyper.min_samples_leaf)
        EventBus.$emit('updateRFNewModels', togetherOutside)
        togetherOutside = []
        togetherOutside.push('max_features')
        togetherOutside.push(RFHyper.max_features)
        EventBus.$emit('updateRFNewModels', togetherOutside)

        togetherOutside = []
        togetherOutside.push('n_estimators')
        togetherOutside.push(ABHyper.n_estimators)
        EventBus.$emit('updateABNewModels', togetherOutside)
        togetherOutside = []
        togetherOutside.push('base_estimator__max_depth')
        togetherOutside.push(ABHyper.base_estimator__max_depth)
        EventBus.$emit('updateABNewModels', togetherOutside)
        togetherOutside = []
        togetherOutside.push('base_estimator__min_samples_leaf')
        togetherOutside.push(ABHyper.base_estimator__min_samples_leaf)
        EventBus.$emit('updateABNewModels', togetherOutside)
        togetherOutside = []
        togetherOutside.push('learning_rate')
        togetherOutside.push(ABHyper.learning_rate)
        EventBus.$emit('updateABNewModels', togetherOutside)
      
      var pc = ParCoords()("#chart")
        .data(DataSetParseRF)
        .width(width)
        .height(height)
        .margin({ top: 15, left: 20, bottom: 10, right: 18})
        .color(function(d, i) { return colors[d.color] })
        .bundlingStrength(0) // set bundling strength
        .smoothness(0)
        .bundleDimension("Ov. Score (%)")
        .showControlPoints(false)
        .hideAxis(["color","ID"])
        .dimensions({'Ov. Score (%)': {
            title: 'Ov. Score (%)',
            ticks: 4,
            type: 'number',
        }, 
        'n_estimators': {
                          title: 'n_estimators',
                          type: 'number',
                          //ticks: 20,
                          ticks: RFHyper.n_estimators.length,
                          tickValues: RFHyper.n_estimators
                        },
        'max_depth': {
                        title: 'max_depth',
                        type: 'number',
                        ticks: RFHyper.max_depth.length,
                        tickValues: RFHyper.max_depth
                      },
        'min_samples_leaf': {
                        title: 'min_samples_leaf',
                        type: 'number',
                        ticks: RFHyper.min_samples_leaf.length,
                        tickValues: RFHyper.min_samples_leaf
                      },
        'max_features': {
                        title: 'max_features',
                        type: 'number',
                        ticks: RFHyper.max_features.length,
                        tickValues: RFHyper.max_features
                      }
        })
        .render()
        .brushMode('1D-axes')

      var pc2 = ParCoords()("#chart2")
        .data(DataSetParseAB)
        .width(width)
        .height(height)
        .margin({ top: 15, left: 20, bottom: 10, right: 18})
        .color(function(d, i) { return colors[d.color] })
        .bundlingStrength(0) // set bundling strength
        .smoothness(0)
        .bundleDimension("Ov. Score (%)")
        .showControlPoints(false)
        .hideAxis(["color","ID"])
        .dimensions({'Ov. Score (%)': {
            type: 'number',
            ticks: 4
        }, 
        'n_estimators': {
                            type: 'number',
                            //ticks: 20,
                            ticks: ABHyper.n_estimators.length,
                            tickValues: ABHyper.n_estimators
                        },
        'max_depth': {
                          type: 'number',
                          ticks: ABHyper.base_estimator__max_depth.length,
                          tickValues: ABHyper.base_estimator__max_depth
                      },
        'min_samples_leaf': {
                          type: 'number',
                          ticks: ABHyper.base_estimator__min_samples_leaf.length,
                          tickValues: ABHyper.base_estimator__min_samples_leaf
                      },
        'learning_rate': {
                          type: 'number',
                          ticks: ABHyper.learning_rate.length,
                          tickValues: ABHyper.learning_rate
                      }
        })
        .render()
        .brushMode('1D-axes')

      pc.on('brushend', function(brushed, args){
        var together = []
        if (Object.keys(pc.brushExtents()).length == 0) {
          together.push('n_estimators')
          together.push(RFHyper.n_estimators)
          EventBus.$emit('updateRFNewModels', together)
          together = []
          together.push('max_depth')
          together.push(RFHyper.max_depth)
          EventBus.$emit('updateRFNewModels', together)
          together = []
          together.push('min_samples_leaf')
          together.push(RFHyper.min_samples_leaf)
          EventBus.$emit('updateRFNewModels', together)
          together = []
          together.push('max_features')
          together.push(RFHyper.max_features)
          EventBus.$emit('updateRFNewModels', together)
        }
        for (let index = 0; index < Object.keys(pc.brushExtents()).length; index++) {
          var extracted = Object.values(Object.values(Object.values(pc.brushExtents())[index])[1])[1]
          var number1 = extracted[0]
          var number2 = extracted[1]
          var gatherRanges = [];
          if (number1 > number2) {
            for (var i = Math.ceil(number2); i <= parseInt(number1); i++) {
                gatherRanges.push(i);
            }
          } else {
            for (var i = Math.ceil(number1); i <= parseInt(number2); i++) {
                gatherRanges.push(i);
            }
          }
          together.push(Object.keys(pc.brushExtents())[index])
          together.push(gatherRanges)
          EventBus.$emit('updateRFNewModels', together)
        }
      })

      pc2.on('brushend', function(brushed, args){
        var together = []
        if (Object.keys(pc2.brushExtents()).length == 0) {
          together.push('n_estimators')
          together.push(ABHyper.n_estimators)
          EventBus.$emit('updateABNewModels', together)
          together = []
          together.push('base_estimator__max_depth')
          together.push(ABHyper.base_estimator__max_depth)
          EventBus.$emit('updateABNewModels', together)
          together = []
          together.push('base_estimator__min_samples_leaf')
          together.push(ABHyper.base_estimator__min_samples_leaf)
          EventBus.$emit('updateABNewModels', together)
          together = []
          together.push('learning_rate')
          together.push(ABHyper.learning_rate)
          EventBus.$emit('updateABNewModels', together)
        }
        for (let index = 0; index < Object.keys(pc2.brushExtents()).length; index++) {
          var extracted = Object.values(Object.values(Object.values(pc2.brushExtents())[index])[1])[1]
          var number1 = extracted[0]
          var number2 = extracted[1]
          var gatherRanges = [];
          if((Object.keys(pc2.brushExtents())[index]) == 'learning_rate') {
            if (number1 > number2) {
              for (var i = Math.ceil(number2*10); i <= parseInt(number1*10); i++) {
                  gatherRanges.push(i/10);
              }
            } else {
              for (var i = Math.ceil(number1*10); i <= parseInt(number2*10); i++) {
                  gatherRanges.push(i/10);
              }
            }
          } else {
            if (number1 > number2) {
              for (var i = Math.ceil(number2); i <= parseInt(number1); i++) {
                  gatherRanges.push(i);
              }
            } else {
              for (var i = Math.ceil(number1); i <= parseInt(number2); i++) {
                  gatherRanges.push(i);
              }
            }
          }
          together.push(Object.keys(pc2.brushExtents())[index])
          together.push(gatherRanges)
          EventBus.$emit('updateABNewModels', together)
        }
      })

    },
    reset () {
      d3.selectAll("#thres > *").remove();
      var svg = d3v5.select("#chart");
      svg.selectAll("*").remove();
      Plotly.purge('finalDecision')
      d3.selectAll("#chart > *").remove();
      d3.selectAll("#chart2 > *").remove();
    },
  },
  mounted() {

    EventBus.$on('StatesUpdate', data => {
      this.states = data})

    EventBus.$on('CorrThres', data => { this.threshold = data })
    EventBus.$on('callSliderAgain', this.InitSlider)

    EventBus.$on('indicesRFSend', data => { this.RFSort = data })
    EventBus.$on('indicesGBSend', data => { this.GBSort = data })

    EventBus.$on('sendCombinedPerformanceRF', data => { this.totalPerformRF = data })
    EventBus.$on('sendCombinedPerformanceAB', data => { this.totalPerformAB = data })
    EventBus.$on('emittedEventCallingHyperParams', data => { this.HyperParamsAll = data })

    EventBus.$on('changeInNumberOfModelsImp', data => { this.states = data })
    EventBus.$on('changeInNumberOfModelsImp', this.chartView)

    EventBus.$on('manualDecisions', data => { this.manualDecisions = data })
    EventBus.$on('manualDecisions', this.finalDecisionView)
    EventBus.$on('emittedEventCallingResult', data => { this.resultsFinal = data })

    EventBus.$on('emittedEventCallingRules', data => { this.descriptiveRules = data })
    EventBus.$on('emittedEventCallingRules', this.chartView)

    EventBus.$on('reset', this.reset)
  }
}
</script>

<style>

g.profile g.multi {
  opacity: 0.8;
}
g.profile g.multi:hover {
  opacity: 1.0;
}

.nav-link {
  color: black !important;
}

.nav-link.active {
  color: #000 !important;
}

.slider-handle {
  background: #000 !important;
}

.checkID input[type=checkbox] {
    display: none;
}

.checkID input:checked + label {
    color: #000;
}

.checkID input:checked + label:before {
    content: "\2713 ";
}

.checkID {
  border: solid 1px black;
}

/* new stuff */
.check {
    visibility: hidden;
}

input:checked + label .check {
    visibility: visible;
}

input.checkbox:checked + label:before {
  
    content: "";
}



.switch-toggle {
  font-size: 16px;
}

.switch-toggle label:not(.disabled) {
  cursor: pointer;
}

.switch-toggle a, .switch-light span span {
  display: none; }

/* We can't test for a specific feature,
 * so we only target browsers with support for media queries.
 */
@media only screen {
  /* Checkbox
 */
  .switch-light {
    position: relative;
    display: block;
    /* simulate default browser focus outlines on the switch,
   * when the inputs are focused.
   */ }
    .switch-light::after {
      clear: both;
      content: "";
      display: table; }
    .switch-light *, .switch-light *:before, .switch-light *:after {
      box-sizing: border-box; }
    .switch-light a {
      display: block;
      -webkit-transition: all 0.2s ease-out;
      -moz-transition: all 0.2s ease-out;
      transition: all 0.2s ease-out; }
    .switch-light label, .switch-light > span {
      /* breathing room for bootstrap/foundation classes.
     */
      line-height: 2em;
      vertical-align: middle; }
    .switch-light input:focus ~ span a, .switch-light input:focus + label {
      outline-width: 2px;
      outline-style: solid;
      outline-color: Highlight;
      /* Chrome/Opera gets its native focus styles.
     */ }
      @media (-webkit-min-device-pixel-ratio: 0) {
        .switch-light input:focus ~ span a, .switch-light input:focus + label {
          outline-color: -webkit-focus-ring-color;
          outline-style: auto; } }
  /* don't hide the input from screen-readers and keyboard access
 */
  .switch-light input {
    position: absolute;
    opacity: 0;
    z-index: 3; }
  .switch-light input:checked ~ span a {
    right: 0%; }
  /* inherit from label
 */
  .switch-light strong {
    font-weight: inherit; }
  .switch-light > span {
    position: relative;
    overflow: hidden;
    display: block;
    min-height: 2em;
    /* overwrite 3rd party classes padding
   * eg. bootstrap .well
   */
    padding: 0;
    text-align: left; }
  .switch-light span span {
    position: relative;
    z-index: 2;
    display: block;
    float: left;
    width: 50%;
    text-align: center;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none; }
  .switch-light a {
    position: absolute;
    right: 50%;
    top: 0;
    z-index: 1;
    display: block;
    width: 50%;
    height: 100%;
    padding: 0; }
  /* Radio Switch
 */
  .switch-toggle {
    position: relative;
    display: block;
    /* simulate default browser focus outlines on the switch,
   * when the inputs are focused.
   */
    /* For callout panels in foundation
  */
    padding: 0 !important;
    /* 2 items
   */
    /* 3 items
   */
    /* 4 items
   */
    /* 5 items
   */
    /* 6 items
   */ }
    .switch-toggle::after {
      clear: both;
      content: "";
      display: table; }
    .switch-toggle *, .switch-toggle *:before, .switch-toggle *:after {
      box-sizing: border-box; }
    .switch-toggle a {
      display: block;
      -webkit-transition: all 0.2s ease-out;
      -moz-transition: all 0.2s ease-out;
      transition: all 0.2s ease-out; }
    .switch-toggle label, .switch-toggle > span {
      /* breathing room for bootstrap/foundation classes.
     */
      line-height: 2em;
      vertical-align: middle; }
    .switch-toggle input:focus ~ span a, .switch-toggle input:focus + label {
      outline-width: 2px;
      outline-style: solid;
      outline-color: Highlight;
      /* Chrome/Opera gets its native focus styles.
     */ }
      @media (-webkit-min-device-pixel-ratio: 0) {
        .switch-toggle input:focus ~ span a, .switch-toggle input:focus + label {
          outline-color: -webkit-focus-ring-color;
          outline-style: auto; } }
    .switch-toggle input {
      position: absolute;
      left: 0;
      opacity: 0; }
    .switch-toggle input + label {
      position: relative;
      z-index: 2;
      display: block;
      float: left;
      padding: 0 0.5em;
      margin: 0;
      text-align: center; }
    .switch-toggle a {
      position: absolute;
      top: 0;
      left: 0;
      padding: 0;
      z-index: 1;
      width: 10px;
      height: 100%; }
    .switch-toggle label:nth-child(2):nth-last-child(4), .switch-toggle label:nth-child(2):nth-last-child(4) ~ label, .switch-toggle label:nth-child(2):nth-last-child(4) ~ a {
      width: 50%; }
    .switch-toggle label:nth-child(2):nth-last-child(4) ~ input:checked:nth-child(3) + label ~ a {
      left: 50%; }
    .switch-toggle label:nth-child(2):nth-last-child(6), .switch-toggle label:nth-child(2):nth-last-child(6) ~ label, .switch-toggle label:nth-child(2):nth-last-child(6) ~ a {
      width: 33.33%; }
    .switch-toggle label:nth-child(2):nth-last-child(6) ~ input:checked:nth-child(3) + label ~ a {
      left: 33.33%; }
    .switch-toggle label:nth-child(2):nth-last-child(6) ~ input:checked:nth-child(5) + label ~ a {
      left: 66.66%; }
    .switch-toggle label:nth-child(2):nth-last-child(8), .switch-toggle label:nth-child(2):nth-last-child(8) ~ label, .switch-toggle label:nth-child(2):nth-last-child(8) ~ a {
      width: 25%; }
    .switch-toggle label:nth-child(2):nth-last-child(8) ~ input:checked:nth-child(3) + label ~ a {
      left: 25%; }
    .switch-toggle label:nth-child(2):nth-last-child(8) ~ input:checked:nth-child(5) + label ~ a {
      left: 50%; }
    .switch-toggle label:nth-child(2):nth-last-child(8) ~ input:checked:nth-child(7) + label ~ a {
      left: 75%; }
    .switch-toggle label:nth-child(2):nth-last-child(10), .switch-toggle label:nth-child(2):nth-last-child(10) ~ label, .switch-toggle label:nth-child(2):nth-last-child(10) ~ a {
      width: 20%; }
    .switch-toggle label:nth-child(2):nth-last-child(10) ~ input:checked:nth-child(3) + label ~ a {
      left: 20%; }
    .switch-toggle label:nth-child(2):nth-last-child(10) ~ input:checked:nth-child(5) + label ~ a {
      left: 40%; }
    .switch-toggle label:nth-child(2):nth-last-child(10) ~ input:checked:nth-child(7) + label ~ a {
      left: 60%; }
    .switch-toggle label:nth-child(2):nth-last-child(10) ~ input:checked:nth-child(9) + label ~ a {
      left: 80%; }
    .switch-toggle label:nth-child(2):nth-last-child(12), .switch-toggle label:nth-child(2):nth-last-child(12) ~ label, .switch-toggle label:nth-child(2):nth-last-child(12) ~ a {
      width: 16.6%; }
    .switch-toggle label:nth-child(2):nth-last-child(12) ~ input:checked:nth-child(3) + label ~ a {
      left: 16.6%; }
    .switch-toggle label:nth-child(2):nth-last-child(12) ~ input:checked:nth-child(5) + label ~ a {
      left: 33.2%; }
    .switch-toggle label:nth-child(2):nth-last-child(12) ~ input:checked:nth-child(7) + label ~ a {
      left: 49.8%; }
    .switch-toggle label:nth-child(2):nth-last-child(12) ~ input:checked:nth-child(9) + label ~ a {
      left: 66.4%; }
    .switch-toggle label:nth-child(2):nth-last-child(12) ~ input:checked:nth-child(11) + label ~ a {
      left: 83%; }
  /* Candy Theme
 * Based on the "Sort Switches / Toggles (PSD)" by Ormal Clarck
 * http://www.premiumpixels.com/freebies/sort-switches-toggles-psd/
 */
  .switch-toggle.switch-candy, .switch-light.switch-candy > span {
    background-color: #efefef;
    border-radius: 3px;
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.3), 0 1px 0 rgba(255, 255, 255, 0.2); }
  .switch-light.switch-candy span span, .switch-light.switch-candy input:checked ~ span span:first-child, .switch-toggle.switch-candy label {
    color: #000;
    font-weight: bold;
    text-align: center;
    text-shadow: 0 0 0 #191b1e; }
  .switch-light.switch-candy input ~ span span:first-child, .switch-light.switch-candy input:checked ~ span span:nth-child(2), .switch-candy input:checked + label {
    color: #fff;
    text-shadow: 0 0 0 rgba(255, 255, 255, 0.5); }
  .switch-candy a {
    border: 1px solid #333;
    border-radius: 3px;
    box-shadow: 0 1px 1px rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.45);
    background-color: #000;
    background-image: -webkit-linear-gradient(top, rgba(255, 255, 255, 0.2), transparent);
    background-image: linear-gradient(to bottom, rgba(255, 255, 255, 0.2), transparent); }
  .switch-candy-blue a {
    background-color: #000; }
  .switch-candy-yellow a {
    background-color: #f5e560; }
  /* iOS Theme
*/
  .switch-ios.switch-light span span {
    color: #888b92; }
  .switch-ios.switch-light a {
    left: 0;
    top: 0;
    width: 2em;
    height: 2em;
    background-color: #fff;
    border-radius: 100%;
    border: 0.25em solid #D8D9DB;
    -webkit-transition: all .2s ease-out;
    -moz-transition: all .2s ease-out;
    transition: all .2s ease-out; }
  .switch-ios.switch-light > span {
    display: block;
    width: 100%;
    height: 2em;
    background-color: #D8D9DB;
    border-radius: 1.75em;
    -webkit-transition: all .4s ease-out;
    -moz-transition: all .4s ease-out;
    transition: all .4s ease-out; }
  .switch-ios.switch-light > span span {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    opacity: 0;
    line-height: 1.875em;
    vertical-align: middle;
    -webkit-transition: all .2s ease-out;
    -moz-transition: all .2s ease-out;
    transition: all .2s ease-out; }
    .switch-ios.switch-light > span span:first-of-type {
      opacity: 1;
      padding-left: 1.875em; }
    .switch-ios.switch-light > span span:last-of-type {
      padding-right: 1.875em; }
  .switch-ios.switch-light input:checked ~ span a {
    left: 100%;
    border-color: #4BD865;
    margin-left: -2em; }
  .switch-ios.switch-light input:checked ~ span {
    border-color: #4BD865;
    box-shadow: inset 0 0 0 30px #4BD865; }
  .switch-ios.switch-light input:checked ~ span span:first-of-type {
    opacity: 0; }
  .switch-ios.switch-light input:checked ~ span span:last-of-type {
    opacity: 1;
    color: #fff; }
  .switch-ios.switch-toggle {
    background-color: #D8D9DB;
    border-radius: 30px;
    box-shadow: inset rgba(0, 0, 0, 0.1) 0 1px 0; }
    .switch-ios.switch-toggle a {
      background-color: #4BD865;
      border: 0.125em solid #D8D9DB;
      border-radius: 1.75em;
      -webkit-transition: all 0.12s ease-out;
      -moz-transition: all 0.12s ease-out;
      transition: all 0.12s ease-out; }
    .switch-ios.switch-toggle label {
      height: 2.4em;
      color: #888b92;
      line-height: 2.4em;
      vertical-align: middle; }
  .switch-ios input:checked + label {
    color: #3e4043; }
  /* Holo Theme
 */
  .switch-toggle.switch-holo, .switch-light.switch-holo > span {
    background-color: #464747;
    border-radius: 1px;
    box-shadow: inset rgba(0, 0, 0, 0.1) 0 1px 0;
    color: #fff;
    text-transform: uppercase; }
  .switch-holo label {
    color: #fff; }
  .switch-holo > span span {
    opacity: 0;
    -webkit-transition: all 0.1s;
    -moz-transition: all 0.1s;
    transition: all 0.1s; }
    .switch-holo > span span:first-of-type {
      opacity: 1; }
  .switch-holo > span span, .switch-holo label {
    font-size: 85%;
    line-height: 2.15625em; }
  .switch-holo a {
    background-color: #666;
    border-radius: 1px;
    box-shadow: inset rgba(255, 255, 255, 0.2) 0 1px 0, inset rgba(0, 0, 0, 0.3) 0 -1px 0; }
  /* Selected ON switch-light
*/
  .switch-holo.switch-light input:checked ~ span a {
    background-color: #000; }
  .switch-holo.switch-light input:checked ~ span span:first-of-type {
    opacity: 0; }
  .switch-holo.switch-light input:checked ~ span span:last-of-type {
    opacity: 1; }
  /* Material Theme
 */
  /* switch-light
 */
  .switch-light.switch-material a {
    top: -0.1875em;
    width: 1.75em;
    height: 1.75em;
    border-radius: 50%;
    background: #fafafa;
    box-shadow: 0 0.125em 0.125em 0 rgba(0, 0, 0, 0.14), 0 0.1875em 0.125em -0.125em rgba(0, 0, 0, 0.2), 0 0.125em 0.25em 0 rgba(0, 0, 0, 0.12);
    -webkit-transition: right .28s cubic-bezier(.4, 0, .2, 1);
    -moz-transition: right .28s cubic-bezier(.4, 0, .2, 1);
    transition: right .28s cubic-bezier(.4, 0, .2, 1); }
  .switch-material.switch-light {
    overflow: visible; }
    .switch-material.switch-light::after {
      clear: both;
      content: "";
      display: table; }
  .switch-material.switch-light > span {
    overflow: visible;
    position: relative;
    top: 0.1875em;
    width: 3.25em;
    height: 1.5em;
    min-height: auto;
    border-radius: 1em;
    background: rgba(0, 0, 0, 0.26); }
  .switch-material.switch-light span span {
    position: absolute;
    clip: rect(0 0 0 0); }
  .switch-material.switch-light input:checked ~ span a {
    right: 0;
    background: #000;
    box-shadow: 0 0.1875em 0.25em 0 rgba(0, 0, 0, 0.14), 0 0.1875em 0.1875em -0.125em rgba(0, 0, 0, 0.2), 0 0.0625em 0.375em 0 rgba(0, 0, 0, 0.12); }
  .switch-material.switch-light input:checked ~ span {
    background: rgba(63, 81, 181, 0.5); }
  /* switch-toggle
 */
  .switch-toggle.switch-material {
    overflow: visible; }
    .switch-toggle.switch-material::after {
      clear: both;
      content: "";
      display: table; }
  .switch-toggle.switch-material a {
    top: 48%;
    width: 0.375em !important;
    height: 0.375em;
    margin-left: 0.25em;
    background: #000;
    border-radius: 100%;
    -webkit-transform: translateY(-50%);
    -moz-transform: translateY(-50%);
    -ms-transform: translateY(-50%);
    -o-transform: translateY(-50%);
    transform: translateY(-50%);
    -webkit-transition: -webkit-transform 0.4s ease-in;
    -moz-transition: -moz-transform 0.4s ease-in;
    transition: transform 0.4s ease-in; }
  .switch-toggle.switch-material label {
    color: rgba(0, 0, 0, 0.54);
    font-size: 1em; }
  .switch-toggle.switch-material label:before {
    content: '';
    position: absolute;
    top: 48%;
    left: 0;
    display: block;
    width: 0.875em;
    height: 0.875em;
    border-radius: 100%;
    border: 0.125em solid rgba(0, 0, 0, 0.54);
    -webkit-transform: translateY(-50%);
    -moz-transform: translateY(-50%);
    -ms-transform: translateY(-50%);
    -o-transform: translateY(-50%);
    transform: translateY(-50%); }
  .switch-toggle.switch-material input:checked + label:before {
    border-color: #000; }
  /* ripple
 */
  .switch-light.switch-material > span:before, .switch-light.switch-material > span:after, .switch-toggle.switch-material label:after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    z-index: 3;
    display: block;
    width: 4em;
    height: 4em;
    border-radius: 100%;
    background: #000;
    opacity: .4;
    margin-left: -1.25em;
    margin-top: -1.25em;
    -webkit-transform: scale(0);
    -moz-transform: scale(0);
    -ms-transform: scale(0);
    -o-transform: scale(0);
    transform: scale(0);
    -webkit-transition: opacity .4s ease-in;
    -moz-transition: opacity .4s ease-in;
    transition: opacity .4s ease-in; }
  .switch-light.switch-material > span:after {
    left: auto;
    right: 0;
    margin-left: 0;
    margin-right: -1.25em; }
  .switch-toggle.switch-material label:after {
    width: 3.25em;
    height: 3.25em;
    margin-top: -0.75em; }
  @-webkit-keyframes materialRipple {
    0% {
      -webkit-transform: scale(0); }

    20% {
      -webkit-transform: scale(1); }

    100% {
      opacity: 0;
      -webkit-transform: scale(1); } }

  @-moz-keyframes materialRipple {
    0% {
      -moz-transform: scale(0); }

    20% {
      -moz-transform: scale(1); }

    100% {
      opacity: 0;
      -moz-transform: scale(1); } }

  @keyframes materialRipple {
    0% {
      -webkit-transform: scale(0);
      -moz-transform: scale(0);
      -ms-transform: scale(0);
      -o-transform: scale(0);
      transform: scale(0); }

    20% {
      -webkit-transform: scale(1);
      -moz-transform: scale(1);
      -ms-transform: scale(1);
      -o-transform: scale(1);
      transform: scale(1); }

    100% {
      opacity: 0;
      -webkit-transform: scale(1);
      -moz-transform: scale(1);
      -ms-transform: scale(1);
      -o-transform: scale(1);
      transform: scale(1); } }

  .switch-material.switch-light input:not(:checked) ~ span:after, .switch-material.switch-light input:checked ~ span:before, .switch-toggle.switch-material input:checked + label:after {
    -webkit-animation: materialRipple .4s ease-in;
    -moz-animation: materialRipple .4s ease-in;
    animation: materialRipple .4s ease-in; }
  /* trick to prevent the default checked ripple animation from showing
 * when the page loads.
 * the ripples are hidden by default, and shown only when the input is focused.
 */
  .switch-light.switch-material.switch-light input ~ span:before, .switch-light.switch-material.switch-light input ~ span:after, .switch-material.switch-toggle input + label:after {
    visibility: hidden; }
  .switch-light.switch-material.switch-light input:focus:checked ~ span:before, .switch-light.switch-material.switch-light input:focus:not(:checked) ~ span:after, .switch-material.switch-toggle input:focus:checked + label:after {
    visibility: visible; } }

/* Bugfix for older Webkit, including mobile Webkit. Adapted from
 * http://css-tricks.com/webkit-sibling-bug/
 */
@media only screen and (-webkit-max-device-pixel-ratio: 2) and (max-device-width: 80em) {
  .switch-light, .switch-toggle {
    -webkit-animation: webkitSiblingBugfix infinite 1s; } }

@-webkit-keyframes webkitSiblingBugfix {
  from {
    -webkit-transform: translate3d(0, 0, 0); }

  to {
    -webkit-transform: translate3d(0, 0, 0); } }

/*# sourceMappingURL=toggle-switch.css.map */

.parcoords svg {
  position: relative !important;
  z-index: 1;
}

</style>
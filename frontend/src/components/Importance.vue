<template>
<div id = "absoluteGather">
  <div id="LayerOnTop"></div>
  <div id="BoxPlot"></div>
</div>
</template>

<script>

import { EventBus } from '../main.js'
import * as Plotly from 'plotly.js'
import $ from 'jquery'; // <-to import jquery

export default {
  name: "Importance",
  data () {
    return {
      FinalResultsImp: 0,
      states: [],
      xaxis: 10,
      xaxis2: 10, 
    }
  },
  methods: {
    reply_click(clicked_id)
    {
        alert(clicked_id);
    },
    reset () {
      Plotly.purge('BoxPlot')
    },
    BoxPlotView () {

      Plotly.purge('BoxPlot')

      var FIRFRaw = JSON.parse(this.FinalResultsImp[5])
      var FIGBRaw = JSON.parse(this.FinalResultsImp[22])
      var features = JSON.parse(this.FinalResultsImp[12])
      var FIRFTotal = [...FIRFRaw]
      var FIGBTotal = [...FIGBRaw]

      var splitStatesRF = []
      var splitStatesAB = []
      for (let i = 0; i < this.states.length; i++) {
        if (i%2 == 0) {
          splitStatesRF.push(this.states[i])
        } else {
          splitStatesAB.push(this.states[i])
        }
      }

      for (let i = 0; i < splitStatesRF.length; i++) {
        if (splitStatesRF[i] == 0) {
              FIRFRaw[i] = null
            }
      }
      for (let i = 0; i < splitStatesAB.length; i++) {
        if (splitStatesAB[i] == 0) {
              FIGBRaw[i] = null
            }
      }

      var FIRF = FIRFRaw.filter(function (el) {
        return el != null;
      });
      var FIGB = FIGBRaw.filter(function (el) {
        return el != null;
      });

      var maxPerModel = []
      var minPerModel = []

      for (var i = 0; i < this.xaxis; i++) {
        maxPerModel.push(Math.max(...FIRF[i]))
        minPerModel.push(Math.min(...FIRF[i]))
      }

      for (var i = 0; i < this.xaxis2; i++) {
        maxPerModel.push(Math.max(...FIGB[i]))
        minPerModel.push(Math.min(...FIGB[i]))
      }

      var maximum = Math.max(...maxPerModel)
      var minimum = Math.min(...minPerModel)

      var countFeaturesRF = []
      var countFeaturesGB = []
      var countDataRF = []
      var countDataGB = []

      for (var i = 0; i < this.xaxis; i++) {
        for (var j = 0; j < features.length; j++) {
          countDataRF.push((FIRF[i][j] - minimum) / (maximum - minimum))
          countFeaturesRF.push(features[j])
        }
      }

      for (var i = 0; i < this.xaxis2; i++) {
        for (var j = 0; j < features.length; j++) {
          countDataGB.push((FIGB[i][j] - minimum) / (maximum - minimum))
          countFeaturesGB.push(features[j])
        }
      }

      var indicesRF = []
      var indicesGB = []

      for (var j = 0; j < features.length; j++) {
        var indexesRF = getAllIndexes(countFeaturesRF, features[j]);
        indicesRF.push(indexesRF)
      }

      for (var j = 0; j < features.length; j++) {
        var indexesGB = getAllIndexes(countFeaturesGB, features[j]);
        indicesGB.push(indexesGB)
      }

      function getAllIndexes(arr, val) {
          var indexes = [], i;
          for(i = 0; i < arr.length; i++)
              if (arr[i] === val)
                  indexes.push(i);
          return indexes;
      }
      var sumForAverageRF
      var sumForAverageGB
      var averageAll = []
      var averageRF = []
      var averageGB = []

      for (var k = 0; k < indicesRF.length; k++) {
        sumForAverageRF = 0
        //sumForAverageGB = 0
        //sumForAverageAll = 0
        for (var l = 0; l < indicesRF[k].length; l++) {
          sumForAverageRF = sumForAverageRF + countDataRF[indicesRF[k][l]]
          //sumForAverageGB = sumForAverageGB + countDataGB[indices[k][l]]
          //sumForAverageAll = sumForAverageAll + countDataRF[indices[k][l]] + countDataGB[indices[k][l]]
        }
        averageRF.push(sumForAverageRF / (this.xaxis))
        //averageGB.push(sumForAverageGB / (this.xaxis2))
        //averageAll.push((sumForAverageRF + sumForAverageGB) / (this.xaxis + this.xaxis2))
      }

      for (var k = 0; k < indicesGB.length; k++) {
        //sumForAverageRF = 0
        sumForAverageGB = 0
        //sumForAverageAll = 0
        for (var l = 0; l < indicesGB[k].length; l++) {
          //sumForAverageRF = sumForAverageRF + countDataRF[indices[k][l]]
          sumForAverageGB = sumForAverageGB + countDataGB[indicesGB[k][l]]
          //sumForAverageAll = sumForAverageAll + countDataRF[indices[k][l]] + countDataGB[indices[k][l]]
        }
        //averageRF.push(sumForAverageRF / (this.xaxis))
        averageGB.push(sumForAverageGB / (this.xaxis2))
        //averageAll.push((sumForAverageRF + sumForAverageGB) / (this.xaxis + this.xaxis2))
      }

      for (let loop = 0; loop < averageRF.length; loop++) {
        averageAll.push(((averageRF[loop] + averageGB[loop])/2))
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
      // check average!
      var sortedInd = sortWithIndeces(averageAll)
      var n = averageAll.length
      
      // var newIndList = [...Array(n)];

      // for (let i = 0; i < sortedInd.sortIndices.length; i++) {
      //   newIndList[sortedInd.sortIndices[i]] = i
      // }

      EventBus.$emit('globalSortingFeatures', sortedInd.sortIndices)

      var countFeaturesSortRF = []
      var countFeaturesSortGB = []
      var countDataRFSort = []
      var countDataGBSort = []

      for (var k = 0; k < sortedInd.sortIndices.length; k++) {
        for (var l = 0; l < indicesRF[sortedInd.sortIndices[k]].length; l++) {
          countDataRFSort.push(countDataRF[indicesRF[sortedInd.sortIndices[k]][l]])
          countFeaturesSortRF.push(countFeaturesRF[indicesRF[sortedInd.sortIndices[k]][l]])
        }
      }

      for (var k = 0; k < sortedInd.sortIndices.length; k++) {
        for (var l = 0; l < indicesGB[sortedInd.sortIndices[k]].length; l++) {
          countDataGBSort.push(countDataGB[indicesGB[sortedInd.sortIndices[k]][l]])
          countFeaturesSortGB.push(countFeaturesGB[indicesGB[sortedInd.sortIndices[k]][l]])
        }
      }
          
      // For all models!    
      var maxPerModelTotal = []
      var minPerModelTotal = []

      for (var i = 0; i < this.states.length/2; i++) {
        maxPerModelTotal.push(Math.max(...FIRFTotal[i]))
        minPerModelTotal.push(Math.min(...FIRFTotal[i]))
      }

      for (var i = 0; i < this.states.length/2; i++) {
        maxPerModelTotal.push(Math.max(...FIGBTotal[i]))
        minPerModelTotal.push(Math.min(...FIGBTotal[i]))
      }

      var maximum = Math.max(...maxPerModelTotal)
      var minimum = Math.min(...minPerModelTotal)

      var countFeaturesRFTotal = []
      var countFeaturesGBTotal = []
      var countDataRFTotal = []
      var countDataGBTotal = []

      for (var i = 0; i < this.states.length/2; i++) {
        for (var j = 0; j < features.length; j++) {
          countDataRFTotal.push((FIRFTotal[i][j] - minimum) / (maximum - minimum))
          countFeaturesRFTotal.push(features[j])
        }
      }

      for (var i = 0; i < this.states.length/2; i++) {
        for (var j = 0; j < features.length; j++) {
          countDataGBTotal.push((FIGBTotal[i][j] - minimum) / (maximum - minimum))
          countFeaturesGBTotal.push(features[j])
        }
      }

      var indicesRFTotal = []
      var indicesGBTotal = []

      for (var j = 0; j < features.length; j++) {
        var indexesRFTotal = getAllIndexes(countFeaturesRFTotal, features[j]);
        indicesRFTotal.push(indexesRFTotal)
      }

      for (var j = 0; j < features.length; j++) {
        var indexesGBTotal = getAllIndexes(countFeaturesGBTotal, features[j]);
        indicesGBTotal.push(indexesGBTotal)
      }

      var sumForAverageRFTotal
      var sumForAverageGBTotal
      var averageAllTotal = []
      var averageRFTotal = []
      var averageGBTotal = []

      for (var k = 0; k < indicesRFTotal.length; k++) {
        sumForAverageRFTotal = 0
        for (var l = 0; l < indicesRFTotal[k].length; l++) {
          sumForAverageRFTotal = sumForAverageRFTotal + countDataRFTotal[indicesRFTotal[k][l]]
        }
        averageRFTotal.push(sumForAverageRFTotal / (this.states.length/2))
      }

      for (var k = 0; k < indicesGBTotal.length; k++) {
        sumForAverageGBTotal = 0
        for (var l = 0; l < indicesGBTotal[k].length; l++) {
          sumForAverageGBTotal = sumForAverageGBTotal + countDataGBTotal[indicesRFTotal[k][l]]
        }
        averageGBTotal.push(sumForAverageGBTotal / (this.states.length/2))
      }

      for (let loop = 0; loop < averageRFTotal.length; loop++) {
        averageAllTotal.push(((averageRFTotal[loop] + averageGBTotal[loop])/2))
      }

      var sortedIndTotal = sortWithIndeces(averageAllTotal)     
      
      // function reorder(arr, index, n) {
      //   var temp = [...Array(n)];
 
      //   // arr[i] should be present at index[i] index
      //   for (var i = 0; i < n; i++) temp[index[i]] = arr[i];

      //   // Copy temp[] to arr[]
      //   for (var i = 0; i < n; i++) {
      //     arr[i] = temp[i];
      //     index[i] = i;
      //   }

      //   return arr;
      // }

      // var sortedIndRF = reorder(averageRF, copyIndicesRF, averageRF.length)
      // var sortedIndGB = reorder(averageGB, copyIndicesGB, averageGB.length)
    
      var traceRF = {
        x: countDataRFSort,
        y: countFeaturesSortRF,
        name: '(RF)',
        marker: {color: '#33A02C'},
        type: 'box',
        boxmean: true,
        orientation: 'h'
      }

      var traceGB = {
        x: countDataGBSort,
        y: countFeaturesSortGB,
        name: '(AB)',
        marker: {color: '#1f78b4'},
        type: 'box',
        boxmean: true,
        orientation: 'h'
      }

      var traceGauge = []
      
      var upper = 1
      var step = upper/features.length

      for (let i = sortedInd.length-1; i >= 0; i--) {
        if (i == (sortedInd.length-1)) {
          // if (sortedIndRF[i] < sortedIndGB[i]) {
          //   traceGauge.push({
          //     domain: { x: [0.82, 1], y: [upper-step, upper] },
          //     value: sortedInd[i],
          //     xaxis: 'x2',
          //     yaxis: 'y2',
          //     gauge: {
          //       shape: 'bullet',
          //       'bar': {'color': "#00FFFF"},
          //       axis: { range: [0, 1] },
          //       steps: [
          //         { range: [sortedIndRF[i], sortedIndGB[i]], color: "#C0C0C0" },
          //       ],
          //       threshold: {
          //         line: { color: "black", width: 3 },
          //         thickness: 1,
          //         value: sortedInd[i]
          //       }
          //     },
          //     title: { text: "Median" },
          //     type: "indicator",
          //     mode: "gauge+number",
          //     //delta: { reference: sortedInd[i], increasing: { color: "#018571" }, decreasing: { color: "#a6611a" } },
          //   })
          // } else {
            traceGauge.push({
              domain: { x: [0.81, 1], y: [upper-step, upper] },
              value: sortedInd[i].toFixed(2),
              number: { font: { size: 35 }},
              xaxis: 'x2',
              yaxis: 'y2',
              gauge: {
                shape: 'bullet',
                'bar': {'color': "#00FFFF"},
                axis: { range: [0, 1] },
                // steps: [
                //   { range: [sortedIndGB[i], sortedIndRF[i]], color: "#C0C0C0" },
                // ],
                threshold: {
                  line: { color: "black", width: 3 },
                  thickness: 1,
                  value: sortedInd[i]
                }
              },
              title: { text: "Average", font: { size: 16 } },
              type: "indicator",
              mode: "number+delta",
              delta: { reference: sortedIndTotal[i].toFixed(2), increasing: { color: "#a65628" }, decreasing: { color: "#a65628" } },
            })
          //}
        } else {
          // if (sortedIndRF[i] < sortedIndGB[i]) {
          //   traceGauge.push({
          //     domain: { x: [0.82, 1], y: [upper-step, upper] },
          //     value: sortedInd[i],
          //     gauge: {
          //       shape: 'bullet',
          //       'bar': {'color': "#00FFFF"},
          //       axis: { range: [0, 1] },
          //       steps: [
          //         { range: [sortedIndRF[i], sortedIndGB[i]], color: "#C0C0C0" },
          //       ],
          //       threshold: {
          //         line: { color: "black", width: 3 },
          //         thickness: 1,
          //         value: sortedInd[i]
          //       }
          //     },
          //     xaxis: 'x2',
          //     yaxis: 'y2',
          //     type: "indicator",
          //     mode: "gauge+number",
          //     //delta: { reference: sortedInd[i], increasing: { color: "#018571" }, decreasing: { color: "#a6611a" } },
          //   })
          // } else {
            traceGauge.push({
              domain: { x: [0.81, 1], y: [upper-step, upper] },
              value: sortedInd[i].toFixed(2),
              number: { font: { size: 35 }},
              gauge: {
                shape: 'bullet',
                'bar': {'color': "#00FFFF"},
                axis: { range: [0, 1] },
                // steps: [
                //   { range: [sortedIndGB[i], sortedIndRF[i]], color: "#C0C0C0" },
                // ],
                threshold: {
                  line: { color: "black", width: 3 },
                  thickness: 1,
                  value: sortedInd[i]
                }
              },
              xaxis: 'x2',
              yaxis: 'y2',
              type: "indicator",
              mode: "number+delta",
              delta: { reference: sortedIndTotal[i].toFixed(2), increasing: { color: "#a65628" }, decreasing: { color: "#a65628" } },
            })
          //}

        }
        upper = upper - step
      }

      var traces = [traceGB, traceRF]

      for (let i = 0; i < features.length; i++) {
        traces[i+2] = traceGauge[i]
      }

      var width = 380
      var height = 776

      var layout = {
        xaxis: {
          title: 'Normalized Importance',
          zeroline: false,
          domain: [0, 0.79],
          anchor: 'y1',
        },
        font: { family: 'Helvetica', size: 14, color: '#000000' },
        yaxis: {
          title: 'Feature',
          domain: [0, 1],
          anchor: 'x1',
        },
        showlegend: false,
        boxmode: 'group',
        boxgap: 0.1,
        autosize: false,
        width: width,
        height: height,
        margin: {
          t: 10,
          r: 15,
          l: 90,
          b: 40
        },
        xaxis2: {
        domain: [0.8, 1],
        anchor: 'y2',
        visible: false
        },
        yaxis2: {
        title: 'Trees',
        domain: [0, 1],
        anchor: 'x2',
        },
      };

      var config = {staticPlot: true, displayModeBar: false, scrollZoom: false, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage'], responsive: true}

      Plotly.newPlot('BoxPlot', traces, layout, config);

      var elements = document.getElementsByClassName('numbers')

      function getTranslateXY(element) {
          const style = window.getComputedStyle(element)
          const matrix = new DOMMatrixReadOnly(style.transform)
          return {
              translateX: matrix.m41,
              translateY: matrix.m42
          }
      }

      $(document).ready(function () {
      var html = "";
      for (var i = 0 ; i < features.length ; i++) {
        var each = getTranslateXY(elements[i])
        var result = each.translateY + 25 - (30 * i)
        html += '<button id="' + i + '" class="myCustomButtons" style="margin-left: 294px; transform: translateY(' + result + 'px);">Remove</button>';
      }
      $("#LayerOnTop").html(html);
      $('.myCustomButtons').on('click', function() {
        var ButtonID = parseInt(this.id)
        EventBus.$emit('firstAllTrue', true)
        EventBus.$emit('onHold', true)
        EventBus.$emit('ButtonIDRemove', features[sortedInd.sortIndices[ButtonID]])
      });
      });

      var titleImp = document.getElementsByClassName('g-ytitle')
      var titleResul = titleImp[2].getElementsByClassName('ytitle')[0]
      titleResul.setAttribute('y', 365)

    },
  },
  mounted () {

    EventBus.$on('totalModelsUpdate', data => {
      this.xaxis = (data/2) 
      this.xaxis2 = (data/2)
    })

    EventBus.$on('StatesUpdate', data => {
      this.states = data})

    EventBus.$on('changeInNumberOfModelsRF', data => { this.xaxis = data })
    EventBus.$on('changeInNumberOfModelsAB', data => { this.xaxis2 = data })

    EventBus.$on('changeInNumberOfModelsImp', data => { this.states = data })
    EventBus.$on('changeInNumberOfModelsImp', this.BoxPlotView)
    EventBus.$on('emittedEventCallingTrainingResults', data => {
      this.FinalResultsImp = data})
    //EventBus.$on('ConfirmDataSet', this.BoxPlotView)
    EventBus.$on('emittedEventCallingTrainingResults', this.BoxPlotView)

    EventBus.$on('reset', this.reset)
  }
}
</script>

<style>
text.number {
  fill: #008080 !important
}

#buildLegend { position: relative}
#BoxPlot { position: absolute; z-index: 1}
#LayerOnTop { position: absolute; z-index: 2}
</style>
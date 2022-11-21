<template>
<div id="AllClass">
  <div id="container">
    <div id="LinePlot" style="min-height: 150px; margin-left:125px;"></div>
     <div id="Legend"></div> 
     <div id="Legend2"></div> 
     <div id="Legend3"></div> 
  </div>
  <div id="SankeyDiagram" style="min-height: 150px; margin-left:135px;"></div>
  <div id="BarChart" style="min-height: 150px;"></div>
  <div id='test'></div>
</div> 
</template>

<script>

import { EventBus } from '../main.js'
import * as Plotly from 'plotly.js'
import $ from 'jquery'; // <-to import jquery
import * as d3Base from 'd3'
// attach all d3 plugins to the d3v5 library
const d3v5 = Object.assign(d3Base)

export default {
  name: 'Filtering',
  data () {
    return {
      FinalResultsFilt: 0,
      states: [],
      xaxis: [], // 25 models each
      indRF: [],
      indGB: [],
    }
  },
  methods: {
    reset () {
      var svg = d3v5.select("#test");
      svg.selectAll("*").remove();
      Plotly.purge('LinePlot')
      Plotly.purge('Legend')
      Plotly.purge('Legend2')
      Plotly.purge('Legend3')
      Plotly.purge('SankeyDiagram')
      Plotly.purge('BarChart')
    },
     LinePlotView () {

      Plotly.purge('LinePlot')

      var scoresMeanRF1 = []
      var scoresMeanRF2 = []
      var scoresMeanRF3 = []
      var totalScoreRF = []

      var scoresMeanGB1 = []
      var scoresMeanGB2 = []
      var scoresMeanGB3 = []
      var totalScoreAB = []

      var scoresMeanRF1Sorted = []
      var scoresMeanRF2Sorted = []
      var scoresMeanRF3Sorted = []
      var totalScoreRFSorted = []

      var scoresMeanGB1Sorted = []
      var scoresMeanGB2Sorted = []
      var scoresMeanGB3Sorted = []
      var totalScoreABSorted = []

      for (let i = 0; i < Object.keys(JSON.parse(this.FinalResultsFilt[2]).mean_test_accuracy).length; i++) {
        scoresMeanRF1.push((Object.values(JSON.parse(this.FinalResultsFilt[2]).mean_test_accuracy)[i]*100).toFixed(2))
        scoresMeanRF2.push((Object.values(JSON.parse(this.FinalResultsFilt[2]).mean_test_precision_macro)[i]*100).toFixed(2))
        scoresMeanRF3.push((Object.values(JSON.parse(this.FinalResultsFilt[2]).mean_test_recall_macro)[i]*100).toFixed(2))
        totalScoreRF.push(((parseFloat(scoresMeanRF1[i])+parseFloat(scoresMeanRF2[i])+parseFloat(scoresMeanRF3[i]))/3).toFixed(2))
        scoresMeanGB1.push((Object.values(JSON.parse(this.FinalResultsFilt[19]).mean_test_accuracy)[i]*100).toFixed(2))
        scoresMeanGB2.push((Object.values(JSON.parse(this.FinalResultsFilt[19]).mean_test_precision_macro)[i]*100).toFixed(2))
        scoresMeanGB3.push((Object.values(JSON.parse(this.FinalResultsFilt[19]).mean_test_recall_macro)[i]*100).toFixed(2))
        totalScoreAB.push(((parseFloat(scoresMeanGB1[i])+parseFloat(scoresMeanGB2[i])+parseFloat(scoresMeanGB3[i]))/3).toFixed(2))
      }

      var lenRF = totalScoreRF.length;
      var indicesRF = new Array(lenRF);
      for (var i = 0; i < lenRF; ++i) indicesRF[i] = i;
      indicesRF.sort(function (a, b) { return totalScoreRF[a] < totalScoreRF[b] ? -1 : totalScoreRF[a] > totalScoreRF[b] ? 1 : 0; });

      for (let j = 0; j < indicesRF.length; j++) {
        scoresMeanRF1Sorted.push(scoresMeanRF1[indicesRF[j]])
        scoresMeanRF2Sorted.push(scoresMeanRF2[indicesRF[j]])
        scoresMeanRF3Sorted.push(scoresMeanRF3[indicesRF[j]])
        totalScoreRFSorted.push(totalScoreRF[indicesRF[j]])
      }
      EventBus.$emit('sendCombinedPerformanceRF', totalScoreRFSorted)
      EventBus.$emit('indicesRFSend', indicesRF)

      var lenGB = totalScoreAB.length;
      var indicesGB = new Array(lenGB);
      for (var i = 0; i < lenGB; ++i) indicesGB[i] = i;
      indicesGB.sort(function (a, b) { return totalScoreAB[a] < totalScoreAB[b] ? -1 : totalScoreAB[a] > totalScoreAB[b] ? 1 : 0; });

      for (let j = 0; j < indicesGB.length; j++) {
        scoresMeanGB1Sorted.push(scoresMeanGB1[indicesGB[j]])
        scoresMeanGB2Sorted.push(scoresMeanGB2[indicesGB[j]])
        scoresMeanGB3Sorted.push(scoresMeanGB3[indicesGB[j]])
        totalScoreABSorted.push(totalScoreAB[indicesGB[j]])
      }

      EventBus.$emit('sendCombinedPerformanceAB', totalScoreABSorted)
      EventBus.$emit('indicesGBSend', indicesGB)

      var trace1 = {
        x: this.xaxis, 
        y: scoresMeanRF1Sorted, 
        line: {color: "rgb(51,160,44)"}, 
        mode: "lines+markers", 
        marker : {
          symbol: 'circle' },
        name: "Accuracy (RF)",
        type: "scatter"
      }

      var trace2 = {
        x: this.xaxis, 
        y: scoresMeanRF2Sorted, 
        line: {color: "rgb(51,160,44)"}, 
        mode: "lines+markers", 
        marker : {
            symbol: 'triangle-up' },
        name: "Precision (RF)", 
        type: "scatter"
      }

      var trace3 = {
        x: this.xaxis, 
        y: scoresMeanRF3Sorted, 
        line: {color: "rgb(51,160,44)"}, 
        mode: "lines+markers", 
        marker : {
            symbol: 'triangle-down' },
        name: "Recall (RF)", 
        type: "scatter"
      }

      var trace5 = {
        x: this.xaxis, 
        y: scoresMeanGB1Sorted, 
        line: {color: "rgb(31,120,180)"}, 
        mode: "lines+markers", 
        marker : {
          symbol: 'circle' },
        name: "Accuracy (AB)",
        type: "scatter"
      }

      var trace6 = {
        x: this.xaxis, 
        y: scoresMeanGB2Sorted, 
        line: {color: "rgb(31,120,180)"}, 
        mode: "lines+markers", 
        marker : {
            symbol: 'triangle-up' },
        name: "Precision (AB)", 
        type: "scatter"
      }

      var trace7 = {
        x: this.xaxis, 
        y: scoresMeanGB3Sorted, 
        line: {color: "rgb(31,120,180)"}, 
        mode: "lines+markers", 
        marker : {
            symbol: 'triangle-down' },
        name: "Recall (AB)", 
        type: "scatter"
      }

      const DataforLinePlot = [trace1, trace2, trace3, trace5, trace6, trace7]

      var width = 2514 - 125 - 126
      var height = 150

      var layout = {
        showlegend: false,
        font: { family: 'Helvetica', size: 14, color: '#000000' },
        xaxis: {
            gridcolor: "rgb(229,229,229)",
            title: 'Model ID',
            visible: false,
            tickformat: '.0f',
            range: [0.99, this.xaxis.length+0.01], 
            showgrid: true, 
            showline: false, 
            showticklabels: false, 
            tickcolor: "rgb(127,127,127)", 
            ticks: "outside", 
            zeroline: false
        }, 
        yaxis: {
            gridcolor: "rgb(229,229,229)", 
            title: 'Score (%)',
            showgrid: true, 
            autorange: true,
            showline: false, 
            showticklabels: true, 
            tickcolor: "rgb(127,127,127)", 
            ticks: "outside", 
            nticks: 8,
            zeroline: false
        },
        autosize: false,
        width: width,
        height: height,
        margin: {
          l: 48,
          r: 14,
          b: 24,
          t: 0,
          pad: 0
        },
      }
      var config = {displayModeBar: false, scrollZoom: false, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage'], responsive: true}
      Plotly.newPlot('LinePlot', DataforLinePlot, layout, config)

      this.SankeyDiagramView()
    },
    LegendView () {

      Plotly.purge('Legend')

      var colorRange = ["#bebada", "#fdb462", "#fb8072"];

      var target_names = JSON.parse(this.FinalResultsFilt[9])

      var data = []

      for (let i = 0; i < target_names.length; i++) {
        data.push({
          x: [0],
          y: [0],
          type: 'bar',
          hoverinfo: 'skip',
          name: target_names[i],
          marker: {
            color: colorRange[i],
          }
        })
      }
      
      var width = 2514
      var height = 150

      var layout = {
        legend: {"orientation": "v", x: 0.95, y: 0},
        //showlegend: false,
        font: { family: 'Helvetica', size: 14, color: '#000000' },
        autosize: false,
        width: width,
        height: height,
        margin: {
          l: 0,
          r: 0,
          b: 0,
          t: 0,
          pad: 0
        },
        xaxis: {
          visible: false
        },
        yaxis: {
          visible: false
        },
      }

      var graphDiv = document.getElementById('Legend')
      var config = {displayModeBar: false, staticPlot: true, scrollZoom: false, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage'], responsive: true}
      Plotly.react(graphDiv, data, layout, config)

      var titleBox = graphDiv.getElementsByClassName("main-svg")
      Plotly.d3.select(titleBox[0]).style("background", "rgba(255,255,255,0)")

      Plotly.purge('Legend2')

      var colorRange2 = ["#a65628","#007F7F"];

      var dataNames = ['All Models','Active Models<br>(RF+AB)']

      var data2 = []

      for (let i = 0; i < dataNames.length; i++) {
        data2.push({
          x: [0],
          y: [0],
          type: 'bar',
          hoverinfo: 'skip',
          name: dataNames[i],
          marker: {
            color: colorRange2[i],
          }
        })
      }

      var layout2 = {
        legend: {"orientation": "v", x: 0, y: 0},
        //showlegend: false,
        font: { family: 'Helvetica', size: 14, color: '#000000' },
        autosize: false,
        width: width,
        height: height,
        margin: {
          l: 0,
          r: 0,
          b: 0,
          t: 0,
          pad: 0
        },
        xaxis: {
          visible: false
        },
        yaxis: {
          visible: false
        },
      }

      var graphDiv2 = document.getElementById('Legend2')
      Plotly.react(graphDiv2, data2, layout2, config)

      var titleBox2 = graphDiv2.getElementsByClassName("main-svg")
      Plotly.d3.select(titleBox2[0]).style("background", "rgba(255,255,255,0)")

      Plotly.purge('Legend3')

      var colorRange3 = ["#33a02c", "#33a02c", "#33a02c", "#1f78b4", "#1f78b4", "#1f78b4"];

      var dataNamesNew = ['Accuracy (RF)','Precision (RF)','Recall (RF)','Accuracy (AB)','Precision (AB)','Recall (AB)']
      var symbolsNew = ['circle','triangle-up','triangle-down','circle','triangle-up','triangle-down']

      var data3 = []

      for (let i = 0; i < dataNamesNew.length; i++) {
        data3.push({
          x: [0],
          y: [0],
          type: "scatter",
          hoverinfo: 'skip',
          name: dataNamesNew[i],
          marker: {
            color: colorRange3[i],
            symbol: symbolsNew[i]
          }
        })
      }

      var layout3 = {
        legend: {"orientation": "v", x: 0, y: 0},
        //showlegend: false,
        font: { family: 'Helvetica', size: 14, color: '#000000' },
        autosize: false,
        width: 165,
        height: height,
        margin: {
          l: 0,
          r: 0,
          b: 0,
          t: 0,
          pad: 0
        },
        xaxis: {
          visible: false
        },
        yaxis: {
          visible: false
        },
      }

      var graphDiv3 = document.getElementById('Legend3')
      var config = {displayModeBar: false, staticPlot: true, scrollZoom: false, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage'], responsive: true}
      Plotly.react(graphDiv3, data3, layout3, config)

      var titleBox3 = graphDiv3.getElementsByClassName("main-svg")
      Plotly.d3.select(titleBox3[0]).style("background", "rgba(255,255,255,0)")

      this.LinePlotView()

    },
    SankeyDiagramView () {

      Plotly.purge('SankeyDiagram')

      var Xaxis = this.xaxis
      var FP_RF = JSON.parse(this.FinalResultsFilt[3])
      var FN_RF = JSON.parse(this.FinalResultsFilt[4])
      var FP_GB = JSON.parse(this.FinalResultsFilt[20])
      var FN_GB = JSON.parse(this.FinalResultsFilt[21])
      var FP_RFCom = JSON.parse(this.FinalResultsFilt[15])
      var FN_RFCom = JSON.parse(this.FinalResultsFilt[16])
      var FP_GBCom = JSON.parse(this.FinalResultsFilt[32])
      var FN_GBCom = JSON.parse(this.FinalResultsFilt[33])
      var target_names = JSON.parse(this.FinalResultsFilt[9])

      var FP_RFSorted = []
      var FN_RFSorted = []
      var FP_GBSorted = []
      var FN_GBSorted = []
      var FP_RFSortedCom = []
      var FN_RFSortedCom = []
      var FP_GBSortedCom = []
      var FN_GBSortedCom = []
      
      for (let j = 0; j < this.indicesRF.length; j++) {
        FP_RFSorted.push(FP_RF[this.indicesRF[j]])
        FN_RFSorted.push(FN_RF[this.indicesRF[j]])
        FP_RFSortedCom.push(FP_RFCom[this.indicesRF[j]])
        FN_RFSortedCom.push(FN_RFCom[this.indicesRF[j]])
      }

      for (let j = 0; j < this.indicesGB.length; j++) {
        FP_GBSorted.push(FP_GB[this.indicesGB[j]])
        FN_GBSorted.push(FN_GB[this.indicesGB[j]])
        FP_GBSortedCom.push(FP_GBCom[this.indicesGB[j]])
        FN_GBSortedCom.push(FN_GBCom[this.indicesGB[j]])
      } 

      const reducer = (accumulator, curr) => accumulator + curr;
      var FPconfusionRFCom = []
      var FPconfusionRFComSet = []
      for (let j = 0; j < FP_RFSortedCom.length; j++) {
        if (j != (FP_RFSortedCom.length-1)) {
        FPconfusionRFComSet = []
        for (let k=0; k < target_names.length; k++) {
            if (target_names.length == 2) {
              var filteredArray = FP_RFSortedCom[j].filter(value => FP_RFSortedCom[j+1].includes(value));
              var valueDiff = FP_RFSorted[j+1][1] - filteredArray.length
            } else {
              var filteredArray = (FP_RFSortedCom[j][k].filter(value => FP_RFSortedCom[j+1][k].includes(value)));
              var valueDiff = FP_RFSorted[j+1][k] - filteredArray.length
            }
            FPconfusionRFComSet.push(valueDiff)
          }
        if (target_names.length == 2) {
          FPconfusionRFComSet.pop()
          var residue = FP_RFSorted[j+1][1] - FPconfusionRFComSet[0]
        } else {
          var residue = FP_RFSorted[j+1].reduce(reducer) - FPconfusionRFComSet.reduce(reducer)
        }
        FPconfusionRFComSet.push(residue)
        FPconfusionRFCom.push(FPconfusionRFComSet)
        }
      }

      var FNconfusionRFCom = []
      var FNconfusionRFComSet = []
      for (let j = 0; j < FN_RFSortedCom.length; j++) {
        if (j != (FN_RFSortedCom.length-1)) {
        FNconfusionRFComSet = []
        for (let k=0; k < target_names.length; k++) {
            if (target_names.length == 2) {
              var filteredArray = FN_RFSortedCom[j].filter(value => FN_RFSortedCom[j+1].includes(value));
              var valueDiff = FN_RFSorted[j+1][1] - filteredArray.length
            } else {
              var filteredArray = FN_RFSortedCom[j][k].filter(value => FN_RFSortedCom[j+1][k].includes(value));
              var valueDiff = FN_RFSorted[j+1][k] - filteredArray.length
            }
            FNconfusionRFComSet.push(valueDiff)
          }
        if (target_names.length == 2) {
          FNconfusionRFComSet.pop()
          var residue = FN_RFSorted[j+1][1] - FNconfusionRFComSet[0]
        } else {
          var residue = FN_RFSorted[j+1].reduce(reducer) - FNconfusionRFComSet.reduce(reducer)
        }
        FNconfusionRFComSet.push(residue)
        FNconfusionRFCom.push(FNconfusionRFComSet)
        }
      }
      var FPconfusionABCom = []
      var FPconfusionABComSet = []
      for (let j = 0; j < FP_GBSortedCom.length; j++) {
        if (j != (FP_GBSortedCom.length-1)) {
        FPconfusionABComSet = []
        for (let k=0; k < target_names.length; k++) {
            if (target_names.length == 2) {
              var filteredArray = FP_GBSortedCom[j].filter(value => FP_GBSortedCom[j+1].includes(value));
              var valueDiff = FP_GBSorted[j+1][1] - filteredArray.length
            } else {
              var filteredArray = FP_GBSortedCom[j][k].filter(value => FP_GBSortedCom[j+1][k].includes(value));
              var valueDiff = FP_GBSorted[j+1][k] - filteredArray.length
            }
            FPconfusionABComSet.push(valueDiff)
          }
        if (target_names.length == 2) {
          FPconfusionABComSet.pop()
          var residue = FP_GBSorted[j+1][1] - FPconfusionABComSet[0]
        } else {
          var residue = FP_GBSorted[j+1].reduce(reducer) - FPconfusionABComSet.reduce(reducer)
        }
        FPconfusionABComSet.push(residue)
        FPconfusionABCom.push(FPconfusionABComSet)
        }
      }
      var FNconfusionABCom = []
      var FNconfusionABComSet = []
      for (let j = 0; j < FN_GBSortedCom.length; j++) {
        if (j != (FN_GBSortedCom.length-1)) {
        FNconfusionABComSet = []
        for (let k=0; k < target_names.length; k++) {
            if (target_names.length == 2) {
              var filteredArray = FN_GBSortedCom[j].filter(value => FN_GBSortedCom[j+1].includes(value));
              var valueDiff = FN_GBSorted[j+1][1] - filteredArray.length
            } else {
              var filteredArray = FN_GBSortedCom[j][k].filter(value => FN_GBSortedCom[j+1][k].includes(value));
              var valueDiff = FN_GBSorted[j+1][k] - filteredArray.length
            }
            FNconfusionABComSet.push(valueDiff)
          }
        if (target_names.length == 2) {
          FNconfusionABComSet.pop()
          var residue = FN_GBSorted[j+1][1] - FNconfusionABComSet[0]
        } else {
          var residue = FN_GBSorted[j+1].reduce(reducer) - FNconfusionABComSet.reduce(reducer)
        }
        FNconfusionABComSet.push(residue)
        FNconfusionABCom.push(FNconfusionABComSet)
        }
      }

      var colorRange = ["#bebada", "#fdb462", "#fb8072", "#ffffff"];

      var labels = []
      var colors = []
      var sources = []
      var targets = []
      var values = []
      var colorLinks = []
      if (target_names.length == 2) {
        for (var i = 0; i < Xaxis.length; i++) {
          if (i != (Xaxis.length-1)) {
            sources.push(0+i*4)
            sources.push(1+i*4)
            sources.push(2+i*4)
            sources.push(3+i*4)
            targets.push(4+i*4)
            targets.push(5+i*4)
            targets.push(6+i*4)
            targets.push(7+i*4)
            sources.push(0+i*4)
            sources.push(1+i*4)
            sources.push(2+i*4)
            sources.push(3+i*4)
            targets.push(4+i*4)
            targets.push(5+i*4)
            targets.push(6+i*4)
            targets.push(7+i*4)
          }
          if (i != (Xaxis.length-1)) {
            values.push(FPconfusionRFCom[i][1])
            values.push(FNconfusionRFCom[i][1])
            values.push(FPconfusionABCom[i][1])
            values.push(FNconfusionABCom[i][1])
            values.push(FPconfusionRFCom[i][0])
            values.push(FNconfusionRFCom[i][0])
            values.push(FPconfusionABCom[i][0])
            values.push(FNconfusionABCom[i][0])
          }
          if (i != 0) {
            colorLinks.push(colorRange[0])
            colorLinks.push(colorRange[1])
            colorLinks.push(colorRange[0])
            colorLinks.push(colorRange[1])
            colorLinks.push(colorRange[3])
            colorLinks.push(colorRange[3])
            colorLinks.push(colorRange[3])
            colorLinks.push(colorRange[3])
          }
          labels.push("FP (RF)")
          labels.push("FN (RF)")
          labels.push("FP (AB)")
          labels.push("FN (AB)")
          colors.push("#33a02c")
          colors.push("#33a02c")
          colors.push("#1f78b4")
          colors.push("#1f78b4")
        }
      } else {
        for (var i = 0; i < Xaxis.length; i++) {
          for (var j = 0; j <= target_names.length; j++) {
            if (i != (Xaxis.length-1)) {
              sources.push(0+i*4)
              sources.push(1+i*4)
              sources.push(2+i*4)
              sources.push(3+i*4)
              targets.push(4+i*4)
              targets.push(5+i*4)
              targets.push(6+i*4)
              targets.push(7+i*4)
            }
            if (i != (Xaxis.length-1)) {
              values.push(FPconfusionRFCom[i][j])
              values.push(FNconfusionRFCom[i][j])
              values.push(FPconfusionABCom[i][j])
              values.push(FNconfusionABCom[i][j])
            }
            if (i != 0) {
              colorLinks.push(colorRange[j])
              colorLinks.push(colorRange[j])
              colorLinks.push(colorRange[j])
              colorLinks.push(colorRange[j])
            }
          }
          labels.push("FP (RF)")
          labels.push("FN (RF)")
          labels.push("FP (AB)")
          labels.push("FN (AB)")
          colors.push("#33a02c")
          colors.push("#33a02c")
          colors.push("#1f78b4")
          colors.push("#1f78b4")
        }       
      }

      var width = 2514 - 135 - 112
      var height = 150

      for (var j = 0; j < values.length; j++) {
          if (values[j] == 0) {
              values[j] = 0.2
              colorLinks[j] = "#ffffff"
          }
      }

      var data = {
        type: "sankey",
        orientation: "h",
        node: {
          arrangement: "snap",
          pad: 10,
          thickness: 30,
          line: {
            color: "black",
            width: 0.5
          },
          label: labels,
          color: colors,
        },

        link: {
          source: sources,
          target: targets,
          value: values,
          color: colorLinks
        }
      }

      var data = [data]

      var layout = {
        showlegend: false,
        title: {
          text: 'Confusion (False)',
          font: {
            family: 'Helvetica',
            size: 16,
            color: '#000000'
          },
          x: 0,
          xanchor: 'center',
          y: 0.5,
          yanchor: 'top'
        },
        font: { family: 'Helvetica', size: 14, color: '#000000' },
        autosize: false,
        width: width,
        height: height,
        margin: {
          l: 28,
          r: 12,
          b: 20,
          t: 5,
          pad: 0
        },
      }

      var graphDiv = document.getElementById('SankeyDiagram')  
      var config = {displayModeBar: false, scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage'], responsive: true}
      Plotly.react(graphDiv, data, layout, config)

      var titleBox = graphDiv.getElementsByClassName("infolayer")
      Plotly.d3.select(titleBox[0]).attr("transform", "translate(-70,69) rotate(-90)")

      this.BarChartView()

    },
    BarChartView () {

      Plotly.purge('BarChart')

      var numberEstimRF = JSON.parse(this.FinalResultsFilt[1]).params
      var numberEstimGB = JSON.parse(this.FinalResultsFilt[18]).params
      var n_estimRF = JSON.parse(JSON.parse(this.FinalResultsFilt[11]))
      var n_estimGB = JSON.parse(JSON.parse(this.FinalResultsFilt[28]))

      var yValueRF = []
      var yValueGB = []

      var n_estimRFSorted = []
      var n_estimGBSorted = []
      
      for (let j = 0; j < this.indicesRF.length; j++) {
        yValueRF.push(numberEstimRF[this.indicesRF[j]].n_estimators)
        n_estimRFSorted.push(n_estimRF[0][this.indicesRF[j]])
      }

      for (let j = 0; j < this.indicesGB.length; j++) {
        yValueGB.push(numberEstimGB[this.indicesGB[j]].n_estimators)
        n_estimGBSorted.push(n_estimGB[0][this.indicesGB[j]])
      } 

      var xValue = this.xaxis

      var trace1 = {
        x: xValue,
        y: yValueRF,
        type: 'bar',
        xaxis: 'x2',
        yaxis: 'y2',
        text: yValueRF.map(String),
        textposition: 'auto',
        opacity: 1,
        name:'(RF)',
        marker: {
          color: 'rgb(51,160,44)',
          line: {
            color: 'rgb(0,0,0)',
            width: 1
          }
        }
      };

      var trace2 = {
        x: xValue,
        y: yValueGB,
        type: 'bar',
        xaxis: 'x2',
        yaxis: 'y2',
        text: yValueGB.map(String),
        textposition: 'auto',
        name:'(AB)',
        marker: {
          color: 'rgb(31,120,180)',
          line: {
            color: 'rgb(0,0,0)',
            width: 1
          }
        }
      };

      var trace3 = {
        x: xValue,
        y: n_estimRFSorted,
        type: 'bar',
        text: n_estimRFSorted.map(String),
        textposition: 'auto',
        name:'(RF)',
        marker: {
          color: 'rgb(51,160,44)',
          line: {
            color: 'rgb(0,0,0)',
            width: 1
          }
        }
      };

      var trace4 = {
        x: xValue,
        y: n_estimGBSorted,
        type: 'bar',
        text: n_estimGBSorted.map(String),
        textposition: 'auto',
        name:'(AB)',
        marker: {
          color: 'rgb(31,120,180)',
          line: {
            color: 'rgb(0,0,0)',
            width: 1
          }
        }
      };

      var width = 2514
      var height = 150

      var data = [trace1,trace2,trace3,trace4];

      var layout = {
        font: { family: 'Helvetica', size: 14, color: '#000000' },
        autosize: false,
        width: width,
        height: height,
        margin: {
          l: 55,
          r: 14,
          b: 35,
          t: 5,
          pad: 0
        },
        xaxis: {
          title: 'Model ID',
          domain: [0, 1],
          anchor: 'y1',
          tickmode: "array", // If "array", the placement of the ticks is set via `tickvals` and the tick text is `ticktext`.
          tickvals: this.xaxis,
          ticktext: this.xaxis
        },
        yaxis: {
          gridcolor: "rgb(229,229,229)", 
          title: 'Decisions',
          showgrid: true, 
          showline: false, 
          showticklabels: true, 
          tickcolor: "rgb(127,127,127)", 
          ticks: "outside", 
          domain: [0, 0.40],
          nticks: 4,
          anchor: 'x1'
        },
          xaxis2: {
            domain: [0, 1],
            anchor: 'y2',
            visible: false
          },
          yaxis2: {
            title: 'Trees',
            domain: [0.6, 1],
            anchor: 'x2',
            nticks: 4
          },
        showlegend: false,
      }

      var graphDiv = document.getElementById('BarChart')
      var config = {staticPlot: true, displayModeBar: false, scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage'], responsive: true}
      Plotly.react(graphDiv, data, layout, config)

      this.OnOFF()
    },
    OnOFF () {
      var svg = d3v5.select("#test");
      svg.selectAll("*").remove();
      var length = this.xaxis.length * 2
      var allWas = 20
      var width = 2508 - (length * 39)
      var width2 = 2508 - (length * 39) + ((allWas - length) * 120)
      var step = width/length
      var step2 = width2/length

      for (var id = 0; id < length; id++) {
        var element = $('#test');
        if (id == 0) {
          var toggle_button = '<div id="labelSwitches">State</div>'
          element.append(toggle_button);
        }
        if ((id == (length - 1)) || (id == (length - 2))) {
          if (id%2 == 0) {
            var toggle_button = '<div id="switchdiv">\
                <input type="checkbox" id="switch' + id + '" onclick="switchAction(' + id + ')" name="switch' + id + '" class="switch" visible="false" checked/>\
                <label for="switch' + id + '" >&nbsp</label>';
          } else {
            var toggle_button = '<div id="switchdiv">\
                <input type="checkbox" id="switch' + id + '" onclick="switchAction(' + id + ')" name="switch' + id + '" class="switch2" visible="false" checked/>\
                <label for="switch' + id + '" >&nbsp</label>';
          }
        } else {
          if (id%2 == 0) {
            if (id == 0) {
              if (length <= 10) {
              var toggle_button = '<div id="switchdiv">\
                  <input type="checkbox" id="switch' + id + '" onclick="switchAction(' + id + ')" name="switch' + id + '" class="switch" visible="false" checked/>\
                  <label for="switch' + id + '" style="margin-left:' + (step+10) + 'px">&nbsp</label>';              
              } else {
              var toggle_button = '<div id="switchdiv">\
                  <input type="checkbox" id="switch' + id + '" onclick="switchAction(' + id + ')" name="switch' + id + '" class="switch" visible="false" checked/>\
                  <label for="switch' + id + '" style="margin-left:' + (step+18.6) + 'px">&nbsp</label>';
              }
            } else{
              var toggle_button = '<div id="switchdiv">\
                  <input type="checkbox" id="switch' + id + '" onclick="switchAction(' + id + ')" name="switch' + id + '" class="switch" visible="false" checked/>\
                  <label for="switch' + id + '">&nbsp</label>';
            }
          } else {
            var toggle_button = '<div id="switchdiv">\
                <input type="checkbox" id="switch' + id + '" onclick="switchAction(' + id + ')" name="switch' + id + '" class="switch2" visible="false" checked/>\
                <label for="switch' + id + '" style="margin-right:' + step2 + 'px">&nbsp</label>';
          }
        }
        element.append(toggle_button);
      }
    },
    switchAction(idToChange) {
      var counter = 0
      var counter1 = 0
      var counter2 = 0
      if (this.states[idToChange] == 1) {
        this.states[idToChange] = 0
      } else {
        this.states[idToChange] = 1
      }
      for (let i = 0; i < this.states.length; i++) {
        if (this.states[i] == 1) {
          counter = counter + 1
          if (i%2 == 0) {
            counter1 = counter1 + 1
          } else {
            counter2 = counter2 + 1
          }
        }
      }
      EventBus.$emit('firstAllTrue', true)
      EventBus.$emit('changeInNumberOfModels', counter)
      EventBus.$emit('changeInNumberOfModelsRF', counter1)
      EventBus.$emit('changeInNumberOfModelsAB', counter2)
      EventBus.$emit('changeInNumberOfModelsImp', this.states)
    }
  },
  created(){window.switchAction =this.switchAction;},
  mounted() {

    EventBus.$on('numberOfModelsUpdate', data => {
      this.xaxis = data})
    EventBus.$on('StatesUpdate', data => {
      this.states = data})

    EventBus.$on('emittedEventCallingTrainingResults', data => {
      this.FinalResultsFilt = data})
    EventBus.$on('emittedEventCallingTrainingResults', this.LegendView)

    EventBus.$on('indicesRFSend', data => {
      this.indicesRF = data})
    EventBus.$on('indicesGBSend', data => {
      this.indicesGB = data})

    // reset the views
    EventBus.$on('resetViews', this.reset)
  }
}
</script>

<style>
#container {
  width: 100px;
  height: 150px;
  position: relative;
}

#LinePlot {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
}

#Legend {
  background-color: transparent;
  transform: translateY(95px);
  z-index: 2;
}

#Legend2 {
  background-color: transparent;
  transform: translateY(-10px);
  z-index: 2;
}

#Legend3 {
  background-color: transparent;
  transform: translateY(-314px) translateX(2383px);
  z-index: 0;
}

 #switchdiv
{
  display: inline-block
}

 #labelSwitches
{
  display: inline-block;
  position: absolute;
  left: 12px;
  bottom: 14px;
}

input.switch:empty
{
  margin-left: -100000px;
}

input.switch:empty ~ label
 {
  position: relative;
  float: left;
  line-height: 1.6em;
  text-indent: 4em;
  margin: 0.2em 0;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
     user-select: none;
 }

input.switch:empty ~ label:before, 
input.switch:empty ~ label:after
{
position: absolute;
display: block;
top: 0;
bottom: 0;
left: 0;
content: ' ';
width: 3.6em;
background-color: #a65628;
border-radius: 0.3em;
box-shadow: inset 0 0.2em 0 rgba(0,0,0,0.3);
-webkit-transition: all 100ms ease-in;
     transition: all 100ms ease-in;
 }

input.switch:empty ~ label:after
{
width: 1.4em;
top: 0.1em;
bottom: 0.1em;
margin-left: 0.1em;
background-color: #a65628;
border-radius: 0.15em;
border: 2px solid #fff;
box-shadow: inset 0 -0.2em 0 rgba(0,0,0,0.2);
}

 input.switch:checked ~ label:before
{
background-color: #33A02C;
 }

input.switch:checked ~ label:after
{
margin-left: 2.1em;
}

input.switch2:empty
{
margin-left: -100000px;
}

input.switch2:empty ~ label
 {
position: relative;
float: left;
line-height: 1.6em;
text-indent: 4em;
margin: 0.2em 0;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
     user-select: none;
 }

input.switch2:empty ~ label:before, 
input.switch2:empty ~ label:after
{
position: absolute;
display: block;
top: 0;
bottom: 0;
left: 0;
content: ' ';
width: 3.6em;
background-color: #a65628;
border-radius: 0.3em;
box-shadow: inset 0 0.2em 0 rgba(51, 160, 44,0.3);
-webkit-transition: all 100ms ease-in;
     transition: all 100ms ease-in;
 }

input.switch2:empty ~ label:after
{
width: 1.4em;
top: 0.1em;
bottom: 0.1em;
margin-left: 0.1em;
background-color: #a65628;
border-radius: 0.15em;
border: 2px solid #fff;
box-shadow: inset 0 -0.2em 0 rgba(0,0,0,0.2);
}

 input.switch2:checked ~ label:before
{
background-color: #1f78b4;
 }

input.switch2:checked ~ label:after
{
margin-left: 2.1em;
}
</style>
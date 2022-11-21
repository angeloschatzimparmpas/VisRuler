<template>
<div style="margin-top:-8px">
  Rounding:
  <b-form-slider ref="basic1" v-model="basicValue1" :min="0" :max="15" trigger-change-event @slide-start="slideStart" @slide-stop="slideStop" style="padding-right: 10px; padding-left: 10px"></b-form-slider>{{ basicValue1 }}
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <button style="float: center;" class="btn-outline-dark"
  id="anchorID"
  v-on:click="anchorClicked">
  <font-awesome-icon icon="anchor" />
  {{ valueAnchor }}
  </button>
  <button style="float: center; margin-right: 15px;" class="btn-outline-dark"
  id="detachID"
  v-on:click="detachClicked">
  <font-awesome-icon icon="ship" />
  {{ valueDetach }}
  </button>
  Show Overlap (or Difference):
  <input id="modeComparison" checked type="checkbox" @change="triggeredChangeMode" data-toggle="toggle">
  <div id="Scatterplot"></div>
  <div style="margin-top: 5px; margin-bottom: 13px"> 
    <table id="tableManual" class="table table-borderless table-sm" style="margin-top: -12px; margin-bottom: -12px">
      <tbody>
      <td>Limit Decisions due to Test Instance:</td>
      <td><input id="triggeredChangeModeSpaceID" checked type="checkbox" @change="triggeredChangeModeSpace" data-toggle="toggle"></td>
      <td>
      <td>
      <td>Impurity for Layout (≤):</td>
      <td><b-form-slider ref="basic2" v-model="basicValue2" :min="0" :max="1" :step="0.1" trigger-change-event @slide-start="slideStart2" @slide-stop="slideStop2" style="padding-right: 10px; padding-left: 10px"></b-form-slider>{{ basicValue2 }}</td>
      </tbody>
    </table>
  </div>
  <div id="vis" style="margin: 0px 0px 0px 0px !important"></div>
</div>
</template>

<script>

import { EventBus } from '../main.js'
import * as Plotly from 'plotly.js'
import * as d3Base from 'd3'

// attach all d3 plugins to the d3 library
const d3v5 = Object.assign(d3Base)

export default {
  name: 'Space',
  data () {
    return {
      basicValue1: 15,
      basicValue2: 1,
      valueAnchor: 'Anchor',
      valueDetach: 'Detach',
      FinalResultsScatter: 0,
      FinalResultsGeneral: 0,
      truth: 0,
      selectDecisionsTestLimitation: [],
      selectDecisions: [],
      activeTestInstance: 0,
      X_testData: [],
      RFSort: [],
      GBSort: [],
      states: [],
      flagCheckedMode: true,
      currentListOfPoints: [],
      anchoredPoints: [],
      triggeredChangeChecker: true,
      RetrieveName: '',
    }
  },
  methods: {
      slideStart () {
      
      },
      slideStop () {
        EventBus.$emit('changedRoundingPrecision', this.basicValue1)
      },
      slideStart2 () {
      
      },
      refreshImm () {
        EventBus.$emit('onHold', false)
        this.selectDecisionsTestLimitation = []
        this.ScatterplotView()
      },
      triggeredChangeModeSpace () {
        this.triggeredChangeChecker = document.getElementById("triggeredChangeModeSpaceID").checked
        EventBus.$emit('onHold', false)
        this.selectDecisionsTestLimitation = []
        this.ScatterplotView()
        this.InitThresh()
      },
      slideStop2 () {
        EventBus.$emit('onHold', false)
        this.selectDecisionsTestLimitation = []
        this.ScatterplotView()
      },
      anchorClicked () {  
        this.anchoredPoints = this.currentListOfPoints
        var element = document.getElementById('lassoInteract01')
        element.style["stroke-width"] = 2.5
        element.style["stroke"] = "#ff00ff"
        EventBus.$emit('sendAnchoredPoints', this.anchoredPoints)
      },
      detachClicked () {
        this.anchoredPoints = []
        this.selectDecisionsTestLimitation = []
        EventBus.$emit('onHold', false)
        EventBus.$emit('sendAnchoredPoints', this.anchoredPoints)
        this.ScatterplotView()
      },
      triggeredChangeMode () {
        this.flagCheckedMode = document.getElementById("modeComparison").checked
        EventBus.$emit('activeMode', this.flagCheckedMode)
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
      InitThresh() {

        var svg = d3.select("#vis");
        svg.selectAll("*").remove();

        var RFStats = JSON.parse(this.FinalResultsGeneral[10])
        var RFStatsRead = JSON.parse(RFStats)
        var RFLength = Object.values(RFStatsRead.predicted_value).length
        
        var GBStats = JSON.parse(this.FinalResultsGeneral[27])
        var GBStatsRead = JSON.parse(GBStats)
        var GBLength = Object.values(GBStatsRead.predicted_value).length

        var RFSamples = []
        var GBSamples = []

        var splitStatesRF = []
        var splitStatesAB = []
        for (let i = 0; i < this.states.length; i++) {
          if (i%2 == 0) {
            splitStatesRF.push(this.states[i])
          } else {
            splitStatesAB.push(this.states[i])
          }
        }

        var decisionsRF = JSON.parse(this.FinalResultsGeneral[11])
        var decisionsRFRead = JSON.parse(decisionsRF)

        var decisionsRFReadSort = []
        for (let j = 0; j < this.RFSort.length; j++) {
          decisionsRFReadSort.push(Object.values(decisionsRFRead)[0][this.RFSort[j]])
        }
        decisionsRFReadSort = decisionsRFReadSort.map((elem, index) => decisionsRFReadSort.slice(0,index + 1).reduce((a, b) => a + b));

        var decisionsAB = JSON.parse(this.FinalResultsGeneral[28])
        var decisionsABRead = JSON.parse(decisionsAB)

        var decisionsABReadSort = []
        for (let j = 0; j < this.GBSort.length; j++) {
          decisionsABReadSort.push(Object.values(decisionsABRead)[0][this.GBSort[j]])
        }
        decisionsABReadSort = decisionsABReadSort.map((elem, index) => decisionsABReadSort.slice(0,index + 1).reduce((a, b) => a + b));

        var startingPointRF = 0
        var startingPointAB = 0

        for (let i = 0; i < RFLength; i++) {
        // for (let k = 0; k < splitStatesRF.length; k++) {
        //   if (splitStatesRF[k] == 1) {
        //     if (k == 0) {
        //       startingPointRF = 0
        //     } else {
        //       startingPointRF = decisionsRFReadSort[k-1]
        //     }
        //     for (let i = startingPointRF; i < decisionsRFReadSort[k]; i++) {
              RFSamples.push((Object.values(RFStatsRead.samples)[i]))
          //   }
          // }
        }
        
        for (let i = 0; i < GBLength; i++) {
        // for (let k = 0; k < splitStatesAB.length; k++) {
        //   if (splitStatesAB[k] == 1) {
        //     if (k == 0) {
        //       startingPointAB = 0
        //     } else {
        //       startingPointAB = decisionsABReadSort[k-1]
        //     }
        //     for (let i = startingPointAB; i < decisionsABReadSort[k]; i++) {
              GBSamples.push((Object.values(GBStatsRead.samples)[i]))
          //   }
          // }
        }
        
        var summativeArray = RFSamples.concat(GBSamples)
 
        var summativeArrayFiltered = []

        if (this.selectDecisionsTestLimitation.length == 0 || this.triggeredChangeModeSpace == false) {
          summativeArrayFiltered = [...summativeArray];
        } else {
          for (let j = 0; j < summativeArray.length; j++) {
            if (this.selectDecisionsTestLimitation.includes(j)) {
              summativeArrayFiltered.push(summativeArray[j])
            }
          }
        }

        var maxArray = Math.max.apply(Math, summativeArrayFiltered);
        var minArray = Math.min.apply(Math, summativeArrayFiltered);

        var dataObj = []
        if (this.selectDecisionsTestLimitation.length == 0 || this.triggeredChangeModeSpace == false) {
          for (let j = 0; j< summativeArrayFiltered.length; j++) {
            dataObj.push({id:j, date:summativeArrayFiltered[j], value:1})
          }     
        } else {
          for (let j = 0; j< summativeArrayFiltered.length; j++) {
            dataObj.push({id:this.selectDecisionsTestLimitation[j], date:summativeArrayFiltered[j], value:1})
          }
        }

        var margin = {top:0, right:20, bottom:15, left:20},
        width = 805 - margin.left - margin.right,
        height = 135 - margin.top - margin.bottom;

        var histHeight = height - 40;

        var colours = d3v5.scaleOrdinal()
            .domain([minArray, maxArray])
            .range(['#008080']);

        // x scale for time
        var x = d3v5.scaleLinear()
            .domain([minArray, maxArray+10])
            .range([0, width])

        // y scale for histogram
        var y = d3v5.scaleLinear()
            .range([histHeight, 0]);


        ////////// histogram set up //////////

        // set parameters for histogram
        var histogram = d3v5.histogram()
            .value(function(d) { return d.date; })
            .domain(x.domain())
            .thresholds(x.ticks(15));

        var svg = d3v5.select("#vis")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom);

        var hist = svg.append("g")
            .attr("class", "histogram")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
 
        // group data for bars
        var bins = histogram(dataObj);
        var lengthOfBins = bins.length - 1
        // y domain based on binned data
        y.domain([0, d3v5.max(bins, function(d) { return d.length; })]);

        var bar = hist.selectAll(".bar")
            .data(bins)
            .enter()
            .append("g")
            .attr("class", "bar")
            .attr("transform", function(d) {
              return "translate(" + x(d.x0) + "," + y(d.length) + ")";
            });
            
        bar.append("text")
            .attr("dy", ".75em")
            .attr("y", function(d) { return (((y(d.length)))*(-1)) })
            .attr("x", function(d) { return (x(d.x1) - x(d.x0))/2; })
            .attr("text-anchor", "middle")
            .text(function(d,i) { 
              if (i == lengthOfBins) {
               return;
              } else {
                return d.length;
              }
            })
            .style("fill", "black");

        bar.append("rect")
            .attr("class", "bar")
            .attr("x", 1)
            .attr("y", 16)
            .attr("width", function(d, i) {
            if(i == lengthOfBins) {
                return x(d.x1+10) - x(d.x0); 
              } else {
                return x(d.x1) - x(d.x0); 
              }
            })
            .attr("height", function(d) { return histHeight - y(d.length); })
            .attr("fill", function(d) { return colours(d.x0); });

        ////////// slider //////////
      var sqrt3 = Math.sqrt(3);

        var currentValue = -2;

        var slider = svg.append("g")
            .attr("class", "slider")
            .attr("transform", "translate(" + margin.left + "," + (margin.top+histHeight+23) + ")");

        slider.append("line")
            .attr("class", "track")
            .attr("x1", x.range()[0])
            .attr("x2", x.range()[1])
          .select(function() { return this.parentNode.appendChild(this.cloneNode(true)); })
            .attr("class", "track-inset")
          .select(function() { return this.parentNode.appendChild(this.cloneNode(true)); })
            .attr("class", "track-overlay");
  
        slider.insert("g", ".track-overlay")
            .attr("class", "ticks")
            .attr("transform", "translate(0," + 18 + ")")
          .selectAll("text")
            .data(x.ticks(lengthOfBins))
            .enter()
            .append("text")
            .attr("x", x)
            .attr("y", -2)
            .attr("text-anchor", "middle")
            .text(function(d) { return d; });        

        svg.append("text")
            .attr("class", "x label")
            .attr("text-anchor", "end")
            .attr("x", width-280)
            .attr("y", height + 14)
            .text("Distribution of Instances"); 

        svg.append("text")
            .attr("class", "y label")
            .attr("text-anchor", "end")
            .attr("x", -15)
            .attr("y", 6)
            .attr("dy", ".75em")
            .attr("transform", "rotate(-90)")
            .text("Decisions");

        //     .call(d3v5.drag()
        //         //.on("start.interrupt", function() { slider.interrupt(); })
        //         .on("start drag", function() {
        //           currentValue = d3v5.event.x;
        //           update(x.invert(currentValue), false); 
        //         })
        //         .on("end", function() {
        //           currentValue = d3v5.event.x;
        //           update(x.invert(currentValue), true); 
        //         })
        //     );

  var triangleRight = {
        draw: function (context, size) {
          var x = -Math.sqrt(size / (sqrt3 * 3));
          context.moveTo(-x * 2, 0);
          context.lineTo(x, -sqrt3 * x);
          context.lineTo(x, sqrt3 * x);
          context.closePath();
        }
      };

      var triangleLeft = {
        draw: function (context, size) {
          var x = -Math.sqrt(size / (sqrt3 * 3));
          context.moveTo(x * 2, 0);
          context.lineTo(-x, -sqrt3 * x);
          context.lineTo(-x, sqrt3 * x);
          context.closePath();
        }
      };

      let leftTrgl = d3v5.symbol().type(triangleLeft)
        .size(180);
      let rightTrgl = d3v5.symbol().type(triangleRight)
        .size(180);

      let head1 = slider.append('path')
        .attr('d', leftTrgl)
        .style('fill', 'black')
      	.style('stroke', 'none')
        .classed('slider-circle-time-from', true)
        .attr('transform', 'translate(' + currentValue + ', 0)')
        .call(d3v5.drag()
          .on('start.interrupt', function () {
            head1.interrupt();
          })
          .on('drag', function () {
            currentValue = d3v5.event.x;
            update(x.invert(currentValue), x.invert(currentValue2), false, 1); 
          })
          .on("end", function() {
              currentValue = d3v5.event.x;
              update(x.invert(currentValue), x.invert(currentValue2), true, 1); 
            })
          );

      var currentValue2 = 768

      let head2 = slider.append('path')
        .attr('d', rightTrgl)
        .style('fill', 'black')
      	.style('stroke', 'none')
        .classed('slider-circle-time-to', true)
        .attr('transform', 'translate(' + currentValue2 + ', 0)')
        .call(d3v5.drag()
          .on('start.interrupt', function () {
            head2.interrupt();
          })
          .on('drag', function () {
            currentValue2 = d3v5.event.x;
            update(x.invert(currentValue), x.invert(currentValue2), false, 2); 
          })
          .on("end", function() {
              currentValue2 = d3v5.event.x;
              update(x.invert(currentValue), x.invert(currentValue2), true, 2); 
            })
          );
        
        function update(h1, h2, flagLocal, flagOneOrTwo) {

          if (flagOneOrTwo == 1) {
            head1.attr("transform", "translate(" + x(h1) + ",0)")
          } else {
            head2.attr("transform", "translate(" + x(h2) + ",0)")
          }

            // filter data set and redraw plot
            var IDsThresh = dataObj.filter(function(d) {
              return d.date > h1 && d.date < h2;
            })

          // histogram bar colours
          hist.selectAll(".bar")
            .attr("fill", function(d) {
              if (d.x0 > h1 && d.x0 < h2) {
                return colours(d.x0);
              } else {
                return "#eaeaea";
              }
            })

          var localIDs = []
          for (let j = 0; j < IDsThresh.length; j++) {
            localIDs.push(IDsThresh[j].id)
          }
          if (flagLocal) {
            EventBus.$emit('updateSpace', localIDs)
          }
        }
      },
      updateSpaceFun() {
        this.ScatterplotView()
      },
      reset () {
        Plotly.purge('Scatterplot')
        var svg = d3.select("#vis");
        svg.selectAll("*").remove();
      },
      ScatterplotView() {
        EventBus.$emit('CallFromSpace', this.activeTestInstance)
        var XTestData = JSON.parse(this.X_testData)

        Plotly.purge('Scatterplot')

        var splitStatesRF = []
        var splitStatesAB = []
        for (let i = 0; i < this.states.length; i++) {
          if (i%2 == 0) {
            splitStatesRF.push(this.states[i])
          } else {
            splitStatesAB.push(this.states[i])
          }
        }

        var IDsRF = []
        var IDsAB = []

        var RFStats = JSON.parse(this.FinalResultsGeneral[10])
        var decisionsRF = JSON.parse(this.FinalResultsGeneral[11])
        var decisionsRFRead = JSON.parse(decisionsRF)

        var decisionsRFReadSort = []
        for (let j = 0; j < this.RFSort.length; j++) {
          decisionsRFReadSort.push(Object.values(decisionsRFRead)[0][this.RFSort[j]])
        }
        decisionsRFReadSort = decisionsRFReadSort.map((elem, index) => decisionsRFReadSort.slice(0,index + 1).reduce((a, b) => a + b));

        var RFStatsRead = JSON.parse(RFStats)   
        var RFLength = Object.values(RFStatsRead.predicted_value).length

        var RFDecisions = JSON.parse(this.FinalResultsGeneral[6])
        var RFDecisionsRead = JSON.parse(RFDecisions)

        var GBStats = JSON.parse(this.FinalResultsGeneral[27])
        var decisionsAB = JSON.parse(this.FinalResultsGeneral[28])
        var decisionsABRead = JSON.parse(decisionsAB)
        var decisionsABReadSort = []
    
        for (let j = 0; j < this.GBSort.length; j++) {
          decisionsABReadSort.push(Object.values(decisionsABRead)[0][this.GBSort[j]])
        }
        decisionsABReadSort = decisionsABReadSort.map((elem, index) => decisionsABReadSort.slice(0,index + 1).reduce((a, b) => a + b));
        var GBStatsRead = JSON.parse(GBStats)
        var GBLength = Object.values(GBStatsRead.predicted_value).length
        var GBDecisions = JSON.parse(this.FinalResultsGeneral[23])
        var GBDecisionsRead = JSON.parse(GBDecisions)

        var startingPointRF = 0
        var startingPointAB = 0
        for (var m = 0; m < splitStatesRF.length; m++) {
          if (splitStatesRF[m] == 1) {
            if (m == 0) {
              startingPointRF = 0
            } else {
              startingPointRF = decisionsRFReadSort[m-1]
            }
            for (var i = startingPointRF; i < decisionsRFReadSort[m]; i++) {
              var flagArrayRF = new Array(Object.values(RFDecisionsRead).length).fill(0);
              var loopSlowerRF = 0
              for (let k = 0; k < Object.values(RFDecisionsRead).length; k++) {
                if (k == (Object.values(RFDecisionsRead).length/2)) {
                  loopSlowerRF = 0
                }
                if (Object.values(Object.values(RFDecisionsRead)[k])[i] == 2) {
                  flagArrayRF[k] = 1
                } else if (k < (Object.values(RFDecisionsRead).length/2)) {
                  if (Object.values(Object.values(XTestData)[loopSlowerRF])[this.activeTestInstance] > Object.values(Object.values(RFDecisionsRead)[k])[i]) {
                    flagArrayRF[k] = 1
                  }
                } else {
                  if (Object.values(Object.values(XTestData)[loopSlowerRF])[this.activeTestInstance] <= Object.values(Object.values(RFDecisionsRead)[k])[i]) {
                    flagArrayRF[k] = 1
                  }
                }
                loopSlowerRF = loopSlowerRF + 1
              }
              if (this.triggeredChangeChecker) {
                if ((flagArrayRF.reduce((a, b) => a + b, 0)) == Object.values(RFDecisionsRead).length) {
                  this.selectDecisionsTestLimitation.push(i)
                  IDsRF.push(i.toString())
                }
              } else {
                this.selectDecisionsTestLimitation.push(i)
                IDsRF.push(i.toString())
              }
            }
          }
        }

        for (var m = 0; m < splitStatesAB.length; m++) {
          if (splitStatesAB[m] == 1) {
            if (m == 0) {
              startingPointAB = 0
            } else {
              startingPointAB = decisionsABReadSort[m-1]
            }
            for (var i = startingPointAB; i < decisionsABReadSort[m]; i++) {
              //for (let i = 0; i < (GBLength); i++) {
                var flagArrayGB = new Array(Object.values(GBDecisionsRead).length).fill(0);
                var loopSlowerGB = 0
                for (var k = 0; k < Object.values(GBDecisionsRead).length; k++) {
                  if (k == (Object.values(GBDecisionsRead).length/2)) {
                    loopSlowerGB = 0
                  }
                  if (Object.values(Object.values(GBDecisionsRead)[k])[i] == 2) {
                    flagArrayGB[k] = 1
                  } else if (k < (Object.values(GBDecisionsRead).length/2)) {
                    if (Object.values(Object.values(XTestData)[loopSlowerGB])[this.activeTestInstance] > Object.values(Object.values(GBDecisionsRead)[k])[i]) {
                      flagArrayGB[k] = 1
                    }
                  } else {
                    if (Object.values(Object.values(XTestData)[loopSlowerGB])[this.activeTestInstance] <= Object.values(Object.values(GBDecisionsRead)[k])[i]) {
                      flagArrayGB[k] = 1
                    }
                  }
                  loopSlowerGB = loopSlowerGB + 1
                }
                if (this.triggeredChangeChecker) {
                  if ((flagArrayGB.reduce((a, b) => a + b, 0)) == Object.values(GBDecisionsRead).length) {
                    this.selectDecisionsTestLimitation.push(RFLength+i)
                    IDsAB.push((RFLength+i).toString())
                  }
                } else {
                  this.selectDecisionsTestLimitation.push(RFLength+i)
                  IDsAB.push((RFLength+i).toString())
                }
              }
           }
        }

        var colorRange = ["#bebada", "#fdb462", "#fb8072"];        
        function foo(arrlocal) {
          var a = [],
            b = [],
            prev;

          var arr = [...arrlocal];
          arr.sort()
          for (var i = 0; i < arr.length; i++) {
            if (arr[i] !== prev) {
              a.push(arr[i]);
              b.push(1);
            } else {
              b[b.length - 1]++;
            }
            prev = arr[i];
          }

          return [a, b];
        }

        var targetData = this.truth
        var result = foo(targetData);

        var UMAPData = this.FinalResultsScatter
        var UMAPDataRFx = []
        var UMAPDataRFy = []
        var UMAPDataGBx = []
        var UMAPDataGBy = []
        var RFImpurity = []
        var GBImpurity = []
        var RFPredValue = []
        var GBPredValue = []
        var RFSamples = []
        var GBSamples = []

        var classifiersInfoProcessingRF = []
        var classifiersInfoProcessingAB = []
        var classifiersInfoProcessingAR = []

        var parametersLocRF = JSON.parse(this.FinalResultsGeneral[1])
        var parametersRF = parametersLocRF.params
        var parametersLocAB = JSON.parse(this.FinalResultsGeneral[18])
        var parametersAB = parametersLocAB.params
        var target_names = JSON.parse(this.FinalResultsGeneral[9])

        var stringParametersUnSortRF = []
        for (let i = 0; i < Object.values(parametersRF).length; i++) {
          this.clean(Object.values(parametersRF)[i])
          stringParametersUnSortRF.push(JSON.stringify(Object.values(parametersRF)[i]).replace(/,/gi, '<br>'))
        }
        
        var stringParametersUnSortAB = []
        for (let i = 0; i < Object.values(parametersAB).length; i++) {
          this.clean(Object.values(parametersAB)[i])
          stringParametersUnSortAB.push(JSON.stringify(Object.values(parametersAB)[i]).replace(/,/gi, '<br>'))
        }

        var stringParametersRF = []
        for (let j = 0; j < this.RFSort.length; j++) {
          stringParametersRF.push(stringParametersUnSortRF[this.RFSort[j]])
        }

        var stringParametersAB = []
        for (let j = 0; j < this.GBSort.length; j++) {
          stringParametersAB.push(stringParametersUnSortAB[this.GBSort[j]])
        }

        if (this.RetrieveName == 'IrisC') {
          var constantMultiplier = d3v5.scaleLinear()
              .domain([0, 1])
              .range([10, 30]) // 60 everywhere except case study with bank credit 100
        } else if (this.RetrieveName == 'CreditC') {
          var constantMultiplier = d3v5.scaleLinear()
              .domain([0, 1])
              .range([10, 100]) // 60 everywhere except case study with bank credit 100
        } else {
          var constantMultiplier = d3v5.scaleLinear()
              .domain([0, 1])
              .range([10, 60]) // 60 everywhere except case study with bank credit 100
        }


        startingPointRF = 0
        startingPointAB = 0
        for (let k = 0; k < splitStatesRF.length; k++) {
          if (splitStatesRF[k] == 1) {
            if (k == 0) {
              startingPointRF = 0
            } else {
              startingPointRF = decisionsRFReadSort[k-1]
            }
            for (let i = startingPointRF; i < decisionsRFReadSort[k]; i++) {
                if (this.selectDecisionsTestLimitation.length == 0) {
                  if (this.selectDecisions.length == 0) {
                    UMAPDataRFx.push(UMAPData[0][i])
                    UMAPDataRFy.push(UMAPData[1][i])
                    let active = Object.values(RFStatsRead.predicted_value)[i]
                    RFPredValue.push(colorRange[active])
                    if (Object.values(RFStatsRead.impurity)[i] <= this.basicValue2) {
                      RFImpurity.push((1 - Object.values(RFStatsRead.impurity)[i]))
                    } else {
                      RFImpurity.push(0.1)
                    }
                    RFSamples.push(constantMultiplier(Object.values(RFStatsRead.samples)[i] / result[1][active]))
                    classifiersInfoProcessingRF.push('<b>Model ID:</b> ' + 'RF' + (k+1) + '<br><b>Tree ID:</b> ' + (Object.values(RFStatsRead.tree_index)[i]) + '<br><b>Decision ID:</b> ' + (Object.values(RFStatsRead.node)[i]) + '<br><b>Predicted Value:</b> ' + target_names[active] + '<br><b>Decision Impurity:</b> ' + (Object.values(RFStatsRead.impurity)[i]) + '<br><b>Influenced Instances:</b> ' + (Object.values(RFStatsRead.samples)[i]) + '<br><b>Hyperparameters:</b> ' + stringParametersRF[k])
                  } else {
                    if (this.selectDecisions.includes(i)) {
                      UMAPDataRFx.push(UMAPData[0][i])
                      UMAPDataRFy.push(UMAPData[1][i])
                      let active = Object.values(RFStatsRead.predicted_value)[i]
                      RFPredValue.push(colorRange[active])
                      if (Object.values(RFStatsRead.impurity)[i] <= this.basicValue2) {
                        RFImpurity.push((1 - Object.values(RFStatsRead.impurity)[i]))
                      } else {
                        RFImpurity.push(0.1)
                      }
                      RFSamples.push(constantMultiplier(Object.values(RFStatsRead.samples)[i] / result[1][active]))
                      classifiersInfoProcessingRF.push('<b>Model ID:</b> ' + 'RF' + (k+1) + '<br><b>Tree ID:</b> ' + (Object.values(RFStatsRead.tree_index)[i]) + '<br><b>Decision ID:</b> ' + (Object.values(RFStatsRead.node)[i]) + '<br><b>Predicted Value:</b> ' + target_names[active] + '<br><b>Decision Impurity:</b> ' + (Object.values(RFStatsRead.impurity)[i]) + '<br><b>Influenced Instances:</b> ' + (Object.values(RFStatsRead.samples)[i]) + '<br><b>Hyperparameters:</b> ' + stringParametersRF[k])
                    }
                  }
                } else {
                  if (this.selectDecisionsTestLimitation.includes(i)) {
                    if (this.selectDecisions.length == 0) {
                      UMAPDataRFx.push(UMAPData[0][i])
                      UMAPDataRFy.push(UMAPData[1][i])
                      let active = Object.values(RFStatsRead.predicted_value)[i]
                      RFPredValue.push(colorRange[active])
                      if (Object.values(RFStatsRead.impurity)[i] <= this.basicValue2) {
                        RFImpurity.push((1 - Object.values(RFStatsRead.impurity)[i]))
                      } else {
                        RFImpurity.push(0.1)
                      }
                      RFSamples.push(constantMultiplier(Object.values(RFStatsRead.samples)[i] / result[1][active]))
                      classifiersInfoProcessingRF.push('<b>Model ID:</b> ' + 'RF' + (k+1) + '<br><b>Tree ID:</b> ' + (Object.values(RFStatsRead.tree_index)[i]) + '<br><b>Decision ID:</b> ' + (Object.values(RFStatsRead.node)[i]) + '<br><b>Predicted Value:</b> ' + target_names[active] + '<br><b>Decision Impurity:</b> ' + (Object.values(RFStatsRead.impurity)[i]) + '<br><b>Influenced Instances:</b> ' + (Object.values(RFStatsRead.samples)[i]) + '<br><b>Hyperparameters:</b> ' + stringParametersRF[k])
                    } else {
                      if (this.selectDecisions.includes(i)) {
                        UMAPDataRFx.push(UMAPData[0][i])
                        UMAPDataRFy.push(UMAPData[1][i])
                        let active = Object.values(RFStatsRead.predicted_value)[i]
                        RFPredValue.push(colorRange[active])
                        if (Object.values(RFStatsRead.impurity)[i] <= this.basicValue2) {
                          RFImpurity.push((1 - Object.values(RFStatsRead.impurity)[i]))
                        } else {
                          RFImpurity.push(0.1)
                        }
                        RFSamples.push(constantMultiplier(Object.values(RFStatsRead.samples)[i] / result[1][active]))
                        classifiersInfoProcessingRF.push('<b>Model ID:</b> ' + 'RF' + (k+1) + '<br><b>Tree ID:</b> ' + (Object.values(RFStatsRead.tree_index)[i]) + '<br><b>Decision ID:</b> ' + (Object.values(RFStatsRead.node)[i]) + '<br><b>Predicted Value:</b> ' + target_names[active] + '<br><b>Decision Impurity:</b> ' + (Object.values(RFStatsRead.impurity)[i]) + '<br><b>Influenced Instances:</b> ' + (Object.values(RFStatsRead.samples)[i]) + '<br><b>Hyperparameters:</b> ' + stringParametersRF[k])
                      }
                    }
                  }
                }
             }
           }
        }
        for (let k = 0; k < splitStatesAB.length; k++) {
          if (splitStatesAB[k] == 1) {
            if (k == 0) {
              startingPointAB = 0
            } else {
              startingPointAB = decisionsABReadSort[k-1]
            }
        //for (let i = RFLength; i < (RFLength+GBLength); i++) {
            for (let i = (RFLength+startingPointAB); i < (RFLength+decisionsABReadSort[k]); i++) {
              if (this.selectDecisionsTestLimitation.length == 0) {
                  if (this.selectDecisions.length == 0) {
                    UMAPDataGBx.push(UMAPData[0][i])
                    UMAPDataGBy.push(UMAPData[1][i])
                    var reduceID = i - RFLength
                    let active = Object.values(GBStatsRead.predicted_value)[reduceID]
                    GBPredValue.push(colorRange[active])
                    if (Object.values(GBStatsRead.impurity)[reduceID] <= this.basicValue2) {
                      GBImpurity.push((1 - Object.values(GBStatsRead.impurity)[reduceID]))
                    } else {
                      GBImpurity.push(0.1)
                    }
                    GBSamples.push(constantMultiplier(Object.values(GBStatsRead.samples)[reduceID] / result[1][active]))
                    classifiersInfoProcessingAB.push('<b>Model ID:</b> ' + 'AB' + (k+1) + '<br><b>Tree ID:</b> ' + (Object.values(GBStatsRead.tree_index)[reduceID]) + '<br><b>Decision ID:</b> ' + (Object.values(GBStatsRead.node)[reduceID]) + '<br><b>Predicted Value:</b> ' + target_names[active] + '<br><b>Decision Impurity:</b> ' + (Object.values(GBStatsRead.impurity)[reduceID]) + '<br><b>Influenced Instances:</b> ' + (Object.values(GBStatsRead.samples)[reduceID]) + '<br><b>Hyperparameters:</b> ' + stringParametersAB[k])
                  } else {
                    if (this.selectDecisions.includes(i)) {
                      UMAPDataGBx.push(UMAPData[0][i])
                      UMAPDataGBy.push(UMAPData[1][i])
                      var reduceID = i - RFLength
                      let active = Object.values(GBStatsRead.predicted_value)[reduceID]
                      GBPredValue.push(colorRange[active])
                      if (Object.values(GBStatsRead.impurity)[reduceID] <= this.basicValue2) {
                        GBImpurity.push((1 - Object.values(GBStatsRead.impurity)[reduceID]))
                      } else {
                        GBImpurity.push(0.1)
                      }
                      GBSamples.push(constantMultiplier(Object.values(GBStatsRead.samples)[reduceID] / result[1][active]))
                      classifiersInfoProcessingAB.push('<b>Model ID:</b> ' + 'AB' + (k+1) + '<br><b>Tree ID:</b> ' + (Object.values(GBStatsRead.tree_index)[reduceID]) + '<br><b>Decision ID:</b> ' + (Object.values(GBStatsRead.node)[reduceID]) + '<br><b>Predicted Value:</b> ' + target_names[active] + '<br><b>Decision Impurity:</b> ' + (Object.values(GBStatsRead.impurity)[reduceID]) + '<br><b>Influenced Instances:</b> ' + (Object.values(GBStatsRead.samples)[reduceID]) + '<br><b>Hyperparameters:</b> ' + stringParametersAB[k])
                    }
                  }
              } else {
                if (this.selectDecisionsTestLimitation.includes(i)) {
                  if (this.selectDecisions.length == 0) {
                    UMAPDataGBx.push(UMAPData[0][i])
                    UMAPDataGBy.push(UMAPData[1][i])
                    var reduceID = i - RFLength
                    let active = Object.values(GBStatsRead.predicted_value)[reduceID]
                    GBPredValue.push(colorRange[active])
                    if (Object.values(GBStatsRead.impurity)[reduceID] <= this.basicValue2) {
                      GBImpurity.push((1 - Object.values(GBStatsRead.impurity)[reduceID]))
                    } else {
                      GBImpurity.push(0.1)
                    }
                    GBSamples.push(constantMultiplier(Object.values(GBStatsRead.samples)[reduceID] / result[1][active]))
                    classifiersInfoProcessingAB.push('<b>Model ID:</b> ' + 'AB' + (k+1) + '<br><b>Tree ID:</b> ' + (Object.values(GBStatsRead.tree_index)[reduceID]) + '<br><b>Decision ID:</b> ' + (Object.values(GBStatsRead.node)[reduceID]) + '<br><b>Predicted Value:</b> ' + target_names[active] + '<br><b>Decision Impurity:</b> ' + (Object.values(GBStatsRead.impurity)[reduceID]) + '<br><b>Influenced Instances:</b> ' + (Object.values(GBStatsRead.samples)[reduceID]) + '<br><b>Hyperparameters:</b> ' + stringParametersAB[k])
                  } else {
                    if (this.selectDecisions.includes(i)) {
                      UMAPDataGBx.push(UMAPData[0][i])
                      UMAPDataGBy.push(UMAPData[1][i])
                      var reduceID = i - RFLength
                      let active = Object.values(GBStatsRead.predicted_value)[reduceID]
                      GBPredValue.push(colorRange[active])
                      if (Object.values(GBStatsRead.impurity)[reduceID] <= this.basicValue2) {
                        GBImpurity.push((1 - Object.values(GBStatsRead.impurity)[reduceID]))
                      } else {
                        GBImpurity.push(0.1)
                      }
                      GBSamples.push(constantMultiplier(Object.values(GBStatsRead.samples)[reduceID] / result[1][active]))
                      classifiersInfoProcessingAB.push('<b>Model ID:</b> ' + 'AB' + (k+1) + '<br><b>Tree ID:</b> ' + (Object.values(GBStatsRead.tree_index)[reduceID]) + '<br><b>Decision ID:</b> ' + (Object.values(GBStatsRead.node)[reduceID]) + '<br><b>Predicted Value:</b> ' + target_names[active] + '<br><b>Decision Impurity:</b> ' + (Object.values(GBStatsRead.impurity)[reduceID]) + '<br><b>Influenced Instances:</b> ' + (Object.values(GBStatsRead.samples)[reduceID]) + '<br><b>Hyperparameters:</b> ' + stringParametersAB[k])
                    }
                  }
                }
              }
            }
          }
        }

        if (this.selectDecisions.length != 0) {
          IDsRF = []
          IDsAB = []
          for (let k = 0; k < this.selectDecisions.length; k++) {
            if (this.selectDecisions[k] < RFLength) {
              IDsRF.push(this.selectDecisions[k].toString())
            } else {
              IDsAB.push(this.selectDecisions[k].toString())
            }
          }
        }

        // problems with order!
        // //1) combine the arrays:
        // var listRF = [];
        // for (var j = 0; j < RFSamples.length; j++) 
        //     listRF.push({'samples': RFSamples[j], 'impurity': RFImpurity[j], 'prediction':RFPredValue[j], 'UMAPX': UMAPDataRFx[j], 'UMAPY': UMAPDataRFy[j]});

        // //2) sort:
        // listRF.sort(function(a, b) {
        //     return ((a.samples > b.samples) ? -1 : ((a.samples == b.samples) ? 0 : 1));
        //     //Sort could be modified to, for example, sort on the age 
        //     // if the name is the same.
        // });

        // //3) separate them back out:
        // for (var k = 0; k < listRF.length; k++) {
        //     RFSamples[k] = listRF[k].samples;
        //     RFImpurity[k] = listRF[k].impurity;
        //     RFPredValue[k] = listRF[k].prediction;
        //     UMAPDataRFx[k] = listRF[k].UMAPX;
        //     UMAPDataRFy[k] = listRF[k].UMAPY;
        // }

        // //1) combine the arrays:
        // var listAB = [];
        // for (var j = 0; j < GBSamples.length; j++) 
        //     listAB.push({'samples': GBSamples[j], 'impurity': GBImpurity[j], 'prediction':GBPredValue[j], 'UMAPX': UMAPDataGBx[j], 'UMAPY': UMAPDataGBy[j]});

        // //2) sort:
        // listAB.sort(function(a, b) {
        //     return ((a.samples > b.samples) ? -1 : ((a.samples == b.samples) ? 0 : 1));
        //     //Sort could be modified to, for example, sort on the age 
        //     // if the name is the same.
        // });

        // //3) separate them back out:
        // for (var k = 0; k < listAB.length; k++) {
        //     GBSamples[k] = listAB[k].samples;
        //     GBImpurity[k] = listAB[k].impurity;
        //     GBPredValue[k] = listAB[k].prediction;
        //     UMAPDataGBx[k] = listAB[k].UMAPX;
        //     UMAPDataGBy[k] = listAB[k].UMAPY;
        // }

        var DataGeneral = []
          DataGeneral.push({
            type: 'scatter',
            mode: 'markers',
            x: UMAPDataRFx,
            y: UMAPDataRFy,
            hovertemplate: 
                  "%{text}<br><br>" +
                  "<extra></extra>",
            text: classifiersInfoProcessingRF,
            name: 'Random Forest (RF)',
            ids: IDsRF,
            marker: {
            size: RFSamples,
            opacity: RFImpurity,
            color: 'rgb(51,160,44)',
              line: {
                color: RFPredValue,
                width: 5
              }
            }
            // hovertemplate: 
            //       "%{text}<br><br>" +
            //       "<extra></extra>",
            // text: classifiersInfoProcessing,
            // marker: {
            //  line: { color: 'rgb(0, 0, 0)', width: 3 },
            //   //forScatterPlot,
            //   size: 12,
            //   colorscale: 'Viridis',
            //   colorbar: {
            //     title: '# Ov. Performance (%) #',
            //     titleside: 'right'
            //   },
            // }
          
          })

        DataGeneral.push({
          x: UMAPDataRFx,
          y: UMAPDataRFy,
          name: 'Density (RF)',
          ncontours: 10,
          showlegend: true,
          opacity: 1,
          hoverinfo: 'skip',
          colorscale: [[0, 'rgb(237,248,233)'], [0.25, 'rgb(186,228,179)'], [0.5, 'rgb(116,196,118)'], [0.75, 'rgb(49,163,84)'], [1, 'rgb(0,109,44)']],
          reversescale: false,
          showscale: false,
          visible: 'legendonly',
          colorbar: {
              title: 'Density Ranges',
              titleside:'right',
            },
          type: 'histogram2dcontour'
        })

        DataGeneral.push({
          type: 'scatter',
          mode: 'markers',
          x: UMAPDataGBx,
          y: UMAPDataGBy,
          hovertemplate: 
                "%{text}<br><br>" +
                "<extra></extra>",
          text: classifiersInfoProcessingAB,
          name: 'Adaptive Boosting (AB)',
          ids: IDsAB,
          marker: {
          size: GBSamples,
          opacity: GBImpurity,
          color: 'rgb(31,120,180)',
            line: {
              color: GBPredValue,
              width: 5
            }
          }

          // hovertemplate: 
          //       "%{text}<br><br>" +
          //       "<extra></extra>",
          // text: classifiersInfoProcessing,
          // marker: {
          //  line: { color: 'rgb(0, 0, 0)', width: 3 },
          //   //forScatterPlot,
          //   size: 12,
          //   colorscale: 'Viridis',
          //   colorbar: {
          //     title: '# Ov. Performance (%) #',
          //     titleside: 'right'
          //   },
          // }
        
        })

        DataGeneral.push({
          x: UMAPDataGBx,
          y: UMAPDataGBy,
          hoverinfo: 'skip',
          name: 'Density (AB)',
          ncontours: 10,
          opacity: 1,
          showlegend: true,
          colorscale: [[0, 'rgb(239,243,255)'], [0.25, 'rgb(189,215,231)'], [0.5, 'rgb(107,174,214)'], [0.75, 'rgb(49,130,189)'], [1, 'rgb(8,81,156)']],
          reversescale: false,
          showscale: false,
          visible: 'legendonly',
          colorbar: {
              title: 'Density Ranges',
              titleside:'right',
            },
          type: 'histogram2dcontour'
        })

        var width = 805
        var height = 590

        var layout = {
          xaxis: {
              visible: false,
              autorange: true
          },
          yaxis: {
              visible: false,
              autorange: true
          },
          font: { family: 'Helvetica', size: 14, color: '#000000' },
          autosize: false,
          width: width,
          height: height,
          dragmode: 'lasso',
          hovermode: "closest",
          hoverlabel: { bgcolor: "#FFF" },
          legend: {orientation: 'h', x: 0.15, y: 0},
          margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0,
            pad: 0
          },
        }
     
        var graphDiv = document.getElementById('Scatterplot')
        var config = {scrollZoom: true, displaylogo: false, showLink: false, showSendToCloud: false, modeBarButtonsToRemove: ['toImage', 'toggleSpikelines', 'autoScale2d', 'hoverClosestGl2d','hoverCompareCartesian','select2d','hoverClosestCartesian'], responsive: true}

        Plotly.newPlot(graphDiv, DataGeneral, layout, config)

        var legendColors = ['rgba(31,120,180,1)','rgba(51,160,44,1)']
        var legendBoxes = graphDiv.getElementsByClassName("scatterpts")
        
        for (let i = 0; i < legendBoxes.length; i++) {
          Plotly.d3.select(legendBoxes[i]).style("fill", legendColors[(legendBoxes.length-1) - i]);
          Plotly.d3.select(legendBoxes[i]).style("stroke", '#dcdcdc');
          Plotly.d3.select(legendBoxes[i]).attr("d", 'M7,0A7,7 0 1,1 0,-7A7,7 0 0,1 7,0Z');
        }

        if (this.selectDecisionsTestLimitation != 0) {
          if (this.selectDecisions != 0) {
            EventBus.$emit('emittedEventCallingTestingView', this.selectDecisions)
          } else {
            EventBus.$emit('emittedEventCallingTestingView', this.selectDecisionsTestLimitation)
          }
        }

        graphDiv.on('plotly_selected', function(evt) {
          if (typeof evt !== 'undefined') {
            var ClassifierIDsListCleared = []
            var resultsSelection = []
            var countRFLoc = 0
            var countABLoc = 0
            var countARLoc = 0
            for (let i = 0; evt.points.length; i++) {
              if (evt.points[i] === undefined) {
                break
              } else {
                var obj = {}
                var splittedHover = evt.points[i].text.split(/[ ,]+/)
                obj["model"] = splittedHover[2][0] + splittedHover[2][1]
                if (obj["model"] == "AR") {

                } else {
                  obj["model_id"] = parseInt(splittedHover[2].match(/\d/g).join(''), 10)
                  obj["tree_id"] = parseInt(splittedHover[4].match(/\d/g).join(''), 10)
                  obj["decision_id"] = parseInt(splittedHover[6].match(/\d/g).join(''), 10)
                }
                resultsSelection.push(obj)
                ClassifierIDsListCleared.push(parseInt(evt.points[i].id))
                if (IDsRF.includes(evt.points[i].id)) {
                  countRFLoc = countRFLoc + 1
                } else if (IDsAB.includes(evt.points[i].id)) {
                  countABLoc = countABLoc + 1
                } else {
                  countARLoc = countARLoc + 1
                }
              }
            }
          }
          EventBus.$emit('sendDecisionsFiltered', resultsSelection)
          EventBus.$emit('numberRF', countRFLoc)
          EventBus.$emit('numberAB', countABLoc)       
          EventBus.$emit('numberTotalActive', (countRFLoc+countABLoc)) 
          EventBus.$emit('emittedEventCallingTestingView', ClassifierIDsListCleared)
        });
        EventBus.$emit('numberRF', IDsRF.length)
        EventBus.$emit('numberAB', IDsAB.length)
        EventBus.$emit('numberTotalActive', (IDsRF.length+IDsAB.length))
        EventBus.$emit('numberTotal', this.selectDecisionsTestLimitation.length)
        
        EventBus.$emit('selectDecisionsTestLimitation', this.selectDecisionsTestLimitation)
        EventBus.$emit('selectDecisions', this.selectDecisions)
      }
    },
  mounted () {    

    EventBus.$on('StatesUpdate', data => {
      this.states = data})

    EventBus.$on('indicesRFSend', data => { this.RFSort = data })
    EventBus.$on('indicesGBSend', data => { this.GBSort = data })
    EventBus.$on('changeInNumberOfModelsImp', data => { EventBus.$emit('TrueFlag', true) })
    EventBus.$on('changeInNumberOfModelsImp', data => { this.states = data })
    EventBus.$on('changeInNumberOfModelsImp', data => { this.selectDecisionsTestLimitation = [] })
    EventBus.$on('changeInNumberOfModelsImp', data => { this.selectDecisions = [] })
    EventBus.$on('changeInNumberOfModelsImp', this.ScatterplotView)
    EventBus.$on('changeInNumberOfModelsImp', this.InitThresh)

    EventBus.$on('emittedEventCallingThresh', this.InitThresh)

    EventBus.$on('emittedEventCallingXData', data => {
      this.truth = data})
    EventBus.$on('emittedEventCallingTrainingResults', data => {
      this.FinalResultsGeneral = data})
    EventBus.$on('emittedEventCallingUMAPDecisions', data => { this.FinalResultsScatter = data })
    EventBus.$on('emittedEventCallingUMAPDecisions', this.ScatterplotView)

    EventBus.$on('updateSpace', data => { this.selectDecisions = data })
    EventBus.$on('updateSpace', data => { this.selectDecisionsTestLimitation = [] })
    EventBus.$on('updateSpace', this.updateSpaceFun)

    EventBus.$on('emittedEventCallingTestXData', data => { this.X_testData = data })
    EventBus.$on('activeTestInstance', data => { this.activeTestInstance = data })
    EventBus.$on('activeTestInstance', data => { this.selectDecisionsTestLimitation = [] })
    EventBus.$on('activeTestInstance', data => { this.selectDecisions = [] })
    EventBus.$on('activeTestInstance', this.ScatterplotView)
    EventBus.$on('activeTestInstance', this.InitThresh)

    EventBus.$on('refreshImmediately', this.refreshImm)

    EventBus.$on('empty', data => { this.selectDecisionsTestLimitation = [] })
    EventBus.$on('empty', data => { this.selectDecisions = [] })

    EventBus.$on('emittedEventCallingTestingView', data => { this.currentListOfPoints = data })

    EventBus.$on('SendToServerDataSetBasicConfirm', data => { this.RetrieveName = data })

    EventBus.$on('reset', this.reset)
  }
}
</script>

<style>

  .ticks {
      font-size: 10px;
    }

    .track,
    .track-inset,
    .track-overlay {
      stroke-linecap: round;
    }

    .track {
      stroke: #dcdcdc;
      stroke-width: 10px;
    }

    .track-inset {
      stroke: #dcdcdc;
      stroke-width: 8px;
    }

    .track-overlay {
      pointer-events: stroke;
      stroke-width: 50px;
      stroke: transparent;
      cursor: crosshair;
    }

    .handle {
      fill: #fff;
      stroke: #000;
      stroke-opacity: 0.5;
      stroke-width: 1.25px;
    }
</style>
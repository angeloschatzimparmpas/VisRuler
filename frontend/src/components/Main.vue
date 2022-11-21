<!-- Main Visualization View -->

<template>
<body>
    <b-container fluid class="bv-example-row">
      <b-row class="md-3">
        <b-col cols="12">
          <mdb-card>
            <mdb-card-header color="primary-color" tag="h5" class="text-center"><DataSetSlider/></mdb-card-header>
            <mdb-card-body>
              <mdb-card-text class="text-left" style="font-size: 18.5px; min-height: 485px">
                <Filtering/>
              </mdb-card-text>
            </mdb-card-body>
          </mdb-card>
        </b-col>
      </b-row>
      <b-row class="md-3" style="margin-top:-8px">
        <b-col cols="2">
          <mdb-card style="margin-top: 15px;">
            <mdb-card-header color="primary-color" tag="h5" class="text-center"><font-awesome-icon icon="star" style="margin-right: 5px"/>Global Feature Ranking (Training)
              </mdb-card-header>
              <mdb-card-body>
                <mdb-card-text class="text-center"  style="min-height: 776px">
                  <Importance/>
                </mdb-card-text>
              </mdb-card-body>
          </mdb-card>
        </b-col>
          <b-col cols="4">
            <mdb-card style="margin-top: 15px;">
              <mdb-card-header color="primary-color" tag="h5" class="text-left"><font-awesome-icon icon="ruler-combined" style="margin-right: 5px;"/>Decisions Space (Training)<span class="float-right">{{ activeDecisions }} ({{numberofRF}}+{{numberofAB}}) out of {{ totalDecisions }} decisions</span>
                </mdb-card-header>
                <mdb-card-body>
                  <mdb-card-text class="text-center"  style="min-height: 784px">
                    <Space/>
                  </mdb-card-text>
                </mdb-card-body>
            </mdb-card>
          </b-col>
          <b-col cols="4">
            <mdb-card style="margin-top: 15px;">
              <mdb-card-header color="primary-color" tag="h5" class="text-left" style="background-color: #C0C0C0; z-index: 2"><font-awesome-icon icon="gavel" style="margin-right: 5px;"/>Manual Decisions (Testing)<span class="float-right">{{ trainingInstances }} ({{instanceDistribution}}) training instances</span>
              </mdb-card-header>
              <mdb-card-body>
                <mdb-card-text class="text-center"  style="min-height: 788px !important; max-height: 788px !important">
                  <Test/>
                </mdb-card-text>
              </mdb-card-body>
            </mdb-card>
          </b-col>
          <b-col cols="2">
            <mdb-card style="margin-top: 15px;">
              <mdb-card-header color="primary-color" tag="h5" class="text-center" style="background-color: #C0C0C0;"><font-awesome-icon icon="envelope-open-text" style="margin-right: 5px;"/>Decisions Evaluation (Testing)
              </mdb-card-header>
              <mdb-card-body>
                <mdb-card-text class="text-center"  style="min-height: 776px">
                  <Rules/>
                </mdb-card-text>
              </mdb-card-body>
            </mdb-card>
          </b-col>
        </b-row>
    </b-container>
  <div class="w3-container">
      <div id="myModal" class="w3-modal" style="position: fixed;">
        <div class="w3-modal-content w3-card-4 w3-animate-zoom">
          <header class="w3-container w3-blue"> 
          <h3 style="display:inline-block; font-size: 22px; margin-top: 15px; margin-bottom:15px">Extracting Manual Decisions (using Cryo)</h3>
          </header>
          <Export/>
          <div class="w3-container w3-light-grey w3-padding">
          <button style="float: right; margin-top: -3px; margin-bottom: -3px"
            id="closeModal" class="w3-button w3-right w3-white w3-border" 
            v-on:click="closeModalFun">
            <font-awesome-icon icon="window-close" />
            {{ valuePickled }}
            </button>
          </div>
          </div>
        </div>
      </div>
  </body>
</template>

<script>

import Vue from 'vue'
import DataSetSlider from './DataSetSlider.vue'
import Filtering from './Filtering.vue'
import Importance from './Importance.vue'
import Space from './Space.vue'
import Test from './Test.vue'
import Rules from './Rules.vue'
import Export from './Export.vue'
import axios from 'axios'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'
import 'bootstrap-css-only/css/bootstrap.min.css'
import { mdbCard, mdbCardBody, mdbCardText, mdbCardHeader } from 'mdbvue'
import { EventBus } from '../main.js'
import $ from 'jquery'; // <-to import jquery
import 'bootstrap';
import * as d3Base from 'd3'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base)

export default Vue.extend({
  name: 'Main',
  components: {
    DataSetSlider,
    Filtering,
    Importance,
    Space,
    Test,
    Rules,
    Export,
    mdbCard,
    mdbCardBody,
    mdbCardHeader,
    mdbCardText
  },
  data () {
    return {
      roundingValue: 15,
      valuePickled: 'Close',
      RetrieveValueFile: 'HappinessC', // this is for the default data set
      reset: false,
      ModelSpaceUMAPSend: 0,
      PerformancePerModel: 0,
      X_train: 0,
      X_test: 0,
      y_train: 0,
      y_test: 0,
      RulesVa: 0,
      RulesStats: 0,
      RulesPr: 0,
      HypRF: 0,
      HypAB: 0,
      activeDecisions: 0,
      numberofRF: 0,
      numberofAB: 0,
      totalDecisions: 0,
      trainingInstances: 0,
      instanceDistribution: '0+0+0',
      RFNewModels: {},
      ABNewModels: {},
      thresholdMain: 0,
      whoWasRemoved: -1,
    }
  },
  methods: {
    removeFeature () {
      const path = `http://127.0.0.1:5000/data/askToRemoveAFeature`

      const postData = {
        whoWasRemoved: this.whoWasRemoved
      }
      const axiosConfig = {
      headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
      'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
      }
      }
      axios.post(path, postData, axiosConfig)
      .then(response => {
        console.log('Successfully removed a feature!')
        this.getModelsPerformanceFromBackend()
      })
      .catch(error => {
      console.log(error)
      })
    },
    updateRoundingFun () {
      const path = `http://127.0.0.1:5000/data/updateRounding`

      const postData = {
        roundingValue: this.roundingValue
      }
      const axiosConfig = {
      headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
      'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
      }
      }
      axios.post(path, postData, axiosConfig)
      .then(response => {
        console.log('Updated rounding decisions!')
        this.getModelsPerformanceFromBackend()
      })
      .catch(error => {
      console.log(error)
      })
    },
    openModalFun () {
      $('#myModal').modal('show')
    },
    closeModalFun () {
      $('#myModal').modal('hide')
    },
    getCollectionFromBackend () {
      const path = `http://localhost:5000/data/ClientRequest`

      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.get(path, axiosConfig)
        .then(response => {
          this.Collection = response.data.Collection
          EventBus.$emit('emittedEventCallingDataPlot', this.Collection)
          console.log('Collection was overwritten with new data sent by the server!')
        })
        .catch(error => {
          console.log(error)
        })
    },
    getDatafromtheBackEnd () {
      const path = `http://localhost:5000/data/PlotClassifiers`
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.get(path, axiosConfig)
        .then(response => {
          this.OverviewResults = response.data.OverviewResults
          console.log('Server successfully sent all the data related to visualizations!')
          EventBus.$emit('emittedEventCallingScatterPlot', this.OverviewResults)
          EventBus.$emit('emittedEventCallingGrid', this.OverviewResults)
          EventBus.$emit('emittedEventCallingGridSelection', this.OverviewResults)
          //this.getFinalResults()
        })
        .catch(error => {
          console.log(error)
        })
    },
    getCMComputedData () {
      const path = `http://localhost:5000/data/PlotCrossMutate`

      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.get(path, axiosConfig)
        .then(response => {
          this.OverviewResultsCM = response.data.OverviewResultsCM
          console.log('Server successfully sent all the data related to visualizations!')
          EventBus.$emit('emittedEventCallingCrossoverMutation', this.OverviewResultsCM)
          //this.getFinalResults()
        })
        .catch(error => {
          console.log(error)
        })
    },
    SendToServerData () {
      const path = `http://127.0.0.1:5000/data/SendtoSeverDataSet`

      const postData = {
        uploadedData: this.localFile
      }
      const axiosConfig = {
      headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
      'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
      }
      }
      axios.post(path, postData, axiosConfig)
      .then(response => {
        console.log('Sent the new uploaded data to the server!')
      })
      .catch(error => {
      console.log(error)
      })
    },
    SearchForNewModels () {
      const path = `http://127.0.0.1:5000/data/SearchingAgain`

      const postData = {
        RFNewModels: this.RFNewModels,
        ABNewModels: this.ABNewModels,
        thresholdMain: this.thresholdMain
      }
      const axiosConfig = {
      headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
      'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
      }
      }
      axios.post(path, postData, axiosConfig)
      .then(response => {
        console.log('Sent new search details!')
        this.getModelsPerformanceFromBackend()
      })
      .catch(error => {
      console.log(error)
      })
    },
    getFinalResultsFromBackend () {
      const path = `http://localhost:5000/data/SendFinalResultsBacktoVisualize`

      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.get(path, axiosConfig)
        .then(response => {
          this.FinalResults = response.data.FinalResults
          console.log(this.FinalResults)
          EventBus.$emit('emittedEventCallingLinePlot', this.FinalResults)
        })
        .catch(error => {
          console.log(error)
        })
    },
    fileNameSend () {
      const path = `http://127.0.0.1:5000/data/ServerRequest`
      EventBus.$emit('SendToServerDataSetBasicConfirm', this.RetrieveValueFile)
      const postData = {
        fileName: this.RetrieveValueFile,
      }
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.post(path, postData, axiosConfig)
      .then(response => {
        console.log('File name was sent successfully!')
        this.getModelsPerformanceFromBackend()
      })
      .catch(error => {
        console.log(error)
      })
    },
    getModelsPerformanceFromBackend () {
      const path = `http://localhost:5000/data/PerformanceForEachModel`

      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.get(path, axiosConfig)
        .then(response => {
          this.PerformancePerModel = response.data.PerformancePerModel
          this.ModelSpaceUMAPSend = response.data.ModelSpaceUMAPSend
          this.X_train = response.data.X_train
          this.y_train = response.data.y_train
          this.y_test = response.data.y_test
          this.X_test = response.data.X_test
          this.RulesVa = response.data.RulesVa
          this.RulesStats = response.data.RulesStats
          this.RulesPr = response.data.RulesPr
          this.HypRF = response.data.HypRF
          this.HypAB = response.data.HypAB
          EventBus.$emit('empty')
          var NumberOfModels = response.data.NumberOfModels
          EventBus.$emit('numberOfModelsUpdate', NumberOfModels)
          var States = response.data.States
          EventBus.$emit('StatesUpdate', States) 
          EventBus.$emit('changeInNumberOfModelsRF', NumberOfModels.length)
          EventBus.$emit('changeInNumberOfModelsAB', NumberOfModels.length)
          EventBus.$emit('changeInNumberOfModels', States.length)  
          EventBus.$emit('totalModelsUpdate', States.length) 
          
          var target_names = JSON.parse(this.PerformancePerModel[9])
          if (target_names.length == 2) {
            this.instanceDistribution = '0+0'
          }
          var RFPredictions = JSON.parse(this.PerformancePerModel[13])
          var GBPredictions = JSON.parse(this.PerformancePerModel[30])
          var results = []
          results.push(RFPredictions) // 0
          results.push(GBPredictions) // 1
          results.push(this.y_test) // 2
          results.push(target_names) // 3
          results.push(this.X_train) // 4
          results.push(this.y_train) // 5
          results.push(this.X_test) // 6
          results.push(this.HypRF) // 10 -> 7
          results.push(this.HypAB) // 11 -> 8
          results.push(this.PerformancePerModel[12]) // 12 -> 9
          EventBus.$emit('emittedEventCallingXData', this.y_train)
          EventBus.$emit('emittedEventCallingHyperParams', this.PerformancePerModel)
          EventBus.$emit('emittedEventCallingResult', results)
          EventBus.$emit('emittedEventCallingTrainingResults', this.PerformancePerModel)
          EventBus.$emit('emittedEventCallingRules', results)
          EventBus.$emit('emittedEventCallingTestXData', this.X_test)
          EventBus.$emit('emittedEventCallingUMAPDecisions', this.ModelSpaceUMAPSend)
          EventBus.$emit('emittedEventCallingThresh')
          EventBus.$emit('emittedEventCallingEvaluation')

          EventBus.$emit('CorrThres', 0)
          EventBus.$emit('callSliderAgain')

          console.log('Server successfully sent all computed information!')
          
        })
        .catch(error => {
          console.log(error)
        })
    },
    Reset () {
      const path = `http://127.0.0.1:5000/data/Reset`
      this.reset = true
      const postData = {
        ClassifiersList: this.reset
      }
      const axiosConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS'
        }
      }
      axios.post(path, postData, axiosConfig)
        .then(response => {
          console.log('The server side was reset! Done.')
          this.reset = false
          EventBus.$emit('resetViews')
          this.fileNameSend()
        })
        .catch(error => {
          console.log(error)
        })
    },
    render (flag) {
      this.combineWH = []
      this.width = document.body.clientWidth / 12 - 30
      this.height = document.body.clientHeight / 3
      this.combineWH.push(this.width)
      this.combineWH.push(this.height)
      if(flag) {
        EventBus.$emit('Responsive', this.combineWH)
      }
      else {
        EventBus.$emit('ResponsiveandChange', this.combineWH)
      }
    },
    change () {
      this.render(false)
    },
  },
  created () {

    // does the browser support the Navigation Timing API?
    if (window.performance) {
        console.info("window.performance is supported");
    }
    // do something based on the navigation type...
    if(performance.navigation.type === 1) {
        console.info("TYPE_RELOAD");
        this.Reset();
    }
  },
  mounted() {

    EventBus.$on('CorrThres', data => { this.thresholdMain = data })
    EventBus.$on('CallNewModels', this.SearchForNewModels)

    EventBus.$on('updateRFNewModels', data => {
      this.RFNewModels[data[0]] = data[1]
    })

    EventBus.$on('updateABNewModels', data => {
      this.ABNewModels[data[0]] = data[1]
    })

    $(document).ready(function(){ 
        $(window).scroll(function(){
          $('.bottom').css('transform', 'translate3d(0,' + $(this).scrollTop()*2 + 'px, 0)'); 
        }).scroll();
    });  

    var modal = document.getElementById('myModal')
    window.onclick = function(event) {
      //alert(event.target)
        if (event.target == modal) {
            modal.style.display = "none";
        } 
    }
    this.render(true)
    loadProgressBar()
    window.onbeforeunload = function(e) {
      return 'Dialog text here.'
    }
    $(window).on("unload", function(e) {
      alert('Handler for .unload() called.');
    })

    EventBus.$on('OpenModal', this.openModalFun)

    EventBus.$on('numberRF', data => { this.numberofRF = data })
    EventBus.$on('numberAB', data => { this.numberofAB = data })
    EventBus.$on('numberTotalActive', data => { this.activeDecisions = data })
    EventBus.$on('numberTotal', data => { this.totalDecisions = data })

    EventBus.$on('sendInstancesSeg', data => { this.instanceDistribution = data })
    EventBus.$on('sendInstancesSum', data => { this.trainingInstances = data })

    EventBus.$on('changedRoundingPrecision', data => { this.roundingValue = data })
    EventBus.$on('changedRoundingPrecision', this.updateRoundingFun)

    EventBus.$on('ButtonIDRemove', data => { this.whoWasRemoved = data })
    EventBus.$on('ButtonIDRemove', this.removeFeature)

    EventBus.$on('SendToServerDataSetConfirmation', data => { this.RetrieveValueFile = data })
    EventBus.$on('SendToServerDataSetConfirmation', this.fileNameSend)

    //Prevent double click to search for a word. 
    document.addEventListener('mousedown', function (event) {
      if (event.detail > 1) {
      event.preventDefault();
      }
    }, false);

  },
})
</script>

<style lang="scss">

#nprogress .bar {
background: red !important;
}

#nprogress .peg {
box-shadow: 0 0 10px red, 0 0 5px red !important;
}

#nprogress .spinner-icon {
border-top-color: red !important;
border-left-color: red !important;
}

body {
  font-family: 'Helvetica', 'Arial', sans-serif !important;
  left: 0px;
  right: 0px;
  top: 0px;
  bottom: 0px;
  margin-top: -8px !important;
  overflow-x: hidden !important;
  overflow-y: hidden !important;
}

.modal-backdrop {
  z-index: -1 !important;
}

.card-body {
   padding: 0.60rem !important;
}

hr {
  margin-top: 1rem;
  margin-bottom: 1rem;
  border: 0;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

@import './../assets/w3.css';
</style>
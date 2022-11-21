<template>
    <b-row style="padding-top: 5px;">
      <b-col cols="3" style="margin-left: -35px">
        <label id="data" for="param-dataset" data-toggle="tooltip" data-placement="right" title="Tip: use one of the data sets already provided or upload a new file.">{{ dataset }}</label>
        <select id="selectFile" @change="selectDataSet()">
            <option value="IrisC.csv" >Iris Flower</option>
            <option value="CreditC.csv" >Credit Bank</option>
            <option value="HappinessC.csv" selected>Happiness</option>
        </select>
        <button class="btn-outline-dark"
        id="resetID"
        v-on:click="reset">
        <font-awesome-icon icon="trash" />
        {{ resetText }}
        </button>
      </b-col>
      <b-col cols="6"><font-awesome-icon icon="ruler-vertical" style="margin-right: 5px"/><font-awesome-icon icon="ruler-horizontal" style="margin-right: 5px;"/>
        Models Overview (Training)
      </b-col>
      <b-col cols="3">
        {{ numberofActiveModels }} ({{numberofActiveModelsRF}}+{{numberofActiveModelsAB}}) out of {{ numberofTotalModels }} models currently active
      </b-col>
    </b-row>
</template>

<script>
import { EventBus } from '../main.js'
import * as d3Base from 'd3'
import { sliderBottom } from 'd3-simple-slider'

// attach all d3 plugins to the d3 library
const d3 = Object.assign(d3Base, { sliderBottom })

export default {
  name: 'DataSetSlider',
  data () {
    return {
      defaultDataSet: '', // default value for the first data set
      resetText: 'Reset',
      numberofActiveModelsRF: '10',
      numberofActiveModelsAB: '10',
      numberofActiveModels: '20',
      numberofTotalModels: '20',
      dataset: 'Data Set'
    }
  },
  methods: {
    selectDataSet () {   
      const fileName = document.getElementById('selectFile')
      this.defaultDataSet = fileName.options[fileName.selectedIndex].value
      this.defaultDataSet = this.defaultDataSet.split('.')[0]

      this.dataset = "Data set"
      d3.select("#data").select("input").remove(); // Remove the selection field.
      EventBus.$emit('SendToServerDataSetConfirmation', this.defaultDataSet)
    },
    reset () {
      EventBus.$emit('reset')
      EventBus.$emit('alternateFlagLock')
    },
    search () {
      
    },
    filter () {
      EventBus.$emit('ConfirmDataSet')
    },
  },
  mounted () {
    EventBus.$on('totalModelsUpdate', data => { this.numberofTotalModels = data.toString() })
    EventBus.$on('changeInNumberOfModelsRF', data => { this.numberofActiveModelsRF = data.toString() })
    EventBus.$on('changeInNumberOfModelsAB', data => { this.numberofActiveModelsAB = data.toString() })
    EventBus.$on('changeInNumberOfModels', data => { this.numberofActiveModels = data.toString() })
  },
}
</script>

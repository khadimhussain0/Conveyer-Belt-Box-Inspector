<template>
  <div id="app">
    <Canvas ref="canvas"/>
    <div class="info-container">
      <InfoCard title="Number of Boxes Detected" :content="numberOfBoxesDetected" />
      <InfoCard title="Line Card" :content="currentLine" />
      <InfoCard title="App Started" :content="startTimeFormatted" />
      <Button @start-line-inspector="startLineInspector" @stop-line-inspector="stopLineInspector" />
    </div>
  </div>
</template>

<script>
import Canvas from './components/Canvas.vue';
import InfoCard from './components/InfoCard.vue';
import Button from './components/Button.vue';
import axios from 'axios';

export default {
  name: 'App',
  components: {
    Canvas,
    InfoCard,
    Button
  },
  data() {
    return {
      numberOfBoxesDetected: 0,
      currentLine: '1',
      startTime: new Date(),
      timer: null
    };
  },
  computed: {
    startTimeFormatted() {
      return this.startTime.toLocaleString();
    }
  },
  methods: {
    async startLineInspector() {
      this.timer = setInterval(this.fetchDetectionResults, 1000);
    },
    stopLineInspector() {
      clearInterval(this.timer);
    },
    async fetchDetectionResults() {
      try {
        const response = await axios.get('YOUR_FASTAPI_BACKEND_ENDPOINT');
        this.numberOfBoxesDetected = response.data.numberOfBoxesDetected;
        this.currentLine = response.data.currentLine;
      } catch (error) {
        console.error('Error fetching detection results:', error);
      }
    }
  }
};
</script>

<style>
#app {
  display: flex;
  height: 100vh;
}

.info-container {
  flex: 1;
  padding: 20px;
}
</style>

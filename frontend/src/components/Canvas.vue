<template>
    <div class="canvas-container" :style="{ position: lineInspectorActive ? 'relative' : 'static' }">
        <div class="dropdown" @click="toggleDropdown">
            <button class="dropbtn">{{ selectedOption }}</button>
            <div v-show="showDropdown" class="dropdown-content">
                <a @click="selectOption('Live Camera')">Live Camera</a>
                <a @click="selectOption('Video')">Video</a>
                <a @click="selectOption('Image')">Image</a>
            </div>
        </div>
        <video ref="videoPlayer" style="width: 100%; height: auto; position: relative;" @play="onVideoPlay"></video>
        <input type="file" ref="fileInput" accept="image/*,video/*" style="display: none;" @change="handleFileInput">
        <button @click="toggleLineInspector" v-if="selectedOption !== 'Select Option'">
            {{ lineInspectorActive ? 'Stop Line Inspector' : 'Start Line Inspector' }}
        </button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            showDropdown: false,
            selectedOption: 'Select Option',
            videoStream: null,
            lineInspectorActive: false,
            intervalId: null,
            detections: []
        };
    },
    methods: {
        toggleDropdown() {
            this.showDropdown = !this.showDropdown;
        },
        selectOption(option) {
            this.selectedOption = option;
            this.showDropdown = false;
            if (option === 'Video') {
                this.$refs.fileInput.click();
            } else if (option === 'Live Camera') {
                this.startLiveCamera();
            } else if (option === 'Image') {
                this.$refs.fileInput.click();
            }
        },
        async startLiveCamera() {
            try {
                const devices = await navigator.mediaDevices.enumerateDevices();
                const hasVideoDevice = devices.some(device => device.kind === 'videoinput');
                if (!hasVideoDevice) {
                    throw new Error('No video input device found.');
                }
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                this.$refs.videoPlayer.srcObject = stream;
                this.$refs.videoPlayer.play();
                this.videoStream = stream;
            } catch (error) {
                console.error('Error accessing camera:', error);
                alert('Error accessing camera. Please make sure your camera is connected and accessible.');
            }
        },
        async handleFileInput(event) {
            const file = event.target.files[0];
            if (!file) return;

            if (this.selectedOption === 'Video') {
                this.$refs.videoPlayer.src = URL.createObjectURL(file);
                this.$refs.videoPlayer.play();
            } else if (this.selectedOption === 'Image') {
                const reader = new FileReader();
                reader.onload = () => {
                    this.$refs.videoPlayer.src = reader.result;
                    this.$refs.videoPlayer.play();
                };
                reader.readAsDataURL(file);
            }
        },
        toggleLineInspector() {
            this.lineInspectorActive = !this.lineInspectorActive;
            if (this.lineInspectorActive) {
                this.intervalId = setInterval(this.detectAndDrawBoundingBoxes, 1000);
            } else {
                clearInterval(this.intervalId);
            }
        },
        detectAndDrawBoundingBoxes() {
            const mockResponse = [
                { bbox: [100, 100, 200, 200], confidence: 0.95, class: 'person' },
                { bbox: [300, 300, 400, 400], confidence: 0.85, class: 'car' }
            ];
            this.detections = mockResponse;
            this.drawDetections();
        },
        drawDetections() {
            const overlay = document.createElement('div');
            overlay.className = 'detections-overlay';
            const videoContainer = this.$refs.videoPlayer.parentElement;
            videoContainer.appendChild(overlay);
            overlay.innerHTML = '';
            const video = this.$refs.videoPlayer;
            const videoWidth = video.offsetWidth;
            const videoHeight = video.offsetHeight;
            this.detections.forEach(detection => {
                const [x1, y1, x2, y2] = detection.bbox;
                const boxElement = document.createElement('div');
                boxElement.style.position = 'absolute';
                boxElement.style.left = `${(x1 / video.videoWidth) * videoWidth}px`;
                boxElement.style.top = `${(y1 / video.videoHeight) * videoHeight}px`;
                boxElement.style.width = `${((x2 - x1) / video.videoWidth) * videoWidth}px`;
                boxElement.style.height = `${((y2 - y1) / video.videoHeight) * videoHeight}px`;
                boxElement.style.border = '2px solid #00ff00';
                boxElement.innerText = `${detection.class}: ${detection.confidence.toFixed(2)}`;
                overlay.appendChild(boxElement);
            });
        },
        onVideoPlay() {
            if (this.lineInspectorActive) {
                this.drawDetections();
            }
        }
    }
};
</script>

<style scoped>
.canvas-container {
    width: 50%;
    height: 100%;
}

.dropdown {
    position: relative;
    display: inline-block;
}

.dropbtn {
    background-color: #4CAF50;
    color: white;
    padding: 16px;
    font-size: 16px;
    border: none;
    cursor: pointer;
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
    z-index: 1;
}

.dropdown-content a {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
}

.dropdown-content a:hover {
    background-color: #f1f1f1;
}

.dropdown:hover .dropdown-content {
    display: block;
}

.dropdown:hover .dropbtn {
    background-color: #3e8e41;
}

.detections-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
</style>

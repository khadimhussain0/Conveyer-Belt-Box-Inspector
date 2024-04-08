<template>
    <div class="canvas-container">
        <div class="dropdown" @click="toggleDropdown">
            <button class="dropbtn">{{ selectedOption }}</button>
            <div v-show="showDropdown" class="dropdown-content">
                <a @click="selectOption('Live Camera')">Live Camera</a>
                <a @click="selectOption('Video')">Video</a>
                <a @click="selectOption('Image')">Image</a>
            </div>
        </div>
        <canvas ref="canvas"></canvas>
        <input type="file" ref="fileInput" accept="image/*,video/*" style="display: none;" @change="handleFileInput">
        <video ref="videoPlayer" style="display: none;"></video>
    </div>
</template>

<script>
export default {
    data() {
        return {
            canvas: null,
            ctx: null,
            showDropdown: false,
            selectedOption: 'Select Option',
            videoStream: null
        };
    },
    mounted() {
        this.canvas = this.$refs.canvas;
        this.ctx = this.canvas.getContext('2d');
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
                this.renderLiveCamera(stream);
            } catch (error) {
                console.error('Error accessing camera:', error);
                alert('Error accessing camera. Please make sure your camera is connected and accessible.');
            }
        },
        renderLiveCamera(stream) {
            this.stopVideo();
            const video = this.$refs.videoPlayer;
            video.srcObject = stream;
            video.onloadedmetadata = () => {
                this.canvas.width = video.videoWidth;
                this.canvas.height = video.videoHeight;
                video.play();
                const drawFrame = () => {
                    this.ctx.drawImage(video, 0, 0);
                    requestAnimationFrame(drawFrame);
                };
                drawFrame();
            };
        },
        handleFileInput(event) {
            const file = event.target.files[0];
            if (!file) return;

            if (this.selectedOption === 'Video') {
                this.stopVideo();
                this.renderVideo(file);
            } else if (this.selectedOption === 'Image') {
                this.stopVideo();
                const reader = new FileReader();
                reader.onload = () => {
                    this.renderImage(reader.result);
                };
                reader.readAsDataURL(file);
            }
        },
        renderImage(imageData) {
            this.clearCanvas();
            const image = new Image();
            image.onload = () => {
                this.canvas.width = image.width;
                this.canvas.height = image.height;
                this.ctx.drawImage(image, 0, 0);
            };
            image.src = imageData;
        },
        renderVideo(videoFile) {
            this.clearCanvas();
            const video = this.$refs.videoPlayer;
            video.src = URL.createObjectURL(videoFile);
            video.onloadedmetadata = () => {
                this.canvas.width = video.videoWidth;
                this.canvas.height = video.videoHeight;
                video.play();
                const drawFrame = () => {
                    this.ctx.drawImage(video, 0, 0);
                    requestAnimationFrame(drawFrame);
                };
                drawFrame();
            };
        },
        stopVideo() {
            const video = this.$refs.videoPlayer;
            video.pause();
            video.src = '';
            if (this.videoStream) {
                const tracks = this.videoStream.getTracks();
                tracks.forEach(track => track.stop());
                this.videoStream = null;
            }
            this.clearCanvas();
        },
        clearCanvas() {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }
};
</script>

<style scoped>
.canvas-container {
    width: 50%;
    height: 100%;
}

canvas {
    width: 100%;
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
</style>

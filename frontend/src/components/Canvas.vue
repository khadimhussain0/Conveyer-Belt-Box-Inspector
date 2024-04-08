<template>
    <div class="canvas-container">
        <canvas ref="canvas"></canvas>
    </div>
</template>

<script>
export default {
    data() {
        return {
            canvas: null,
            ctx: null
        };
    },
    mounted() {
        this.canvas = this.$refs.canvas;
        this.ctx = this.canvas.getContext('2d');
    },
    methods: {
        renderImage(imageData) {
            const image = new Image();
            image.onload = () => {
                this.canvas.width = image.width;
                this.canvas.height = image.height;
                this.ctx.drawImage(image, 0, 0);
            };
            image.src = imageData;
        },
        renderVideo(videoStream) {
            const video = document.createElement('video');
            video.srcObject = videoStream;
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
</style>

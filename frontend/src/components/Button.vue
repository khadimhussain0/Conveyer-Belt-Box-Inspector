<template>
    <div>
        <button @click="toggleLineInspector"
            :class="{ 'btn-start': !lineInspectorStarted, 'btn-stop': lineInspectorStarted }">
            {{ lineInspectorStarted ? 'Stop Line Inspector' : 'Start Line Inspector' }}
        </button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            lineInspectorStarted: false
        };
    },
    methods: {
        toggleLineInspector() {
            this.lineInspectorStarted = !this.lineInspectorStarted;
            if (this.lineInspectorStarted) {
                // Start line inspector functionality
                this.$emit('start-line-inspector');
            } else {
                // Stop line inspector functionality
                this.$emit('stop-line-inspector');
            }
        }
    }
};
</script>

<style scoped>
.btn-start {
    background-color: green;
    color: white;
}

.btn-stop {
    background-color: red;
    color: white;
}

button {
    padding: 10px 20px;
    cursor: pointer;
    border: none;
    border-radius: 5px;
    font-size: 16px;
}
</style>

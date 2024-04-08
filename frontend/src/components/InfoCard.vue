<template>
    <div class="info-card">
        <h2>{{ title }}</h2>
        <p>{{ content }}</p>
    </div>
</template>

<script>
export default {
    props: ['title', 'content']
};
</script>

<style scoped>
.info-card {
    background-color: #f0f0f0;
    padding: 10px;
    margin-bottom: 10px;
}
</style>

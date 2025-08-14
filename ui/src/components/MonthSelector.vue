<template>
    <select v-model="model" @change="onMonthSelected">
        <option v-for="monthNumber in months" :value="monthNumber">{{ monthNumber }}</option>
    </select>
</template>


<script setup>

import { ref, defineModel } from 'vue';

const emit = defineEmits(['onMonthSelected'])

const currentTime = new Date()
const currentMonth = currentTime.getMonth() + 1
const months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

const model = defineModel()
model.value = model.value || currentMonth

function onMonthSelected(e) {
    emit('onMonthSelected', model.value)
}

</script>
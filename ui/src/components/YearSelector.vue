<template>
    <select v-model="model" @change="onYearSelected">
        <option v-for="year in years" :value="year">{{ year }}</option>
    </select>
</template>


<script setup>

import {ref, defineModel} from 'vue'

const emit = defineEmits(['yearSelected'])

const currentTime = new Date()
const currentYear = currentTime.getFullYear()
const years = [0, 1].map(delta => currentYear + delta)

const model = defineModel()
model.value = model.value || currentYear

function onYearSelected(event) {
    emit('yearSelected', model.value)
}


</script>
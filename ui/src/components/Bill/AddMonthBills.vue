<template>
    <h1>Adicionar Contas do Mês</h1>
    <form>
        <ul>
            <li>Mês:
                <MonthSelector v-model="selectedMonth" />
            </li>
            <li>Ano:
                <YearSelector v-model="selectedYear" />
            </li>

        </ul>
        <button type="button" @click="buttonCreateClick">Criar</button>
    </form>

</template>


<script setup>

import { ref } from 'vue';
import MonthSelector from '@/components/MonthSelector.vue';
import YearSelector from '../YearSelector.vue';

const emit = defineEmits(['createButtonClicked'])

const selectedMonth = ref()
const selectedYear = ref()


function buttonCreateClick(e) {
    emit('createButtonClicked', selectedMonth.value, selectedYear.value)
}

</script>
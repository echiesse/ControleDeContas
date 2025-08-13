<template>
    <h1>Nova Conta</h1>
    <form>
        <ul>
            <li>Tipo:
                <select v-model="typeId">
                    <option v-for="type in types" :value="type.id">{{ type.name }}</option>
                </select>
            </li>
            <li>Mês:
                <select v-model="selectedMonth">
                    <option v-for="monthNumber in months" :value="monthNumber">{{ monthNumber }}</option>
                </select>
            </li>
            <li>Ano:
                <select v-model="selectedYear">
                    <option v-for="year in years" :value="year">{{ year }}</option>
                </select>
            </li>
        </ul>
        <button type="button" @click="addBillClick">Criar</button>
    </form>

</template>



<script setup>
import {ref, onMounted, watch} from 'vue'
import { post } from '@/support/http'
import { now } from '@/support/datetime'

const emit = defineEmits(['billAdded'])

const typeId = ref()
const types = ref([])

const currentTime = now()
const currentMonth = currentTime.getMonth() + 1
const months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
const selectedMonth = ref(currentMonth)

const currentYear = currentTime.getFullYear()
const years = [0, 1].map(delta => currentYear + delta)
const selectedYear = ref(currentYear)


onMounted (async() => {
    types.value = await fetchTypes()
})


const typeListUrl = '/api/bill-control/bill-types/'
const createBillUrl = '/api/bill-control/bills/create/'


async function fetchTypes() {
    const response = await fetch (typeListUrl);
    const types = {}
    const type_list = await response.json()
    for (const type of type_list) {
        types[type.id] = type
    }
    return types
}

async function addBillClick(event) {
    const billData = {
        type: typeId.value,
        month: selectedMonth.value,
        year: selectedYear.value,
    }
    const contents = await post(createBillUrl, {data: billData})

    emit('billAdded', contents)
}


</script>
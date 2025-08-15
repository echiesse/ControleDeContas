<template>
    <tr :id="formattedBill.id">
        <td>{{ formattedBill.name }}</td>
        <td>{{ formattedBill.due_date }}</td>
        <td :class="paidClass" >
            <input type="checkbox" @change="onBillPaidChange" v-model="billPaid">
            <span @click="onPaidDateClick">{{ formattedBill.paid_date }}</span>
            <input type="date" @blur="onBillPaidDateChange" v-model="newPaidDate" v-show="isDateInputVisible"/>
        </td>
    </tr>
</template>


<script setup>

import { ref, defineProps, computed } from 'vue'
import { formatDateToSend } from '@/support/formatters'
import { put } from '@/support/http'
import { newDateFromLocalDateStr, now } from '@/support/datetime'

const props = defineProps({
    bill: Object
})

const emit = defineEmits(['billUpdated'])


const billPaid = ref()
billPaid.value = props.bill.paid_date != null
const newPaidDate = ref(props.bill.paid_date && formatDateToSend(props.bill.paid_date))
const formattedBill = computed(() => formatBill(props.bill))
const paidClass = computed(() => props.bill.paid_date == null ? 'unpaid' : 'paid')

const paidDate = computed(() => newDateFromLocalDateStr(newPaidDate.value))

const isDateInputVisible = ref(false)


function formatDate(d) {
    if (d == null) return null
    return d.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
    })
}


function formatBill(bill) {
    return {
        ...bill,
        due_date: formatDate(bill.due_date),
        paid_date: bill.paid_date && formatDate(bill.paid_date)
    }
}

function formatBillToSend(bill) {
    return {
        ...bill,
        due_date: formatDateToSend(bill.due_date),
        paid_date: bill.paid_date && formatDateToSend(bill.paid_date)
    }
}

const updateBillUrl = '/api/bill-control/bill'


async function updateBill(bill) {
    return await put(`${updateBillUrl}/${bill.id}/`, {data: formatBillToSend(bill)})
}


async function onBillPaidChange(e) {
    const paidDate = billPaid.value ? now() : null
    console.log(`Paid Date ${paidDate}`); //<<<<<
    const bill = {...props.bill, paid_date: paidDate}
    await updateBill(bill)
    emit('billUpdated')
}

async function onBillPaidDateChange(e) {
    console.log(`onBillPaidDateChangee ${paidDate.value}`); //<<<<<
    isDateInputVisible.value = false
    const bill = {...props.bill, paid_date: paidDate.value}
    await updateBill(bill)
    emit('billUpdated')
}


function onPaidDateClick(e) {
    isDateInputVisible.value = !isDateInputVisible.value
    if (isDateInputVisible.value == true) {
        newPaidDate.value = props.bill.paid_date && formatDateToSend(props.bill.paid_date)
    }
}

</script>


<style scoped>

table td, table th {
    border: solid;
    border-collapse: collapse;
    border-color: silver;
    border-width: 1px;
}

table td, table th {
    text-align: left;
}

.unpaid {
    background-color: rgb(255, 150, 150);
}
.paid {
    background-color: rgb(154, 226, 154);
}
</style>
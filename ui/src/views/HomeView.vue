<template>
  <main>
    <div class="container">
        <BillTable
            v-for="month in billMonths"
            :title="`Contas de ${monthStr(month)}`"
            :bills="billsPerMonth[month]"
            @billUpdated="billUpdated"
        />
        <AddMonthBills @createButtonClicked="createMonthBills"/>
    </div>
  </main>
</template>


<script setup>
import {ref, onMounted} from 'vue'
import BillTable from '@/components/Bill/BillTable/BillTable.vue'
import AddBill from '@/components/Bill/AddBill.vue'
import AddMonthBills from '@/components/Bill/AddMonthBills.vue'
import { newDateFromLocalDateStr } from '@/support/datetime'

//------------------------------------------------------------------------------
// Data:
const bills = ref([])
const billsPerMonth = ref({})
const billMonths = ref([])


//------------------------------------------------------------------------------
// Hooks:
onMounted (async() => await updateBillsFromBackEnd())


//------------------------------------------------------------------------------
// Functions:
async function updateBillsFromBackEnd() {
    let _bills = await fetchBills()
    bills.value = sortBills(_bills)
    billMonths.value = []
    billsPerMonth.value = {}
    for (const bill of _bills) {
        if (! billsPerMonth.value[bill.due_date.getMonth()]) {
            billMonths.value.push(bill.due_date.getMonth())
            billsPerMonth.value[bill.due_date.getMonth()] = []
        }
        billsPerMonth.value[bill.due_date.getMonth()].push(bill)
    }
}

async function billAdded(bill) {
    if (typeof bill.error != 'undefined') {
        return null
    }
    bill = normalizeBill(bill)
    bills.value.push(bill)
    sortBills(bills.value)
}

async function billUpdated(bill) {
    await updateBillsFromBackEnd()
}


async function createMonthBills(month, year) {
    const createdBills = await post(createMonthBillsUrl, {data: {month: month, year: year}})
    console.log(createdBills); //<<<<<
    for (const bill of createdBills.data) {
        console.log(bill)
        bills.value.push(bill)
        sortBills(bills.value)
    }
}

</script>


<script>
import { post } from '@/support/http'
const billListUrl = '/api/bill-control/bills/'
const createMonthBillsUrl = '/api/bill-control/bills/create-for-month/'

function sortBills(bills) {
    return bills.sort((b1, b2) => b1.due_date - b2.due_date)
}

function normalizeBill(bill) {
    return {
        ...bill,
        due_date: newDateFromLocalDateStr(bill.due_date),
        paid_date: bill.paid_date && newDateFromLocalDateStr(bill.paid_date)
    }
}

async function fetchBills() {
    const response = await fetch(billListUrl)
    let bills = await response.json()
    bills = bills.map(normalizeBill)
    return bills
}

function monthStr(month){
    const date = new Date()
    date.setDate(15) // Just to be in the middle of the month
    date.setMonth(month)
    return date.toLocaleString('default', { month: 'long' });
}

</script>

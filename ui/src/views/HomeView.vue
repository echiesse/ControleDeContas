
<template>
  <main>
    <BillTable
        v-for="month in billMonths"
        :title="`Contas ${month+1}`"
        :bills="billsPerMonth[month]"
        @billUpdated="billUpdated"
    />
    <AddBill @billAdded="billAdded" />
    <AddMonthBills @createButtonClicked="createMonthBills"/>
  </main>
</template>


<script setup>
import {ref, onMounted} from 'vue'
import BillTable from '@/components/Bill/BillTable/BillTable.vue'
import AddBill from '@/components/Bill/AddBill.vue'
import AddMonthBills from '@/components/Bill/AddMonthBills.vue'
import { newDateFromLocalDateStr } from '@/support/datetime'


const bills = ref([])
const billsPerMonth = ref({})
const billMonths = ref([])

onMounted (async() => await updateBillsFromBackEnd())

async function updateBillsFromBackEnd() {
    let _bills = await fetchBills()
    bills.value = sortBills(_bills)
    for (const bill of _bills) {
        if (! billsPerMonth.value[bill.due_date.getMonth()]) {
            billMonths.value.push(bill.due_date.getMonth())
            billsPerMonth.value[bill.due_date.getMonth()] = []
        }
        billsPerMonth.value[bill.due_date.getMonth()].push(bill)
    }
    console.log(billMonths.value); //<<<<<
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
    console.log('Created Bills:'); //<<<<<
    console.log(createdBills); //<<<<<

    for (const bill of createdBills) {
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
    console.log(bills); //<<<<<
    return bills
}

</script>

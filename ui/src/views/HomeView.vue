
<template>
  <main>
    <BillTable :bills = "bills" @billUpdated="billUpdated"/>
    <AddBill @billAdded="billAdded" />
  </main>
</template>


<script setup>
import {ref, onMounted} from 'vue'
import BillTable from '@/components/BillTable/BillTable.vue'
import AddBill from '@/components/AddBill.vue'
import { newDateFromLocalDateStr as newDateFromLocalDateStr, newUTCDateFromStr } from '@/support/datetime'

async function updateBillsFromBackEnd() {
    let _bills = await fetchBills()
    _bills = _bills.sort((b1, b2) => b1.due_date - b2.due_date)
    bills.value = _bills
}


const bills = ref([])
onMounted (async() => await updateBillsFromBackEnd())

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

</script>


<script>
const billListUrl = '/api/bill-control/bills/'

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

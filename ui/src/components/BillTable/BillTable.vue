<template>
    <h1>Contas</h1>
    <table class="table">
        <thead>
            <tr>
                <th>Conta</th>
                <th>Vencimento</th>
                <th>Pago</th>
            </tr>
        </thead>
        <tbody>
            <tr v-if="bills.length == 0" >
                <td colspan="3"> <span style="font-style: italic;">Não há contas registradas</span> </td>
            </tr>
            <BillTableRow v-else v-for="bill in bills" :bill="bill" @billUpdated="$emit('billUpdated')" />
        </tbody>
    </table>
</template>


<script setup>

import BillTableRow from './BillTableRow.vue'

const props = defineProps({
    bills: Array
})

const emit = defineEmits(['billUpdated'])

</script>


<style scoped>
table, table td, table th {
    border: solid;
    border-collapse: collapse;
    border-color: silver;
    border-width: 1px;
}

table td, table th {
    text-align: left;
}

</style>
<template>
    <h1>{{title}}</h1>
    <table class="table table-bordered">
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
    bills: Array,
    title: String,
})

const emit = defineEmits(['billUpdated'])

</script>


<style scoped>

</style>
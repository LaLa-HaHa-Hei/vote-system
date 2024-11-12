<template>
    <header>投票结果</header>
    <main>
        <table border="1px solid #ccc" cellspacing="0" cellpadding="0">
            <thead>
                <tr>
                    <th>id</th>
                    <th>票数</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in voteResults" :key="index">
                    <td>{{ item.id }}</td>
                    <td>{{ item.votes }}</td>
                </tr>
            </tbody>
        </table>
    </main>
</template>

<script setup>
import axios from 'axios'
import { ref, onBeforeMount } from 'vue'

const voteResults = ref([])

onBeforeMount(async () => {
    const { data } = await axios.get('/api/get-vote-results')
    voteResults.value = data.voteResults
})
</script>

<style scoped></style>
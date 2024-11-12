<template>
    <header>投票结果</header>
    <main style="width: 100%; height: 500px;">
    </main>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'

// [{ id: '1', votes: 10 }, { id: '2', votes: 20 }, { id: '3', votes: 30 }]
const voteResults = ref([])

onMounted(async () => {
    await nextTick()
    const { data } = await axios.get('/api/get-vote-results')
    voteResults.value = data.voteResults
    var chartDom = document.querySelector('main');
    var myChart = echarts.init(chartDom);
    var option;

    option = {
        xAxis: {
            type: 'category',
            data: voteResults.value.map(item => item.id)
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                data: voteResults.value.map(item => item.votes),
                type: 'bar'
            }
        ]
    };
    option && myChart.setOption(option);
})
</script>

<style scoped>
header {
    text-align: center;
    font-size: 24px;
    margin: 20px 0;
}
</style>
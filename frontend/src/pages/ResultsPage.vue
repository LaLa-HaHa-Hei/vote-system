<template>
    <header>投票结果</header>
    <main>
        <div class="echarts" style="width: 100%; height: 500px;"></div>
        <p>获票排名如下：</p>
        <ul class="score">
            <li v-for="(item, index) in sortedVoteResults" :key="item.id">
                {{ item.id }} - {{ 100 - index }} 分
            </li>
        </ul>
    </main>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, nextTick, onBeforeMount } from 'vue'
import * as echarts from 'echarts/core';
import { GridComponent } from 'echarts/components';
import { BarChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';
import { useRouter } from 'vue-router';

echarts.use([GridComponent, BarChart, CanvasRenderer]);

const router = useRouter();

const voteResults = ref([])
const sortedVoteResults = ref([])

onBeforeMount(async () => {
    const response = await axios.post('/api/does-have-voted', {
        md5Fingerprint: window.md5Fingerprint
    })
    if(!response.data.hasVoted)
    {
        alert('请先投票')
        router.push('/')
    }
})

onMounted(async () => {
    await nextTick()
    const { data } = await axios.get('/api/get-vote-results')
    voteResults.value = data.voteResults

    sortedVoteResults.value = voteResults.value.sort((a, b) => b.votes - a.votes)

    var chartDom = document.querySelector('.echarts');
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
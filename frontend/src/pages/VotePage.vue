<template>
    <header>
        <h1>请投票</h1>
        <p>每人2票</p>
        <button @click="router.push('/results')" style="color: red;">查看结果</button>
    </header>
    <main>
        <template v-for="item in voteItems" :key="item.id">
            <div class="vote-item">
                <input type="checkbox" v-model="selectedItems[item.id]" @change="checkVote(item.id)">
                <span>{{ item.name }}</span>
                <div style="flex: 1;"></div>
                <img :src="item.image" alt="">
            </div>
        </template>
    </main>
    <footer>
        <button @click="submit">提交</button>
    </footer>
</template>

<script setup>
import axios from 'axios'
import { ref, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router';

const router = useRouter();
const voteItems = ref([])
const selectedItems = ref({})

onBeforeMount(async () => {
    const { data } = await axios.get('/api/get-vote-items')
    voteItems.value = data.voteItems
})

function checkVote(id) {
    const selectedCount = Object.values(selectedItems.value).filter(Boolean).length
    if (selectedCount > 2) {
        alert('每人最多只能投2票！')
        // 取消最后一个选中的项
        const lastSelected = Object.keys(selectedItems.value).reverse().find(key => selectedItems.value[key])
        selectedItems.value[lastSelected] = false
    }
}

async function submit() {
    // console.log(selectedItems.value)
    const { data } = await axios.post('/api/submit-vote-result', { 
        md5Fingerprint: window.md5Fingerprint, 
        selectedItems: selectedItems.value
    })
    if (data.success) {
        alert('投票成功！')
    }
    else{
        alert(`投票失败！ error: ${data.error}`)
    }
}
</script>

<style scoped>
header {
    text-align: center;
}

main {
    margin-top: 20px;
    padding-left: 10%;
    padding-right: 10%;
    padding-bottom: 65px;
}

.vote-item {
    display: flex;
    align-items: center;
    margin: 10px;
    border: 1px solid #ccc;
    padding: 10px;
}

.vote-item img {
    height: 200px;
}

footer {
    background-color: #ccc;
    position: fixed;
    display: flex;
    width: 100%;
    height: 60px;
    bottom: 0;
    left: 0;
    justify-content: center;
    align-items: center;
}

footer button {
    width: 100px;
    height: 35px;
    background-color: #1ea0fa;
    color: white;
    border: none;
    border-radius: 7px;
    margin: 10px;
}
</style>
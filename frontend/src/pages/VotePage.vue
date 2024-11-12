<template>
    <header>
        <h1>笔尖笃志，流墨生辉</h1>
        <p>每人做多可投 {{ votesNum }} 票</p>
        <button @click="router.push('/results')" style="color: red;">查看结果</button>
    </header>
    <main>
        <template v-for="item in voteItems" :key="item.id">
            <div class="vote-item">
                <img :src="item.image" alt="">
                <input type="checkbox" v-model="selectedItems[item.id]" @change="checkVote(item.id)">
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
const votesNum = ref(10)

onBeforeMount(async () => {
    voteItems.value = [
        {
            "id": 1,
            "image": "./vote-item-img/1.png"
        },
        {
            "id": 2,
            "image": "./vote-item-img/2.png"
        },
        {
            "id": 3,
            "image": "./vote-item-img/3.png"
        },
        {
            "id": 4,
            "image": "./vote-item-img/4.png"
        },
        {
            "id": 5,
            "image": "./vote-item-img/5.png"
        },
        {
            "id": 6,
            "image": "./vote-item-img/6.png"
        },
        {
            "id": 7,
            "image": "./vote-item-img/7.png"
        },
        {
            "id": 8,
            "image": "./vote-item-img/8.png"
        },
        {
            "id": 9,
            "image": "./vote-item-img/9.png"
        },
        {
            "id": 10,
            "image": "./vote-item-img/10.png"
        },
        {
            "id": 11,
            "image": "./vote-item-img/11.png"
        },
        {
            "id": 12,
            "image": "./vote-item-img/12.png"
        },
        {
            "id": 13,
            "image": "./vote-item-img/13.png"
        },
        {
            "id": 14,
            "image": "./vote-item-img/14.png"
        },
        {
            "id": 15,
            "image": "./vote-item-img/15.png"
        },
        {
            "id": 16,
            "image": "./vote-item-img/16.png"
        }]
    // const { data } = await axios.get('/api/get-vote-items')
    // voteItems.value = data.voteItems
})

function checkVote(id) {
    const selectedCount = Object.values(selectedItems.value).filter(Boolean).length
    if (selectedCount > votesNum.value) {
        alert(`每人最多只能投${votesNum.value}票！`)
        // 取消最后一个选中的项
        selectedItems.value[id] = false
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
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    grid-gap: 15px;
}

.vote-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 10px;
    border: 1px solid #ccc;
    padding: 10px;
}

.vote-item img {
    height: 200px;
    width: 200px;
}

.vote-item input[type="checkbox"] {
    margin-top: 15px;
    width: 20px;
    height: 20px;
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
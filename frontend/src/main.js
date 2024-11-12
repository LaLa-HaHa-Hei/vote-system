import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import CryptoJS from 'crypto-js'
import axios from 'axios'

const app = createApp(App)

// 调用函数获取指纹字符串
const fingerprint = getCanvasFingerprint()
window.md5Fingerprint = CryptoJS.MD5(fingerprint).toString()

app.use(router)

app.mount('#app')

function getCanvasFingerprint() {
    // 创建一个 canvas 元素
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    // 设置 canvas 的宽度和高度
    canvas.width = 200;
    canvas.height = 100;

    // 绘制一些内容到 canvas 上
    ctx.font = '16px Arial';
    ctx.fillStyle = '#f44336';
    ctx.fillRect(0, 0, 100, 50);
    ctx.fillStyle = '#2196f3';
    ctx.fillText('Canvas Fingerprint', 10, 40);

    // 获取 canvas 的像素数据
    const dataURL = canvas.toDataURL();

    // 将 dataURL 转换为 base64 字符串
    const base64String = dataURL.replace(/^data:image\/(png|jpg);base64,/, '');

    // 将 base64 字符串转换为二进制数据
    const binaryString = atob(base64String);

    // 将二进制数据转换为十六进制字符串
    let hexString = '';
    for (let i = 0; i < binaryString.length; i++) {
        const hex = binaryString.charCodeAt(i).toString(16);
        hexString += (hex.length === 1 ? '0' : '') + hex;
    }

    // 返回十六进制字符串作为指纹
    return hexString;
}
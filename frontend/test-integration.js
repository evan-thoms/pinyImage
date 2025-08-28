// Test script to verify frontend-backend integration
const axios = require('axios');

const API_BASE = 'https://pinyimage-backend.onrender.com';

async function testIntegration() {
    console.log('🧪 Testing Frontend-Backend Integration');
    console.log('=====================================');
    
    try {
        // Test 1: Health Check
        console.log('\n1. Testing Health Check...');
        const health = await axios.get(`${API_BASE}/api/health`);
        console.log('✅ Health Check:', health.data.status);
        
        // Test 2: Status Check
        console.log('\n2. Testing Status Check...');
        const status = await axios.get(`${API_BASE}/api/status`);
        console.log('✅ Status Check:', status.data.database, '| AI:', status.data.ai_available);
        
        // Test 3: Get Cards
        console.log('\n3. Testing Get Cards...');
        const cards = await axios.get(`${API_BASE}/api/cards`);
        console.log('✅ Get Cards:', cards.data.length, 'cards found');
        
        // Test 4: Character Analysis
        console.log('\n4. Testing Character Analysis...');
        const analysis = await axios.post(`${API_BASE}/api/result`, {
            user_input: '水'
        });
        console.log('✅ Character Analysis:', analysis.data.pinyin, '-', analysis.data.meaning);
        
        // Test 5: Add Card
        console.log('\n5. Testing Add Card...');
        const newCard = await axios.post(`${API_BASE}/api/post`, {
            title: '测试',
            pinyin: 'cè shì',
            meaning: 'test',
            con: 'This is a test connection'
        });
        console.log('✅ Add Card:', newCard.data.status);
        
        console.log('\n🎉 All tests passed! Frontend-Backend integration is working.');
        
    } catch (error) {
        console.error('❌ Test failed:', error.message);
        if (error.response) {
            console.error('Response:', error.response.data);
        }
    }
}

testIntegration();

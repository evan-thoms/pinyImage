// Test script to verify authentication integration
const axios = require('axios');

const API_BASE = 'https://pinyimage-backend.onrender.com';

async function testAuthIntegration() {
    console.log('🧪 Testing Authentication Integration');
    console.log('=====================================');
    
    try {
        // Test 1: Check if auth endpoints exist
        console.log('\n1. Testing Authentication Endpoints...');
        
        // Try to access register endpoint
        try {
            const registerResponse = await axios.post(`${API_BASE}/api/register`, {
                username: 'testuser',
                email: 'test@example.com',
                password: 'testpass123'
            });
            console.log('✅ Register endpoint working');
        } catch (error) {
            if (error.response && error.response.status === 405) {
                console.log('❌ Register endpoint not found (405 Method Not Allowed)');
            } else {
                console.log('⚠️ Register endpoint error:', error.response?.status, error.response?.data);
            }
        }
        
        // Try to access login endpoint
        try {
            const loginResponse = await axios.post(`${API_BASE}/api/login`, {
                username: 'testuser',
                password: 'testpass123'
            });
            console.log('✅ Login endpoint working');
        } catch (error) {
            if (error.response && error.response.status === 405) {
                console.log('❌ Login endpoint not found (405 Method Not Allowed)');
            } else {
                console.log('⚠️ Login endpoint error:', error.response?.status, error.response?.data);
            }
        }
        
        // Test 2: Check existing endpoints still work
        console.log('\n2. Testing Existing Endpoints...');
        
        const health = await axios.get(`${API_BASE}/api/health`);
        console.log('✅ Health endpoint working');
        
        const status = await axios.get(`${API_BASE}/api/status`);
        console.log('✅ Status endpoint working');
        
        const cards = await axios.get(`${API_BASE}/api/cards`);
        console.log('✅ Cards endpoint working');
        
        console.log('\n📋 Summary:');
        console.log('- Backend is running and healthy');
        console.log('- Core endpoints are working');
        console.log('- Authentication endpoints may need deployment time or have issues');
        
    } catch (error) {
        console.error('❌ Test failed:', error.message);
    }
}

testAuthIntegration();

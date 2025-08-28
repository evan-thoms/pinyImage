// Frontend Authentication Test
// Run this in browser console to test the authentication flow

console.log('🧪 Frontend Authentication Test');
console.log('=' * 40);

// Test 1: Check if user is authenticated
function testAuthentication() {
    console.log('1. Testing authentication state...');
    
    // Check if user is signed in
    const isSignedIn = window.Clerk && window.Clerk.user;
    console.log(`   Signed in: ${isSignedIn}`);
    
    if (isSignedIn) {
        console.log(`   User: ${window.Clerk.user.emailAddresses[0]?.emailAddress}`);
        console.log(`   User ID: ${window.Clerk.user.id}`);
    }
    
    return isSignedIn;
}

// Test 2: Check axios headers
function testAxiosHeaders() {
    console.log('\n2. Testing axios headers...');
    
    const headers = window.axios?.defaults?.headers?.common;
    console.log('   Headers:', headers);
    
    if (headers) {
        console.log(`   Authorization: ${headers.Authorization ? 'Set' : 'Not set'}`);
        console.log(`   X-User-Email: ${headers['X-User-Email'] || 'Not set'}`);
        console.log(`   X-User-ID: ${headers['X-User-ID'] || 'Not set'}`);
    }
    
    return headers;
}

// Test 3: Test API calls
async function testAPICalls() {
    console.log('\n3. Testing API calls...');
    
    try {
        // Test cards endpoint
        const cardsResponse = await fetch('/api/cards', {
            headers: {
                'Authorization': window.axios?.defaults?.headers?.common?.Authorization,
                'X-User-Email': window.axios?.defaults?.headers?.common?.['X-User-Email'],
                'X-User-ID': window.axios?.defaults?.headers?.common?.['X-User-ID']
            }
        });
        
        console.log(`   Cards endpoint: ${cardsResponse.status}`);
        
        if (cardsResponse.ok) {
            const cards = await cardsResponse.json();
            console.log(`   Retrieved ${cards.length} cards`);
        } else {
            console.log(`   Error: ${await cardsResponse.text()}`);
        }
        
    } catch (error) {
        console.log(`   Error: ${error.message}`);
    }
}

// Test 4: Check React state
function testReactState() {
    console.log('\n4. Testing React state...');
    
    // Try to access React component state
    const appElement = document.querySelector('.App');
    console.log('   App element found:', !!appElement);
    
    // Check if cards are displayed
    const cards = document.querySelectorAll('.cards');
    console.log(`   Cards displayed: ${cards.length}`);
    
    return cards.length;
}

// Run all tests
async function runAllTests() {
    console.log('🧪 Running Frontend Authentication Tests...\n');
    
    const authResult = testAuthentication();
    const headersResult = testAxiosHeaders();
    await testAPICalls();
    const stateResult = testReactState();
    
    console.log('\n📊 Test Results:');
    console.log(`   Authentication: ${authResult ? '✅' : '❌'}`);
    console.log(`   Headers: ${headersResult ? '✅' : '❌'}`);
    console.log(`   Cards displayed: ${stateResult}`);
    
    if (authResult && headersResult && stateResult > 0) {
        console.log('\n🎉 All tests passed!');
    } else {
        console.log('\n⚠️ Some tests failed. Check the details above.');
    }
}

// Export for manual testing
window.testFrontendAuth = runAllTests;
console.log('Run testFrontendAuth() to execute all tests');

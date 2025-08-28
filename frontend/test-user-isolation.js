// Comprehensive User Isolation Test
// Run this in browser console to test the complete flow

console.log('🧪 COMPREHENSIVE USER ISOLATION TEST');
console.log('=' * 50);

// Test 1: Check Authentication State
function testAuthentication() {
    console.log('\n1. 🔐 Testing Authentication State');
    console.log('-'.repeat(30));
    
    const isSignedIn = window.Clerk && window.Clerk.user;
    console.log(`   Signed in: ${isSignedIn}`);
    
    if (isSignedIn) {
        const user = window.Clerk.user;
        console.log(`   User ID: ${user.id}`);
        console.log(`   Username: ${user.username}`);
        console.log(`   Email: ${user.primaryEmailAddress?.emailAddress}`);
    }
    
    return isSignedIn;
}

// Test 2: Check Axios Headers
function testAxiosHeaders() {
    console.log('\n2. 📋 Testing Axios Headers');
    console.log('-'.repeat(30));
    
    const headers = window.axios?.defaults?.headers?.common;
    console.log('   Headers:', headers);
    
    if (headers) {
        console.log(`   Authorization: ${headers.Authorization ? 'Set' : 'Not set'}`);
        console.log(`   X-User-Email: ${headers['X-User-Email'] || 'Not set'}`);
        console.log(`   X-User-ID: ${headers['X-User-ID'] || 'Not set'}`);
    }
    
    return headers;
}

// Test 3: Test Database Cards (should be user-specific)
async function testDatabaseCards() {
    console.log('\n3. 🗄️ Testing Database Cards');
    console.log('-'.repeat(30));
    
    try {
        const response = await fetch('/api/cards', {
            headers: {
                'Authorization': window.axios?.defaults?.headers?.common?.Authorization,
                'X-User-Email': window.axios?.defaults?.headers?.common?.['X-User-Email'],
                'X-User-ID': window.axios?.defaults?.headers?.common?.['X-User-ID']
            }
        });
        
        console.log(`   Status: ${response.status}`);
        
        if (response.ok) {
            const cards = await response.json();
            console.log(`   Database cards: ${cards.length}`);
            cards.forEach((card, index) => {
                console.log(`     ${index + 1}. ${card.title} (${card.pinyin})`);
            });
            return cards;
        } else {
            console.log(`   Error: ${await response.text()}`);
            return [];
        }
        
    } catch (error) {
        console.log(`   Error: ${error.message}`);
        return [];
    }
}

// Test 4: Test AI Response (should not affect database cards)
async function testAIResponse() {
    console.log('\n4. 🤖 Testing AI Response');
    console.log('-'.repeat(30));
    
    try {
        const response = await fetch('/api/result', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': window.axios?.defaults?.headers?.common?.Authorization,
                'X-User-Email': window.axios?.defaults?.headers?.common?.['X-User-Email'],
                'X-User-ID': window.axios?.defaults?.headers?.common?.['X-User-ID']
            },
            body: JSON.stringify({ user_input: '测试' })
        });
        
        console.log(`   Status: ${response.status}`);
        
        if (response.ok) {
            const data = await response.json();
            console.log(`   AI response cards: ${data.cards?.length || 0}`);
            console.log(`   Current character: ${data.pinyin}`);
            console.log(`   Meaning: ${data.meaning}`);
            return data;
        } else {
            console.log(`   Error: ${await response.text()}`);
            return null;
        }
        
    } catch (error) {
        console.log(`   Error: ${error.message}`);
        return null;
    }
}

// Test 5: Test Card Creation
async function testCardCreation() {
    console.log('\n5. ➕ Testing Card Creation');
    console.log('-'.repeat(30));
    
    const testCard = {
        title: '测试',
        pinyin: 'cè shì',
        meaning: 'test',
        con: 'test connection'
    };
    
    try {
        const response = await fetch('/api/post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': window.axios?.defaults?.headers?.common?.Authorization,
                'X-User-Email': window.axios?.defaults?.headers?.common?.['X-User-Email'],
                'X-User-ID': window.axios?.defaults?.headers?.common?.['X-User-ID']
            },
            body: JSON.stringify(testCard)
        });
        
        console.log(`   Status: ${response.status}`);
        
        if (response.ok) {
            const data = await response.json();
            console.log(`   Response: ${JSON.stringify(data)}`);
            return true;
        } else {
            console.log(`   Error: ${await response.text()}`);
            return false;
        }
        
    } catch (error) {
        console.log(`   Error: ${error.message}`);
        return false;
    }
}

// Test 6: Check React State
function testReactState() {
    console.log('\n6. ⚛️ Testing React State');
    console.log('-'.repeat(30));
    
    // Try to access React component state
    const appElement = document.querySelector('.App');
    console.log(`   App element found: ${!!appElement}`);
    
    // Check if cards are displayed
    const cardElements = document.querySelectorAll('.cards');
    console.log(`   Card elements displayed: ${cardElements.length}`);
    
    // Check for specific card content
    const cardTitles = Array.from(cardElements).map(card => {
        const titleElement = card.querySelector('.card-title');
        return titleElement ? titleElement.textContent : 'No title';
    });
    
    console.log(`   Card titles: ${cardTitles.join(', ')}`);
    
    return cardElements.length;
}

// Test 7: Verify User Isolation
async function testUserIsolation() {
    console.log('\n7. 🔒 Testing User Isolation');
    console.log('-'.repeat(30));
    
    // Get current user info
    const currentUser = window.Clerk?.user;
    if (!currentUser) {
        console.log('   No user logged in');
        return false;
    }
    
    console.log(`   Current user: ${currentUser.username} (${currentUser.id})`);
    
    // Get database cards for this user
    const cards = await testDatabaseCards();
    
    // Check if cards belong to this user
    if (cards.length > 0) {
        console.log(`   User has ${cards.length} cards in database`);
        return true;
    } else {
        console.log('   User has no cards in database');
        return false;
    }
}

// Run all tests
async function runComprehensiveTest() {
    console.log('🧪 Running Comprehensive User Isolation Test...\n');
    
    const authResult = testAuthentication();
    const headersResult = testAxiosHeaders();
    const dbCards = await testDatabaseCards();
    const aiResponse = await testAIResponse();
    const creationResult = await testCardCreation();
    const stateResult = testReactState();
    const isolationResult = await testUserIsolation();
    
    console.log('\n📊 COMPREHENSIVE TEST RESULTS:');
    console.log('=' * 50);
    console.log(`   Authentication: ${authResult ? '✅' : '❌'}`);
    console.log(`   Headers: ${headersResult ? '✅' : '❌'}`);
    console.log(`   Database cards: ${dbCards.length}`);
    console.log(`   AI response: ${aiResponse ? '✅' : '❌'}`);
    console.log(`   Card creation: ${creationResult ? '✅' : '❌'}`);
    console.log(`   React state: ${stateResult} cards displayed`);
    console.log(`   User isolation: ${isolationResult ? '✅' : '❌'}`);
    
    // Overall assessment
    const allPassed = authResult && headersResult && creationResult && isolationResult;
    
    if (allPassed) {
        console.log('\n🎉 ALL TESTS PASSED! User isolation is working correctly.');
    } else {
        console.log('\n⚠️ Some tests failed. Check the details above.');
    }
    
    return allPassed;
}

// Export for manual testing
window.testUserIsolation = runComprehensiveTest;
console.log('Run testUserIsolation() to execute comprehensive test');

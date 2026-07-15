/* ==========================================================================
   🧠 VoyageAI Core Interactive Logic & API Integrations (app.js)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // --- 🧭 DOM Selections ---
    const plannerForm = document.getElementById('travel-planner-form');
    const chatFeed = document.getElementById('chat-feed');
    const chatInputForm = document.getElementById('chat-input-form');
    const inputCustomQuery = document.getElementById('input-custom-query');
    const btnClearChat = document.getElementById('btn-clear-chat');
    const durationInput = document.getElementById('input-duration');
    const durationDisplay = document.getElementById('duration-display');
    const agentStatusText = document.getElementById('agent-status-text');
    
    // Mode switcher buttons
    const btnModeMock = document.getElementById('btn-mode-mock');
    const btnModeLive = document.getElementById('btn-mode-live');
    
    // Widgets DOM elements
    const widgetWeatherCard = document.getElementById('widget-weather-card');
    const weatherActiveContent = document.getElementById('weather-active-content');
    const weatherTemp = document.getElementById('weather-temp');
    const weatherTempF = document.getElementById('weather-temp-f');
    const weatherSkyIcon = document.getElementById('weather-sky-icon');
    const weatherDestName = document.getElementById('weather-destination-name');
    const weatherDesc = document.getElementById('weather-desc');
    const weatherPacking = document.getElementById('weather-packing');
    const attractionsFeed = document.getElementById('attractions-feed');

    // --- ⚙️ State Variables ---
    let executionMode = 'mock'; // Default: high-fidelity simulated response
    let activeSessionId = null;

    // --- ⛅ High-Fidelity Regional Weather Directory ---
    const weatherData = {
        Tokyo: {
            January: { tempC: '6°C', tempF: '43°F', icon: 'fa-regular fa-snowflake', desc: 'Chilly, crisp, and clear skies with low humidity.', packing: 'Heavy wool coats, warm thermal layers, gloves, boots, and scarves.' },
            May: { tempC: '19°C', tempF: '66°F', icon: 'fa-solid fa-cloud-sun', desc: 'Mild, warm, and highly comfortable with spring blooms.', packing: 'Light cardigans, cotton shirts, light denim, and comfortable sneakers.' },
            October: { tempC: '12°C', tempF: '54°F', icon: 'fa-solid fa-wind', desc: 'Cool, crisp, and beautifully sunny with clear blue skies.', packing: 'Layered jackets, cardigans, walking shoes, and a light autumn scarf.' },
            December: { tempC: '8°C', tempF: '46°F', icon: 'fa-solid fa-snowflake', desc: 'Cold, brisk, and festive with sparkling night illuminations.', packing: 'Heavy winter coat, gloves, warm socks, thermal wear, and beanies.' }
        },
        Paris: {
            January: { tempC: '5°C', tempF: '41°F', icon: 'fa-solid fa-cloud-showers-water', desc: 'Cold, damp, and romantic with occasional light winter rain.', packing: 'Waterproof heavy coat, warm layers, an umbrella, and sturdy winter boots.' },
            May: { tempC: '15°C', tempF: '59°F', icon: 'fa-solid fa-cloud-sun', desc: 'Wonderfully mild, breezy, and pleasant spring conditions.', packing: 'Trench coat, light knitwear, sunglasses, and comfortable flats.' },
            October: { tempC: '11°C', tempF: '52°F', icon: 'fa-solid fa-cloud-sun', desc: 'Cool, fresh, and scenic with stunning golden foliage.', packing: 'Medium coat, casual sweaters, layered shirts, and an umbrella.' },
            December: { tempC: '6°C', tempF: '43°F', icon: 'fa-solid fa-snowflake', desc: 'Chilly, festive, and magical with glowing Christmas markets.', packing: 'Puffer jacket, thick scarf, thermal innerwear, gloves, and a beanie.' }
        },
        'New York': {
            January: { tempC: '-1°C', tempF: '30°F', icon: 'fa-solid fa-snowflake', desc: 'Freezing, sunny, and windy with occasional winter snow.', packing: 'Down parka, insulated boots, thick gloves, warm scarf, and earmuffs.' },
            May: { tempC: '18°C', tempF: '64°F', icon: 'fa-solid fa-sun', desc: 'Warm, sunny, and gorgeous in Central Park.', packing: 'Jeans, light shirts, sneakers, sunglasses, and a light jacket for evenings.' },
            October: { tempC: '14°C', tempF: '57°F', icon: 'fa-solid fa-leaf', desc: 'Cool, brisk, and delightful autumn conditions.', packing: 'Light coat, flannel shirts, boots, and layered clothing.' },
            December: { tempC: '3°C', tempF: '37°F', icon: 'fa-regular fa-snowflake', desc: 'Cold, brisk, and festive with holiday decorations and lights.', packing: 'Thick overcoat, layered sweaters, scarves, gloves, and warm sneakers.' }
        }
    };

    // --- 🏛️ High-Fidelity Regional Attractions Directory ---
    const attractionData = {
        Tokyo: [
            { name: 'Shinjuku Gyoen National Garden', category: 'Garden / Nature', rating: 4.8, desc: 'Spacious, scenic traditional park with English and French gardens. Beautiful year-round walks.', tags: ['Relaxed Pace', 'Nature'], vegan: true },
            { name: 'Meiji Jingu Shrine', category: 'Shrine / Culture', rating: 4.7, desc: 'A serene, forested Shinto shrine located right in the heart of Shibuya. Features peaceful walkways.', tags: ['Quiet', 'Historical'], vegan: true },
            { name: 'Kyushu Jangara (Harajuku)', category: 'Dining / Food', rating: 4.5, desc: 'World-famous ramen spot featuring a fully dedicated, rich, and highly-rated vegan broth menu.', tags: ['Vegan Friendly', 'Quick Bite'], vegan: true, success: true },
            { name: 'Vegan Sushi Tokyo (Roppongi)', category: 'Dining / Luxury', rating: 4.9, desc: 'Exquisite, artistic vegan sushi crafted from premium organic seasonal vegetables and traditional grains.', tags: ['Vegan Exclusive', 'Fine Dining'], vegan: true, success: true }
        ],
        Paris: [
            { name: 'Tuileries Garden', category: 'Nature / Scenic', rating: 4.6, desc: 'A historic public garden between the Louvre and Place de la Concorde. Perfect for coffee and strolls.', tags: ['Relaxed Pace', 'Scenic'], vegan: true },
            { name: 'Sainte-Chapelle', category: 'Monument / Art', rating: 4.8, desc: 'A gothic royal chapel featuring breathtaking, world-class 13th-century stained glass windows.', tags: ['Historical', 'Art'], vegan: true },
            { name: 'Chambelland (Bastille)', category: 'Dining / Bakery', rating: 4.7, desc: 'An artisan bakery serving 100% organic gluten-free breads, tarts, and delicious Parisian pastries.', tags: ['Gluten-Free', 'Bakery'], vegan: true, success: true },
            { name: 'No Glu (Saint-Germain)', category: 'Dining / Gourmet', rating: 4.4, desc: 'A chic bistro offering a fully gluten-free gourmet dining menu, including pastas, burgers, and desserts.', tags: ['Gluten-Free', 'Cozy'], vegan: true, success: true }
        ],
        'New York': [
            { name: 'The High Line', category: 'Nature / Landmark', rating: 4.7, desc: 'A stunning, elevated linear public park created on a historic freight rail line on Manhattan’s West Side.', tags: ['Scenic Walk', 'Relaxed'], vegan: true },
            { name: 'The Morgan Library & Museum', category: 'Museum / Library', rating: 4.8, desc: 'A breathtakingly scholarly, tranquil, and historic research library housing majestic rare manuscripts.', tags: ['Historical', 'Tranquil'], vegan: true },
            { name: 'Halal Guys (Midtown)', category: 'Dining / Street Food', rating: 4.6, desc: 'The absolute legendary street platter cart serving premium certified halal chicken, falafel, and white sauce.', tags: ['Halal Platter', 'Iconic'], vegan: true, success: true },
            { name: 'Ravagh Persian Grill (Midtown)', category: 'Dining / Persian', rating: 4.5, desc: 'Elegant and popular grill serving authentic, high-quality halal lamb, kebabs, hummus, and rice dishes.', tags: ['Halal Meat', 'Fine Dining'], vegan: true, success: true }
        ]
    };

    // --- 🎨 High-Fidelity Preloaded Mock Itineraries ---
    const mockItineraries = {
        'Tokyo-October-1-relaxed-vegan': `# 🗺️ Custom Travel Itinerary: Tokyo (1-day)
Generated by **VoyageAI Travel Concierge** under Mock Execution.

### 🗓️ Day 1: Serene Garden Strolls & Artisan Dining

*   **9:00 AM - 11:00 AM: Meiji Jingu Shrine**
    *   Explore the serene Meiji Jingu Shrine, a peaceful oasis dedicated to Emperor Meiji and Empress Shoken. Enjoy a relaxed stroll through the forested grounds and marvel at the towering torii gates.
*   **12:00 PM - 1:00 PM: Lunch at Kyushu Jangara Ramen (Harajuku)**
    *   Savor a delicious vegan ramen lunch at Kyushu Jangara Ramen in Harajuku. This spot is known for its hearty and authentic ramen, with a dedicated and highly-rated vegan menu.
*   **2:00 PM - 4:00 PM: Shinjuku Gyoen National Garden**
    *   Immerse yourself in the beauty of Shinjuku Gyoen National Garden. This spacious park features traditional Japanese, English Landscape, and French Formal gardens, perfect for a relaxed afternoon stroll.
*   **6:00 PM - 7:00 PM: Dinner at Vegan Sushi Tokyo (Roppongi)**
    *   Indulge in an exquisite vegan sushi experience at Vegan Sushi Tokyo in Roppongi. Enjoy artistic sushi crafted from seasonal organic vegetables.

---
### ☁️ Autumn Trip Notes
Keep in mind that October weather in Tokyo is refreshingly cool. I recommend packing a light cardigan and comfortable walking sneakers for your garden walks. Enjoy your voyage!`,

        'Paris-May-1-active-gluten-free': `# 🗺️ Custom Travel Itinerary: Paris (1-day)
Generated by **VoyageAI Travel Concierge** under Mock Execution.

### 🗓️ Day 1: Gothic Art & Gluten-Free Patisserie

*   **9:30 AM - 11:30 AM: Sainte-Chapelle & Île de la Cité**
    *   Marvel at the towering, gorgeous stained glass of Sainte-Chapelle. Walk along the Seine river past Notre-Dame Cathedral.
*   **12:00 PM - 1:00 PM: Lunch at Chambelland Bastille**
    *   Savor organic gluten-free breads, gourmet sandwiches, and classic French pastries at bastille's premier gluten-free destination.
*   **1:30 PM - 3:30 PM: Tuileries Garden & Louvre Courtyard**
    *   Stroll through the scenic Tuileries Garden. Grab a traditional coffee and take photos by the iconic glass pyramids.
*   **6:00 PM - 8:00 PM: Dinner at No Glu Saint-Germain**
    *   Enjoy a premium, fully gluten-free Italian-French pasta or bistro dinner at a cozy, highly-rated Saint-Germain eatery.

---
### ☁️ Spring Trip Notes
Paris in May is beautiful and breezy. Be sure to carry a light trench coat and an umbrella for occasional spring showers.`,

        'New York-December-1-active-halal': `# 🗺️ Custom Travel Itinerary: New York (1-day)
Generated by **VoyageAI Travel Concierge** under Mock Execution.

### 🗓️ Day 1: High Line Views & Iconic Halal Street Platters

*   **10:00 AM - 12:00 PM: The High Line Walkway**
    *   Embark on a refreshing walk along the elevated rail line garden, enjoying panoramic views of Chelsea and the Hudson River.
*   **12:30 PM - 1:30 PM: Lunch at Halal Guys (Midtown)**
    *   Grab the legendary, highly optimized gyro or falafel platter topped with their world-famous hot and white sauces.
*   **2:00 PM - 4:00 PM: Central Park Winter Walk & Ice Rink**
    *   Wander past the Wollman Ice Rink and Bethesda Fountain, taking in the majestic winter atmosphere.
*   **6:00 PM - 8:00 PM: Dinner at Ravagh Persian Grill**
    *   Warm up with an authentic, premium halal Persian dinner of lamb kebabs, hummus, and warm basmati rice.

---
### ☁️ Winter Trip Notes
New York in December is freezing but festive. Bundle up in a heavy winter parka, gloves, and a thermal scarf for your walks!`
    };

    // --- 🎮 Slider Interaction Listener ---
    durationInput.addEventListener('input', (e) => {
        const val = e.target.value;
        durationDisplay.textContent = `${val} Day${val > 1 ? 's' : ''}`;
    });

    // --- 🔀 Mode Switcher Event Handlers ---
    btnModeMock.addEventListener('click', () => {
        setExecutionMode('mock');
    });

    btnModeLive.addEventListener('click', () => {
        setExecutionMode('live');
    });

    function setExecutionMode(mode) {
        executionMode = mode;
        if (mode === 'mock') {
            btnModeMock.classList.add('active');
            btnModeLive.classList.remove('active');
            agentStatusText.textContent = 'Simulating instant response';
            addSystemMessage("Switched to **Mock Demo Mode**. Itineraries will generate instantly using premium simulated data.");
        } else {
            btnModeMock.classList.remove('active');
            btnModeLive.classList.add('active');
            agentStatusText.textContent = 'Connected to Vertex AI API';
            addSystemMessage("Switched to **Live Engine Mode**. Itineraries will query your live hosted **Vertex AI Reasoning Engine** on GCP in real-time.");
        }
    }

    // --- 🧹 Clear Chat Handler ---
    btnClearChat.addEventListener('click', () => {
        chatFeed.innerHTML = '';
        addSystemMessage("Console feed cleared. Fill out the planner form to start a new voyage design!");
    });

    // --- 🤖 Message Append Helpers ---
    function addSystemMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'chat-message assistant';
        msgDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fa-solid fa-gears"></i>
            </div>
            <div class="message-bubble-wrapper">
                <div class="message-bubble">
                    <p>${parseMarkdownText(text)}</p>
                </div>
            </div>
        `;
        chatFeed.appendChild(msgDiv);
        scrollToBottom();
    }

    function addUserMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'chat-message user';
        msgDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fa-solid fa-user"></i>
            </div>
            <div class="message-bubble-wrapper">
                <div class="message-bubble">
                    <p>${escapeHTML(text)}</p>
                </div>
            </div>
        `;
        chatFeed.appendChild(msgDiv);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatFeed.scrollTop = chatFeed.scrollHeight;
    }

    // --- ⚙️ Custom Markdown & Text Formatter Engine ---
    function parseMarkdownText(markdown) {
        if (!markdown) return '';
        
        let html = markdown;
        
        // Escape HTML tags to protect integrity
        html = escapeHTML(html);

        // Parse bold markers **word**
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Parse code snippets \`code\`
        html = html.replace(/\`(.*?)\`/g, '<code>$1</code>');

        return html;
    }

    function escapeHTML(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // High fidelity full Markdown rendering
    function renderItineraryMarkdown(markdown) {
        const container = document.createElement('div');
        container.className = 'itinerary-markdown-container';

        const lines = markdown.split('\n');
        let activityList = null;

        for (let i = 0; i < lines.length; i++) {
            let line = lines[i].trim();

            if (!line) continue;

            // Header level 1 (Itinerary Title)
            if (line.startsWith('# ')) {
                const titleCard = document.createElement('div');
                titleCard.className = 'itinerary-title-card';
                titleCard.innerHTML = `<h1><i class="fa-solid fa-compass"></i> ${line.slice(2).replace(/\*\*/g, '')}</h1>`;
                container.appendChild(titleCard);
                continue;
            }

            // Header level 3 (Day Header)
            if (line.startsWith('### ')) {
                // If we were parsing activities, close the active list
                if (activityList) {
                    container.appendChild(activityList);
                    activityList = null;
                }
                const dayHeader = document.createElement('div');
                dayHeader.className = 'day-header-card';
                dayHeader.innerHTML = `<i class="fa-solid fa-calendar-day"></i> ${line.slice(4).replace(/\*\*/g, '')}`;
                container.appendChild(dayHeader);
                continue;
            }

            // Bold headers or subheaders
            if (line.startsWith('---')) {
                if (activityList) {
                    container.appendChild(activityList);
                    activityList = null;
                }
                const hr = document.createElement('hr');
                hr.style.border = 'none';
                hr.style.borderTop = '1px solid var(--clr-border)';
                hr.style.margin = '20px 0';
                container.appendChild(hr);
                continue;
            }

            // Check if it's an activity bullet item (* 9:00 AM - Activity)
            if (line.startsWith('* ')) {
                if (!activityList) {
                    activityList = document.createElement('div');
                    activityList.className = 'activity-list-wrapper';
                }

                const bulletText = line.slice(2);
                const parts = bulletText.split(':');
                
                const timeBlock = parts[0] ? parts[0].trim() : '';
                const titleBlock = parts[1] ? parts[1].trim() : '';
                
                // Read description from following line if it starts with a dash/tab
                let descBlock = '';
                if (i + 1 < lines.length && lines[i + 1].trim().startsWith('*')) {
                    // Following line is another bullet, no subdetails
                } else if (i + 1 < lines.length) {
                    const nextLine = lines[i + 1].trim();
                    if (nextLine.startsWith('-') || nextLine.startsWith('*') === false) {
                        descBlock = nextLine.replace(/^[-*\s]+/, '');
                        i++; // Consume next line
                    }
                }

                const activityCard = document.createElement('div');
                activityCard.className = 'activity-item-card';
                activityCard.innerHTML = `
                    <div class="activity-time"><i class="fa-regular fa-clock"></i> ${timeBlock}</div>
                    <div class="activity-name">${titleBlock.replace(/\*\*/g, '')}</div>
                    <p class="activity-details">${descBlock.replace(/\*\*/g, '')}</p>
                `;
                activityList.appendChild(activityCard);
                continue;
            }

            // Render general text paragraphs
            if (line.startsWith('- ')) {
                line = line.slice(2);
            }
            
            const p = document.createElement('p');
            p.style.fontSize = '14px';
            p.style.color = 'var(--clr-text-muted)';
            p.style.lineHeight = '1.6';
            p.innerHTML = parseMarkdownText(line);
            container.appendChild(p);
        }

        // Close any trailing active activity lists
        if (activityList) {
            container.appendChild(activityList);
        }

        return container;
    }

    // --- 🌤️ Sync Widgets & Highlights with State ---
    function updateSidebarWidgets(destination, month) {
        // 1. Sync Weather
        const regionWeather = weatherData[destination];
        if (regionWeather && regionWeather[month]) {
            const data = regionWeather[month];
            weatherTemp.textContent = data.tempC;
            weatherTempF.textContent = data.tempF;
            weatherSkyIcon.className = data.icon;
            weatherDestName.textContent = `${destination} | ${month}`;
            weatherDesc.textContent = data.desc;
            weatherPacking.textContent = data.packing;

            weatherActiveContent.classList.remove('hidden');
            widgetWeatherCard.querySelector('.widget-loading-placeholder').classList.add('hidden');
        }

        // 2. Sync Attractions
        const regionAttractions = attractionData[destination];
        if (regionAttractions) {
            attractionsFeed.innerHTML = '';
            regionAttractions.forEach(spot => {
                const spotCard = document.createElement('div');
                spotCard.className = 'attraction-widget-card';
                
                const tagsHtml = spot.tags.map(tag => `<span class="attraction-tag">${tag}</span>`).join('');
                const successTagHtml = spot.success ? `<span class="attraction-tag success"><i class="fa-solid fa-leaf"></i> Compliant</span>` : '';

                spotCard.innerHTML = `
                    <div class="attraction-title-row">
                        <h4>${spot.name}</h4>
                        <div class="attraction-rating">
                            <i class="fa-solid fa-star"></i> ${spot.rating}
                        </div>
                    </div>
                    <p class="attraction-desc">${spot.desc}</p>
                    <div class="attraction-tags">
                        ${tagsHtml}
                        ${successTagHtml}
                    </div>
                `;
                attractionsFeed.appendChild(spotCard);
            });
        }
    }

    // --- ⏳ Loading Skeletons Helper ---
    function appendSkeletonLoader() {
        const loaderDiv = document.createElement('div');
        loaderDiv.className = 'chat-message assistant loader-message';
        loaderDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fa-solid fa-circle-notch fa-spin"></i>
            </div>
            <div class="message-bubble-wrapper" style="width: 100%;">
                <div class="message-bubble" style="width: 100%;">
                    <div class="skeleton-box">
                        <div class="skeleton-item skeleton-header"></div>
                        <div class="skeleton-item skeleton-paragraph"></div>
                        <div class="skeleton-item skeleton-paragraph short"></div>
                        <div class="skeleton-item skeleton-paragraph shorter"></div>
                    </div>
                </div>
            </div>
        `;
        chatFeed.appendChild(loaderDiv);
        scrollToBottom();
        return loaderDiv;
    }

    // --- 📨 Interactive Planner Form Handler ---
    plannerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const dest = document.getElementById('input-destination').value;
        const month = document.getElementById('input-month').value;
        const duration = durationInput.value;
        const pace = document.querySelector('input[name="input-pace"]:checked').value;
        
        // Accumulate checkboxes
        const diets = [];
        document.querySelectorAll('input[name="input-diet"]:checked').forEach(cb => {
            diets.push(cb.value);
        });

        // Compile query prompt matching spec requirements
        const dietText = diets.length > 0 ? `I am a ${diets.join(', ')}.` : '';
        const compiledQuery = `Hi, please plan a ${duration}-day ${pace} trip to ${dest} in ${month}. ${dietText}`;

        addUserMessage(compiledQuery);
        updateSidebarWidgets(dest, month);

        if (executionMode === 'mock') {
            await handleMockQuery(dest, month, duration, pace, diets);
        } else {
            await handleLiveQuery(compiledQuery, dest, month);
        }
    });

    // Custom chat prompt input
    chatInputForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const customQuery = inputCustomQuery.value.trim();
        if (!customQuery) return;

        addUserMessage(customQuery);
        inputCustomQuery.value = '';

        // Derive destination based on keyword triggers
        let dest = 'Tokyo';
        if (customQuery.toLowerCase().includes('paris')) dest = 'Paris';
        else if (customQuery.toLowerCase().includes('new york') || customQuery.toLowerCase().includes('ny')) dest = 'New York';

        let month = 'October';
        if (customQuery.toLowerCase().includes('january')) month = 'January';
        else if (customQuery.toLowerCase().includes('may')) month = 'May';
        else if (customQuery.toLowerCase().includes('december')) month = 'December';

        updateSidebarWidgets(dest, month);

        if (executionMode === 'mock') {
            await handleMockQuery(dest, month, 1, 'relaxed', ['vegan']);
        } else {
            await handleLiveQuery(customQuery, dest, month);
        }
    });

    // --- 🪄 Execute Mock Query ---
    async function handleMockQuery(dest, month, duration, pace, diets) {
        const skeleton = appendSkeletonLoader();
        agentStatusText.textContent = 'Designing luxury simulated layout...';

        // Simulate model generation network lag
        await new Promise(resolve => setTimeout(resolve, 1400));

        skeleton.remove();
        agentStatusText.textContent = 'Ready';

        // Lookup exact key, or fall back gracefully
        const mockKey = `${dest}-${month}-${duration}-${pace}-${diets.join('-')}`;
        const mockMarkdown = mockItineraries[mockKey] || mockItineraries['Tokyo-October-1-relaxed-vegan'];

        const itineraryResponseDiv = document.createElement('div');
        itineraryResponseDiv.className = 'chat-message assistant';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i>`;
        
        const bubbleWrapper = document.createElement('div');
        bubbleWrapper.className = 'message-bubble-wrapper';
        bubbleWrapper.style.width = '100%';
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.style.width = '100%';
        
        // Render rich html segments
        bubble.appendChild(renderItineraryMarkdown(mockMarkdown));
        
        bubbleWrapper.appendChild(bubble);
        itineraryResponseDiv.appendChild(avatar);
        itineraryResponseDiv.appendChild(bubbleWrapper);
        chatFeed.appendChild(itineraryResponseDiv);
        scrollToBottom();
    }

    // --- ⚡ Execute Live API Query ---
    async function handleLiveQuery(compiledQuery, dest, month) {
        const skeleton = appendSkeletonLoader();
        agentStatusText.textContent = 'Compiling live Vertex AI model parameters...';

        try {
            const response = await fetch('/api/reasoning_engine', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    class_method: 'query',
                    input: {
                        input: compiledQuery
                    }
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP network error: status ${response.status}`);
            }

            const data = await response.json();
            skeleton.remove();
            agentStatusText.textContent = 'Ready';

            const outputText = data.output || '';
            
            const itineraryResponseDiv = document.createElement('div');
            itineraryResponseDiv.className = 'chat-message assistant';
            
            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';
            avatar.innerHTML = `<i class="fa-solid fa-cloud-bolt"></i>`;
            
            const bubbleWrapper = document.createElement('div');
            bubbleWrapper.className = 'message-bubble-wrapper';
            bubbleWrapper.style.width = '100%';
            
            const bubble = document.createElement('div');
            bubble.className = 'message-bubble';
            bubble.style.width = '100%';
            
            // Render rich HTML segments from the live engine's markdown output
            bubble.appendChild(renderItineraryMarkdown(outputText));
            
            bubbleWrapper.appendChild(bubble);
            itineraryResponseDiv.appendChild(avatar);
            itineraryResponseDiv.appendChild(bubbleWrapper);
            chatFeed.appendChild(itineraryResponseDiv);
            scrollToBottom();

        } catch (error) {
            console.error("Live Query Error:", error);
            skeleton.remove();
            agentStatusText.textContent = 'Connection failed';
            addSystemMessage(`⚠️ **Vertex AI Connection Failed**: ${error.message}. Ensure your local backend is running (\`agents-cli run\` or \`python -m app.fast_api_app\`) and that your terminal is authenticated with GCP!`);
        }
    }
});

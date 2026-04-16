/**
 * BA Eats - Frontend Logic
 * Handles state management, API interaction, and UI updates.
 */

document.addEventListener('DOMContentLoaded', () => {
    // State management
    let state = {
        view: 'hero', // 'hero', 'question', 'results', 'empty', 'loading'
        question: null,
        progress: { current: 0, total: 0 },
        results: []
    };

    // DOM Elements
    const views = {
        hero: document.getElementById('hero'),
        question: document.getElementById('question-container'),
        results: document.getElementById('results-container'),
        empty: document.getElementById('empty-state'),
        loading: document.getElementById('loading-view')
    };

    const startBtn = document.getElementById('start-btn');
    const resetBtn = document.getElementById('reset-btn');
    const retryBtn = document.getElementById('retry-btn');
    const questionText = document.getElementById('question-text');
    const optionsGrid = document.getElementById('options-grid');
    const progressFill = document.getElementById('progress-fill');
    const resultsList = document.getElementById('results-list');

    // View Switcher
    function switchView(viewName) {
        Object.keys(views).forEach(v => {
            views[v].classList.add('hidden');
        });
        views[viewName].classList.remove('hidden');
        state.view = viewName;
        window.scrollTo(0, 0);
    }

    // API Calls
    async function startQuiz() {
        switchView('loading');
        try {
            const response = await fetch('/api/start', { method: 'POST' });
            const data = await response.json();
            handleResponse(data);
        } catch (error) {
            console.error('Error starting quiz:', error);
            switchView('hero');
        }
    }

    async function submitAnswer(questionId, answer) {
        switchView('loading');
        try {
            const response = await fetch('/api/answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question_id: questionId, answer: answer })
            });
            const data = await response.json();
            handleResponse(data);
        } catch (error) {
            console.error('Error submitting answer:', error);
            switchView('hero');
        }
    }

    function handleResponse(data) {
        if (data.done) {
            if (data.results && data.results.length > 0) {
                renderResults(data.results);
                switchView('results');
            } else {
                switchView('empty');
            }
        } else {
            renderQuestion(data.question, data.progress);
            switchView('question');
        }
    }

    // Rendering
    function renderQuestion(question, progress) {
        questionText.textContent = question.text;
        optionsGrid.innerHTML = '';
        
        const labelMap = {
            'celiac': 'Gluten-free / Celiac',
            'cafe': 'Café',
            'street_food': 'Street Food',
            'fast_food': 'Fast Food',
            'same_area': 'Near the Res Hall (Centro/Retiro)'
        };

        question.options.forEach(option => {
            const btn = document.createElement('button');
            btn.className = 'option-btn';
            
            // Use custom label if it exists, otherwise format the option string
            let label = labelMap[option] || option.replace('_', ' ').charAt(0).toUpperCase() + option.replace('_', ' ').slice(1);
            btn.textContent = label;
            
            btn.onclick = () => submitAnswer(question.id, option);
            optionsGrid.appendChild(btn);
        });

        const percent = (progress.current / progress.total) * 100;
        progressFill.style.width = `${percent}%`;
    }

    function renderResults(results) {
        resultsList.innerHTML = '';
        results.forEach(res => {
            const card = document.createElement('div');
            card.className = 'restaurant-card';
            
            const info = document.createElement('div');
            info.className = 'res-info';
            info.innerHTML = `
                <h4>${res.name}</h4>
                <div class="res-meta">${res.neighborhood} • ${res.cuisine.charAt(0).toUpperCase() + res.cuisine.slice(1)}</div>
                <div class="res-tags">
                    ${res.tags.map(tag => `<span class="tag">${tag.replace('_', ' ')}</span>`).join('')}
                </div>
            `;
            
            card.appendChild(info);
            resultsList.appendChild(card);
        });
    }

    // Event Listeners
    startBtn.onclick = startQuiz;
    resetBtn.onclick = startQuiz;
    retryBtn.onclick = startQuiz;
});
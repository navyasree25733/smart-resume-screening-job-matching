class ConsumerDashboard {
    constructor() {
        this.form = document.getElementById('resumeForm');
        this.resultsSection = document.getElementById('resultsSection');
        this.initEventListeners();
    }

    initEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    async handleSubmit(e) {
        e.preventDefault();
        const formData = new FormData();
        const resumeFile = document.getElementById('resumeFile').files[0];
        const jobTitle = document.getElementById('jobTitle').value;
        const jobDesc = document.getElementById('jobDesc').value;

        formData.append('resume', resumeFile);
        formData.append('job_title', jobTitle);
        formData.append('job_description', jobDesc);

        try {
            this.showLoading();
            const response = await fetch('http://localhost:8000/api/screen-resume', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) throw new Error('Screening failed');
            
            const result = await response.json();
            this.displayResults(result);
        } catch (error) {
            alert('Error screening resume: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    showLoading() {
        const btn = this.form.querySelector('button');
        btn.textContent = '⏳ Screening...';
        btn.disabled = true;
    }

    hideLoading() {
        const btn = this.form.querySelector('button');
        btn.textContent = '🚀 Screen My Resume';
        btn.disabled = false;
    }

    displayResults(data) {
        this.resultsSection.style.display = 'block';
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });

        // ATS Score
        document.getElementById('atsScore').textContent = data.ats_score;
        this.updateScoreCircle(data.ats_score);

        // Charts
        this.renderComponentChart(data.component_scores);
        this.renderSkillsChart(data);

        // Skills lists
        this.renderSkillsLists(data.skills, data.missing_skills);

        // Suggestions
        this.renderSuggestions(data.improvement_suggestions);
    }

    updateScoreCircle(score) {
        const circle = document.getElementById('scoreCircle');
        const angle = (score / 100) * 360;
        circle.style.background = `conic-gradient(#4ade80 0deg ${angle}deg, #e1e5e9 ${angle}deg 360deg)`;
    }

    renderComponentChart(scores) {
        const ctx = document.getElementById('componentChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Skills', 'Semantic', 'Exp', 'Degree', 'Certs', 'Projects'],
                datasets: [{
                    data: [scores.S, scores.M, scores.E, scores.D, scores.C, scores.P],
                    backgroundColor: ['#4ade80', '#3b82f6', '#f59e0b', '#10b981', '#8b5cf6', '#ef4444']
                }]
            },
            options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
        });
    }

    renderSkillsChart(data) {
        // Simple placeholder chart
        const ctx = document.getElementById('skillsChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Skill Match', 'Semantic Match'],
                datasets: [{
                    data: [data.skill_match * 100, data.semantic_match * 100],
                    backgroundColor: ['#4ade80', '#3b82f6']
                }]
            },
            options: { responsive: true, scales: { y: { beginAtZero: true, max: 100 } } }
        });
    }

    renderSkillsLists(skills, missing) {
        document.getElementById('matchedSkills').innerHTML = 
            skills.extracted_skills.slice(0, 8).map(skill => `<li>${skill}</li>`).join('');
        document.getElementById('missingSkills').innerHTML = 
            missing.map(skill => `<li>${skill}</li>`).join('');
    }

    renderSuggestions(suggestions) {
        document.getElementById('suggestions').innerHTML = 
            suggestions.map(s => `<li>${s}</li>`).join('');
    }
}

new ConsumerDashboard();